from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, Integer
# from flaskext.mysql import MySQL

# DATABASE_URL = "postgres://kbsvpvqhjkrrlo:4d168ed12be5e40e5578ed832857932faa8ba341b9a94fd19fa5426e5da1578d@ec2-23-23-153-145.compute-1.amazonaws.com:5432/d6b9rdf9dvnreh"

import os
import psycopg2
import json

DATABASE_URL = os.environ['DATABASE_URL']
app = Flask(__name__)
db = create_engine(DATABASE_URL)
meta = MetaData(db)
conn = db.connect()

# result = db.execute("SELECT * from Persons ")
# rows = result.fetchall()
# print(rows)

phenotypes_table = Table('phenotypes', meta,
							Column('id', Integer),
							Column('title', String),
							Column('description', String),
							Column('icd9_inclusion', String),
							Column('icd9_exclusion', String),
							Column('icd10_inclusion', String),
							Column('icd10_exclusion', String),
							Column('medications', String),
							Column('demographics_id', Integer),
							Column('lab_results_id', Integer),
							Column('vital_signs_id', Integer),
							Column('contributors_id', Integer))

demographics_table = Table('demographics', meta,
							Column('id', Integer),
							Column('sex', String),
							Column('age', String),
							Column('race', String),
							Column('ethnicity', String))

lab_results_table = Table('lab_results', meta,
							Column('id', Integer),
							Column('red_blood_cells', String),
							Column('white_blood_cells', String),
							Column('hemoglobin', String),
							Column('hematocrit', String),
							Column('cardiac_makers', String),
							Column('general_chemistry', String),
							Column('urine', Integer),
							Column('coagulation', String),
							Column('cerebral_spine_fluid', Integer),
							Column('hemodynamic_parameters', String),
							Column('neurological_values', String),
							Column('arterial_values', String),
							Column('venous_values', String))

vital_signs_table = Table('vital_signs', meta,
							Column('id', Integer),
							Column('body_temperature', String),
							Column('pulse_rate', String),
							Column('respiration_rate', String),
							Column('blood_pressure', String))

contributors_table = Table('contributors', meta,
							Column('id', Integer),
							Column('name', String),
							Column('email', String),
							Column('organization', String),
							Column('reference', String))

# # Create
# insert_statement = film_table.insert().values(title="Doctor Strange", director="Scott Derrickson", year="2016")
# conn.execute(insert_statement)

# Read
select_statement = phenotypes_table.select()
result_set = conn.execute(select_statement)
for r in result_set:
	print(r)

# # Update
# update_statement = film_table.update().where(film_table.c.year=="2016").values(title = "Some2016Film")
# conn.execute(update_statement)

# # Delete
# delete_statement = film_table.delete().where(film_table.c.year == "2016")
# conn.execute(delete_statement)

########################### helper functions ###########################

def find_phenotype(phenotype):
	print("looking for: %s" % phenotype)
	select_statement = phenotypes_table.select()
	result = []
	# for r in conn.execute(select_statement):
	# 	result.append(r)
	rows = conn.execute(select_statement)
	list_of_dicts = [{key: value for (key, value) in row.items()} for row in rows]
	return list_of_dicts

########################################################################

@app.route("/")
def main():
	return render_template('dashboard.html')

@app.route('/lookup', methods=["POST"])
def lookup():
	req = request.json['search']
	print("request: %s" % req)
	resp = find_phenotype(req)
	print(resp)
	# return jsonify(resp)
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
