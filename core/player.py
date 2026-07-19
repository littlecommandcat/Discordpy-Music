import lava_lyra
from .queue import CustomQueue

# Set CustomPlayer
class CustomPlayer(lava_lyra.Player):
    def __init__(self, client, channel, *, node = None):
        super().__init__(client, channel, node=node)
        self.queue = CustomQueue()
        self._last_track: lava_lyra.Track | None = None

    async def play_next(self):
        # Play next song in the queue
        if self.queue.is_empty:
            return

        # Get next track
        track = self.queue.get()
        self._last_track = track
        if not self.queue.loop_mode:
            self.queue.put_history(track)

        # Play the track
        await self.play(track)