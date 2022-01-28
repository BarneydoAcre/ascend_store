import requests
import json

url = 'http://127.0.0.1:8000/notifications/'

data = {
    

  'action': "test.created",

  'api_version': "v1",

  'application_id': "7203257079331323",

  'date_created': "2021-01-01 02:02:02 +0000 UTC",

  'id': "123456",

  'live_mode': "false",

  'type': "test",

  'user_id': "255738925"


}

r = requests.post(url,data=json.dumps(data),headers={'content-type': 'application/json'})