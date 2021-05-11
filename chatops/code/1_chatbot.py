from flask import Flask, request, json

app = Flask(__name__)
port = 5005

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    print(json.dumps(data,indent=4))
    return data

app.run(host="0.0.0.0", port=port, debug=True)