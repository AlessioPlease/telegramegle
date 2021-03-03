import mechanize
import urllib
import time

class CustomClient:
    browser = mechanize.Browser()
    browser.addheaders = []

    def __init__(self, client, checkpoint):
        self.client = client
        self.checkpoint = checkpoint

# Send a message to Omegle's stranger
    def send(self, message):
        SEND_URL = 'http://%s/send'

        url = SEND_URL % self.client.server
        data = {'msg': message, 'id': self.client.client_id}
        try:
            self.request(url, data)
            print('You: %s' % message)
            return True
        except Exception as ex:
            print(ex)
            return False

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
        TYPING_URL = 'http://%s/typing'

        url = TYPING_URL % self.client.server
        data = {'id': self.client.client_id}
        try:
            self.request(url, data)
            print('You are typing...')
            return True
        except Exception:
            return False

# Calculates typing time with a given WPM (words per minute)
# The human average typing WPM is: 40
    def _typingtime(self, msglen):
        return msglen / self.client.wpm * 60

# Disconnect from the current conversation
    def disconnect(self):
        DISCONNECT_URL = 'http://%s/disconnect'

        self.checkpoint.reset()
        self.client.connected = False
        url = DISCONNECT_URL % self.client.server
        data = {'id': self.client.client_id}
        try:
            self.client.thread.stop()
            self.request(url, data)
            print('You have disconnected.')
            return True
        except Exception:
            return False

# Open the url with data info
    def request(self, url, data):
        data = urllib.parse.urlencode(data)

        try:
            response = self.browser.open(url, data)
            return response
        except Exception as ex:
            print("Request Error")
            print(ex)
