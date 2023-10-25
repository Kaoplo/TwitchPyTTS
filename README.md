# TwitchPyTTS
Powered by PyTwitchAPI

## Prerequisites 
Clone the git repo
```bash
git clone https://github.com/Kaoplo/TwitchPyTTS.git
```
```bash
cd TwitchPyTTS
```
Create a venv
```bash
python -m venv .
```
Enter the venv
```bash
source bin/activate
```

Install the required packages
```bash
pip install twitchapi pyttsx3
```

Install the required packages on your system (needed by pyttsx3)
- Debian, or other Ubuntu based distributions 
```bash
sudo apt update && sudo apt install espeak ffmpeg libespeak1
```
- Arch
```bash
sudo pacman -S espeak-ng
```

## Running the application
Create an application on dev.twitch.tv, make sure to add `http://localhost:17563` as an allowed URL

Edit the `config.json` file
```json
{
  "AppID": "",
  "AppSecret": "",
  "Channel": ""
}
```
Channel can be any channel you want to listen to

While in the venv, run `main.py`
```bash
python main.py
```