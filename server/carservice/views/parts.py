from flask import Blueprint, jsonify, request

from carservice import db
from carservice.models import parts

parts_bp = Blueprint('parts_bp', __name__)


@parts_bp.route('/parts', methods=['GET', 'POST'])
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


@parts_bp.route('/parts/<part_id>', methods=['PUT', 'DELETE'])
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
