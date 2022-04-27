#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:39:03 2022

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("CamminoMinimo", LpMinimize)

# Set e parametri
V = ["A","B","C","D","E","F","H","S"]
A = {
     ("A","B"): 9, ("A","F"): 6, ("B","S"): 10, ("C","D"): 5, ("C","E"): 5, ("C","S"): 7, ("D","A"): 5,
     ("D","B"): 7, ("D","S"): 3, ("E","B"): 12, ("E","C"): 5, ("E","F"): 1, ("F","A"): 6, ("F","C"): 8,
     ("F","D"): 2, ("F","E"): 1, ("F","S"): 15, ("H","A"): 9, ("H","C"): 11, ("H","E"): 5, ("H","F"): 6}

source = "H"
destination = "S"

# Variabili
x = LpVariable.dicts("x", A.keys(), 0, 1, LpBinary)

# Funzione obiettivo
model += lpSum(x[i,j]*A[i,j] for i,j in A.keys()) 

# Vincoli
model += lpSum(x[i,j] for i,j in A.keys() if i == source) == 1
model += lpSum(x[i,j] for i,j in A.keys() if j == destination) == 1

for v in V:
    if v not in [source, destination]:
        model += lpSum(x[i,j] for i,j in A.keys() if j == v) == lpSum(x[i,j] for i,j in A.keys() if i == v)

# Chiamata al solver
model.solve()


# Stampa soluzione ottima se trovata
if LpStatus[model.status] == "Optimal":
    print("Soluzione ottima:")
    for v in model.variables():
        print("{} = {}".format(v.name, v.varValue))
        
    # Valore della funzione obiettivo
    print("\nCammino minimo = {}".format(round(value(model.objective),2)))

elif LpStatus[model.status] == "Infeasible":
    print("Istanza non ammissibile")