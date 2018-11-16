from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, Integer, select
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
							Column('id', Integer, primary_key=True, autoincrement=True, nullable=True),
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
							Column('id', Integer, primary_key=True, autoincrement=True, nullable=True),
							Column('sex', String),
							Column('age', String),
							Column('race', String),
							Column('ethnicity', String))

lab_results_table = Table('lab_results', meta,
							Column('id', Integer, primary_key=True, autoincrement=True, nullable=True),
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
							Column('id', Integer, primary_key=True, autoincrement=True, nullable=True),
							Column('body_temperature', String),
							Column('pulse_rate', String),
							Column('respiration_rate', String),
							Column('blood_pressure', String))

contributors_table = Table('contributors', meta,
							Column('id', Integer, primary_key=True, autoincrement=True, nullable=True),
							Column('name', String),
							Column('email', String),
							Column('organization', String),
							Column('reference', String))

# # Create
# insert_statement = film_table.insert().values(title="Doctor Strange", director="Scott Derrickson", year="2016")
# conn.execute(insert_statement)

# Read
# select_statement = phenotypes_table.select()
# result_set = conn.execute(select_statement)
# for r in result_set:
# 	print(r)

# # Update
# update_statement = film_table.update().where(film_table.c.year=="2016").values(title = "Some2016Film")
# conn.execute(update_statement)

# # Delete
# delete_statement = film_table.delete().where(film_table.c.year == "2016")
# conn.execute(delete_statement)

########################### helper functions ###########################

def find_phenotype(phenotype):
	print("looking for: %s" % phenotype)
	phenotype_statement = phenotypes_table.select()
	result = []
	# for r in conn.execute(phenotype_statement):
	# 	result.append(r)
	rows = conn.execute(phenotype_statement)
	list_of_dicts = [{key: value for (key, value) in row.items()} for row in rows]

	for phenotype in list_of_dicts:
		demographics_id = phenotype['demographics_id']
		lab_results_id = phenotype['lab_results_id']
		vital_signs_id = phenotype['vital_signs_id']
		contributors_id = phenotype['contributors_id']

		# demographic dictionary
		demographics_statement = demographics_table.select().where(demographics_table.c.id==demographics_id)
		demographics_dict = [{key: value for (key, value) in row.items()} for row in conn.execute(demographics_statement)]
		
		# lab_results dictionary
		lab_results_statement = lab_results_table.select().where(lab_results_table.c.id==lab_results_id)
		lab_results_dict = [{key: value for (key, value) in row.items()} for row in conn.execute(lab_results_statement)]

		# vital_signs dictionary
		vital_signs_statement = vital_signs_table.select().where(vital_signs_table.c.id==vital_signs_id)
		vital_signs_dict = [{key: value for (key, value) in row.items()} for row in conn.execute(vital_signs_statement)]

		# contributors dictionary
		contributors_statement = contributors_table.select().where(contributors_table.c.id==contributors_id)
		contributors_dict = [{key: value for (key, value) in row.items()} for row in conn.execute(contributors_statement)]
		
		phenotype['demographics'] = demographics_dict[0]
		phenotype['lab_results'] = lab_results_dict[0]
		phenotype['vital_signs'] = vital_signs_dict[0]
		phenotype['contributors'] = contributors_dict[0]

	return list_of_dicts

########################################################################

@app.route("/")
def main():
	return render_template('dashboard.html')

@app.route('/lookup', methods=["POST"])
def lookup():
	req = request.json['search']
	#print("request: %s" % req)
	resp = find_phenotype(req)
	#print(resp)
	# return jsonify(resp)
	return jsonify(resp)

@app.route('/add_phenotype', methods=["POST"])
def add_phenotype():
	print("########## New Phenotype ##########")
	print(request.form)
	print("########## New Phenotype ##########")


	# Demographics
	sex = request.form['sex']
	age = request.form['age']
	race = request.form['race']
	ethnicity = request.form['ethnicity']

	# Lab Results
	red_blood_cells = request.form['red_blood_cells']
	white_blood_cells = request.form['white_blood_cells']
	hemoglobin = request.form['hemoglobin']
	hematocrit = request.form['hematocrit']
	cardiac_makers = request.form['cardiac_makers']
	general_chemistry = request.form['general_chemistry']
	urine = request.form['urine']
	coagulation = request.form['coagulation']
	cerebral_spine_fluid = request.form['cerebral_spine_fluid']
	hemodynamic_parameters = request.form['hemodynamic_parameters']
	neurological_values = request.form['neurological_values']
	arterial_values = request.form['arterial_values']
	venous_values = request.form['venous_values']

	# Vital Signs
	body_temperature = request.form['body_temperature']
	blood_pressure = request.form['blood_pressure']
	pulse_rate = request.form['pulse_rate']
	respiration_rate = request.form['respiration_rate']

	# Contributor
	contributor_name = request.form['contributor_name']
	organization = request.form['organization']
	email = request.form['email']
	reference = request.form['reference']

	# Phenotypes
	title = request.form['phenotype_title']
	icd9_inclusion = request.form['icd9_inclusion']
	icd9_exclusion = request.form['icd9_exclusion']
	icd10_inclusion = request.form['icd10_inclusion']
	icd10_exclusion = request.form['icd10_exclusion']
	description = request.form['description']
	medications = request.form['medications']

	demographics_statement = demographics_table.insert().values(
		sex=sex, 
		age=age, 
		race=race, 
		ethnicity=ethnicity)

	lab_results_statement = lab_results_table.insert().values(
		red_blood_cells=red_blood_cells, 
		white_blood_cells=white_blood_cells, 
		hemoglobin=hemoglobin,
		hematocrit=hematocrit,
		cardiac_makers=cardiac_makers,
		general_chemistry=general_chemistry,
		urine=urine,
		coagulation=coagulation,
		cerebral_spine_fluid=cerebral_spine_fluid,
		hemodynamic_parameters=hemodynamic_parameters,
		neurological_values=neurological_values,
		arterial_values=arterial_values,
		venous_values=venous_values)

	vital_signs_statement = vital_signs_table.insert().values(
		body_temperature=body_temperature, 
		pulse_rate=pulse_rate, 
		respiration_rate=respiration_rate, 
		blood_pressure=blood_pressure)

	contributor_statement = contributors_table.insert().values(
		name=contributor_name, 
		email=email, 
		organization=organization, 
		reference=reference)

	demographics_id = conn.execute(demographics_statement).inserted_primary_key[0]
	lab_results_id = conn.execute(lab_results_statement).inserted_primary_key[0]
	vital_signs_id = conn.execute(vital_signs_statement).inserted_primary_key[0]
	contributors_id = conn.execute(contributor_statement).inserted_primary_key[0]

	phenotypes_statement = phenotypes_table.insert().values(
		title=title, 
		icd9_inclusion=icd9_inclusion, 
		icd9_exclusion=icd9_exclusion,
		icd10_inclusion=icd10_inclusion,
		icd10_exclusion=icd10_exclusion,
		description=description,
		medications=medications,
		demographics_id=demographics_id,
		lab_results_id=lab_results_id,
		vital_signs_id=vital_signs_id,
		contributors_id=contributors_id)

	phenotypes_id = conn.execute(phenotypes_statement).inserted_primary_key[0]

	return redirect(redirect_url())

# Helper function for redirecting back
def redirect_url(default='index'):
	return request.args.get('next') or request.referrer or url_for(default)

if __name__ == "__main__":
	app.debug = True
	app.run(debug=True, port=5000)
