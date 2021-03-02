import requests
import json

class Telegram:
    messageUrl = 'https://api.telegram.org/<YOUR BOT TOKEN>/sendMessage'
    updatesUrl = 'https://api.telegram.org/<YOUR BOT TOKEN>/getUpdates'
    chatId = '<YOUR CHAT ID>'
    update_id = 0

    def __init__(self):
        response = requests.post(self.updatesUrl)
        responseData = json.loads(response.text)

        if responseData['ok']:
            for result in responseData['result']:
                self.update_id = result['update_id']
            self.update_id += 1
        else:
            print("FROM Telegram: [COULD NOT RETRIEVE UPDATES]")

# Send the message to your chatID
    def send(self, message):
        data = {
            'chat_id': self.chatId,
            'text': message
        }
        response = requests.post(self.messageUrl, data=data)
        responseData = json.loads(response.text)

        if responseData['ok']:
            print("TO Telegram: ", message)
        else:
            print("TO Telegram: [ERROR SENDING MESSAGE]")

# Get the latest messages that the bot received and only
# considers the ones sent by you (checking your chatId)
    def getUpdates(self):
        data = {
            'offset': self.update_id
        }
        response = requests.post(self.updatesUrl, data=data)
        responseData = json.loads(response.text)

        if responseData['ok']:
            if responseData['result']:
                for result in responseData['result']:
                    self.update_id = result['update_id']
                    if result['message']['from']['id'] == int(self.chatId):
                        return result['message']['text']
                    else:
                        return ''
            else:
                return ''
        else:
            print("FROM Telegram: [COULD NOT RETRIEVE UPDATES]")
            return ''

    def informUser(self, strangerName, strangerAge):
        customText = 'Hi, I have found {}, {} years old. Type "link" to keep chatting on here'.format(strangerName, strangerAge)
        self.send(customText)
