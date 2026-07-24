import discord
from discord.ext import commands, tasks
import lava_lyra
import re

class PresenceTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def cog_load(self):
        if self.update_presence.is_running():
            return
        
        self.update_presence.start()

    async def cog_unload(self):
        if self.update_presence.is_running() and not self.update_presence.is_being_cancelled():
            self.update_presence.cancel()

    def is_youtube(self, url: str) -> bool:
        youtube_regex = (
            r'(https?://)?(www\.|m\.)?'
            r'(youtube\.com|youtu\.be)/'
            r'(watch\?v=|embed/|shorts/)?'
            r'([a-zA-Z0-9_-]{11})'
        )
        match = re.search(youtube_regex, url)
        return bool(match)

    def is_twitch(self, url: str) -> bool:
        pattern = r'^(https?://)?(www\.|m\.)?twitch\.tv/[a-zA-Z0-9_]{4,25}/?$'
        match = re.match(pattern, url)
        return bool(match)
    
    @tasks.loop(seconds=10)
    async def update_presence(self):
        nodes: dict[str, lava_lyra.Node] = lava_lyra.NodePool._nodes
        if not nodes:
            return
        
        for node in nodes.values():
            for player in node.players.values():
                current = player.current
                if player.is_playing and current:
                    if self.is_youtube(current.uri) or self.is_twitch(current.uri):
                        await self.bot.change_presence(
                            activity=discord.Streaming(name=player.current.title[:120], url=current.uri)
                        )
                    else:
                        await self.bot.change_presence(
                            activity=discord.Activity(name=player.current.title[:120], type=discord.ActivityType.listening)
                        )
                        
                    return
        
        await self.bot.change_presence(activity=None)
                
async def setup(bot: commands.Bot):
    await bot.add_cog(PresenceTask(bot))