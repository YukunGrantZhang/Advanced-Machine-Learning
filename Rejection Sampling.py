# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 09:59:04 2020

@author: Grant
"""

import numpy
import math
import random
#q distribution
mu_1 = 0
sigma_1 = 0.1

#p* distribution
mu_2 = 0.2
sigma_2 = 0.3 

L = 5
M = 5

samples = []

for l in range(L):
    a = 0
    u = 1
    sample = 0
    while u > a:
        sample = (numpy.random.normal(mu_1, sigma_1, 1))[0]
        
        q = (1 / (2 * math.pi * sigma_1**2)**(1/2)) * math.exp(-(sample - mu_1)**2 / (2 * sigma_1**2))
        p = (1 / (2 * math.pi * sigma_2**2)**(1/2)) * math.exp(-(sample - mu_2)**2 / (2 * sigma_2**2))
        
        a = p / (M * q)
        print(a)
        
        u = random.uniform(0, 1)
    samples.append(sample)
print(samples)
        
        
    