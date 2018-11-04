#! /usr/bin/python
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import datetime

def aero(airline):
#liste les aéroports de départ et d'arrivée compatibles avec une compagnie
    
    # Chargement des données
    name_dep = 'Aeroports/Liste_ORIGIN_' + airline + '.csv'
    dep = pd.read_csv(name_dep).iloc[:,1].tolist()
    name_arr = 'Aeroports/Liste_ARR_' + airline + '.csv'
    arr = pd.read_csv(name_arr).iloc[:,1].tolist()
    
    return dep, arr 

def predict_vol(vol):
#renvoie le retard et l'heure d'arrivée ajustée

    # Chargement des données
    unique_carrier = vol[4]
    name = 'Coefficients/coeff_' + unique_carrier + '.csv'
    coeff = pd.read_csv(name).iloc[:,1].tolist()
    liste = pd.read_csv('Aeroports/L_AIRPORT_ID.csv', sep=',', index_col = 'Description', low_memory=False)
    
    # Création des variables
    month = int(vol[0].split('/')[1])
    day_of_month = int(vol[0].split('/')[0])
    day_of_week = datetime.date(int(vol[0].split('/')[2]), month, day_of_month).isoweekday()
    try:
        origin_airport_id = int(liste.loc[vol[5]][0])
    except KeyError:
        origin_airport_id = int(liste.loc[vol[5]].Code.tolist()[0])
    try:
        dest_airport_id = int(liste.loc[vol[6]][0])
    except KeyError:
        dest_airport_id = int(liste.loc[vol[6]].Code.tolist()[0])
    try:
        crs_dep_time = int(str(vol[1]).split(':')[0].zfill(2) + str(vol[1]).split(':')[1].zfill(2))
    except IndexError:
        crs_dep_time = int(vol[1])
    try:
        crs_arr_time = int(str(vol[2]).split(':')[0].zfill(2) + str(vol[2]).split(':')[1].zfill(2))
    except IndexError:
        crs_arr_time = int(vol[2])
    crs_elapsed_time = int(vol[3])
    
    
    # Calcul de la prédiction du retard
    x = [month, day_of_month, day_of_week, origin_airport_id, dest_airport_id, crs_dep_time, crs_arr_time, crs_elapsed_time]
    p = PolynomialFeatures(3)
    x3 = p.fit_transform([[1,1,1,1,1,1,1,1],x])
    
    theta = coeff[:-1]
    theta0 = coeff[-1]
    ret = int((np.dot(x3, theta) + theta0)[1])
    
    # Nouvelle heure d'arrivée
    d = 0
    h = int(str(crs_arr_time).zfill(4)[:2])
    m = int(str(crs_arr_time)[-2:])
    if (m+ret) >= 0:
        d = int((h + int((m + ret)/60)) / 24)
        h = (h + int((m + ret)/60)) % 24
        m = (m + ret) % 60
    else:
        if (h - int((m + (int(ret / 60) + 2)*60 + ret) / 60)) >= 0:
            h = (h - int((m + (int(ret / 60) + 2)*60 + ret) / 60)) % 24
        else:
            d = 1 #Arrivée la veille au maximum
            h = (h + 24 -int((m + (int(ret / 60) + 1)*60 + ret) / 60)) % 24
        m = (m + (int(ret / 60) + 1)*60 + ret) % 60
    if d>0:
        arrivee = str(h).zfill(2)+':'+str(m).zfill(2)+' +{}jour'.format(d)
    else:
        arrivee = str(h).zfill(2)+':'+str(m).zfill(2)
        
    return ret, arrivee
