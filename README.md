# TwitchPyTTS
Powered by PyTwitchAPI and gTTS

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
Enter the venv
```bash
source bin/activate
```

Install the required packages
```bash
pip install twitchapi gTTS
```


### Running the application
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
python src/main.py
```

## Running from release
Go to the releases tab and donwload the latest binary for your OS

Create an application on dev.twitch.tv, make sure to add `http://localhost:17563` as an allowed URL

Create the `config.json` file in the same directory as the binary
```json
{
  "AppID": "",
  "AppSecret": "",
  "Channel": ""
}
```
Channel can be any channel you want to listen to

Run the binary