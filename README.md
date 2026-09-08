# TwitchPyTTS
Reads out a Twitch channel's chat using a small, local, offline neural TTS voice
(powered by [Piper](https://github.com/OHF-Voice/piper1-gpl)).

## Features/TODO
- [x] Read out chat
- [x] Ignore commands
- [x] Ignore user list
- [x] GUI
- [x] Configurable
- [x] Anonymous chat login (no Twitch application / OAuth needed)
- [x] Local/offline neural voice model (Piper) instead of a cloud TTS API
- [x] Moderator command to interrupt/skip the message currently being read
- [x] Highlight the message currently being read in the UI
- [ ] Add support for multiple channels
- [ ] Add support for multiple languages
- [ ] Add support for multiple voices

## How it works
- **Chat connection**: connects to Twitch IRC anonymously with a throwaway
  `justinfanXXXXXX` nickname - this is Twitch's supported read-only anonymous
  login, so you don't need to register an app on dev.twitch.tv or get an
  OAuth token. It also requests the `tags`/`commands` IRCv3 capabilities so it
  can see a chatter's badges (needed for the mod-only skip command).
- **Voice**: uses [Piper](https://github.com/rhasspy/piper), a small, fast,
  fully-offline neural TTS engine (voices are ~20-60MB and run in real time on
  CPU). The default voice (`en_US-lessac-medium`) is downloaded automatically
  the first time you start the app and cached in `voices/`.
- **Moderator skip command**: a moderator or the broadcaster can type
  `!skip` (configurable) in chat to immediately interrupt whatever is
  currently being read out loud.
- **UI**: the chat list highlights whichever message is currently being
  spoken.

## Running the application
Download the binary from the releases page! Run the application and configure from the configure window. You might need to change the file permissions to allow for execution.

## Project layout
```
src/
├── app_config.py          # config.json load/save + legacy-schema migration
├── core/
│   ├── chat_message.py    # ChatMessage dataclass shared by every layer
│   ├── commands.py        # pure "is this the mod skip command?" logic (unit tested)
│   └── speech_queue_worker.py  # QThread worker: queue -> synthesize -> play
├── twitch/
│   ├── irc_parse.py       # pure IRC line parsing (unit tested, no socket)
│   └── irc_client.py      # QThread worker: socket I/O using irc_parse
├── tts/
│   ├── base.py             # VoiceEngine interface
│   ├── piper_engine.py     # Piper implementation + voice auto-download
│   ├── voice_models.py     # voice name -> file path / download URL (unit tested)
│   └── playback.py         # interruptible audio playback (sounddevice)
└── gui/
    ├── main_window.py      # wires IRC thread + speech thread + list widget together
    ├── config_window.py
    └── ui/                 # Qt Designer files + generated ui_*.py
```
The networking, TTS, and command-decision logic are kept Qt-free on purpose
so they can be unit tested directly - see `tests/`.



## Running from source
### Prerequisites
Clone the git repo, then create and enter a venv:
```bash
python -m venv .venv
source .venv/bin/activate   # .venv\Scripts\activate.ps1 on Windows
```
Install the required packages:
```bash
pip install -r requirements.txt
```
### Running

No Twitch application/client id is needed. While in the venv, run:
```bash
python -m src
```
Click **configure**, set the channel you want to read out loud, then hit
**start**. The first time you start the app it will download the default
voice model.

### Running the tests

```bash
python -m unittest discover -s tests
```
