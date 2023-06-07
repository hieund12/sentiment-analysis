import requests
from requests.auth import HTTPBasicAuth

api_url = 'http://localhost:8000/sentiment-analysis'
username = 'username'  # Thay thế bằng tên đăng nhập của bạn
password = 'password'  # Thay thế bằng mật khẩu của bạn

data = {
    'text': 'This is a great product!'
}

response = requests.post(api_url, json=data, auth=HTTPBasicAuth(username, password))
result = response.json()

print(result['sentiment'])  # Output: Positive
