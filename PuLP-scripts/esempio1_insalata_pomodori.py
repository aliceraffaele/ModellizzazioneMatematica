#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 18:32:13 2022

@author: Alice Raffaele
"""
from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("Ettari", LpMinimize)

# Variabili
xL = LpVariable("Num_ettari_lattuga", 0, None, LpContinuous)
xP = LpVariable("Num_ettari_pomodori", 0, None, LpContinuous)

# Vincoli
model += 1*xL + 2*xP <= 100
model += 2000*xL + 4500*xP >= 50000 

# Funzione obiettivo
model += xL + xP

# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    print(v.name, " = ", round(v.varValue,2))
    
# Valore della funzione obiettivo
print("Numero minimo di ettari richiesti = {}".format(round(value(model.objective),2)))







