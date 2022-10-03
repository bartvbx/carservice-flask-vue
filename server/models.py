from main import db

part_identifier = db.Table('part_identifier',
                           db.Column('service_id', db.Integer,
                                     db.ForeignKey('services.id')),
                           db.Column('part_id', db.Integer,
                                     db.ForeignKey('parts.id'))
                           )

service_identifier = db.Table('service_identifier',
                              db.Column('visit_id', db.Integer,
                                        db.ForeignKey('visits.id')),
                              db.Column('service_id', db.Integer,
                                        db.ForeignKey('services.id'))
                              )

client_identifier = db.Table('client_identifier',
                             db.Column('client_id', db.Integer,
                                       db.ForeignKey('clients.id')),
                             db.Column('service_id', db.Integer,
                                       db.ForeignKey('services.id'))
                             )


class parts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    price = db.Column(db.Float)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    price = db.Column(db.Float)
    parts = db.relationship("parts",
                            secondary=part_identifier)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    car_brand = db.Column(db.String(64))
    car_model = db.Column(db.String(64))
    contact = db.Column(db.String(64))
    visit = db.relationship("visits")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class visits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(128))
    client = db.Column(db.Integer, db.ForeignKey('clients.id'))
    price = db.Column(db.Float)
    discount = db.Column(db.Float)
    state = db.Column(db.Boolean)
    services = db.relationship("services", secondary=service_identifier)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    login = db.Column(db.String(128))
    password = db.Column(db.String(128))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
