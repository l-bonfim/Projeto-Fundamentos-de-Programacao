from flask import request, jsonify

saved_data = [{
    'name': 'admin',
    'id': 0,
    'email': 'admin@admin',
    'password': 'admin'
}]

def register_user():
    data = request.get_json()
    for i in range(len(saved_data)):
        if data['name'] == saved_data[i]['name']:
            return jsonify({
                'message': 'user already exist'
                'status' : 409
            })
    data['id'] = len(saved_data)
    return data


