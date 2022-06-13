# VC-Userbot

A Telegram Userbot to play or streaming Audio and Video songs / files in Telegram Voice Chats.

It's made with [PyTgCalls](https://github.com/pytgcalls/pytgcalls) and [Pyrogram](https://github.com/pyrogram/pyrogram)


## Requirements
- Python +
- FFMPEG
- Nodejs v16+


## Deployment

### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Local Deploy
```
1) Installing NodeJS
bash
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs


2) Installing FFMPEG and Git
bash
sudo apt-get install git ffmpeg -y


3) Cloning the Repo
bash
git clone https://github.com/rioProjectx/Vc-Userbot
cd Vcmusic-Userbot


4) Rename `example.env` to `.env` and Fill in the Environment Variables

5) Installing Requirements
bash
pip3 install -U -r requirements.txt


6) Run the Bot
bash
python3 main.py
```


## Environment Variables
- `API_ID`
- `API_HASH`
- `SESSION` - A Pyrogram String Session. Get one from [Here](https://replit.com/@KennedyProject/String-Session)
- `HNDLR` - Your Userbot Handler (Default is !)


## Commands and Usage
1) Start the Userbot, check if the Userbot is running by `!ping`.
2) Commands of this userbot are accessible to and can be used by the Account itself and it's Contacts.
3) Check `!help` for commands.


## Credits 💭
- [KennedyProject](https://github.com/KennedyProject)
- [Dan](https://github.com/delivrance) for [Pyrogram](https://github.com/pyrogram/pyrogram)
- [Laky](https://github.com/Laky-64) for [PyTgCalls](https://github.com/pytgcalls/pytgcalls)
