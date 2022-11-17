from queue import Empty
from marshmallow import post_load, pre_load

from carservice import db
from carservice import ma


service_part = db.Table('service_part',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id')),
    db.Column('part_id', db.Integer, db.ForeignKey('part.id'))
    )


# service_identifier = db.Table('service_identifier',
#                               db.Column('visit_id', db.Integer,
#                                         db.ForeignKey('visits.id')),
#                               db.Column('service_id', db.Integer,
#                                         db.ForeignKey('services.id'))
#                               )

# client_identifier = db.Table('client_identifier',
#                              db.Column('client_id', db.Integer,
#                                        db.ForeignKey('clients.id')),
#                              db.Column('service_id', db.Integer,
#                                        db.ForeignKey('services.id'))
#  

class Part(db.Model):
    __tablename__ = 'part'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    price = db.Column(db.Float)


class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    labour_price = db.Column(db.Float)
    parts = db.relationship("Part", secondary=service_part)


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    car_brand = db.Column(db.String(64))
    car_model = db.Column(db.String(64))
    contact = db.Column(db.String(64))


# class visits(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime)
#     description = db.Column(db.String(128))
#     client = db.Column(db.Integer, db.ForeignKey('clients.id'))
#     price = db.Column(db.Float)
#     discount = db.Column(db.Float)
#     state = db.Column(db.Boolean)
#     services = db.relationship("services", secondary=service_identifier)

#     def as_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Part

    @post_load
    def make_part(self, data, **kwargs):
        if 'id' in data:
            return db.session.query(Part).filter(Part.id == data['id']).one()
        else:
            return Part(**data)


class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client

    @post_load
    def make_client(self, data, **kwargs):
        return Client(**data)


class ServiceSchema(ma.SQLAlchemyAutoSchema):
    parts = ma.Nested(PartSchema, many=True)

    class Meta:
        model = Service
        include_relationships = True
        include_fk = True

    @post_load
    def make_service(self, data, **kwargs):
        if 'id' in data:
            return db.session.query(Service).filter(Service.id == data['id']).one()
        else:
            return Service(**data)
