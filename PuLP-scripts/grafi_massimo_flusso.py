#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:39:03 2022

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("MassimoFlusso", LpMaximize)

# Set e parametri
V = ["NY","A","B","C","D","SF"]
A = {
     ("NY","A"): 50, ("NY","B"): 40, ("A","C"): 30, ("A","D"): 25, 
     ("B","C"): 20, ("B","D"): 15, ("C","SF"): 40, ("D","SF"): 35}

source = "NY"
dest = "SF"

# Variabili
x = LpVariable.dicts("x", A.keys(), 0, None, LpInteger)
phi = LpVariable("phi", 0, None, LpInteger)

# Funzione obiettivo
model += phi 

# Vincoli
for i,j in A.keys():
    model += x[i,j] <= A[i,j]
    
model += lpSum(x[i,j] for i,j in A.keys() if i == source) == phi
model += lpSum(x[i,j] for i,j in A.keys() if j == dest) == phi

for v in V:
    if v not in [source, dest]:
        model += lpSum(x[i,j] for i,j in A.keys() if j == v) == lpSum(x[i,j] for i,j in A.keys() if i == v)

# Chiamata al solver
model.solve()

# Stampa soluzione ottima se trovata
if LpStatus[model.status] == "Optimal":
    print("Soluzione ottima:")
    for v in model.variables():
        print(v.name, " = ", v.varValue)
        
    # Valore della funzione obiettivo
    print("\nMassimo flusso = {}".format(round(value(model.objective),2)))

elif LpStatus[model.status] == "Infeasible":
    print("Istanza non ammissibile")