from flask import Blueprint, request
from sqlalchemy.exc import NoResultFound

from carservice import db
from carservice.models import Part, PartSchema

parts_bp = Blueprint('parts_bp', __name__)

part_schema = PartSchema()
parts_schema = PartSchema(many=True)


@parts_bp.route('/parts', methods=['GET', 'POST'])
def list_create_part():

    if request.method == 'GET':
        all_parts = Part.query.all()
        return parts_schema.dump(all_parts)

    if request.method == 'POST':
        post_data = request.get_json()
        if not post_data:
            return {"message": "No input data provided"}, 400
        new_part = part_schema.load(post_data)
        db.session.add(new_part)
        db.session.commit()
        return {"message": "New part has been added!"}, 200


@parts_bp.route('/parts/<part_id>', methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_part(part_id):

    if request.method == 'GET':
        try:
            part = Part.query.filter(Part.id == part_id).one()
        except NoResultFound:
            return {"message": "Part could not be found."}, 400
        return part_schema.dump(part)

    if request.method == 'PUT':
        post_data = request.get_json()
        db.session.query(Part).filter(Part.id == part_id).update(post_data)
        db.session.commit()
        return {"message": "Part was successfully updated"}, 200

    if request.method == 'DELETE':
        db.session.query(Part).filter(Part.id == part_id).delete()
        db.session.commit()
        return {"message": "Part was successfully deleted"}, 200
