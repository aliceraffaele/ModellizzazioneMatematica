#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:39:03 2022

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("TrasportoCaffè", LpMinimize)

# Set e parametri
T = [1,2]
B = [1,2,3]
capacita_prod = {1: 54, 2: 44}
domanda = {1: 35, 2: 30, 3: 33}
costi = {
    1: {1: 0.4, 2: 0.3, 3: 0.2},
    2: {1: 0.2, 2: 0.3, 3: 0.5}}

# Variabili
x = LpVariable.dicts("x", (T, B), 0, None, LpContinuous)

# Funzione obiettivo
model += lpSum(x[i][j]*costi[i][j] for i in T for j in B) 

# Vincoli
for i in T:
    model += lpSum(x[i][j] for j in B) <= capacita_prod[i]
    
for j in B:        
    model += lpSum(x[i][j] for i in T) >= domanda[j]

# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    print(v.name, " = ", v.varValue)
    
# Valore della funzione obiettivo
print("Costo minimo per il trasporto = {}".format(round(value(model.objective),2)))
