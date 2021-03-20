from app import db

class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    addr = db.Column(db.String(24))
    leases = db.relationship('Lease', backref='network')
    host_capacity = db.Column(db.Integer)
    num_leases = db.Column(db.Integer)

class Lease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    net_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    lease = db.Column(db.String(64))
    starts = db.Column(db.String(64))
    ends = db.Column(db.String(64))
    cltt = db.Column(db.String(64))
    binding = db.Column(db.String(64))
    next = db.Column(db.String(64))
    rewind = db.Column(db.String(64), nullable=True)
    hardware = db.Column(db.String(64))
    uid = db.Column(db.String(64))
    client = db.Column(db.String(64), nullable=True)

db.drop_all()
db.create_all()
