# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 14:07:12 2020

@author: Grant
"""

import math
import random

training_data = [[1, 3], [2, 5], [10, 1], [6, 8], [3, 8], [11, 5], [9, 5], [6, 11], [15, 3], [12, 9], [8, 12], [6, 11], [15, 9], [14, 7], [16, 8], [18, 11], [19, 12], [12, 8], [11, 19], [9, 12]]

n_leaf = int(math.log(len(training_data)))

print(n_leaf)

final_points = []

def tree(data, n_leaf, xmin, xmax, ymin, ymax):
    global final_points
    
    if len(data) <= n_leaf:        
        x = 0
        y = 0
        
        for i in range(len(data)):
            x += data[i][0]
            y += data[i][1]
        
        final_x = x / len(data)
        final_y = y / len(data)
        
        final_points.append([final_x, final_y])
        
        return
    
    n_xmin = int(xmin * 100)
    n_xmax = int(xmax * 100)
    n_ymin = int(ymin * 100)
    n_ymax = int(ymax * 100)
    
    choice_list = [0, 1]
    choice = random.choice(choice_list)
    
    if choice == 0:
        i = 0
        while i < 10:
            x = random.randint(n_xmin, n_xmax) / 100
        
            left_data = []
            right_data = []
        
            for p in data:
                if p[0] < x:
                    left_data.append(p)
                else:
                    right_data.append(p)
        
            if len(left_data) != 0 and len(right_data) != 0:
                tree(left_data, n_leaf, xmin, x, ymin, ymax)
                tree(right_data, n_leaf, x, xmax, ymin, ymax)
                break
            i += 1
    else:
        i = 0
        while i < 10:
            y = random.randint(n_ymin, n_ymax) / 100
        
            bottom_data = []
            top_data = []
        
            for p in data:
                if p[1] < y:
                    bottom_data.append(p)
                else:
                    top_data.append(p)
            
            if len(bottom_data) != 0 and len(top_data) != 0:
                tree(bottom_data, n_leaf, xmin, xmax, ymin, y)
                tree(top_data, n_leaf, xmin, xmax, y, ymax)
                break
            i += 1

B = 10
input_point = 8
inputs = []

for b in range(B):
    final_points.clear()
    tree(training_data, n_leaf, 0, 20, 0, 20)
    
    distances = []
    for p in final_points:
        d = ((p[0] - input_point)**2)**(1/2)
        distances.append([p[0], p[1], d])
    distances.sort(key = lambda x: x[2])
    
    inputs.append([distances[0][0], distances[0][1]])
    
output_x = 0
output_y = 0
for i in inputs:
    output_x += i[0]
    output_y += i[1]

output_x = output_x / B
output_y = output_y / B
    
print(output_x, output_y)