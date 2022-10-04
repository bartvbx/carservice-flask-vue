from datetime import datetime

from flask import Blueprint, jsonify, request

from carservice import db
from carservice.models import services, clients, visits

visits_bp = Blueprint('visits_bp', __name__)


@visits_bp.route('/visits', methods=['GET', 'POST'])
def all_visits():
    response_object = {'status': 'success'}

    if request.method == 'GET':
        all_visits = visits.query.all()
        visits_list = []

        for visit in all_visits:
            visit_dict = visit.as_dict()
            services_list = []

            for service in visit.services:
                services_list.append(service.as_dict())

            visit_dict['visit_services'] = services_list
            client_id = visit_dict['client']
            client = db.session.query(clients).filter(
                clients.id == client_id).one()
            visit_dict['client'] = client.as_dict()

            visits_list.append(visit_dict)

        response_object['visits'] = visits_list

    if request.method == 'POST':

        post_data = request.get_json()
        print(post_data)
        post_data_date = datetime.strptime(
            post_data.get('date'), '%Y-%m-%dT%H:%M:00.000Z')
        post_data_client = post_data.get('client')['id']

        new_visit = visits(date=post_data_date, description=post_data.get(
            'description'), client=post_data_client, price=0, discount=post_data.get('discount'), state=False)
        new_visit.services = []
        db.session.add(new_visit)
        db.session.flush()
        print(new_visit.services)
        print(post_data['visit_services'])
        sum_price = 0
        for service in post_data['visit_services']:
            sum_price += service.get('price')
            querried_service = db.session.query(services).filter(
                services.id == service.get('id')).one()
            new_visit.services.append(querried_service)
            db.session.add(new_visit)
        new_visit.price = sum_price * (1 - int(new_visit.discount)/100)
        db.session.commit()

        response_object['message'] = 'Nowa wizyta została dodana!'

    return jsonify(response_object)


@visits_bp.route('/visits/state/<visit_id>', methods=['PUT'])
def change_visit_state(visit_id):
    response_object = {'status': 'success'}
    visit = db.session.query(visits).filter(visits.id == visit_id).one()
    if visit.state == False:
        visit.state = True
        response_object['message'] = 'Wizyta została zrealizowana!'
    else:
        visit.state = False
        response_object['message'] = 'Wizyta nie została jeszcze zrealizowana!'
    db.session.commit()

    return jsonify(response_object)


@visits_bp.route('/visits/<visit_id>', methods=['PUT', 'DELETE'])
def single_visit(visit_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        post_data = request.get_json()
        print('post_data')
        print(post_data)
        print('---------')
        # post_data['date'] = datetime.strptime(
        # post_data.get('date'), '%Y-%m-%dT%H:%M:00.000Z')
        services_list = post_data.pop('visit_services')
        client_data = post_data.pop('client')
        date_data = post_data.pop('date')
        print('working_post_data')
        print(post_data)
        selected_visit = db.session.query(
            visits).filter(visits.id == visit_id).one()
        db.session.query(visits).filter(visits.id == visit_id).update(
            post_data)  # not sure about this one
        db.session.query(visits).filter(visits.id == visit_id).update(
            {'client': client_data['id']})
        selected_visit.services.clear()
        db.session.flush()
        sum_price = 0
        for service in services_list:
            sum_price += service.get('price')
            querried_service = db.session.query(services).filter(
                services.id == service.get('id')).one()
            selected_visit.services.append(querried_service)
            db.session.add(selected_visit)

        print(selected_visit.price)
        print(sum_price)
        print(selected_visit.discount)
        db.session.query(visits).filter(visits.id == visit_id).update(
            {'price': sum_price * (1 - int(selected_visit.discount)/100)})
        # selected_visit.price = sum_price * (1 - int(selected_visit.discount)/100)
        db.session.commit()
        response_object['message'] = 'Dane wizyty zostały zaktualizowane!'

    if request.method == 'DELETE':
        db.session.query(visits).filter(visits.id == visit_id).delete()
        db.session.commit()
        response_object['message'] = 'Wizyta została usunięta!'

    return jsonify(response_object)
