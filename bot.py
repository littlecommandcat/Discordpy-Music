import asyncio
import json
import os

import discord
import lava_lyra
from discord.ext import commands
from dotenv import load_dotenv
from lava_lyra.exceptions import NodeConnectionFailure, NodeCreationError

# Get Basic Bot Info
load_dotenv()
TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "?")

# Lavalink/Nodelink Configuration
# HOST = os.getenv("HOST", "localhost")
# PORT = int(os.getenv("PORT", 443))
# PASSWORD = os.getenv("PASSWORD", "youshallnotpass")
# SECURE = os.getenv("SECURE", "false").lower() == "true"

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.presences = True

# Prevent mention roles or everyone
ALLOWED_MENTIONS = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True)


class Bot(commands.Bot):
    def __init__(self):
        # Setup bot intents
        super().__init__(intents=INTENTS, command_prefix=PREFIX, allowed_mentions=ALLOWED_MENTIONS)
        self.pool = lava_lyra.NodePool()

    def load_lavalinks(self):
        try:
            # Load lavalinks' settings
            with open("settings.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Json file not found.")
            return {}
        except json.JSONDecodeError:
            print("Failed to load json.")
            return {}

    async def connect_nodes(self):
        # Get lavalinks
        lavalinks: dict = self.load_lavalinks()
        for node in lavalinks:
            node_info: dict = lavalinks.get(node, {})
            host: str = node_info.get("host", "localhost")
            port: int = node_info.get("port", 443)
            password: str = node_info.get("password", "youshallnotpass")
            secure = bool(node_info.get("enable_secure", False))
            lyrics = bool(node_info.get("enable_lyrics", False))
            search = bool(node_info.get("enable_search", False))
            fallback = bool(node_info.get("enable_fallback", False))
            # Split line
            print("=" * 10)
            try:
                # Create Lavalink node with plugin supports
                node: lava_lyra.Node = await self.pool.create_node(
                    bot=self,
                    host=host,
                    port=port,
                    password=password,
                    secure=secure,
                    identifier=node,  # Node identify
                    lyrics=lyrics,  # Enable LavaLyrics plugin support
                    search=search,  # Enable LavaSearch plugin support
                    fallback=fallback,  # Enable fallback node
                )
                print(f"Created node: {node._identifier}")
            except NodeCreationError as error:
                print(f"Node ({node}) error while creating: {error}")
            except NodeConnectionFailure as error:
                print(f"Node ({node}) error while connecting: {error}")
            except Exception as error:  # noqa: BLE001
                print(f"Exception ({node}): {error}")

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
        print(f"Logged in as {self.user}")
        print(f"Synced {len(commands)} commands")
        # Initialize node connections
        await self.connect_nodes()


# Define the main function
async def main():
    bot = Bot()
    async with bot:
        await bot.start(TOKEN)


# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
