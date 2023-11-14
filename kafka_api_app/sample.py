import requests
import random

url = "http://65.1.111.158:5000/produce"

data_to_send = {"latitude": random.uniform(-90, 90),
                "longitude": random.uniform(-180, 180),
                "id": 'RID' + str(random.choice(range(1,100)))}
response = requests.post(url,json=data_to_send)

if response.status_code == 200:
    print('Response:', response.json())
else:
    print(f'Request failed with status code {response.status_code}')
    print('Response:', response.text)
