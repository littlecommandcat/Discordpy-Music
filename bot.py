import discord
from discord.ext import commands
from discord import app_commands
import lava_lyra

# Set CustomPlayer
class CustomPlayer(lava_lyra.Player):
    def __init__(self, client, channel, *, node = None):
        super().__init__(client, channel, node=node)
        self.queue = lava_lyra.Queue() # Set lavalyra queue
        self.loop_mode = True # Set custom loop mode
        self.current_index = 0 # Set index for custom loop mode

    async def play_next(self):
        # Play next song in the queue
        if self.queue.is_empty:
            return
        
        # Get next track from queue
        track = self.queue.pop() 

        if self.loop_mode:
            # Re-queue the track if loop is enabled
            self.queue.put(track)

        await self.play(track)

class EventHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_lyra_node_connected(self, node_id, is_nodelink, reconnect):
        # Nodelink/Lavalink connected event
        print(f'{node_id}: Nodelink({is_nodelink}) reconnect({reconnect})')

    @commands.Cog.listener()
    async def on_lyra_node_disconnected(self, node_id, is_nodelink, player_count):
        # Nodelink/Lavalink disconnected event
        print(f'{node_id}: Nodelink({is_nodelink}) playercount({player_count})')

    @commands.Cog.listener()
    async def on_lyra_node_reconnecting(self, node_id, is_nodelink, retry_in):
        # Nodelink/Lavalink reconnected event
        print(f'{node_id}: Nodelink({is_nodelink}) retry in {retry_in}s')

    @commands.Cog.listener()
    async def on_lyra_websocket_closed(self, payload):
        # Nodelink/Lavalink websocket closed event
        pass
    
    @commands.Cog.listener()
    async def on_lyra_websocket_open(self, target, ssrc):
        # Nodelink/Lavalink websocket opened event
        pass

    @commands.Cog.listener()
    async def on_lyra_track_start(self, player, track):
        # Nodelink/Lavalink track start event
        print(f'Start playing track: {track.title}')

    @commands.Cog.listener()
    async def on_lyra_track_end(self, player, track, reason):
        # Nodelink/Lavalink track end event
        print(f'End playing track: {track.title}.Reason: {reason}')
        # Play next song by using CustomPlayer
        await player.play_next()

    @commands.Cog.listener()
    async def on_lyra_track_stuck(self, player, track, threshold):
        # Lavalink track stucked event
        print(f'Player stucked. Wait for {threshold}s.')

    @commands.Cog.listener()
    async def on_lyra_track_exception(self, player, track, error):
        # Nodelink/Lavalink track exception event
        print(f'Track exception: {error}.')

    @commands.Cog.listener()
    async def on_lyra_lyrics_found(self, player, track, lyrics):
        # Successfully found lyrics event
        print(f"Lyrics found for {track.title}: {len(lyrics)} lines")

    @commands.Cog.listener()
    async def on_lyra_lyrics_unavailable(self, player, track):
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
        
        track = results[0]
        if player.is_playing:
            # Put the track into queue
            player.queue.put(track)
            return await interaction.response.send_message(f"Add **{track.title}** to play queue")
        else:
            # Play the track directly
            await player.play(track)
            return await interaction.response.send_message(f"Now playing: **{track.title}**")

    @app_commands.command(name='disconnect', description='disconnect voice')
    async def disconnect(self, interaction: discord.Interaction):
        # Check if voice client exists
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("I'm not in a voice channel.")
        
        # Disconnect from current voice channel
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
        player.loop_mode = not player.loop_mode

        return await interaction.response.send_message(f"Current loop mode: `{player.loop_mode}`")

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
bot = Bot()
bot.run('TOKEN')