#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:39:03 2022

@author: Alice Raffaele
"""

from pulp import *
import itertools

def get_combinations(xs):
    returner = []
    for L in range(2, len(xs)+1):
        for subset in itertools.combinations(xs, L):
            returner.append(subset)
    return returner

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("MST", LpMinimize)

# Set e parametri
V = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q"]
E = {
     ("A","B"): 100, ("A","C"): 101, ("B","D"): 47, ("C","D"): 60, ("C","E"): 111,
     ("C","G"): 112, ("D","F"): 79, ("F","G"): 45, ("F","M"): 130, ("G","H"): 120,
     ("H","I"): 43, ("H","L"): 17, ("I","J"): 15, ("J","K"): 18, ("J","L"): 41,
     ("L","M"): 41, ("L","P"): 41, ("M","N"): 37, ("N","O"): 85, ("O","P"): 103,
     ("O","Q"): 113, ("P","Q"): 103}

# Variabili
x = LpVariable.dicts("x", E.keys(), 0, 1, LpBinary)

# Funzione obiettivo
model += lpSum(x[i]*E[i] for i in E.keys()) 

# Vincoli
model += lpSum(x[i] for i in E.keys()) == len(V)-1

combinations = get_combinations(V)
for comb in combinations:
    lati_S = []
    for v in comb:
        lati_v = [i for i in E.keys() if i[0] == v]
        for i in lati_v:
            if i[0] in comb and i[1] in comb:
                lati_S.append(x[i])
    model += lpSum(lati_S) <= len(comb) - 1

# Chiamata al solver
model.solve()

# Stampa soluzione ottima se trovata
if LpStatus[model.status] == "Optimal":
    print("Soluzione ottima:")
    for v in model.variables():
        print(v.name, " = ", v.varValue)
        
    # Valore della funzione obiettivo
    print("Costo MST = {}".format(round(value(model.objective),2)))
    
elif LpStatus[model.status] == "Infeasible":
    print("Istanza non ammissibile")
