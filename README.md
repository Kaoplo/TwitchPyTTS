# TwitchPyTTS
Powered by PyTwitchAPI and gTTS

This is a simple application that will read out the chat of a twitch channel using text to speech
Currently WIP

## Running from source
### Prerequisites 
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
Enter the venv (on linux)
```bash
source bin/activate
```
Enter the venv (on windows)
```dos
.\Scripts\activate.bat
```
Install the required packages
```bash
pip -r requirements.txt
```

### Running the application
Create an application on dev.twitch.tv, make sure to add `http://localhost:17563` as an allowed URL

While in the venv, run `__main__.py`
```bash
python src/__main__.py
```
Click on configure before hitting start, and enter your client id and secret from the application you created on dev.twitch.tv