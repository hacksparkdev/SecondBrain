import requests
import json 

url = 'http://localhost:3000'

data = {
    "name": "Corey Jones",
    "email": "cor3ytat@icloud.com"
}

response = request.post(url, json=data)

print(f'Response: {response.json}')
