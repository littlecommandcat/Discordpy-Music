import discord
from discord.ext import commands, tasks
import lava_lyra

class PresenceTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def cog_load(self):
        if self.update_presence.is_running():
            return
        
        self.update_presence.start()

    @tasks.loop(seconds=10)
    async def update_presence(self):
        nodes: dict[str, lava_lyra.Node] = lava_lyra.NodePool._nodes
        if not nodes:
            return
        
        for node in nodes.values():
            for player in node.players.values():
                if player.is_playing and player.current:
                    await self.bot.change_presence(
                        activity=discord.Activity(name=player.current.title[:120], type=discord.ActivityType.listening)
                    )
                    return
        
        await self.bot.change_presence(activity=None)
                
async def setup(bot: commands.Bot):
    await bot.add_cog(PresenceTask(bot))