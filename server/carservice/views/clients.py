from flask import Blueprint, request
from sqlalchemy.exc import NoResultFound

from carservice import db
from carservice.models import Client, ClientSchema

clients_bp = Blueprint('clients_bp', __name__)

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)


@clients_bp.route('/clients', methods=['GET', 'POST'])
def list_create_client():

    if request.method == 'GET':
        all_clients = Client.query.all()
        return clients_schema.dump(all_clients)

    if request.method == 'POST':
        post_data = request.get_json()
        if not post_data:
            return {"message": "No input data provided"}, 400
        new_client = client_schema.load(post_data)
        db.session.add(new_client)
        db.session.commit()
        return {"message": "New client has been added!"}, 200


@clients_bp.route('/clients/<client_id>', methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_client(client_id):

    if request.method == 'GET':
        try:
            client = Client.query.filter(Client.id == client_id).one()
        except NoResultFound:
            return {"message": "Client could not be found."}, 400
        return client_schema.dump(client)

    if request.method == 'PUT':
        post_data = request.get_json()
        db.session.query(Client).filter(Client.id == client_id).update(post_data)
        db.session.commit()
        return {"message": "Client was successfully updated"}, 200

    if request.method == 'DELETE':
        db.session.query(Client).filter(Client.id == client_id).delete()
        db.session.commit()
        return {"message": "Client was successfully deleted"}, 200
