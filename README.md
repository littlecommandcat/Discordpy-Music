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
    git clone https://github.com/littlecommandcat/discord-music-bot.git
    cd discord-music-bot
```

2. Install dependencies:
```bash
    pip install -r requirements.txt
```

> Make sure requirements.txt includes:
> discord.py
> lava-lyra

3. Setup Lavalink server:
- Download from Lavalink GitHub: https://github.com/freyacodes/Lavalink
- Run with Java 17+
- Default host: localhost, port: 2333, password: youshallnotpass

---

## Configuration

- Replace your bot token in `bot.run('TOKEN')`
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

- Example:

    /play Never Gonna Give You Up

> The bot will automatically join your voice channel, search for the track, and play it.

/disconnect - Disconnect from your current voice channel

- Example:

    /disconnect

> The bot will automatically disconnect from your voice channel.

/queue - Show the current play queue

- Example:

    /queue

> Displays a list of all tracks currently waiting to be played. If the queue is empty, the bot will notify you.



/loop - Toggle loop mode for the queue

- Example:

    /loop

> Switches the loop mode on or off. When enabled, songs that finish playing are added back to the end of the queue for endless music.



/lyrics - Fetch and display lyrics for the current song

- Example:

    /lyrics

> Searches for lyrics matching the currently playing track. The results are displayed with timestamps if available from the node.


---

## Notes

- You must be in a voice channel to use the /play command.
- Supports Lavalink plugins (lyrics, search) if enabled.
- Ensure Lavalink node is running before starting the bot.

---

## License

This project is licensed under **GPL-3.0 License**. See LICENSE for details.

---

## Author

- littlecommandcat
- README.md edit by ChatGPT
- GitHub: https://github.com/littlecommandcat