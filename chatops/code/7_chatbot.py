from flask import Flask, request, json
import requests
import meraki

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
    dashboard = meraki.DashboardAPI()
    data = request.get_json()
    bot_id = requests.get(f'{base_url}/people/me', headers=headers).json().get('id')
    if bot_id == data.get('data').get('personId'):
        return 'Message from self ignored'
    else:
        message_id = data.get('data').get('id')
        message_url = f'{base_url}/messages/{message_id}'
        message_text = requests.get(message_url, headers=headers).json().get('text')
        room_id = data.get('data').get('roomId')
        if message_text.startswith('/meraki'):
            try:
                action = message_text.split()[1]
            except IndexError:
                action = 'ssids'
            if action == 'networks':
                org_id = dashboard.organizations.getOrganizations()[0].get('id')
                network_list = dashboard.organizations.getOrganizationNetworks(org_id)
                print(json.dumps(network_list,indent=4))
                reply = f'Your organization with ID {org_id} includes the following networks:'
                for network in network_list:
                    reply += f"\n- Name: {network['name']}, ID: {network['id']}"
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
