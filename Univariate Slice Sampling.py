# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:14:28 2020

@author: Grant
"""

import math
import random
import scipy.stats

x = []
w = 0.01
L = 5

p_mu = 0.1
p_sigma = 0.5

x.append(0.1)

def p_star(x, mu, sigma):
    return (1 / (2 * math.pi * sigma**2)**(1/2)) * math.exp(-(x - mu)**2 / (2 * sigma**2))

for i in range(L):
    probability = p_star(x[i], p_mu, p_sigma)
    
    y = random.uniform(0, probability)
    
    r = random.uniform(0, 1)
    
    x_left = x[i] - r * w
    x_right = x[i] + (1 - r) * w
    
    while p_star(x_left, p_mu, p_sigma) > y:
        x_left = x_left - w
    
    while p_star(x_right, p_mu, p_sigma) > y:
        x_right = x_right + w
    
    x_dash = 0
    accept = False
    
    while accept == False:
        x_dash = random.uniform(x_left, x_right)
        
        if x_dash > y:
            accept = True
        else:
            if x_dash > x[i]:
                x_right = x_dash
            else:
                x_left = x_dash
    
    x.append(x_dash)

print(x)
    
