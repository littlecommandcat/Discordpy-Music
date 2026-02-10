import discord
from discord.ext import commands
import lava_lyra

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.default(),
            command_prefix='?'
        )
        self.node = None

    async def on_lyra_node_connected(self, node_id, is_lavalink, reconnect):
        # Nodelink/Lavalink connected event
        print(f'{node_id}: lavalink({is_lavalink}) reconnect({reconnect})')

    async def on_ready(self):
        await self.tree.sync()
        print(f'Logged in as {self.user}')

        # Create Lavalink nodes - much simpler than before!
        node: lava_lyra.Node = await lava_lyra.NodePool.create_node(
          bot=self,
          host='localhost',  # Nodelink/Lavalink host
          port=2333,  # Nodelink/Lavalink port
          password='youshallnotpass',  # Nodelink/Lavalink password
          secure=False,  # SSL
          identifier='MAIN',  # Node identifier
          lyrics=False,  # Enable LavaLyrics plugin support
          search=True,  # Enable LavaSearch plugin support
          fallback=True,  # Enable fallback
        )
        print(f"Created node: {node._identifier}")
        # print(f"Created node: {node.identifier}")  Lava-Lyra old method


bot = Bot()

@bot.tree.command(name='play', description='play music')
async def play(interaction: discord.Interaction, query: str):
    # Connect to voice channel
    if not interaction.user.voice:
        return await interaction.response.send_message("You need to be in a voice channel!")
    
    player = await interaction.user.voice.channel.connect(cls=lava_lyra.Player)
    
    # Search for tracks (supports Spotify, YouTube, Apple Music via plugins!)
    results = await player.get_tracks(query)
    
    if not results:
        return await interaction.response.send_message("No tracks found!")
    
    # Play the track
    track = results[0]
    await player.play(track)
    await interaction.response.send_message(f"Now playing: **{track.title}**")

@bot.tree.command(name='disconnect', description='disconnect voice')
async def disconnect(interaction: discord.Interaction):
    if not interaction.guild.voice_client:
        return await interaction.response.send_message("I'm not in a voice channel.")
    
    await interaction.guild.voice_client.disconnect(force=True)
    await interaction.response.send_message("I'm now leaving the voice channel.")


bot.run('TOKEN')  # Put your bot token here