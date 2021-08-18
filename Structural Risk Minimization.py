# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 15:58:17 2020

@author: Grant
"""

import random
import math

delta = 0.1

def function_1_1(x):
    if x > 5:
        return x
    else:
        return -x

def function_1_2(x):
    if x**2 > 8:
        return 2*x
    else:
        return -2*x

def function_1_3(x):
    if x**2 - x > 11:
        return 3*x
    else:
        return -3*x
    
def function_2_1(x):
    if x > 15:
        return 2*x
    else:
        return -2*x

def function_2_2(x):
    if x**2 > 18:
        return 3*x
    else:
        return -3*x

def function_2_3(x):
    if x**2 - x > 21:
        return 4*x
    else:
        return -4*x

number_of_trials = 1000
sum_of_trials = 0
n = 20

trial_data = [[1, 2], [3, 5], [2, 5], [6, 11], [8, 12], [9, 15], [6, 11], [3, 8], [11, 19], [12, 21], [15, 31], [29, 55], [35, 69], [11, 21], [18, 35], [18, 32], [81, 159], [16, 35], [12, 23], [18, 38]]

for u in range(number_of_trials):
    R = []

    sigmas = [random.choice([-1, 1]) for x in range(n)]
    numbers = [random.randint(-20, 20) for x in range(n)]

    for i in range(3):
        summation = 0
    
        if i == 0:
            for j in range(len(numbers)):
                summation += sigmas[j]*function_1_1(numbers[j])
            summation = summation / n
        
            R.append([i, summation])
    
        if i == 1:
            for j in range(len(numbers)):
                summation += sigmas[j]*function_1_2(numbers[j])
            summation = summation / n
        
            R.append([i, summation])
    
        if i == 2:
            for j in range(len(numbers)):
                summation += sigmas[j]*function_1_3(numbers[j])
            summation = summation / n
        
            R.append([i, summation])

    R.sort(key = lambda x: x[1], reverse = True)
    
    sum_of_trials += R[0][1]

Rademacher1 = sum_of_trials / number_of_trials

print(Rademacher1)

e1 = 2*Rademacher1 + (math.log(1/delta) / n)**(1/2)

print(e1)

sum_of_trials = 0
number_of_trials = 1000

for u in range(number_of_trials):
    R = []

    sigmas = [random.choice([-1, 1]) for x in range(n)]
    numbers = [random.randint(-20, 20) for x in range(n)]

    for i in range(3):
        summation = 0
    
        if i == 0:
            for j in range(len(numbers)):
                summation += sigmas[j]*function_2_1(numbers[j])
            summation = summation / n
        
            R.append([i, summation])
    
        if i == 1:
            for j in range(len(numbers)):
                summation += sigmas[j]*function_2_2(numbers[j])
            summation = summation / n
        
            R.append([i, summation])
    
        if i == 2:
            for j in range(len(numbers)):
                summation += sigmas[j]*function_2_3(numbers[j])
            summation = summation / n
        
            R.append([i, summation])

    R.sort(key = lambda x: x[1], reverse = True)
    
    sum_of_trials += R[0][1]

Rademacher2 = sum_of_trials / number_of_trials

print(Rademacher2)

e2 = 2*Rademacher2 + (math.log(1/delta) / n)**(1/2)

print(e2)

structural_risk = []
number_of_points = len(trial_data)

for a in range(6):
    temp_loss = 0
    for b in range(number_of_points):
        if a == 0:
            temp_loss += (function_1_1(trial_data[b][0]) - trial_data[b][1])**2
            
        if a == 1:
            temp_loss += (function_1_2(trial_data[b][0]) - trial_data[b][1])**2
        
        if a == 2:
            temp_loss += (function_1_3(trial_data[b][0]) - trial_data[b][1])**2
        
        if a == 3:
            temp_loss += (function_2_1(trial_data[b][0]) - trial_data[b][1])**2
        
        if a == 4:
            temp_loss += (function_2_2(trial_data[b][0]) - trial_data[b][1])**2
        
        if a == 5:
            temp_loss += (function_2_3(trial_data[b][0]) - trial_data[b][1])**2
    
    temp_loss = temp_loss / number_of_points
    
    if a <= 2:
        temp_loss += e1
    else:
        temp_loss += e2
    
    structural_risk.append([a, temp_loss])

structural_risk.sort(key = lambda x: x[1])

print(structural_risk[0][0])