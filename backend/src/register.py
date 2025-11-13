from flask import request, jsonify
import json

def data_colecting():
     with open('users.json', 'r') as json_file:
        saved_data = json.load(json_file)
        return saved_data


def register_user():
    saved_data = data_colecting()
    data = request.get_json()
    for i in range(len(saved_data)):
        if data['email'] == saved_data[i]['email']:
            return jsonify({
                'message': 'user already exist'
            })
    for i in range(len(saved_data)):
        if saved_data[i]['id'] != i:
            data['id'] = i
            break
        else:
            data['id'] = len(saved_data)
    with open('users.json', 'w') as json_file:
        saved_data.append(data)
        saved_data.sort(key = lambda saved_data: saved_data['id'])
        json.dump(saved_data, json_file, ensure_ascii=False, indent=2)    
    return saved_data


