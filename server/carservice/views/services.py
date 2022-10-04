from flask import Blueprint, jsonify, request

from carservice import db
from carservice.models import parts, services

services_bp = Blueprint('services_bp', __name__)


@services_bp.route('/services', methods=['GET', 'POST'])
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


@services_bp.route('/services/<service_id>', methods=['PUT', 'DELETE'])
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
