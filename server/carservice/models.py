from marshmallow import post_load, EXCLUDE

from carservice import db
from carservice import ma


service_part = db.Table('service_part',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id')),
    db.Column('part_id', db.Integer, db.ForeignKey('part.id'))
    )


visit_service = db.Table('visit_service',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('visit_id', db.Integer, db.ForeignKey('visit.id')),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'))
    )


visit_client = db.Table('visit_client',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('visit_id', db.Integer, db.ForeignKey('visit.id')),
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'))
    )


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

    def parts_price(self):
        return sum(part.price for part in self.parts)
    
    def total_price(self):
        return self.parts_price() + self.labour_price


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    car_brand = db.Column(db.String(64))
    car_model = db.Column(db.String(64))
    contact = db.Column(db.String(64))


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(128))
    # client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship("Client", secondary=visit_client)
    discount = db.Column(db.Float)
    state = db.Column(db.Boolean)
    services = db.relationship("Service", secondary=visit_service)

    def base_price(self):
        return sum(service.total_price() for service in self.services)
    
    def final_price(self):
        return self.base_price() * (1 - self.discount/100)


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
    def load_make_client(self, data, **kwargs):
        if 'id' in data:
            return db.session.query(Client).filter(Client.id == data['id']).one()
        else:
            return Client(**data)


class ServiceSchema(ma.SQLAlchemyAutoSchema):
    parts = ma.Nested(PartSchema, many=True)
    parts_price = ma.Method('get_parts_price')
    total_price = ma.Method('get_total_price')

    class Meta:
        model = Service
        include_relationships = True
        include_fk = True
        unknown = EXCLUDE

    def get_parts_price(self, obj):
        return obj.parts_price()

    def get_total_price(self, obj):
        return obj.total_price()

    @post_load
    def load_make_service(self, data, **kwargs):
        if 'id' in data:
            return db.session.query(Service).filter(Service.id == data['id']).one()
        else:
            return Service(**data)


class VisitSchema(ma.SQLAlchemyAutoSchema):
    client = ma.Nested(ClientSchema, many=True)
    services = ma.Nested(ServiceSchema, many=True)
    base_price = ma.Method('get_base_price')
    final_price = ma.Method('get_final_price')

    class Meta:
        model = Visit
        include_relationships = True
        include_fk = True
        unknown = EXCLUDE

    def get_base_price(self, obj):
        return obj.base_price()

    def get_final_price(self, obj):
        return obj.final_price()

    @post_load
    def load_make_visit(self, data, **kwargs):
        if 'id' in data:
            return db.session.query(Visit).filter(Visit.id == data['id']).one()
        else:
            return Visit(**data)
