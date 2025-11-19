from flask import request, jsonify
import os
import json

JSON_FILE = 'user.json'

def data_colecting():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []


def register_user():
    saved_data = data_colecting()
    if len(saved_data) == 0:
        saved_data = [{
                'username': '',
                'email': '',
                'id': 1
            }]
    data = request.get_json()
    for i in range(len(saved_data)):
        if data['email'] == saved_data[i]['email']:
            return jsonify({
                'message': 'email already registered'
            })
    for i in range(len(saved_data)):
        if data['username'] == saved_data[i]['username']:
            return jsonify({
                'message': 'username already in use'
            })
    for i in range(len(saved_data)):
        if saved_data[i]['id'] != i:
            data['id'] = i
            break
        else:
            data['id'] = len(saved_data)
    if saved_data[0]['email'] == '' and saved_data[0]['id'] == 1:
        saved_data = []
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        saved_data.append(data)
        saved_data.sort(key = lambda saved_data: saved_data['id'])
        json.dump(saved_data, file, ensure_ascii=False, indent=2)    
    return data


