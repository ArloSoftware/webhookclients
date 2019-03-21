
import base64
import binascii
import hashlib
import hmac
import json
import os
import xml.dom.minidom

from flask import Flask, request
from flask import jsonify

app = Flask(__name__)

WEBHOOK_KEY = os.getenv('ARLO_WEBHOOK_KEY', 'Your base64 encoded key here...')


@app.route("/")
def home():
    return jsonify(hello="world")


@app.route("/webhooks", methods=['GET', 'POST'])
def webhooks():
    calculated = None
    try:
        dom = xml.dom.minidom.parseString(request.data)
        pretty_xml_as_string = dom.toprettyxml()
        print(pretty_xml_as_string)
    except:
        print('valid xml not sent')
        pass
    try:
        signature = request.headers.get('x-arlo-signature', '')
        print(signature)
        key_bytes = base64.b64decode(WEBHOOK_KEY)
        calculated = base64.b64encode(hmac.new(
            key_bytes, request.data, digestmod=hashlib.sha512).digest()).decode(encoding='ascii')
        if signature == calculated:
            # Process request
            print('valid signature')
        else:
            print('invalid signature')
    except Exception as ex:
        print(ex)
    return jsonify(valid=(signature == calculated))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9009)
