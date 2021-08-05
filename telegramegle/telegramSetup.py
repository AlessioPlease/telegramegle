import requests
import json

updatesUrl = 'https://api.telegram.org/<YOUR BOT TOKEN>/getUpdates'
userId = ''

data = {
    'offset': ''
}

answer = requests.post(updatesUrl, data=data)
responseData = json.loads(answer.text)
if responseData['ok']:
    if responseData['result']:
        for result in responseData['result']:
            userId = result['message']['from']['id']
else:
    print("COULD NOT RETRIEVE ID")

print(userId)
