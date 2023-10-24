# TwitchPyTTS
Powered by PyTwitchAPI

## Dependencies
Make sure you run these in a venv

Install the required packages
```bash
pip install twitchapi pyttsx3
```

Install the required packages on your system (needed by pyttsx3)
```bash
 sudo apt update && sudo apt install espeak ffmpeg libespeak1
```

## Before running
Create an application on dev.twitch.tv

Edit the `config.json` file
```json
{
  "AppID": "",
  "AppSecret": "",
  "Channel": ""
}
```

## Running the application
While in the venv, run `main.py`
```bash
python main.py
```