import requests

url = 'http://localhost:5000/insert_data_from_csv'
response = requests.post(url)
print(response.text)
