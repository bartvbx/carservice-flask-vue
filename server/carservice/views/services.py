from flask import Blueprint, request
from sqlalchemy.exc import NoResultFound

from carservice import db
from carservice.models import Part, Service, ServiceSchema

services_bp = Blueprint('services_bp', __name__)

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)


@services_bp.route('/services', methods=['GET', 'POST'])
def all_services():

    if request.method == 'GET':
        all_services = Service.query.all()
        return services_schema.dump(all_services)

    if request.method == 'POST':
        post_data = request.get_json()
        if not post_data:
            return {"message": "No input data provided"}, 400
        new_service = service_schema.load(post_data)
        db.session.add(new_service)
        db.session.commit()
        return {"message": "New part has been added!"}, 200


@services_bp.route('/services/<service_id>', methods=['GET', 'PUT', 'DELETE'])
def single_service(service_id):

    try:
        service = Service.query.filter(Service.id == service_id).one()
    except NoResultFound:
        return {"message": "Service could not be found."}, 400

    if request.method == 'GET':
        return service_schema.dump(service)

    if request.method == 'PUT':
        post_data = request.get_json()
        parts_list = post_data.pop('parts')
        db.session.query(Service).filter(Service.id == service_id).update(post_data)
        service.parts.clear()
        for part in parts_list:
            querried_part = db.session.query(Part).filter(Part.id == part.get('id')).one()
            service.parts.append(querried_part)
            db.session.add(service)
        db.session.commit()
        return {"message": "Service was successfully updated"}, 200

    if request.method == 'DELETE':
        db.session.query(Service).filter(Service.id == service_id).delete()
        db.session.commit()
        return {"message": "Service was successfully deleted"}, 200
