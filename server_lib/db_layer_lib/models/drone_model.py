from server_lib.db_layer_lib.database import db


class DroneModel(db.Model):
    __tablename__ = 'drone'
    id = db.Column(db.Integer, primary_key=True)
    drone_type = db.Column(db.String(20))
    drone_positions = db.relationship('DronePositionModel', backref='drone')
    sensor_id = db.Column(db.String(20), db.ForeignKey('sensor.id'))


class DronePositionModel(db.Model):
    __tablename__ = 'drone_position'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(20))
    drone_id = db.Column(db.Integer, db.ForeignKey('drone.id'))
