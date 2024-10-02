import requests
import json 

url = 'http://10.0.100.16:3000/info'

data = {
    "name": "Corey Jones",
    "email": "cor3ytat@icloud.com"
}

response = requests.post(url, json=data)

print(f'Response: {response.json}')
