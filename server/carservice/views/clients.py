from flask import Blueprint, jsonify, request

from carservice import db
from carservice.models import clients

clients_bp = Blueprint('clients_bp', __name__)


@clients_bp.route('/clients/new', methods=['GET'])
def new_client():
    response_object = {'status': 'success'}

    # print('------------')
    # obj = clients.query.order_by(-clients.id).first()
    # print(obj.as_dict())
    # print('------------')

    obj = db.session.query(clients).order_by(clients.id.desc()).first()
    print('------------')
    print(obj.id)
    print(obj.as_dict())
    clients_list = []
    clients_list.append(obj.as_dict())

    # for client in all_clients:
    #     client_dict = client.as_dict()
    #     clients_list.append(client_dict)
    response_object['client'] = clients_list
    print(response_object)

    return jsonify(response_object)


@clients_bp.route('/clients', methods=['GET', 'POST'])
def all_clients():
    response_object = {'status': 'success'}

    if request.method == 'GET':
        all_clients = clients.query.all()
        clients_list = []
        for client in all_clients:
            client_dict = client.as_dict()
            clients_list.append(client_dict)
        response_object['clients'] = clients_list
        print(response_object)

    if request.method == 'POST':
        post_data = request.get_json()
        new_client = clients(name=post_data.get('name'), car_brand=post_data.get(
            'car_brand'), car_model=post_data.get('car_model'), contact=post_data.get('contact'))
        db.session.add(new_client)
        db.session.commit()
        response_object['message'] = 'Nowy klient został dodany!'

    return jsonify(response_object)


@clients_bp.route('/clients/<client_id>', methods=['PUT', 'DELETE'])
def single_client(client_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        post_data = request.get_json()
        db.session.query(clients).filter(
            clients.id == client_id).update(post_data)
        db.session.commit()
        response_object['message'] = 'Dane klienta zostały zaktualizowane!'

    if request.method == 'DELETE':
        db.session.query(clients).filter(clients.id == client_id).delete()
        db.session.commit()
        response_object['message'] = 'Klient został usunięty!'

    return jsonify(response_object)
