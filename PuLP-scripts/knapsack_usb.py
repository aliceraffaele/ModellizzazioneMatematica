#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:39:03 2022

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("ChiavettaUSB", LpMaximize)

# Set e parametri
I = [1,2,3,4,5,6,7,8]
preferenze = { 1: 9.5, 2: 8, 3: 9, 4: 7, 5: 6.5, 6: 9, 7: 10, 8: 8.5}
dimensione = { 1: 25, 2: 20, 3: 30, 4: 20, 5: 18, 6: 22, 7: 27, 8: 19}
capacita_USB = 140

# Variabili
vars = LpVariable.dicts("x", I, 0, 1, LpBinary)

# Funzione obiettivo
model += lpSum(vars[i] * preferenze[i] for i in I)

# Vincoli
model += lpSum(vars[i]*dimensione[i] for i in I) <= 140
model += lpSum(vars[i] for i in I) >= 6
model += vars[1] + vars[2] + vars[7] + vars[8] <= 2

# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    print(v.name, " = ", v.varValue)
    
# Valore della funzione obiettivo
print("Gradimento totale canzoni = {}".format(round(value(model.objective),2)))
