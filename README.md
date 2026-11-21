# Discord Music Bot (LavaLyra)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
[![Discord Bot](https://img.shields.io/badge/Discord-Bot-5865F2?logo=discord&logoColor=white)](https://discord.com/developers/applications)

A simple Discord music bot using **discord.py** and **lava-lyra**.  
Supports music playback from YouTube, Spotify, Apple Music, and more with Lavalink/Nodelink.

---

## Language
[English](README.md)｜[繁體中文](README-zh.md)

## Features

- Play music from multiple sources (YouTube, Spotify, SoundCloud, Apple Music)
- Display music streaming on bot presence (only for YouTube and Twitch)
- Automatic node connection with Lavalink or Nodelink
- Slash commands with Discord app_commands
- Supports LavaLyrics and LavaSearch plugins
- Fallback support for better reliability

---

## Requirements

- Python 3.12+（[`lava-lyra` >= 2.2.0](https://github.com/ParrotXray/lava-lyra/releases/tag/v2.2.0)）
- discord.py
- [lava-lyra](https://github.com/ParrotXray/lava-lyra)
- Lavalink or Nodelink server

---

## Installation

1. Clone this repository:
```bash
git clone https://github.com/littlecommandcat/discordpy-music.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

> Make sure requirements.txt includes (or use git clone):
> discord.py
> lava-lyra

3. Setup music server:
- Lavalink
    - Download from Lavalink GitHub: https://github.com/freyacodes/Lavalink
    - Run with Java 17+ (recommend running the latest LTS version or newer)
    - Default host: localhost, port: 2333, password: youshallnotpass
- Nodelink
    - Download from Nodelink GitHub: https://github.com/PerformanC/NodeLink
    - Run with Node.js v22 or higher (v24 recommended)
---

4. Environment:
```ini
# Discord Bot Configuration
TOKEN=""    # Discord bot token
PREFIX=""   # Bot command prefix

# Lavalink/Nodelink Configuration -> settings.json
```

5. Settings(Lavalink)
```json
{
  "node1": { // Node identify
    "host": "127.0.0.1", // Node host (default "localhost")
    "port": 2333, // Node port (default 443)
    "password": "youshallnotpass", // Lavalink password (default "youshallnotpass")
    "enable_secure": false, // Enable secure (default false)
    "enable_lyrics": true, // Enable lyrics (default false))
    "enable_search": true, // Enable search (default false))
    "enable_fallback": false // Enable fallback (default false))
  }
}
```

## Usage

### Slash Command

/play - Play a song in your current voice channel

- Example: `/play <Never Gonna Give You Up>`

> The bot will automatically join your voice channel, search for the track, and play it.

/disconnect - Disconnect from your current voice channel

- Example: `/disconnect`

> The bot will automatically disconnect from your voice channel and destroy the player.

/queue - Show the current play queue

- Example: `/queue`

> Displays a list of all tracks currently waiting to be played.

/loop - Toggle loop mode for the queue

- Example: `/loop`

> Switches between: `TRACK` (repeat current), `QUEUE` (repeat list), or `DISABLED`.

/shuffle - Shuffle the play queue

- Example: `/shuffle`

> Randomizes the order of tracks in the current queue.

/volume <1-500> - Set bot volume

- Example: `/volume <100>`

> Adjusts the playback volume of the bot.

/lyrics - Fetch and display lyrics for the current song

- Example: `/lyrics`

> Searches for lyrics matching the current track.

/history - Get the play history

- Example: `/history`

> Sends back the recently played tracks.

/nodes - Get nodes info

- Example: `/nodes`

> Sends back Lavalink or Nodelink node information.

---

### Prefix Commands

?rotate [hz] - Apply a rotation filter

- Example: `?rotate 2`

> Applies a stereo rotation effect to the current track. The default rotation speed is `2 Hz`.

?vibrato [depth] [frequency] - Apply a vibrato effect

- Example: `?vibrato 5 2`

> Applies a vibrato effect to the current track. `depth` controls the intensity and `frequency` controls the modulation speed.

?tremolo [depth] [frequency] - Apply a tremolo effect

- Example: `?tremolo 5 2`

> Applies a tremolo effect that rapidly changes the volume of the current track.

?lowpass [strength] - Apply a low-pass filter

- Example: `?lowpass 5`

> Reduces high-frequency sounds. `strength` can be set from `1` to `10`.

?speed <speed> - Change playback speed

- Example: `?speed 1.5`

> Changes the playback speed. The supported range is `0.1x` to `2.0x`.

?nightcore - Apply the Nightcore effect

- Example: `?nightcore`

> Applies a Nightcore-style effect by increasing the playback speed and pitch.

?vaporwave - Apply the Vaporwave effect

- Example: `?vaporwave`

> Applies a Vaporwave-style effect by slowing down the track and lowering its pitch.

?karaoke - Enable karaoke mode

- Example: `?karaoke`

> Attempts to reduce the vocals from the current track.

?channelmix <left_to_left> <right_to_right> <left_to_right> <right_to_left> - Configure stereo channel mixing

- Example: `?channelmix 1 1 0 0`

> Controls how audio from the left and right channels is mixed and routed.

### Clearing Filters

?clearfilters [filters] - Clear active music filters

- Example: `?clearfilters`

> Removes all active music filters.

- Example: `?clearfilters rotate vibrato`

> Removes only the specified filters.

---

## Notes

- You must be in a voice channel to use the /play command.
- Supports Lavalink plugins (lyrics, search) if enabled.
- Ensure Lavalink/Nodelink node is running before starting the bot.

---

## License

This project is licensed under [GPL-3.0 License](/LICENSE). See LICENSE for details.
