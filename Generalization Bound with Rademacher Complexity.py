# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 14:28:42 2020

@author: Grant
"""

import random
import math

delta = 0.1

def function1(x):
    if x > 5:
        return 1
    else:
        return -1

def function2(x):
    if x**2 > 8:
        return 1
    else:
        return -1

def function3(x):
    if x**2 - x > 11:
        return 1
    else:
        return -1

number_of_trials = 1000
sum_of_trials = 0
n = 20

for u in range(number_of_trials):
    R = []

    sigmas = [random.choice([-1, 1]) for x in range(n)]
    numbers = [random.randint(-20, 20) for x in range(n)]

    for i in range(3):
        summation = 0
    
        if i == 0:
            for j in range(len(numbers)):
                summation += sigmas[j]*function1(numbers[j])
            summation = summation / n
        
            R.append([i, summation])
    
        if i == 1:
            for j in range(len(numbers)):
                summation += sigmas[j]*function2(numbers[j])
            summation = summation / n
        
            R.append([i, summation])
    
        if i == 2:
            for j in range(len(numbers)):
                summation += sigmas[j]*function3(numbers[j])
            summation = summation / n
        
            R.append([i, summation])

    R.sort(key = lambda x: x[1], reverse = True)
    
    sum_of_trials += R[0][1]

Rademacher = sum_of_trials / number_of_trials

e = 2*Rademacher + (math.log(1/delta) / n)**(1/2)

print(e)