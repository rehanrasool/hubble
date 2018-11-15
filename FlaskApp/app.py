from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
db = SQLAlchemy(app)

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
import phenotype_transfer as pt

app = Flask(__name__)

# mysql = MySQL()
 
# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'hubble'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'Hubbl3p@ss'
# app.config['MYSQL_DATABASE_DB'] = 'hubble'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
# conn = mysql.connect()
# cursor = conn.cursor()
# print(cursor)
# cursor.execute("SELECT * FROM patients")
# result = cursor.fetchall()
# print(result)

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
