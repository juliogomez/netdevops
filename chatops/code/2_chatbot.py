from flask import Flask, request, json
import requests

app = Flask(__name__)
port = 5005
base_url = 'https://webexapis.com/v1/'
api_key = '<bot_token>'
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    print(json.dumps(data,indent=4))
    message_id = data.get('data').get('id')
    message_url = f'{base_url}/messages/{message_id}'
    message_text = requests.get(message_url, headers=headers).json().get('text')
    print(message_text)
    return data

app.run(host="0.0.0.0", port=port, debug=True)
