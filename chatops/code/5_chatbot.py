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
    bot_id = requests.get(f'{base_url}/people/me', headers=headers).json().get('id')
    if bot_id == data.get('data').get('personId'):
        return 'Message from self ignored'
    else:
        message_id = data.get('data').get('id')
        message_url = f'{base_url}/messages/{message_id}'
        message_text = requests.get(message_url, headers=headers).json().get('text')
        print(message_text)

        room_id = data.get('data').get('roomId')
        if message_text.startswith('/chuck'):
            web_server = 'https://api.chucknorris.io/jokes/random'
            reply = requests.get(web_server, headers=headers).json().get('value')
        else:
            reply = f'You said: "{message_text}"'

        my_msg_data = {
            "roomId": room_id,
            "text": reply,
            }
        post_message_url = f'{base_url}/messages'
        post_message_data = requests.post(post_message_url,headers=headers,data=json.dumps(my_msg_data))

    return data

app.run(host="0.0.0.0", port=port, debug=True)
