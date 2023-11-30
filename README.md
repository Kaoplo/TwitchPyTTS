# TwitchPyTTS
Powered by PyTwitchAPI and gTTS

This is a simple application that will read out the chat of a twitch channel using text to speech
Currently WIP

## Features/TODO
- [x] Read out chat
- [x] Ignore commands
- [x] Ignore user list
- [x] GUI
- [x] Configurable
- [] Add anonymous chat login (currently requires a twitch application)
- [] Add support for multiple channels
- [] Add support for multiple languages
- [] Add support for multiple voices
- [] Add support for multiple tts engines

## Running from source
### Prerequisites 
Clone the git repo
```bash
git clone https://github.com/Kaoplo/TwitchPyTTS.git && cd TwitchPyTTS
```
Create a venv
```bash
python -m venv .
```
Enter the venv 
<details>
<summary>On Linux</summary>

```bash
source bin/activate
```

</details>
<details>
<summary>On Windows</summary>

```powershell
.\Scripts\activate.ps1
```
</details>

Install the required packages
```bash
pip -r requirements.txt
```

### Running the application
Create an application on https://dev.twitch.tv, make sure to add `http://localhost:17563` as an allowed URL

While in the venv, run `__main__.py`
```bash
python src/__main__.py
```
Click on configure before hitting start, and enter your client id and secret from the application you created on https://dev.twitch.tv

