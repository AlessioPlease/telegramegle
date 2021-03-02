from pyomegle import OmegleClient
from CustomHandler import CustomHandler
from CustomClient import CustomClient
from Checkpoints import Checkpoint
from telegram import Telegram
import threading
import time

# Class used to store variables to let the autoMode work
checkpoint = Checkpoint()

# Checks updates from the bot's chat each 0.5 seconds
# /start = starts a new conversation
# /next = disconnects from current stranger and starts a new conversation
# /stop = stops automatically starting new conversations
# /auto = the bot will automatically look for strangers and will notify
#         the user when a stranger meets the user's requirements.
#         You can edit the bot's behavior in CustomHandler.py
# /manual = turns automatic mode off
bol = True
def getUpdates():
    while bol:
        answer = t.getUpdates()
        if answer != '':
            t.update_id += 1
            if answer == '/start':
                h.loop = True
                client.start()
                t.send('Looking for someone you can chat with...')
            elif answer == '/next':
                t.send("NEXT! Starting a new conversation")
                client.next()
            elif answer == '/stop':
                h.loop = False
                cc.disconnect()
                t.send('You have disconnected.')
            elif answer == '/auto':
                t.send('Auto mode: ON')
                checkpoint.autoMode = True
            elif answer == '/manual':
                t.send('Auto mode: OFF')
                checkpoint.autoMode = False
            else:
                cc.send(answer)
        time.sleep(0.5)


# Setting up Omegle Client
h = CustomHandler(checkpoint, loop=True)
client = OmegleClient(h, wpm=600, lang='it')  # COMMENTO PER LA LINGUA
cc = CustomClient(client, checkpoint)

h.cc = cc

# Starting Telegram bot
t = Telegram()
thread = threading.Thread(target=getUpdates)
thread.start()


# Checks for any input from the PC's keyboard
# /next = starts a new conversation
# /stop = stops automatically starting new conversations
# /exit = disconnects from current stranger and doesn't start a new conversation
while True:
    inputStr = input('')

    if inputStr == 'ùù':
        cc.typing()
    elif inputStr.strip() == '/next':
        client.next()
    elif inputStr.strip() == '/stop':
        print('WILL STOP AT NEXT DISCONNECTION')
        h.loop = False
    elif inputStr.strip() == '/exit':
        bol = False
        cc.disconnect()
        break
    else:
        cc.send(inputStr)
