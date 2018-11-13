from flask import Flask, render_template
from flaskext.mysql import MySQL
from flask import request
from flask import jsonify
import phenotype_transfer as pt

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'hubble'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Hubbl3p@ss'
app.config['MYSQL_DATABASE_DB'] = 'hubble'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
print(cursor)
cursor.execute("SELECT * FROM patients")
result = cursor.fetchall()
print(result)

@app.route("/")
def main():
    return render_template('dashboard.html')

@app.route('/lookup', methods=["POST"])
def showSignUp():
	req = request.json['search']
	print("request: %s" % req)
	resp = pt.find_phenotype(req)
	return jsonify(resp)

app.run(debug=True)

if __name__ == "__main__":
    app.run()
