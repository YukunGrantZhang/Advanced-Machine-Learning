# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 10:24:38 2020

@author: Grant
"""

import numpy
import random

starting_mu = 0.1
sigma = [0.1, 0.1, 0.1, 0.1, 0.1]

p_mu = 0.3
p_sigma = 0.1

x = []
starting_point = 0
x.append((numpy.random.normal(starting_mu, sigma[starting_point], 1))[0])

for i in range(starting_point + 1, len(mu)):
    x_rand =  (numpy.random.normal(x[-1], sigma[i], 1))[0]
    q_minus = (1 / (2 * math.pi * sigma[i]**2)**(1/2)) * math.exp(-(x[-1] - x_rand)**2 / (2 * sigma[i]**2))
    q = (1 / (2 * math.pi * sigma[i]**2)**(1/2)) * math.exp(-(x_rand - x[-1])**2 / (2 * sigma[i]**2))
    p = (1 / (2 * math.pi * p_sigma**2)**(1/2)) * math.exp(-(x_rand - p_mu)**2 / (2 * p_sigma**2))
    p_minus = (1 / (2 * math.pi * p_sigma**2)**(1/2)) * math.exp(-(x[-1] - p_mu)**2 / (2 * p_sigma**2))
    a = (q_minus * p) / (q * p_minus)
    if a >= 1:
        x.append(x_rand)
    else:
        u = random.uniform(0, 1)
        if u < a:
            x.append(x_rand)
        else:
            x.append(x[-1])

print(x)