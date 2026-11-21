# Discord 音樂機器人（LavaLyra）

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
[![Discord Bot](https://img.shields.io/badge/Discord-Bot-5865F2?logo=discord&logoColor=white)](https://discord.com/developers/applications)

一個使用**discord.py**與**lava-lyra**的簡易 Discord 音樂機器人。

支援透過 Lavalink/Nodelink從 YouTube、Spotify、Apple Music等多種來源播放音樂。

---

## 語言
[English](README.md)｜[繁體中文](README-zh.md)

## 功能

- 支援多種音樂來源（YouTube、Spotify、SoundCloud、Apple Music）
- 在機器人狀態中顯示目前播放的音樂（僅支援YouTube與Twitch）
- 自動連接Lavalink或Nodelink節點
- 使用Discord`app_commands`的斜線指令
- 支援LavaLyrics與LavaSearch外掛
- 支援Fallback備援機制提高穩定性

---

## 系統需求

- Python 3.12+（[`lava-lyra` >= 2.2.0](https://github.com/ParrotXray/lava-lyra/releases/tag/v2.2.0)）
- discord.py
- [lava-lyra](https://github.com/ParrotXray/lava-lyra)
- Lavalink或Nodelink伺服器

---

## 安裝

### 1. 複製此專案

```bash
git clone https://github.com/littlecommandcat/discordpy-music.git
```

### 2. 安裝依賴套件

```bash
pip install -r requirements.txt
```

> 確認 `requirements.txt` 包含以下套件（或直接使用 git clone）：
>
> discord.py
> lava-lyra

### 3. 設定音樂伺服器

#### Lavalink

- 從 [Lavalink GitHub](https://github.com/freyacodes/Lavalink) 下載
- 使用 Java 17 或更新版本執行（建議使用最新的LTS版本或更新版本）
- 預設主機：`localhost`
- 預設連接埠：`2333`
- 預設密碼：`youshallnotpass`

#### Nodelink

- 從 [Nodelink GitHub](https://github.com/PerformanC/NodeLink) 下載
- 使用Node.js v22或更新版本執行（推薦使用 v24）

---

### 4. 環境變數

```ini
# Discord機器人設定
TOKEN=""    # Discord機器人 Token
PREFIX=""   # 機器人指令前綴

# Lavalink/Nodelink設定 -> settings.json
```

### 5. Lavalink 設定

```json
{
  "node1": { // 節點識別名稱
    "host": "127.0.0.1", // 節點主機（預設為 "localhost"）
    "port": 2333, // 節點連接埠（預設為 443）
    "password": "youshallnotpass", // Lavalink 密碼（預設為 "youshallnotpass"）
    "enable_secure": false, // 是否啟用安全連線（預設為 false）
    "enable_lyrics": true, // 是否啟用歌詞功能（預設為 false）
    "enable_search": true, // 是否啟用搜尋功能（預設為 false）
    "enable_fallback": false // 是否啟用 Fallback 備援（預設為 false）
  }
}
```

---

## 使用方式

### 斜線指令

#### `/play` - 播放音樂

在目前所在的語音頻道中播放歌曲。

- 範例：`/play <Never Gonna Give You Up>`

> 機器人會自動加入你的語音頻道、搜尋歌曲並開始播放。

#### `/disconnect` - 中斷語音連線

- 範例：`/disconnect`

> 機器人會自動離開目前的語音頻道並銷毀播放器。

#### `/queue` - 查看播放佇列

- 範例：`/queue`

> 顯示目前等待播放的所有歌曲。

#### `/loop` - 切換循環模式

- 範例：`/loop`

> 在以下模式之間切換：
>
> 重複目前歌曲、重複整個佇列或停用循環。

#### `/shuffle` - 隨機播放佇列

- 範例：`/shuffle`

> 將目前播放佇列中的歌曲順序隨機打亂。

#### `/volume <1-500>` - 設定音量

- 範例：`/volume <100>`

> 調整機器人的播放音量。

#### `/lyrics` - 取得歌詞

- 範例：`/lyrics`

> 搜尋目前播放歌曲所對應的歌詞。

#### `/history` - 查看播放紀錄

- 範例：`/history`

> 顯示最近播放過的歌曲。

#### `/nodes` - 查看節點資訊

- 範例：`/nodes`

> 顯示Lavalink或Nodelink節點的相關資訊。

---

### 前綴指令

#### `?rotate [hz]` - 套用旋轉效果

- 範例：`?rotate 2`

> 對目前播放的歌曲套用立體聲旋轉效果。預設旋轉速度為`2 Hz`。

#### `?vibrato [depth] [frequency]` - 套用顫音效果

- 範例：`?vibrato 5 2`

> 對目前播放的歌曲套用顫音效果。`depth`控制效果強度，`frequency`控制調變速度。

#### `?tremolo [depth] [frequency]` - 套用震音效果

- 範例：`?tremolo 5 2`

> 套用會快速改變目前歌曲音量的震音效果。

#### `?lowpass [strength]` - 套用低通濾波器

- 範例：`?lowpass 5`

> 降低高頻聲音。`strength`可設定為`1`到`10`。

#### `?speed` - 更改播放速度

- 範例：`?speed 1.5`

> 更改目前歌曲的播放速度。支援範圍為`0.1x`至`2.0x`。

#### `?nightcore` - 套用Nightcore效果

- 範例：`?nightcore`

> 套用Nightcore風格效果，提高歌曲的播放速度與音高。

#### `?vaporwave` - 套用Vaporwave效果

- 範例：`?vaporwave`

> 套用Vaporwave風格效果，降低歌曲的播放速度與音高。

#### `?karaoke` - 啟用卡拉OK模式

- 範例：`?karaoke`

> 嘗試降低目前歌曲中的人聲。

#### `?channelmix <left_to_left> <right_to_right> <left_to_right> <right_to_left>` - 設定立體聲聲道混音

- 範例：`?channelmix 1 1 0 0`

> 控制左右聲道的音訊如何混合與輸出。

### 清除濾鏡

#### `?clearfilters [filters]` - 清除目前套用的音樂濾鏡

- 範例：`?clearfilters`

> 移除所有目前套用的音樂濾鏡。

- 範例：`?clearfilters rotate vibrato`

> 僅移除指定的濾鏡。

---

## 注意事項

- 使用`/play`指令前必須先加入語音頻道。
- 如果已啟用相關外掛則支援Lavalink外掛（歌詞、搜尋）。
- 啟動機器人之前請確保Lavalink/Nodelink節點伺服器已經正常運行。

---

## 授權條款

本專案採用 [GPL-3.0 License](/LICENSE) 授權。

詳細資訊請參閱LICENSE。