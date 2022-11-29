from datetime import datetime

from flask import Blueprint, request
from sqlalchemy.exc import NoResultFound

from carservice import db
from carservice.models import Client, Service, Visit, VisitSchema

visits_bp = Blueprint('visits_bp', __name__)

visit_schema = VisitSchema()
visits_schema = VisitSchema(many=True)


@visits_bp.route('/visits', methods=['GET', 'POST'])
def all_visits():

    if request.method == 'GET':
        all_services = Visit.query.all()
        return visits_schema.dump(all_services)

    if request.method == 'POST':
        post_data = request.get_json()
        if not post_data:
            return {"message": "No input data provided"}, 400

        client = post_data.pop('client')
        querried_client = db.session.query(Client).filter(Client.id == client.get('id')).one()

        new_visit = visit_schema.load(post_data)
        new_visit.client.append(querried_client)
        db.session.add(new_visit)
        db.session.commit()
        return {"message": "New visit has been added!"}, 200


@visits_bp.route('/visits/state/<visit_id>', methods=['PUT'])
def change_visit_state(visit_id):
    visit = db.session.query(Visit).filter(Visit.id == visit_id).one()
    if visit.state == False:
        visit.state = True
        message = 'The visit has been completed!'
    else:
        visit.state = False
        message = 'The visit hasn\'t been completed!'
    db.session.commit()
    return {"message": message}, 200


@visits_bp.route('/visits/<visit_id>', methods=['GET', 'PUT', 'DELETE'])
def single_visit(visit_id):

    try:
        visit = Visit.query.filter(Visit.id == visit_id).one()
    except NoResultFound:
        return {"message": "Visit could not be found."}, 400

    if request.method == 'GET':
        return visit_schema.dump(visit)

    if request.method == 'PUT':
        post_data = request.get_json()
        
        # Handle date, client and services
        post_data['date'] = datetime.strptime(post_data.get('date'), '%Y-%m-%d %H:%M:%S')
        client = post_data.pop('client')
        if isinstance(client, list):
            querried_client = db.session.query(Client).filter(Client.id == client[0].get('id')).one()
        else:
            querried_client = db.session.query(Client).filter(Client.id == client.get('id')).one()
        services_list = post_data.pop('services')
        visit.client.clear()
        visit.services.clear()

        # Update
        db.session.query(Visit).filter(Visit.id == visit_id).update(post_data)
        visit.client.append(querried_client)
        for service in services_list:
            querried_service = db.session.query(Service).filter(Service.id == service.get('id')).one()
            visit.services.append(querried_service)
        db.session.add(visit)
        db.session.commit()
        return {"message": "Visit was successfully updated"}, 200

    if request.method == 'DELETE':
        db.session.query(Visit).filter(Visit.id == visit_id).delete()
        db.session.commit()
        return {"message": "Visit was successfully deleted"}, 200
