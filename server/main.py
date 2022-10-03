from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# from models import *
from datetime import datetime


DB_NAME = 'database.db'

app = Flask(__name__)

app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
from models import *
db.create_all()

CORS(app, resources={r"/*": {'origins': "*"}})


# APIs for parts
@app.route('/parts', methods=['GET', 'POST'])
def all_parts():
    response_object = {'status': 'success'}

    if request.method == 'GET':
        all_parts = parts.query.all()
        parts_list = []
        for part in all_parts:
            part_dict = part.as_dict()
            parts_list.append(part_dict)
        response_object['parts'] = parts_list
        print(response_object)

    if request.method == 'POST':
        post_data = request.get_json()
        new_part = parts(name=post_data.get('name'), description=post_data.get(
            'description'), price=post_data.get('price'))
        db.session.add(new_part)
        db.session.commit()
        response_object['message'] = 'Nowa część została dodana!'

    return jsonify(response_object)


@app.route('/parts/<part_id>', methods=['PUT', 'DELETE'])
def single_part(part_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        post_data = request.get_json()
        db.session.query(parts).filter(parts.id == part_id).update(post_data)
        db.session.commit()
        response_object['message'] = 'Dane części zostały zaktualizowane!'

    if request.method == 'DELETE':
        db.session.query(parts).filter(parts.id == part_id).delete()
        db.session.commit()
        response_object['message'] = 'Część została usunięta!'

    return jsonify(response_object)

@app.route('/clients/new', methods=['GET'])
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

# APIs for clients
@app.route('/clients', methods=['GET', 'POST'])
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


@app.route('/clients/<client_id>', methods=['PUT', 'DELETE'])
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


# APIs for services
@app.route('/services', methods=['GET', 'POST'])
def all_services():
    response_object = {'status': 'success'}

    if request.method == 'GET':
        all_services = services.query.all()
        services_list = []
        for service in all_services:
            service_dict = service.as_dict()
            parts_list = []
            for part in service.parts:
                parts_list.append(part.as_dict())
            service_dict['service_parts'] = parts_list
            services_list.append(service_dict)
        response_object['services'] = services_list

    if request.method == 'POST':
        post_data = request.get_json()
        new_service = services(name=post_data.get('name'), description=post_data.get(
            'description'), price=post_data.get('price'))
        db.session.add(new_service)
        db.session.flush()
        for part in post_data['service_parts']:
            querried_part = db.session.query(parts).filter(
                parts.id == part.get('id')).one()
            new_service.parts.append(querried_part)
            db.session.add(new_service)
        db.session.commit()

        response_object['message'] = 'Nowa usługa została dodana!'

    return jsonify(response_object)


@app.route('/services/<service_id>', methods=['PUT', 'DELETE'])
def single_service(service_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        post_data = request.get_json()
        parts_list = post_data.pop('service_parts')
        selected_service = db.session.query(
            services).filter(services.id == service_id).one()
        db.session.query(services).filter(
            services.id == service_id).update(post_data)
        selected_service.parts.clear()
        db.session.flush()
        for part in parts_list:
            querried_part = db.session.query(parts).filter(
                parts.id == part.get('id')).one()
            selected_service.parts.append(querried_part)
            db.session.add(selected_service)
        db.session.commit()
        response_object['message'] = 'Dane usługi zostały zaktualizowane!'

    if request.method == 'DELETE':
        db.session.query(services).filter(services.id == service_id).delete()
        db.session.commit()
        response_object['message'] = 'Usługa została usunięta!'

    return jsonify(response_object)


# APIs for visits
@app.route('/visits', methods=['GET', 'POST'])
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


@app.route('/visits/state/<visit_id>', methods=['PUT'])
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


@app.route('/visits/<visit_id>', methods=['PUT', 'DELETE'])
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


if __name__ == '__main__':
    app.run(debug=True)
