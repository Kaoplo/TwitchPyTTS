# TwitchPyTTS
Powered by PyTwitchAPI and gTTS

This is a simple application that will read out the chat of a twitch channel using text to speech
Currently WIP

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

Currently, the application does not create a `config.json` file for you, so you will have to create it yourself
```json
{
    "client_id": "",
    "client_secret": "",
    "redirect_uri": ""
}
```

While in the venv, run `__main__.py`
```bash
python src/__main__.py
```
Click on configure before hitting start, and enter your client id and secret from the application you created on https://dev.twitch.tv

