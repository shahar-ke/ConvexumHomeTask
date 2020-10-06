from server_lib.db_layer_lib.database import db


class SensorModel(db.Model):
    __tablename__ = 'sensor'
    id = db.Column(db.String(20), primary_key=True)
    drones = db.relationship('DroneModel', backref='sensor')
