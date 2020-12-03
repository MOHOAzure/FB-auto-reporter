import requests
from flask import Flask, request
app = Flask(__name__)

from conf import secret

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
@app.route('/webhook',methods=['GET'])
def webhook_authorization():
    verify_token = request.args.get("hub.verify_token")
    # Check if sent token is correct
    if verify_token == secret.webhook_verify_token:
        # Responds with the challenge token from the request
        return request.args.get("hub.challenge")
    return 'Unable to authorise.'

@app.route("/webhook", methods=['POST'])
def webhook_handle():
    data = request.get_json()
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    if message['text']:
        request_body = {
                'recipient': {
                    'id': sender_id
                },
                'message': {"text":"hello, world!"}
            }
        url = 'https://graph.facebook.com/v9.0/me/messages?access_token='+secret.webhook_token
        response = requests.post(url,json=request_body).json()
        return response
    return 'ok'
    
if __name__ == "__main__":
    app.run(threaded=True, port=5000)