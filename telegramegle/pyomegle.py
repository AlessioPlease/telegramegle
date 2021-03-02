from __future__ import division
import mechanize
import threading
import urllib
import random
import time
import json
import re


class EventThread(threading.Thread):

    def __init__(self, instance, start_url):
        threading.Thread.__init__(self)
        self.instance = instance
        self.start_url = start_url
        self._stop = threading.Event()

    def run(self):
        try:
            response = self.instance.browser.open(self.start_url)
        except Exception as ex:
            print (str(ex))
            return

        try:
            data = json.load(response)
        except ValueError as ex:
            print (str(ex))

        try:
            self.instance.client_id = data['clientID']
            self.instance._handle_events(data['events'])
        except KeyError:
            if not len(response.read()):
                print("(Blank server response) Error connecting to server. Please try again.")
                print("If problem persists then your IP may be soft banned, try using a VPN.")

        while not self.instance.connected:
            self.instance._events_manager()

        while self.instance.connected:
            self.instance._events_manager()

    def stop(self):
        self._stop.set()


class Omegle(object):
    SERVER_LIST = [f'front{n}.omegle.com' for n in range(1, 33)]

    STATUS_URL =            'http://%s/status?nocache=%s&randid=%s'
    START_URL =             'http://%s/start?caps=recaptcha2&firstevents=%s&spid=%s&randid=%s&lang=%s'
    RECAPTCHA_URL =         'http://%s/recaptcha'
    EVENTS_URL =            'http://%s/events'
    TYPING_URL =            'http://%s/typing'
    STOPPED_TYPING_URL =    'http://%s/stoppedtyping'
    DISCONNECT_URL =        'http://%s/disconnect'
    SEND_URL =              'http://%s/send'

    def __init__(self, events_handler, firstevents=1, spid='', random_id=None, topics=[], lang='en', event_delay=3):
        self.events_handler = events_handler
        self.firstevents = firstevents
        self.spid = spid
        self.topics = topics
        self.lang = lang
        self.event_delay = event_delay
        self.random_id = random_id or self._randID(8)

        self.connected = False

        self.server = random.choice(self.SERVER_LIST)
        self.client_id = None
        self.connected = False
        self.browser = mechanize.Browser()
        self.browser.addheaders = []

        # Call additional setup
        self.events_handler._setup(self)

# Generate a random ID for chat session
    def _randID(self, length):
        return ''.join([random.choice('23456789ABCDEFGHJKLMNPQRSTUVWXYZ')
                        for _ in range(length)])

# Handle the chat events
    def _handle_events(self, events):
        for event in events:
            try:
                self._event_selector(event)
            except TypeError as e:
                print (e)
                print ('DEBUG', event)
            continue

# Select the correct events and call the handler
    def _event_selector(self, event):
        event_type = event[0]

        if event_type == 'waiting':
            self.events_handler.waiting()
        elif event_type == 'typing':
            self.events_handler.typing()
        elif event_type == 'connected':
            self.connected = True
            self.events_handler.connected()
        elif event_type == 'gotMessage':
            message = event[1]
            self.events_handler.message(message)
        elif event_type == 'commonLikes':
            likes = event[1]
            self.events_handler.common_likes(likes)
        elif event_type == 'stoppedTyping':
            self.events_handler.stopped_typing()
        elif event_type == 'strangerDisconnected':
            self.disconnect()
            self.events_handler.disconnected()
        elif event_type == 'recaptchaRequired':
            self.events_handler.captcha_required()
        elif event_type == 'recaptchaRejected':
            self.events_handler.captcha_rejected()
        elif event_type == 'serverMessage':
            message = event[1]
            self.events_handler.server_message(message)
        elif event_type == 'statusInfo':
            status = event[1]
            self.events_handler.status_info(status)
        elif event_type == 'identDigests':
            digests = event[1]
            self.events_handler.ident_digest(digests)
        else:
            print('Unhandled event: %s' % event)
            if event[0] == 'error':
                self.events_handler.handle_error()

# Opens the url with data info
    def _request(self, url, data=None):
        data = urllib.parse.urlencode(data)

        try:
            response = self.browser.open(url, data)
            return response
        except Exception as ex:
            print("Error request", ex)

# Event manager class
    def _events_manager(self):
        url = self.EVENTS_URL % self.server
        data = {'id': self.client_id}
        try:
            response = self._request(url, data)
            data = json.load(response)
        except Exception as ex:
            print(ex)
            return False
        if data:
            self._handle_events(data)
        return True

# Return connection status
    def status(self):
        nocache = '%r' % random.random()
        url = self.STATUS_URL % (self.server, nocache, self.random_id)

        response = self._request(url)
        data = json.load(response)

        return data

