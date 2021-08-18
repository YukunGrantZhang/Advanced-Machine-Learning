# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:06:12 2020

@author: Grant
"""

import math

training_data = [[1, 3], [2, 5], [10, 1], [6, 8], [3, 8], [11, 5], [9, 5], [6, 11], [15, 3], [12, 9], [8, 12], [6, 11], [15, 9], [14, 7], [16, 8], [18, 11], [19, 12], [12, 8], [11, 19], [9, 12]]

n_leaf = int(math.log(len(training_data)))

print(n_leaf)

final_points = []

def tree(data, n_leaf, xmin, xmax, ymin, ymax, step):
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
    
    x_error = []
    used_sums_x = []
    n_xmin = int(xmin * 100)
    n_xmax = int(xmax * 100)
    n_step = int(step * 100)
    for x in range(n_xmin, n_xmax, n_step):
        x = x / 100
        
        left_data = []
        right_data = []
        
        for p in data:
            if p[0] < x:
                left_data.append(p)
            else:
                right_data.append(p)
        
        left_mean_y = 0
        right_mean_y = 0
        for a in left_data:
            left_mean_y += a[1]
        for b in right_data:
            right_mean_y += b[1]
        if len(left_data) > 0:
            left_mean_y = left_mean_y / len(left_data)
        if len(right_data) > 0:
            right_mean_y = right_mean_y / len(right_data)
        
        error_sum = 0
        for c in left_data:
            error_sum += (c[1] - left_mean_y)**2
        for d in right_data:
            error_sum += (d[1] - right_mean_y)**2
        
        if len(left_data) == 0:
            continue
        
        if len(right_data) == 0:
            continue
        
        if x != left_data[len(left_data) - 1][0] and x != right_data[0][0] and error_sum not in used_sums_x:
            x_error.append([xmin, xmax, x, error_sum])
            used_sums_x.append(error_sum)
            
    x_error.sort(key = lambda x:x[3])
    
    
    
    
    y_error = []
    used_sums_y = []
    n_ymin = int(ymin*100)
    n_ymax = int(ymax*100)
    for y in range(n_ymin, n_ymax, n_step):
        y = y / 100
        
        bottom_data = []
        top_data = []
        
        for p in data:
            if p[1] < y:
                bottom_data.append(p)
            else:
                top_data.append(p)
        
        bottom_mean_x = 0
        top_mean_x = 0
        for a in bottom_data:
            bottom_mean_x += a[0]
        for b in top_data:
            top_mean_x += b[0]
        if len(bottom_data) > 0:
            bottom_mean_x = bottom_mean_x / len(bottom_data)
        if len(top_data) > 0:
            top_mean_x = top_mean_x / len(top_data)
        
        error_sum = 0
        for c in bottom_data:
            error_sum += (c[0] - bottom_mean_x)**2
        for d in top_data:
            error_sum += (d[0] - top_mean_x)**2
            
        if len(bottom_data) == 0:
            continue
        
        if len(top_data) == 0:
            continue
        
        if y != bottom_data[len(bottom_data) - 1][1] and y != top_data[0][1] and error_sum not in used_sums_y:
            y_error.append([ymin, ymax, y, error_sum])
            used_sums_y.append(error_sum)
            
    y_error.sort(key = lambda x:x[3])
    
    if x_error[0][3] > y_error[0][3]:
        top_data = []
        bottom_data = []
        
        for p in data:
            if p[1] < y_error[0][2]:
                bottom_data.append(p)
            else:
                top_data.append(p)
        
        tree(bottom_data, n_leaf, xmin, xmax, ymin, y_error[0][2], step)
        tree(top_data, n_leaf, xmin, xmax, y_error[0][2], ymax, step)
    else:
        right_data = []
        left_data = []
        
        for p in data:
            if p[0] < x_error[0][2]:
                left_data.append(p)
            else:
                right_data.append(p)
        
        tree(left_data, n_leaf, xmin, x_error[0][2], ymin, ymax, step)
        tree(right_data, n_leaf, x_error[0][2], xmax, ymin, ymax, step)

tree(training_data, n_leaf, 0, 20, 0, 20, 0.5)

print(final_points)