#! /usr/bin/python
# -*- coding:utf-8 -*-

from modele import predict_vol, aero
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def accueil():
	return render_template('index.html')

@app.route('/aeroport', methods=['POST'])
def selection():
	airline = request.form['compagnie']
	date_dep = request.form['date_dep']
	heure_dep = request.form['heure_dep']
	heure_arr = request.form['heure_arr']
	duree_totale = request.form['duree_totale']
	#aero doit renvoyer un tuple de listes d'aéroports de départ et d'arrivée pour une compagnie
	aero_dep = aero(airline)[0]
	aero_arr = aero(airline)[1]
	
	return render_template('aeroports.html', compagnie = airline, liste_dep = aero_dep, liste_arr = aero_arr, date = date_dep, heure_d = heure_dep, heure_a = heure_arr, duree = duree_totale)

@app.route('/prediction', methods=['POST'])
def vol():
	airline = request.form['airline']
	date_dep = request.form['date_dep']
	heure_dep = request.form['heure_dep']
	heure_arr = request.form['heure_arr']
	duree_totale = request.form['duree_totale']
	aero_dep = request.form['aero_dep']
	aero_arr = request.form['aero_arr']
	 # predict_vol doit renvoyer un tuple retard, heure d'arrivée prévue
	vol = [date_dep, heure_dep, heure_arr, duree_totale, airline, aero_dep, aero_arr]
	retard = predict_vol(vol)[0]
	arrivee_reelle = predict_vol(vol)[1]
	
	return render_template('resultat.html', delai = retard, heure = arrivee_reelle, compagnie = airline, date = date_dep)
	
if __name__ == '__main__':
	app.run(debug = True, use_reloader = True)
