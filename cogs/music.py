import discord
from discord import app_commands
from discord.ext import commands
import lava_lyra
from core import CustomPlayer

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
        
        # Defer before response
        await interaction.response.defer()

        # Search for tracks (supports Spotify, YouTube, Apple Music via plugins!)
        results = await player.get_tracks(query)
        
        if not results:
            return await interaction.followup.send("No tracks found!")
        
        # Get first track
        track = results[0]

        # Put the track into queue
        player.queue.put(track)
        
        if player.is_playing:
            return await interaction.followup.send(f"Add **{track.title}** to play queue")
        else:
            # Play the track directly
            await player.play_next()
            return await interaction.followup.send(f"Now playing: **{track.title}**")

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
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))