import discord
import lava_lyra
from discord.ext import commands

from core import CustomPlayer


class MusicFilters(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.music_embed = discord.Embed(
            title="Music Filter",
            color=discord.Color.blue(),
        )

    async def get_player(self, ctx: commands.Context):
        """Validate the player and voice state."""
        player = ctx.voice_client

        if not isinstance(player, CustomPlayer):
            await ctx.send("No player found in this server.")
            return None

        # Check user voice state
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel.")
            return None

        # Check same voice channel
        if player.channel != ctx.author.voice.channel:
            await ctx.send("You are not in the bot's voice channel.")
            return None

        # Check current track
        if not player.is_playing or not player.current:
            await ctx.send("No music is currently playing.")
            return None

        return player

    @commands.command(name="filters")
    @commands.guild_only()
    async def filters(self, ctx: commands.Context):
        """List all replied filters."""
        player = await self.get_player(ctx)
        if not player:
            return

        # Filters empty
        if player.filters.empty:
            return await ctx.send("No filters had applied")

        self.music_embed.description = (
            f"Filters enabled."
        )

        # Display filters
        for f in player.filters.get_filters():
            for key, value in f.payload.items():
                display = ""
                for n, d in value.items():
                    display += f"{n}: {d}\n"

                self.music_embed.add_field(
                    name=key,
                    value=display
                )

        self.music_embed.footer.text = (
            f"`{self.bot.command_prefix}clearfilters` to disable filters"
        )

        await ctx.send(embed=self.music_embed)
        self.music_embed.clear_fields()


    @commands.command(name="rotate")
    @commands.guild_only()
    async def set_rotate(self, ctx: commands.Context, hz: float = 2.0):
        """Apply a rotation filter."""
        player = await self.get_player(ctx)
        if not player:
            return

        if hz <= 0:
            return await ctx.send("Rotation speed must be greater than `0`.")

        # Add/Set music filter
        await player.add_filter(
            lava_lyra.Rotation(
                tag="rotate",
                rotation_hertz=hz,
            ),
            fast_apply=True,
        )

        self.music_embed.description = (
            f"Rotation filter enabled.\n**Rotation speed: `{hz} Hz`**"
        )
        self.music_embed.footer.text = (
            f"`{self.bot.command_prefix}clearfilters` to disable filters"
        )

        await ctx.send(embed=self.music_embed)

    @commands.command(name="vibrato")
    @commands.guild_only()
    async def set_vibrato(
        self, ctx: commands.Context, depth: int = 5, frequency: float = 2.0
    ):
        """Apply a vibrato filter."""
        player = await self.get_player(ctx)
        if not player:
            return

        depth = depth / 10

        if depth <= 0 or frequency <= 0:
            return await ctx.send("Depth and frequency must be greater than `0`.")

        # Add/Set music filter
        await player.add_filter(
            lava_lyra.Vibrato(
                tag="vibrato",
                depth=depth,
                frequency=frequency,
            ),
            fast_apply=True,
        )

        self.music_embed.description = f"Vibrato filter enabled.\n**Depth: `{depth}` | Frequency: `{frequency} Hz`**"
        self.music_embed.footer.text = (
            f"`{self.bot.command_prefix}clearfilters` to disable filters"
        )

        await ctx.send(embed=self.music_embed)

    @commands.command(name="tremolo")
    @commands.guild_only()
    async def set_tremolo(
        self, ctx: commands.Context, depth: int = 5, frequency: float = 2.0
    ):
        """Apply a tremolo filter."""
        player = await self.get_player(ctx)
        if not player:
            return

        depth = depth / 10

        if depth <= 0 or frequency <= 0:
            return await ctx.send("Depth and frequency must be greater than `0`.")

        # Add/Set music filter
        await player.add_filter(
            lava_lyra.Tremolo(
                tag="tremolo",
                depth=depth,
                frequency=frequency,
            ),
            fast_apply=True,
        )

        self.music_embed.description = f"Tremolo filter enabled.\n**Depth: `{depth}` | Frequency: `{frequency} Hz`**"
        self.music_embed.footer.text = (
            f"`{self.bot.command_prefix}clearfilters` to disable filters"
        )

        await ctx.send(embed=self.music_embed)

    @commands.command(name="lowpass")
    @commands.guild_only()
    async def set_lowpass(self, ctx: commands.Context, strength: int = 5):
        """Apply a low-pass filter."""
        player = await self.get_player(ctx)
        if not player:
            return

        if strength <= 0 or strength > 10:
            return await ctx.send("Strength must be between `1` and `10`.")

        # Add/Set music filter
        await player.add_filter(
            lava_lyra.LowPass(
                tag="lowpass",
                smoothing=strength,
            ),
            fast_apply=True,
        )

        self.music_embed.description = (
            f"Low-pass filter enabled.\n**Filter strength: `{strength}`**"
        )
        self.music_embed.footer.text = (
            f"`{self.bot.command_prefix}clearfilters` to disable filters"
        )

        await ctx.send(embed=self.music_embed)

    @commands.command(name="speed")
    @commands.guild_only()
    async def set_speed(self, ctx: commands.Context, speed: float):
        """Change the music playback speed."""
        player = await self.get_player(ctx)
        if not player:
            return

        if not 0.1 <= speed <= 2.0:
            return await ctx.send("Speed must be between `0.1` and `2.0`.")

        # Add/Set music filter
        await player.add_filter(
            lava_lyra.Timescale(
                tag="speed",
                speed=speed,
            ),
            fast_apply=True,
        )

        self.music_embed.description = f"Playback speed set to `{speed}x`."
        self.music_embed.footer.text = (
            f"`{self.bot.command_prefix}clearfilters` to disable filters"
        )

        await ctx.send(embed=self.music_embed)

    @commands.command(name="nightcore")
    @commands.guild_only()
    async def set_nightcore(self, ctx: commands.Context):
        """Change the music playback speed."""
        player = await self.get_player(ctx)
        if not player:
            return

        # Add/Set music filter
        await player.add_filter(lava_lyra.Timescale.nightcore())

        self.music_embed.description = "Filter set as `nightcore`."
        self.music_embed.footer.text = (
            f"`{self.bot.command_prefix}clearfilters` to disable filters"
        )

        await ctx.send(embed=self.music_embed)

    @commands.command(name="vaporwave")
    @commands.guild_only()
    async def set_vaporwave(self, ctx: commands.Context):
        """Change the music playback speed."""
        player = await self.get_player(ctx)
        if not player:
            return

        # Add/Set music filter
        await player.add_filter(lava_lyra.Timescale.vaporwave())

        self.music_embed.description = "Filter set as `vaporwave`."
        self.music_embed.footer.text = (
            f"`{self.bot.command_prefix}clearfilters` to disable filters"
        )

        await ctx.send(embed=self.music_embed)

    @commands.command(name="karaoke")
    @commands.guild_only()
    async def set_karaoke(self, ctx: commands.Context):
        """Change the music karaoke mode."""
        player = await self.get_player(ctx)
        if not player:
            return

        # Add/Set music filter
        await player.add_filter(lava_lyra.Karaoke(tag="karaoke"))

        self.music_embed.description = "Filter set as `karaoke`."
        self.music_embed.footer.text = (
            f"`{self.bot.command_prefix}clearfilters` to disable filters"
        )

        await ctx.send(embed=self.music_embed)

    @commands.command(name="channelmix")
    @commands.guild_only()
    async def set_channelmix(
        self,
        ctx: commands.Context,
        left_to_left: float,
        right_to_right: float,
        left_to_right: float,
        right_to_left: float,
    ):
        """Set music channel mix."""
        player = await self.get_player(ctx)
        if not player:
            return

        # Add/Set music filter
        await player.add_filter(
            lava_lyra.ChannelMix(
                tag="channelmix",
                left_to_left=left_to_left,
                right_to_right=right_to_right,
                left_to_right=left_to_right,
                right_to_left=right_to_left,
            ),
            fast_apply=True,
        )

        self.music_embed.description = "Channel mix setup."
        self.music_embed.footer.text = (
            f"`{self.bot.command_prefix}clearfilters` to disable filters"
        )

        await ctx.send(embed=self.music_embed)

    @commands.command(name="clearfilters")
    @commands.guild_only()
    async def clear_all_filters(
        self, ctx: commands.Context, *, filters: str | None = None
    ):
        """Clear all active filters."""
        player = await self.get_player(ctx)
        if not player:
            return

        # Filters empty
        if player.filters.empty:
            self.music_embed.description = "No filter enabled."
            return await ctx.send(embed=self.music_embed)

        # Filters
        filter_list = filters.lower().split(" ")

        if not filter_list:
            # Reset all music filters
            await player.reset_filters(fast_apply=True)

            self.music_embed.description = "All music filters have been cleared."

        else:
            # Reset specific filter
            for ftag in filter_list:
                await player.remove_filter(filter_tag=ftag, fast_apply=True)

            self.music_embed.description = "Specific music filters have been cleared."

        self.music_embed.footer.text = ""

        await ctx.send(embed=self.music_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicFilters(bot))
