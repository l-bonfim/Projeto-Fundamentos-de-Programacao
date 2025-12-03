from flask import Flask, request, jsonify
from flask_cors import CORS
from pages.users import register_user, login_user, user_data, edit_user

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register_page():
    if request.method == 'POST':
        return register_user()

@app.route('/login', methods=['POST'])
def login_page():
    if request.method == 'POST':
        return login_user()

@app.route('/profile/<username>/edit', methods=['GET', 'POST'])
def edit_profile_page(username):
    if request.method == 'GET':
        return user_data(username)
    if request.method == 'POST':
        return edit_user()
    
@app.route('/profile/<username>', methods=['GET'])
def profile_page(username):
    if request.method == 'GET':
        return user_data(username)