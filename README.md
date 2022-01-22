# Telegramegle
Telegramegle is a Python API to use Omegle.com through Telegram bots.

# Installation
To use Telegramegle you will need Python3 or a newer version. You can download and install Python from [here](https://www.python.org/downloads/).  
Once you have installed Python, run the following commands to install Telegramegle:
```
cd your_path/telegramegle-master
python setup.py install --user
```

### Run
To run Telegramegle use the following commands 
(however, you will need to set up the Telegram bot first):
```
cd your_path/telegramegle-development/telegramegle
python3 run.py
```

# Telegram bot setup
### 1. Create a telegram bot
As shown in [this guide](https://core.telegram.org/bots#6-botfather), follow these steps:
1. Open the Telegram app
2. Start a chat with [@botfather](https://t.me/botfather) and send the message **/start**
3. Use the **/newbot** command to create a new bot
4. Write a name for your nor
5. Write a username for you bot

The BotFather will now generate a unique *token*, specific for your bot. It will look something like this: `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`  
**Keep your token secure and store it safely, it can be used by anyone to control your bot.**

### 2. Get your Telegram user ID
To retrieve your Telegram user ID you can start a chat with one of these two bots (just typing `/start` will suffice):
1. [@userinfobot](https://t.me/userinfobot) (more informations [here](https://github.com/nadam/userinfobot))
2. [@getmyid_bot](https://t.me/getmyid_bot) (more informations [here](https://botostore.com/c/getmyid_bot/))

If neither of the bots happen to work follow the next steps:
1. Open the Telegram app
2. Start a chat with your bot and send the message **/start** (your bot can be found using the username you've chosen)
3. Open the file `telegramSetup.py`
4. Edit the `updatesUrl` variable replacing `<YOUR BOT TOKEN>` with your bot's token (you must delete the angle brackets too)
5. Finally, run `telegramSetup.py` using following commands:
```
cd your_path/telegramegle-development/telegramegle
python3 telegramSetup.py
```

If everything went according to the plan, the output should contain your Telegram user ID. It will look something like this: `123456789`


### 3. Replace token and user ID
1. Open the file `telegram.py`
2. Edit the `messageUrl` variable replacing `<YOUR BOT TOKEN>` with your bot's token (you must delete the angle brackets too)
3. Edit the `updatesUrl` variable replacing `<YOUR BOT TOKEN>` with your bot's token (you must delete the angle brackets too)
4. Edit the `chatId` variable replacing `<YOUR CHAT ID>` with your Telegram user ID (you must delete the angle brackets too)

### You are all set! Enjoy!

# Customization
In order for the Omegle API to work properly I added two classes: `CustomHandler` and `CustomClient`.  
The `CustomHandler` class (children of OmegleHandler) will process all events coming from the server (for example, incoming messages from the stranger).  
The `CustomClient` class ("clone" of OmegleClient) is used to deal with all client's events and send http requests to the server.  
I suggest not to edit `pyomegle.py` and to edit the custom classes instead.
