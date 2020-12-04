import requests, inspect

from flask import Flask, request
app = Flask(__name__)

import logging, logging.config
logging.config.fileConfig('conf/logging.conf')
file_logger=logging.getLogger('fileLogger')
from MyLogger import file_log_helper

from conf import secret

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

def send_admin_report(msg):
    func_name = inspect.currentframe().f_code.co_name
    request_body = {
            'recipient': {
                'id': secret.admin_PSID
            },
            'message': {"text":msg}
        }
    url = 'https://graph.facebook.com/v9.0/me/messages?access_token='+secret.webhook_token
    response = requests.post(url,json=request_body)
    
    # log this event or an error message
    if response.status_code==200:
        file_log_helper(logging.INFO, func_name, response)
    else:
        file_log_helper(logging.ERROR, func_name, response)

if __name__ == "__main__":
    app.run(threaded=True, port=5000)