from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# DATABASE_URL = "postgres://kbsvpvqhjkrrlo:4d168ed12be5e40e5578ed832857932faa8ba341b9a94fd19fa5426e5da1578d@ec2-23-23-153-145.compute-1.amazonaws.com:5432/d6b9rdf9dvnreh"

import os
import psycopg2
import json

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# db = SQLAlchemy(app)

# # Create our database model
# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True)

#     def __init__(self, email):
#         self.email = email

#     def __repr__(self):
#         return '<E-mail %r>' % self.email

# # Set "homepage" to index.html
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Save e-mail to database and send to success page
# @app.route('/prereg', methods=['POST'])
# def prereg():
#     email = None
#     if request.method == 'POST':
#         email = request.form['email']
#         # Check that email does not already exist (not a great query, but works)
#         if not db.session.query(User).filter(User.email == email).count():
#             reg = User(email)
#             db.session.add(reg)
#             db.session.commit()
#             return render_template('success.html')
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.debug = True
#     app.run()

from flask import Flask, render_template, redirect
# from flaskext.mysql import MySQL
from flask import request
from flask import jsonify

app = Flask(__name__)


########################### helper functions ###########################

def find_phenotype(phenotype):
	print("looking for: %s" % phenotype)
	cursor.execute("SELECT * FROM phenotypes;")
	result = cursor.fetchall()
	print(result)
	output = json.dumps(result)
	return output

########################################################################


@app.route("/")
def main():
	return render_template('dashboard.html')

@app.route('/lookup', methods=["POST"])
def showSignUp():
	req = request.json['search']
	print("request: %s" % req)
	resp = find_phenotype(req)
	return jsonify(resp)

@app.route('/add_phenotype', methods=["POST"])
def add_phenotype():
	phenotype = request.form['phenotype']
	print(phenotype)
	return redirect(redirect_url())

# Helper function for redirecting back
def redirect_url(default='index'):
	return request.args.get('next') or request.referrer or url_for(default)

if __name__ == "__main__":
	app.debug = True
	app.run(debug=True, port=5000)
