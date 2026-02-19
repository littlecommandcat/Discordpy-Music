# Discord Music Bot (LavaLyra)

A simple Discord music bot using **discord.py** and **lava-lyra**.  
Supports music playback from YouTube, Spotify, Apple Music, and more with Lavalink/Nodelink.

---

## Features

- Play music from multiple sources (YouTube, Spotify, Apple Music)
- Automatic node connection with Lavalink or Nodelink
- Slash commands with Discord app_commands
- Supports LavaLyrics and LavaSearch plugins
- Fallback support for better reliability

---

## Requirements

- Python 3.11+
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

> Make sure requirements.txt includes:
> discord.py
> lava-lyra

3. Setup Music server:
- Lavalink
    - Download from Lavalink GitHub: https://github.com/freyacodes/Lavalink
    - Run with Java 17+ (recommend running the latest LTS version or newer)
    - Default host: localhost, port: 2333, password: youshallnotpass
- Nodelink
    - Download from Nodelink GitHub: https://github.com/PerformanC/NodeLink
    - Run with Node.js v22 or higher (v24 recommended)
---

## Configuration

- Replace your bot token in `bot.start('TOKEN')`
- Optionally, modify Lavalink node settings in `on_ready()`:
```
    host='localhost'
    port=2333
    password='youshallnotpass'
    secure=False
    identifier='MAIN'
    lyrics=False
    search=True
    fallback=True
```
---

## Usage

### Slash Command

/play <query> - Play a song in your current voice channel
- Example: `/play Never Gonna Give You Up`
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
- Example: `/volume 100`
> Adjusts the playback volume of the bot.


/lyrics - Fetch and display lyrics for the current song
- Example: `/lyrics`
> Searches for lyrics matching the current track.


---

## Notes

- You must be in a voice channel to use the /play command.
- Supports Lavalink plugins (lyrics, search) if enabled.
- Ensure Lavalink/Nodelink node is running before starting the bot.

---

## License

This project is licensed under **GPL-3.0 License**. See LICENSE for details.

---

## Author

- littlecommandcat
- GitHub: https://github.com/littlecommandcat