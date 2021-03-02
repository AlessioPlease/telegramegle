from pyomegle import OmegleHandler
from Levenshtein import distance
from telegram import Telegram
import threading
import re

t = Telegram()

class CustomHandler(OmegleHandler):
    cc = 0

    def __init__(self, checkpoint, loop=False):
        self.checkpoint = checkpoint
        self.loop = loop

    # Called each time a message is received from the stranger
    def message(self, message):
        print('Stranger: %s' % message)
        # If autoMode is on the bot will try to get the name and the
        # age from the stranger and it will notify the user afterwards.
        # Each message received the bot will look for numbers if the
        # stranger typed their age at the beginning of the chat.
        # Otherwise the bot will ask for these information.
        # The next message after the bot's question is taken
        # for granted to be the answer to the question.
        # distance(message, 'string') --- this is used to understand
        # the stranger answer even if they made a typo.
        # The bigger the number is, the more flexible the bot will be.
        if self.checkpoint.autoMode:
            self.checkpoint.messagesCount += 1
            message = message.strip()
            message = message.lower()

            if "years" in message:
                if not any(char.isdigit() for char in message):
                    if message == 'age'\
                            or message == 'age?'\
                            or distance(message, 'how old') <= 2\
                            or distance(message, 'how old are you') <= 2\
                            or distance(message, 'how old are u') <= 2:
                        thread3 = threading.Thread(target=self.cc.write('I\'m xx years old'))
                        thread3.start()
                else:
                    age = int(''.join(filter(str.isdigit, message)))
                    self.checkpoint.strangerAge = age
            elif any(char.isdigit() for char in message):
                age = int(''.join(filter(str.isdigit, message)))
                self.checkpoint.strangerAge = age
            elif message == 'name':
                thread4 = threading.Thread(target=self.cc.write('my name is User :)'))
                thread4.start()
            else:
                if self.checkpoint.amIAskingForName:
                    name = re.sub('i\'m|my|name|is|am|called|nice|to|meet|you|,| |\?', '', message)
                    self.checkpoint.strangerName = name
                    self.checkpoint.amIAskingForName = False
                    if 'you' in message:
                        thread5 = threading.Thread(target=self.cc.write('my name is User :)'))
                        thread5.start()

            if (self.checkpoint.messagesCount == 2 and self.checkpoint.strangerName == '')\
                    or (self.checkpoint.messagesCount == 1 and ('yes' in message or 'ok' in message)):
                thread1 = threading.Thread(target=self.cc.write('What\'s your name?'))
                thread1.start()
                self.checkpoint.amIAskingForName = True

            if (self.checkpoint.messagesCount == 2 and self.checkpoint.strangerName != '')\
                    or (self.checkpoint.messagesCount == 3 and self.checkpoint.strangerAge == 0):
                thread2 = threading.Thread(target=self.cc.write('How old are you {}?'.format(self.checkpoint.strangerName)))
                thread2.start()

            if self.checkpoint.messagesCount > 2 and not self.checkpoint.informedUser and self.checkpoint.strangerAge != 0 and self.checkpoint.strangerName != '':
                t.informUser(self.checkpoint.strangerName, self.checkpoint.strangerAge)
                self.checkpoint.informedUser = True
        else:
            t.send(message)

# Called when you are connected to a stranger
    def connected(self):
        print('You\'re now chatting with a random stranger. Say hi!')
        if not self.checkpoint.autoMode:
            t.send('You\'re now chatting with a random stranger. Say hi!')
        thread6 = threading.Thread(target=self.cc.write('Hi! I am looking to chat with someone, is that you?'))
        thread6.start()

# Called when a stranger disconnects
    def disconnected(self):
        print('Stranger has disconnected.')
        if not self.checkpoint.autoMode:
            t.send('Stranger has disconnected.')
        if self.loop:
            self.omegle.start()
        self.checkpoint.reset()

# Probably called when the server says you are banned
    def handle_error(self):
        print('You have probably been banned.')
        t.send('You have probably been banned.')