# Start a new conversation
    def start(self):
        url = self.START_URL % (self.server, self.firstevents,
                                self.spid, self.random_id, self.lang)
        if self.topics:
            # Add custom topic to the url
            url += '&' + urllib.parse.urlencode({'topics': json.dumps(self.topics)})

        thread = EventThread(self, url)
        thread.start()
        self.thread = thread

        return thread

# Captcha validation
    def recaptcha(self, challenge, response):
        url = self.RECAPTCHA_URL % self.server
        data = {'id': self.client_id, 'challenge':
                challenge, 'response': response}
        try:
            self._request(url, data)
            return True
        except Exception:
            return False

# Emulate typing in the conversation
    def typing(self):
        url = self.TYPING_URL % self.server
        data = {'id': self.client_id}
        try:
            self._request(url, data)
            print('You are typing...')
            return True
        except Exception:
            return False

# Emulate stopped typing into the conversation
    def stopped_typing(self):
        url = self.STOPPED_TYPING_URL % self.server
        data = {'id': self.client_id}
        try:
            self._request(url, data)
            print('You stopped typing...')
            return True
        except Exception:
            return False

# Send a message to Omegle's stranger
    def send(self, message):
        url = self.SEND_URL % self.server
        data = {'msg': message, 'id': self.client_id}
        try:
            self._request(url, data)
            return True
        except Exception as ex:
            print("Send: ", ex)
            return False

# Disconnect from the current conversation
    def disconnect(self):
        self.connected = False
        url = self.DISCONNECT_URL % self.server
        data = {'id': self.client_id}
        try:
            self.thread.stop()
            self._request(url, data)
            return True
        except Exception:
            return False


# Abstract class for defining Omegle event handlers
class OmegleHandler(object):

    RECAPTCHA_CHALLENGE_URL = 'http://www.google.com/recaptcha/api/challenge?k=%s'
    RECAPTCHA_IMAGE_URL = 'http://www.google.com/recaptcha/api/image?c=%s'
    recaptcha_challenge_regex = re.compile(r"challenge\s*:\s*'(.+)'")

    def __init__(self, loop=False):
        self.loop = loop

# Called by the Omegle class for initial additional settings
    def _setup(self, omegle):
        self.omegle = omegle

# Called while waiting for a stranger to connect
    def waiting(self):
        print('###########################################################')
        print('###########################################################')
        print('Looking for someone you can chat with...')

# Called when you are connected to a stranger
    def connected(self):
        print('You\'re now chatting with a random stranger. Say hi!')

# Called when the stranger is typing a message
    def typing(self):
        print('Stranger is typing...')

# Called when the stranger stops typing a message
    def stopped_typing(self):
        print('Stranger has stopped typing.')

# Called each time a message is received from the stranger
    def message(self, message):
        print('Stranger: %s' % message)

# Called when you and stranger like the same thing
    def common_likes(self, likes):
        print('You both like %s.' % ', '.join(likes))

# Called when a stranger disconnects
    def disconnected(self):
        print('Stranger has disconnected.')

        if self.loop:   # new session
            self.omegle.start()

# Called when the server asks for captcha
    def captcha_required(self):
        url = self.RECAPTCHA_CHALLENGE_URL
        source = self.browser.open(url).read()
        challenge = self.recaptcha_challenge_regex.search(source).groups()[0]
        url = self.RECAPTCHA_IMAGE_URL % challenge

        print('Recaptcha required: %s' % url)
        response = input('Response: ')

        self.omegle.recaptcha(challenge, response)

# Called when server reject captcha
    def captcha_rejected(self):
        pass

# Probably called when the server says you are banned
    def handle_error(self):
        print('You have probably been banned.')

# Called when the server report a message
    def server_message(self, message):
        print(message)

# Status info received from server
    def status_info(self, status):
        pass

# Identity digest received from server
    def ident_digest(self, digests):
        pass


class OmegleClient(Omegle):

    def __init__(self,
                 events_handler, wpm=90, firstevents=1, spid='',
                 random_id=None, topics=[], lang='en', event_delay=3):
        super(OmegleClient, self).__init__(
            events_handler, firstevents,
            spid, random_id, topics, lang, event_delay)
        self.wpm = wpm

# Send a message to Omegle's stranger
    def send(self, message):
        super(OmegleClient, self).send(message)
        print('You: %s' % message)

# Simulate a message completely written by waiting
# an amount of time before sending the message
    def write(self, message):
        msglen = len(message)
        typingtime = self._typingtime(msglen)

        self.typing()
        time.sleep(typingtime)
        self.send(message)

# Emulates typing in the conversation
    def typing(self):
        super(OmegleClient, self).typing()

# Calculates typing time with a given WPM (words per minute)
# The human average typing WPM is: 40
    def _typingtime(self, msglen):
        return msglen / self.wpm * 60

# Starting a new conversation
    def next(self):
        print("NEXT! Starting a new conversation")
        self.disconnect()
        self.start()
