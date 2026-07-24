import discord
from discord.ext import commands
import lava_lyra
from core import CustomPlayer

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
        print(f'End playing track: {track.title}. Reason: {reason}')
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

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild = member.guild
        # Get voice client
        voice_client = guild.voice_client

        if not voice_client:
            return

        # Bot leaves the voice channel
        if member.id == self.bot.user.id:
            if before.channel is not None and after.channel is None:
                if isinstance(voice_client, CustomPlayer):
                    await voice_client.destroy()
            return

        # Bot is not connected to a voice channel
        if not voice_client.channel:
            return

        client_channel = voice_client.channel

        # Member leaves the bot's voice channel
        if before.channel == client_channel and after.channel != client_channel:
            if len(client_channel.members) == 1:
                if isinstance(voice_client, CustomPlayer):
                    await voice_client.destroy()
                else:
                    await voice_client.disconnect()

async def setup(bot: commands.Bot):
    await bot.add_cog(EventHandler(bot))