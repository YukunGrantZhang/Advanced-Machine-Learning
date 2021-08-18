# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 09:45:12 2020

@author: Grant
"""

import math

training_data = [[1, 7, -1], [2, 6, -1], [1, 5, 1], [5, 1, 1], [6, 1, -1], [7, 2, -1]]
solution = [[1, 7, 0], [2, 6, 0], [1, 5, 0], [5, 1, 0], [6, 1, 0], [7, 2, 0]]
lam = 0.3

weight = []
for a in training_data:
    weight.append(1/len(training_data))
#print(weight)

answer = []
answer_line = []

def classify(x, y, w, b):
    result = w*x + b
    if result >= y:
        return 1
    else:
        return -1

def update_classification():
    global training_data
    global lam
    global solution
    global weight
    global answer_line

    results = []
    for b in range(-200, 200, 1):
        b = b / 10
        for w in range(-100, 100, 1):
            w = w / 10
            temp_sum_1 = 0
            temp_sum_2 = 0
        
            temp_result = []
            for a in range(len(training_data)):
                temp = 0
                x = training_data[a][0]
                y = training_data[a][1]
            
                temp += math.log2(1 + math.exp(-(classify(x, y, w, b))*(y - w*x - b)))
                temp_sum_1 = temp_sum_1 + (temp * weight[a])
        
            #temp_sum_1 = temp_sum_1 / len(training_data)
            temp_sum_2 = lam * abs(w)
            temp_sum = temp_sum_1 + temp_sum_2
        
            temp_result.append(w)
            temp_result.append(b)
            temp_result.append(temp_sum)
        
            #print(temp_result)
        
            results.append(temp_result)

    results.sort(key = lambda x: x[2])

    #print(results)

    #print(f"The ideal separation classification line is y={results[0][0]}x + {results[0][1]}")
    
    w = results[0][0]
    
    b = results[0][1]
    
    for s in solution:
        y = w*s[0] + b
        
        if y >= s[1]:
            s[2] = 1
        else:
            s[2] = -1
    
    answer_line.append([w, b])
    
    #print(training_data)
    #print(solution)

def boosting(x, y, T):
    global training_data
    global solution
    global weight
    global answer
    global answer_line
    
    for i in range(T):
        update_classification()
        answer.append(solution[:])
        print(solution)
        
        error = 0
        for j in range(len(solution)):
            temp = 0
            
            if solution[j][2] == training_data[j][2]:
                temp = 0
            else:
                temp = 1
            
            error += weight[j] * temp
        
        print(error)
        if error != 0:
            w = (1/2) * math.log(1/error - 1)
        else:
            w = 0
        print(w)
        
        total_weights = 0
        for k in range(len(weight)):
            total_weights += weight[k] * math.exp(-w * solution[k][2] * training_data[k][2])
        print(total_weights)
        
        for m in range(len(weight)):
            weight[m] = weight[m] * math.exp(-w * solution[m][2] * training_data[m][2]) / total_weights
        
    print(answer)
    print(answer_line)
    
    if y > answer_line[len(answer_line) - 1][0]* x + answer_line[len(answer_line) - 1][1]:
        return -1
    else:
        return 1
    
print(boosting(1, 2, 10))