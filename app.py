# app.py
import os
import logging
from flask import Flask, render_template, request, jsonify
from src.email_sender import send_single_email
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-one-email', methods=['POST'])
def send_one():
    """
    Receives data and sends the email without verification.
    """
    if not request.json:
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    data = request.json
    recipient = data.get('recipient')
    sender = data.get('sender')
    subject = data.get('subject')
    body = data.get('body')

    if not all([recipient, sender, subject, body]):
        return jsonify({"status": "error", "message": "Missing data"}), 400

    recipient_email = recipient.get('email')

    # --- MODIFIED: Directly send without verification ---
    result = send_single_email(recipient, sender, subject, body)
    
    if result['status'] == 'Success':
        return jsonify(result), 200
    else:
        # Use status 500 for a server-side sending failure
        return jsonify(result), 500

# The if __name__ == '__main__': block has been removed, as Vercel
# will run the app using a production server like Gunicorn.
