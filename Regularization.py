# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 08:57:18 2020

@author: Grant
"""

import random
import math

delta = 0.1

def function1(x):
    return x

def function2(x):
    return x**2

def function3(x):
    return x**3

number_of_trials = 1000
sum_of_trials = 0
n = 20

trial_data = [[1, 1], [3, 28], [2, 9], [6, 216], [8, 511], [9, 729], [6, 201], [3, 28], [11, 1331], [12, 1600], [15, 3375], [29, 24389], [35, 42875], [11, 1200], [18, 5832], [18, 5600], [81, 531111], [16, 4000], [12, 1728], [18, 5832]]

regularization = []
number_of_points = len(trial_data)

for a in range(3):
    temp_loss = 0
    lam = 1/number_of_points
    complexity = 0
    
    for b in range(number_of_points):
        if a == 0:
            temp_loss += (function1(trial_data[b][0]) - trial_data[b][1])**2
            complexity = 1
            
        if a == 1:
            temp_loss += (function2(trial_data[b][0]) - trial_data[b][1])**2
            complexity = 2
        
        if a == 2:
            temp_loss += (function3(trial_data[b][0]) - trial_data[b][1])**2
            complexity = 3
    
    temp_loss = temp_loss + lam*complexity
    
    regularization.append([a, temp_loss])

regularization.sort(key = lambda x: x[1])

print(regularization[0][0])