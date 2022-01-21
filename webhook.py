import requests
import json

url = 'http://127.0.0.1:8000/notifications/'

data = {
    'name': 'Luan Gabriel',
    'message': 'Hi, I\'m working'
}

r = requests.post(url,data=json.dumps(data),headers={'content-type': 'application/json'})