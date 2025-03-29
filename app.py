from flask import Flask, render_template, request, jsonify
import pyotp
import time
import base64
import os
import binascii

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    key = data['key']
    try:
        base64.b32decode(key, casefold=True)
        totp = pyotp.TOTP(key)
        code = totp.now()
        return jsonify({'code': code})
    except (binascii.Error, ValueError):
        return jsonify({'error': 'Invalid key'}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
