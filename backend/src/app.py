from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET','POST'])
def handle_test_post():
    if request.method == 'GET':
        data = {
            'teste': 'teste'
        }
        return jsonify(data)
    if request.method == 'POST':
        data2 = request.get_json()
        return data2


