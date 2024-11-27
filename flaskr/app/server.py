from flask import Flask, request, jsonify, render_template_string
from .producer import send_message

app = Flask(__name__)

# HTML template with a form
form_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Message Sender</title>
</head>
<body>
    <h1>Send a Message</h1>
    <form action="/send" method="post">
        <input type="text" name="message" placeholder="Your message here" required>
        <button type="submit">Send</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(form_template)

@app.route('/send', methods=['POST'])
def send():
    message = request.form.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    send_message(message)
    return jsonify({'status': 'Message sent'}), 200

def run_flask():
    app.run(debug=False, port=5000)