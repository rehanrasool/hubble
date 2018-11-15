from app import db

class VitalSigns(db.Model):
    __tablename__ = 'vital_signs'

    id = db.Column(db.Integer, primary_key=True)
    body_temp = db.Column(db.String())
    blood_pressure = db.Column(db.String())
    heart_rate = db.Column(db.String())
    breathing_rate = db.Column(db.String())

    def __init__(self, body_temp, blood_pressure, heart_rate, breathing_rate):
        self.body_temp = body_temp
        self.blood_pressure = blood_pressure
        self.heart_rate = heart_rate
        self.breathing_rate = breathing_rate

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'blood_pressure': self.blood_pressure,
            'heart_rate': self.heart_rate,
            'breathing_rate':self.breathing_rate
        }