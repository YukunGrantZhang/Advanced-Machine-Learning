# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 09:40:50 2020

@author: Grant
"""

import random

states = [1, 2, 3, 4]
probabilities = [0.1, 0.3, 0.3, 0.3]

cumulative_probabilities = []
summation = 0
for p in probabilities:
    summation = summation + p
    cumulative_probabilities.append(summation)
print(cumulative_probabilities)

sample = random.uniform(0, 1)

chosen_state = 0
for q in range(len(cumulative_probabilities)):
    if sample <= cumulative_probabilities[q]:
        chosen_state = states[q]
        break
    
print("Chosen State is", chosen_state)