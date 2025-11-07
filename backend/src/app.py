from flask import Flask, request, jsonify
from flask_cors import CORS
from register import register_user

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register_page():
    if request.method == 'POST':
        return register_user()
