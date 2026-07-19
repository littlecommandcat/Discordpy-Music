import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import lava_lyra
from lava_lyra.exceptions import (
    NodeConnectionFailure,
    NodeCreationError
)

# Get Basic Bot Info
load_dotenv()
TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "?")

# Lavalink/Nodelink Configuration
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 443))
PASSWORD = os.getenv("PASSWORD", "youshallnotpass")
SECURE = os.getenv("SECURE", "false").lower() == "true"

INTENTS = discord.Intents.default()


class Bot(commands.Bot):
    def __init__(self):
        # Setup bot intents
        super().__init__(
            intents=INTENTS,
            command_prefix=PREFIX
        )
        self.pool = lava_lyra.NodePool()

    async def connect_nodes(self):
        try:
            # Create Lavalink node with plugin supports
            node: lava_lyra.Node = await self.pool.create_node(
            bot=self,
            host=HOST, 
            port=PORT, 
            password=PASSWORD, 
            secure=SECURE, 
            identifier='MAIN', 
            lyrics=True, # Enable LavaLyrics plugin support
            search=True, # Enable LavaSearch plugin support
            fallback=True, # Enable fallback node
            )
            print(f"Created node: {node._identifier}")
        except NodeCreationError as error:
            print(f"Node error while creating: {error}")
        except NodeConnectionFailure as error:
            print(f"Node error while connecting: {error}")
        except Exception as error:
            print(f"Exception: {error}")

    async def load_extensions(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                extension = filename[:-3]
                if extension == "__init__":
                    continue
                await self.load_extension(f"cogs.{extension}")

    async def setup_hook(self):
        # Load cogs from ./cogs
        await self.load_extensions()
        
    async def on_ready(self):
        # Sync slash commands
        commands = await self.tree.sync()
        print(f'Logged in as {self.user}')
        print(f"Synced {len(commands)} commands")
        # Initialize node connections
        await self.connect_nodes()

    async def on_close(self):
        super().on_close()

# Run the bot
if __name__ == '__main__':
    bot = Bot()
    asyncio.run(bot.start(TOKEN))