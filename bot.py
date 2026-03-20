import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import lava_lyra

# Set CustomPlayer
class CustomPlayer(lava_lyra.Player):
    def __init__(self, client, channel, *, node = None):
        super().__init__(client, channel, node=node)
        self.queue = self.init_queue()
        
    def init_queue(self):
        if not hasattr(lava_lyra.Queue(), 'max_history'):
            return lava_lyra.Queue()
        else:
            # Set lavalyra track history
            # git clone https://github.com/littlecommandcat/lava-lyra.git (if lava-lyra release <= 1.8.1)
            return lava_lyra.Queue(max_history=10)

    async def play_next(self):
        # Play next song in the queue
        if self.queue.is_empty:
            return
        
        # Get next track
        track = self.queue.get()
        
        # Play the track
        await self.play(track)

class EventHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_lyra_node_connected(self, node_id: str, is_nodelink: bool, reconnect: bool):
        # Nodelink/Lavalink connected event
        print(f'{node_id}: Nodelink({is_nodelink}) reconnect({reconnect})')

    @commands.Cog.listener()
    async def on_lyra_node_disconnected(self, node_id: str, is_nodelink: bool, player_count: int):
        # Nodelink/Lavalink disconnected event
        print(f'{node_id}: Nodelink({is_nodelink}) playercount({player_count})')

    @commands.Cog.listener()
    async def on_lyra_node_reconnecting(self, node_id: str, is_nodelink: bool, retry_in: float):
        # Nodelink/Lavalink reconnected event
        print(f'{node_id}: Nodelink({is_nodelink}) retry in {retry_in}s')

    @commands.Cog.listener()
    async def on_lyra_websocket_closed(self, payload: lava_lyra.WebSocketClosedPayload):
        # Nodelink/Lavalink websocket closed event
        pass
    
    @commands.Cog.listener()
    async def on_lyra_websocket_open(self, target: str, ssrc: int):
        # Nodelink/Lavalink websocket opened event
        pass

    @commands.Cog.listener()
    async def on_lyra_track_start(self, player: CustomPlayer, track: lava_lyra.Track):
        # Nodelink/Lavalink track start event
        print(f'Start playing track: {track.title}')

    @commands.Cog.listener()
    async def on_lyra_track_end(self, player: CustomPlayer, track: lava_lyra.Track, reason: str):
        # Nodelink/Lavalink track end event
        print(f'End playing track: {track.title}.Reason: {reason}')
        # Play next song by using CustomPlayer
        await player.play_next()

    @commands.Cog.listener()
    async def on_lyra_track_stuck(self, player: CustomPlayer, track: lava_lyra.Track, threshold: float):
        # Lavalink track stucked event
        print(f'Player stucked. Wait for {threshold}s.')

    @commands.Cog.listener()
    async def on_lyra_track_exception(self, player: CustomPlayer, track: lava_lyra.Track, error: lava_lyra.TrackExceptionEvent):
        # Nodelink/Lavalink track exception event
        print(f'Track exception: {error}.')

    @commands.Cog.listener()
    async def on_lyra_lyrics_found(self, player: CustomPlayer, track: lava_lyra.Track, lyrics: lava_lyra.Lyrics):
        # Successfully found lyrics event
        print(f"Lyrics found for {track.title}: {len(lyrics.lines)} lines")

    @commands.Cog.listener()
    async def on_lyra_lyrics_unavailable(self, player: CustomPlayer, track:lava_lyra.Track):
        # Lyrics not available event
        print(f"No lyrics available for {track.title}")

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='play', description='play music')
    async def play(self, interaction: discord.Interaction, query: str):
        # Connect to voice channel
        if not interaction.user.voice:
            return await interaction.response.send_message("You need to be in a voice channel!")

        # In voice channel but not CustomPlayer
        if interaction.guild.voice_client and not isinstance(interaction.guild.voice_client, CustomPlayer):
            await interaction.guild.voice_client.disconnect(force=True)
        
        if not interaction.guild.voice_client:
            # Use CustomPlayer
            player = await interaction.user.voice.channel.connect(cls=CustomPlayer)
        else:
            player = interaction.guild.voice_client
        
        # Search for tracks (supports Spotify, YouTube, Apple Music via plugins!)
        results = await player.get_tracks(query)
        
        if not results:
            return await interaction.response.send_message("No tracks found!")
        
        # Get first track
        track = results[0]

        # Put the track into queue
        player.queue.put(track)
        if player.is_playing:
            return await interaction.response.send_message(f"Add **{track.title}** to play queue")
        else:
            # Play the track directly
            await player.play_next()
            return await interaction.response.send_message(f"Now playing: **{track.title}**")

    @app_commands.command(name='disconnect', description='disconnect voice')
    async def disconnect(self, interaction: discord.Interaction):
        # Check if voice client exists
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not in a voice channel.")
        
        # Disconnect from current voice channel
        if isinstance(interaction.guild.voice_client, CustomPlayer):
            await interaction.guild.voice_client.destroy()
        else:
            await interaction.guild.voice_client.disconnect(force=True)
        await interaction.response.send_message("I'm now leaving the voice channel.")

    @app_commands.command(name='queue', description='show play queue')
    async def queue(self, interaction: discord.Interaction):
        # Check voice and player type
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not in a voice channel.")
        
        if not isinstance(interaction.guild.voice_client, CustomPlayer):
            return await interaction.response.send_message("I'm now not a music player.")
        
        player: CustomPlayer = interaction.guild.voice_client
        if player.queue.is_empty:
            return await interaction.response.send_message("There is nothing in the play queue.")
        
        # Build queue list string
        msg = ''
        for i, track in enumerate(player.queue):
            msg += f'{i}. {track.title}\n'
        
        # Send play queue as Embed
        embed = discord.Embed(
            title = 'Play Queue',
            description = msg
        )
        return await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='lyrics', description='show music lyrics')
    async def lyrics(self, interaction: discord.Interaction):
        # Validations
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not in a voice channel.")
        
        if not isinstance(interaction.guild.voice_client, CustomPlayer):
            return await interaction.response.send_message("I'm not a music player now.")
        
        player: CustomPlayer = interaction.guild.voice_client
        if not player.is_playing:
            return await interaction.response.send_message("I'm not playing any music.")
        
        # Fetch lyrics from node
        await interaction.response.defer()
        lyrics = await player.fetch_lyrics(player.current)

        if not lyrics:
            return await interaction.followup.send(f"Couldn't find lyrics for **{player.current.title}**.")

        # Formatting lyric lines
        msg = ''
        for line in lyrics:
            msg += f"[{line.time:.1f}s] {line.text}\n"
        
        # Send lyrics in code block within Embed
        embed = discord.Embed(
            title = f'{player.current.title} Lyrics',
            description = f'```\n{msg[:4000]}\n```'
        )
        return await interaction.followup.send(embed=embed)
    
    @app_commands.command(name='loop', description='enable/disable loop mode')
    async def loop(self, interaction: discord.Interaction):
        # Basic music player check
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not in a voice channel.")
        
        if not isinstance(interaction.guild.voice_client, CustomPlayer):
            return await interaction.response.send_message("I'm not a music player now.")
        
        player: CustomPlayer = interaction.guild.voice_client
        if not player.is_playing:
            return await interaction.response.send_message("I'm not playing any music.")
        
        # Toggle loop mode status
        current_mode = player.queue.loop_mode
        if current_mode == lava_lyra.LoopMode.TRACK:
            player.queue.set_loop_mode(lava_lyra.LoopMode.QUEUE)
            
        elif current_mode == lava_lyra.LoopMode.QUEUE:
            player.queue.disable_loop()
            
        else:
            player.queue.set_loop_mode(lava_lyra.LoopMode.TRACK)

        return await interaction.response.send_message(f"Current loop mode: `{player.queue.loop_mode.name}`")
    
    @app_commands.command(name='shuffle', description='Shuffle play queue')
    async def shuffle(self, interaction: discord.Interaction):
        # Basic music player check
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not in a voice channel.")
        
        if not isinstance(interaction.guild.voice_client, CustomPlayer):
            return await interaction.response.send_message("I'm not a music player now.")
        
        player: CustomPlayer = interaction.guild.voice_client
        if not player.is_playing:
            return await interaction.response.send_message("I'm not playing any music.")
        
        # Suffle the play queue
        player.queue.shuffle()

        return await interaction.response.send_message(f"Shuffled the play queue.")
    
    @app_commands.command(name='volume', description='Set bot volume')
    async def volume(self, interaction: discord.Interaction, volume: app_commands.Range[int, 1, 500]):
        # Basic music player check
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not in a voice channel.")
        
        if not isinstance(interaction.guild.voice_client, CustomPlayer):
            return await interaction.response.send_message("I'm not a music player now.")
        
        player: CustomPlayer = interaction.guild.voice_client
        if not player.is_playing:
            return await interaction.response.send_message("I'm not playing any music.")
        
        # Set player volume
        await player.set_volume(volume)

        return await interaction.response.send_message(f"Set player volume `{volume}`.")

    @app_commands.command(name='queue', description='Show play queue')
    async def queue(self, interaction: discord.Interaction):
        # Basic music player check
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not in a voice channel.")
        
        if not isinstance(interaction.guild.voice_client, CustomPlayer):
            return await interaction.response.send_message("I'm not a music player now.")
        
        player: CustomPlayer = interaction.guild.voice_client
        if player.queue.is_empty:
            return await interaction.response.send_message('The play queue is empty.')

        playqueue = player.queue.get_queue()
        msg = ''
        for i, track in enumerate(playqueue, 1):
            msg += f'{i}. [{track.title}]({track.uri})\n'
        
        embed = discord.Embed(
            title = f'Play Queue',
            description = msg[:4000]
        )

        return await interaction.response.send_message(embed=embed)

    @app_commands.command(name='history', description='Show play history')
    async def history(self, interaction: discord.Interaction):
        # Basic music player check
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not in a voice channel.")
        
        if not isinstance(interaction.guild.voice_client, CustomPlayer):
            return await interaction.response.send_message("I'm not a music player now.")
        
        player: CustomPlayer = interaction.guild.voice_client
        if not hasattr(player.queue, 'max_history'):
            return await interaction.response.send_message(f"Track history is not supported in this version.If the lava-lyra is the latest, try ```bat\ngit clone https://github.com/littlecommandcat/lava-lyra.git```")

        history_tracks = player.queue.get_history()
        msg = ''
        for i, track in enumerate(history_tracks, 1):
            msg += f'{i}. [{track.title}]({track.uri})\n'
        
        if not msg:
            return await interaction.response.send_message(f"There track history is empty.")

        embed = discord.Embed(
            title = f'Track History',
            description = msg[:4000]
        )

        return await interaction.response.send_message(embed=embed)

class Bot(commands.Bot):
    def __init__(self):
        # Setup bot intents
        super().__init__(
            intents=discord.Intents.default(),
            command_prefix='?'
        )
        self.pool = lava_lyra.NodePool()

    async def connect_nodes(self):
        # Create Lavalink node with plugin supports
        node: lava_lyra.Node = await self.pool.create_node(
          bot=self,
          host='localhost', 
          port=2333, 
          password='youshallnotpass', 
          secure=False, 
          identifier='MAIN', 
          lyrics=True, # Enable LavaLyrics plugin support
          search=True, # Enable LavaSearch plugin support
          fallback=True, # Enable fallback node
        )
        print(f"Created node: {node._identifier}")

    async def on_ready(self):
        # Load cogs and sync slash commands
        await self.add_cog(Music(self))
        await self.add_cog(EventHandler(self))
        await self.tree.sync()
        
        print(f'Logged in as {self.user}')
        # Initialize node connections
        await self.connect_nodes()

# Run the bot
if __name__ == '__main__':
    bot = Bot()
    asyncio.run(bot.start('TOKEN'))