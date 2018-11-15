from flask import Flask, render_template, redirect, request, jsonify
from flaskext.mysql import MySQL
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
import os

import phenotype_transfer as pt

app = Flask(__name__)
heroku = Heroku(app)

app.config.update({
    'SQLALCHEMY_DATABASE_URI': os.environ['DATABASE_URL'],
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})
db = SQLAlchemy(app)

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

@app.route("/")
def main():
    return render_template('dashboard.html')

@app.route('/lookup', methods=["POST"])
def showSignUp():
	req = request.json['search']
	print("request: %s" % req)
	resp = pt.find_phenotype(req)
	return jsonify(resp)

@app.route('/add_phenotype', methods=["POST"])
def add_phenotype():
	phenotype = request.form['phenotype']
	print(phenotype)
	return redirect(redirect_url())

# Helper function for redirecting back
def redirect_url(default='index'):
    return request.args.get('next') or request.referrer or url_for(default)

app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
