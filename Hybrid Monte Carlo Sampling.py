# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 10:24:38 2020

@author: Grant
"""

import numpy
import random
import math

starting_mu = 0.1
starting_sigma = 0.1

p_mu = 0.3
p_sigma = 0.1

x = []
starting_point = 0
x.append((numpy.random.normal(starting_mu, starting_sigma, 1))[0])

L = 5

def h(x, y):
    return -1/2 * x**2 - 1/2 * y**2

for i in range(L):
    y = (numpy.random.normal(p_mu, p_sigma, 1))[0]
    
    #direction = [-1, 1]
    #chosen_direction = random.choice(direction)
    chosen_direction = random.uniform(-1, 1)
    
    convergence = 0.1
    difference = 1
    
    x_dash = x[-1]
    y_dash = y
    final_H = 0
    final_H_dash = 0
    while difference > convergence:
        #chosen_direction = random.uniform(-1, 1)
        x_dash = x_dash - chosen_direction * y
        y_dash = y_dash - chosen_direction * abs((-1/2 * x_dash**2) - (-1/2 * x[-1]**2))
        
        H_x_x = h(x[-1], y)
        H_x_dash_x_dash = h(x_dash, y_dash)
        
        difference = abs(H_x_dash_x_dash - H_x_x)
        
        final_H = H_x_x
        final_H_dash = H_x_dash_x_dash
        
        print(difference)
    
    if final_H_dash > final_H:
        x.append(x_dash)
    else:
        probability = math.exp(final_H_dash - final_H)
        p = random.uniform(0, 1)
        
        if p <= probability:
            x.append(x_dash)
        else:
            x.append(x[-1])
print(x)