import discord
import lava_lyra

from .queue import CustomQueue


# Set CustomPlayer
class CustomPlayer(lava_lyra.Player):
    def __init__(self, client, channel, *, node=None):
        super().__init__(client, channel, node=node)
        self.queue = CustomQueue(max_history=50)
        self.home_channel: (
            discord.TextChannel | discord.Thread | discord.GroupChannel | None
        ) = None

    @property
    def channel_exists(self) -> bool:
        return bool(self.home_channel)

    async def update_message(self, **args) -> None:
        # Return if channel not exists
        if not self.channel_exists:
            return

        # Return if not guild
        if not self.home_channel.guild:
            return

        try:
            # Channel send
            await self.home_channel.send(**args)
        except Exception:  # noqa: BLE001
            # Return channel as none
            self.home_channel = None

    # Disconnect
    async def disconnect(self, *, force=False):
        # Clear cache
        self.queue.clear()
        self.queue.clear_history()
        self.home_channel = None

        return await super().disconnect(force=force)

    # Destroy player
    async def destroy(self) -> None:
        # Clear cache(same as disconnect logic)
        self.queue.clear()
        self.queue.clear_history()
        self.home_channel = None

        return await super().destroy()

    async def play_next(self, *, volume: int | None = None) -> lava_lyra.Track | None:
        # Play next song in the queue
        if self.queue.is_empty:
            await self.destroy()
            return

        # Get next track
        track = self.queue.get()

        if volume:
            self.queue.set_loop_mode(lava_lyra.LoopMode.QUEUE)
            await self.set_volume(min(100, max(0, volume)))

        if not self.queue.loop_mode:
            self.queue.put_history(track)

        # Play the track
        return await self.play(track)
