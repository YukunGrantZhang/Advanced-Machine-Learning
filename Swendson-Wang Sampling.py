# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 10:25:56 2020

@author: Grant
"""

import random
import math

edge_set = [[10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10]]

for a in range(len(edge_set)):
    for b in range(len(edge_set[a])):
        edge_set[a][b] = random.choice([0, 1])

print(edge_set)

clusters = []
for a in range(len(edge_set)):
    for b in range(len(edge_set[a])):
        clusters.append([[a, b]])

print(clusters)

L = 25
B = 0.9

for l in range(2, L + 1):
    x = 0
    while x < len(clusters):
        selection = []
        if len(clusters[x]) < l:
            selection = random.choice(clusters[x])
        
        if selection == []:
            break
        horizontal = selection[1]
        vertical = selection[0]
        
        direction = 0
        if horizontal > 0 and horizontal < 4 and vertical > 0 and vertical < 4:
            direction = random.choice([1, 2, 3, 4])
        elif horizontal == 0:
            if vertical == 0:
                direction = random.choice([2, 3])
            elif vertical == 4:
                direction = random.choice([1, 2])
            else:
                direction = random.choice([1, 2, 3])
        elif horizontal == 4:
            if vertical == 0:
                direction = random.choice([3, 4])
            elif vertical == 4:
                direction = random.choice([1, 4])
            else:
                direction = random.choice([1, 3, 4])
        elif vertical == 0:
            if horizontal == 0:
                direction = random.choice([2, 3])
            elif horizontal == 4:
                direction = random.choice([3, 4])
            else:
                direction = random.choice([2, 3, 4])
        elif vertical == 4:
            if horizontal == 0:
                direction = random.choice([1, 2])
            if horizontal == 4:
                direction = random.choice([1, 4])
            else:
                direction = random.choice([1, 2, 4])
        
        horizontal_new = horizontal
        vertical_new = vertical
        
        if direction == 1:
            vertical_new = vertical - 1
        elif direction == 2:
            vhorizontal_new = horizontal + 1
        elif direction == 3:
            vertical_new = vertical + 1
        elif direction == 4:
            horizontal_new = horizontal - 1
        
        breaks = 0
        removal_index = 0
        for m in range(len(clusters)):
            if len(clusters[m]) < l and m != x:
                for n in range(len(clusters[m])):
                    if clusters[m][n] == [vertical_new, horizontal_new]:
                        probability = 0
                        if edge_set[vertical_new][horizontal_new] == edge_set[vertical][horizontal]:
                            probability = 1 - math.exp(-B)
                            
                            chosen_probability = random.uniform(0, 1)
                            
                            if chosen_probability < probability:
                                for p in clusters[m]:
                                    clusters[x].append(p)
                                
                                removal_index = m
                        
                                breaks = 1
                                break
            if breaks == 1:
                break
        
        if breaks == 1:
            clusters_choice = random.choice([0, 1])
            
            temp_clusters = clusters[x][:]
            
            for q in range(len(clusters[x])):
                edge_set[clusters[x][q][0]][clusters[x][q][1]] = clusters_choice
            
            clusters.remove(clusters[removal_index])
            
            x = clusters.index(temp_clusters)
            
            x = x + 1
        else:
            x = x + 1
        
print(edge_set)
        