from flask import request, jsonify
import os
import json

JSON_FILE = 'users.json'
JSON_FILE2 = 'people.json'

def data_colecting():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def people_data_colecting():
    if os.path.exists(JSON_FILE2):
        try:
            with open(JSON_FILE2, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def register_people(data):
    saved_data = people_data_colecting()
    new_data = {
        'email': data['email'],
        'id': data['id'],
        'username': data['username'],
        'edited': False,
        'name': '',
        'age': 0,
        'height': 0,
        'weight': 0
    }
    with open(JSON_FILE2, 'w', encoding='utf-8') as file:
        saved_data.append(new_data)
        saved_data.sort(key = lambda saved_data: saved_data['id'])
        json.dump(saved_data, file, ensure_ascii=False, indent=2)    

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
                'message': 'Email já está em uso.'
            })
    for i in range(len(saved_data)):
        if data['username'] == saved_data[i]['username']:
            return jsonify({
                'message': 'Nome de usuário já está em uso.'
            })
    for i in range(len(saved_data)):
        if saved_data[i]['id'] != i:
            data['id'] = i
            break
        else:
            data['id'] = len(saved_data)
    if saved_data[0]['email'] == '' and saved_data[0]['id'] == 1:
        saved_data = []
    register_people(data)
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        saved_data.append(data)
        saved_data.sort(key = lambda saved_data: saved_data['id'])
        json.dump(saved_data, file, ensure_ascii=False, indent=2)    
    return data

def login_user():
    saved_data = data_colecting()
    person_data = people_data_colecting()
    data = request.get_json()
    for i in range(len(saved_data)):
        if saved_data[i]['email'] == data['email'] and saved_data[i]['password'] == data['password']:
            login = {
                'id': saved_data[i]['id'],
                'username': saved_data[i]['username'],
                'edited': person_data[i]['edited'],
            }
            return jsonify(login)
        else:
            login = {
                'message': 'Email ou senha estão incorretos',
            }
    return jsonify(login)

def user_data(username):
    saved_people = people_data_colecting()
    for p in saved_people:
        if p['username'] == username:
            return p
    return jsonify({
        'message': 'Erro ao buscar usuário.'
    })

def edit_user():
    saved_data = data_colecting()
    people_data = people_data_colecting()
    data = request.get_json()
    for i in range(len(people_data)):
        if people_data[i]['id'] != data['id']:
            if people_data[i]['email'] == data['email']:
                return jsonify({
                    'message': 'Email já está cadastrado por outro usuário.'
                })
            if people_data[i]['username'] == data['username']:
                return jsonify({
                    'message': 'Usuário já está em uso.'
                })
        elif people_data[i]['id'] == data['id']:
            people_data[i] = data
            people_data[i]['edited'] = True
            saved_data[i]['username'] = data['username']
            saved_data[i]['email'] = data['email']
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        saved_data.sort(key = lambda saved_data: saved_data['id'])
        json.dump(saved_data, file, ensure_ascii=False, indent=2)
    with open(JSON_FILE2, 'w', encoding='utf-8') as file2:
        people_data.sort(key = lambda saved_data: saved_data['id'])
        json.dump(people_data, file2, ensure_ascii=False, indent=2)
    return jsonify(data)

