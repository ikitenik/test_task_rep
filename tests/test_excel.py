import requests
import pandas as pd

url = 'http://localhost:8000/api/upload/'
files = {'file': open('test.xlsx', 'rb')}

response = requests.post(url, files=files)

if response.status_code == 201:
    print('Success:', response.json())
else:
    print('Failed:', response.status_code, response.json())
