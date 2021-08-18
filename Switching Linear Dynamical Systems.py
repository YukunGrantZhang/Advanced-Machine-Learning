# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 10:35:50 2020

@author: Grant
"""

num_variables = 8

import numpy

import math

class Edge:
    def __init__(self, src, dest, source_number, source_types, destination_number, destination_types):
        self.src = src
        self.dest = dest
        self.source_number_state = source_number
        self.source_types_state = source_types
        self.destination_number_state = destination_number
        self.destination_types_state = destination_types

class Node:
    def __init__(self, value, source_number_state, source_types_state, destination_number_state, destination_types_state):
        self.value = value
        self.source_number_state = source_number_state
        self.source_types_state = source_types_state
        self.destination_number_state = destination_number_state
        self.destination_types_state = destination_types_state

class Graph:
	def __init__(self, edges):

		self.adj = [None] * num_variables

		for i in range(num_variables):
			self.adj[i] = []

		for e in edges:
			node = Node(e.dest, e.source_number_state, e.source_types_state, e.destination_number_state, e.destination_types_state)
			self.adj[e.src].append(node)
            
hidden_markov_data = [Edge(0, 1, 1, 1, 2, 1), Edge(0, 4, 1, 1, 1, 2), 
                         Edge(1, 2, 2, 1, 3, 1), Edge(1, 5, 2, 1, 2, 2),
                         Edge(2, 3, 3, 1, 4, 1), Edge(2, 6, 3, 1, 3, 2),
                         Edge(3, 7, 4, 1, 4, 2)]

hidden_markov_network = Graph(hidden_markov_data)

for i in range(len(hidden_markov_network.adj)):
    for j in range(len(hidden_markov_network.adj[i])):
        print("Source",i)
        print("Destination",hidden_markov_network.adj[i][j].value)
        print("Source Number State",hidden_markov_network.adj[i][j].source_number_state)
        print("Source Types State",hidden_markov_network.adj[i][j].source_types_state)
        print("Destination Number State",hidden_markov_network.adj[i][j].destination_number_state)
        print("Destination Types State",hidden_markov_network.adj[i][j].destination_types_state)
        print()

A = [[0, 0, 0, 0], [0.1, 0, 0, 0], [0, 0.1, 0, 0], [0, 0, 0.1, 0]]
B = [[0.2, 0, 0, 0], [0, 0.2, 0, 0], [0, 0, 0.2, 0], [0, 0, 0, 0.2]]

switching_schedule = [1, 1, 2, 1, 2]

#original State
A_matrix = numpy.array(A)
B_matrix = numpy.array(B)

v_bias = [0.1, 0.1, 0.1, 0.1]
h_bias = [0.1, 0.1, 0.1, 0.1]
sigma_v = [0.05, 0.05, 0.05, 0.05]
sigma_h = [0.05, 0.05, 0.05, 0.05]

v_bias_series = [0.1, 0.1, 0.1, 0.1, 0.1]
h_bias_series = [0.1, 0.1, 0.1, 0.1, 0.1]
sigma_v_series = [0.05, 0.05, 0.05, 0.05, 0.05]
sigma_h_series = [0.05, 0.05, 0.05, 0.05, 0.05]

matrix_sigma_v = numpy.array([[0.05, 0.05, 0.05, 0.05], [0.05, 0.05, 0.05, 0.05], [0.05, 0.05, 0.05, 0.05], [0.05, 0.05, 0.05, 0.05]])
matrix_sigma_h = numpy.array([[0.05, 0.05, 0.05, 0.05], [0.05, 0.05, 0.05, 0.05], [0.05, 0.05, 0.05, 0.05], [0.05, 0.05, 0.05, 0.05]])

#new State
A_matrix_new = numpy.array(A)
B_matrix_new = numpy.array(B)

v_bias_new = [0.2, 0.2, 0.2, 0.2]
h_bias_new = [0.2, 0.2, 0.2, 0.2]
sigma_v_new = [0.1, 0.1, 0.1, 0.1]
sigma_h_new = [0.1, 0.1, 0.1, 0.1]

v_bias_series_new = [0.2, 0.2, 0.2, 0.2, 0.2]
h_bias_series_new = [0.2, 0.2, 0.2, 0.2, 0.2]
sigma_v_series_new = [0.1, 0.1, 0.1, 0.1, 0.1]
sigma_h_series_new = [0.1, 0.1, 0.1, 0.1, 0.1]

matrix_sigma_v_new = numpy.array([[0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1]])
matrix_sigma_h_new = numpy.array([[0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1]])



def LDS_forward(f, F, v_array, state):
    global A
    global B
    
    global v_bias
    global h_bias
    global matrix_sigma_v
    global matrix_sigma_h
    
    global v_bias_new
    global h_bias_new
    global matrix_sigma_v_new
    global matrix_sigma_h_new
    
    A_matrix = numpy.array(A)
    B_matrix = numpy.array(B)
    
    f_matrix = numpy.array(f)
    F_matrix = numpy.array(F)
    
    h_bias_matrix = []
    v_bias_matrix = []
    
    if state == 1:
        v_bias_matrix = numpy.array(v_bias)
        h_bias_matrix = numpy.array(h_bias)
        matrix_sigma_v = matrix_sigma_v
        matrix_sigma_h = matrix_sigma_h
    
    if state == 2:
        v_bias_matrix = numpy.array(v_bias_new)
        h_bias_matrix = numpy.array(h_bias_new)
        matrix_sigma_v = matrix_sigma_v_new
        matrix_sigma_h = matrix_sigma_h_new
    
    mean_h = numpy.add(numpy.dot(A_matrix, f_matrix), h_bias_matrix)

    mean_v = numpy.add(numpy.dot(B_matrix, mean_h), v_bias_matrix)

    cov_h_h = numpy.add(numpy.dot(numpy.dot(A_matrix, F_matrix), A_matrix.T), matrix_sigma_h)

    cov_v_v = numpy.add(numpy.dot(numpy.dot(B_matrix, cov_h_h), B_matrix.T), matrix_sigma_v)

    cov_v_h = numpy.dot(B_matrix, cov_h_h)

    v_array_matrix = numpy.array(v_array)
    f_new = numpy.add(mean_h, numpy.dot(numpy.dot(cov_v_h.T, numpy.linalg.pinv(cov_v_v)), numpy.subtract(v_array_matrix, mean_v)))

    F_new = numpy.subtract(cov_h_h, numpy.dot(numpy.dot(cov_v_h.T, numpy.linalg.pinv(cov_v_v)), cov_v_h))
    
    v_minus_mean = numpy.subtract(v_array_matrix, mean_v)
    numerator = math.exp(-1/2 * numpy.dot(numpy.dot(v_minus_mean.T, numpy.linalg.pinv(cov_v_v)), v_minus_mean))
    
    Pi_matrix = numpy.array([[2 * math.pi] * 4] * 4)
    denominator = (numpy.linalg.det(numpy.multiply(Pi_matrix, cov_v_v)))

    if denominator < 0:
        denominator = 0
    else:
        denominator = denominator ** (1/2)
    
    likelihood = 0
    
    if denominator != 0:
        likelihood = numerator / denominator
    else:
        likelihood = numerator
    
    return f_new, F_new, likelihood

def LDS_backward(g, G, f, F, state):
    global A
    global B
    
    global h_bias
    global matrix_sigma_h
    
    global h_bias_new
    global matrix_sigma_h_new
    
    A_matrix = numpy.array(A)
    B_matrix = numpy.array(B)
    
    h_bias_matrix = []
    
    if state == 1:
        h_bias_matrix = numpy.array(h_bias)
        matrix_sigma_h = matrix_sigma_h
    
    if state == 2:
        h_bias_matrix = numpy.array(h_bias_new)
        matrix_sigma_h = matrix_sigma_h_new
    
    f_matrix = numpy.array(f)
    F_matrix = numpy.array(F)
    g_matrix = numpy.array(g)
    G_matrix = numpy.array(G)

    mean_h = numpy.add(numpy.dot(A_matrix, f_matrix), h_bias_matrix)

    cov_h_dash_h_dash = numpy.add(numpy.dot(numpy.dot(A_matrix, F_matrix), A_matrix.T), matrix_sigma_h)

    cov_h_dash_h = numpy.dot(A_matrix, F_matrix)

    sigma_backward = numpy.subtract(F_matrix, numpy.dot(numpy.dot(cov_h_dash_h.T, numpy.linalg.pinv(cov_h_dash_h_dash)), cov_h_dash_h))

    A_backward = numpy.dot(cov_h_dash_h.T, numpy.linalg.pinv(cov_h_dash_h_dash))

    m_backward = numpy.subtract(f_matrix, numpy.dot(A_backward, mean_h))

    new_g = numpy.add(numpy.dot(A_backward, g_matrix), m_backward)
    new_G = numpy.add(numpy.dot(numpy.dot(A_backward, G_matrix), A_backward.T), sigma_backward)
    
    return new_g, new_G
    
n = 1000

max_likelihood = -10000000000

A_MAX = []
B_MAX = []

while i < n:
    #original state
    A_matrix = numpy.array(A)
    B_matrix = numpy.array(B)

    v_bias = [0.1, 0.1, 0.1, 0.1]
    h_bias = [0.1, 0.1, 0.1, 0.1]
    sigma_v = [0.05, 0.05, 0.05, 0.05]
    sigma_h = [0.05, 0.05, 0.05, 0.05]

    v_bias_series = [0.1, 0.1, 0.1, 0.1, 0.1]
    h_bias_series = [0.1, 0.1, 0.1, 0.1, 0.1]
    sigma_v_series = [0.05, 0.05, 0.05, 0.05, 0.05]
    sigma_h_series = [0.05, 0.05, 0.05, 0.05, 0.05]
    
    #new State
    v_bias_new = [0.2, 0.2, 0.2, 0.2]
    h_bias_new = [0.2, 0.2, 0.2, 0.2]
    sigma_v_new = [0.1, 0.1, 0.1, 0.1]
    sigma_h_new = [0.1, 0.1, 0.1, 0.1]

    v_bias_series_new = [0.2, 0.2, 0.2, 0.2, 0.2]
    h_bias_series_new = [0.2, 0.2, 0.2, 0.2, 0.2]
    sigma_v_series_new = [0.1, 0.1, 0.1, 0.1, 0.1]
    sigma_h_series_new = [0.1, 0.1, 0.1, 0.1, 0.1]
    
    

    f_1 = [0, 0, 0, 0] #initial mean

    F_1 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] #initial covariance

    v_1 = [0, 0, 0, 0] #v probabilities

    h_1 = [0, 0, 0, 0] #h probabilities

    T = 4
    
    last_value = numpy.random.normal(h_bias_series[4], sigma_h_series[4], 1)[0] 
    
    
    
    
    
    
    
    noise_v = []
    noise_h = []

    for w1 in range(T + 1):
        temp = []
        if switching_schedule[w1] == 1:
            for s in B[w1 - 1]:
                if s != 0:
                    temp.append(numpy.random.normal(v_bias_series[w1], sigma_v_series[w1], 1)[0])
                else:
                    temp.append(0)
        if switching_schedule[w1] == 2:
            for s in B_1[w1 - 1]:
                if s != 0:
                    temp.append(numpy.random.normal(v_bias_series_new[w1], sigma_v_series_new[w1], 1)[0])
                else:
                    temp.append(0)
        noise_v.append(temp)
        
        
        temp = []
        if switching_schedule[w1] == 1:
            for s in A[w1 - 1]:
                if s != 0:
                    temp.append(numpy.random.normal(h_bias_series[w1], sigma_h_series[w1], 1)[0])
                else:
                    temp.append(0)
        if switching_schedule[w1] == 2:
            for s in A_1[w1 - 1]:
                if s != 0:
                    temp.append(numpy.random.normal(h_bias_series_new[w1], sigma_h_series_new[w1], 1)[0])
                else:
                    temp.append(0)
        noise_h.append(temp)    

    v_1_matrix = numpy.array(v_1)
    h_1_matrix = numpy.array(h_1)
    
    v = []
    v.append(v_1_matrix)
    
    h = []
    h.append(h_1_matrix)
    
    for b in range(1, T + 1):
        previous_h = numpy.array(h[b - 1])
        new_h = numpy.add(numpy.dot(A_matrix, previous_h), noise_h[b])
        h.append(new_h)
    
    for a in range(1, T + 1):
        previous_v = numpy.array(v[a - 1])
        new_v = []
        for x in range(len(noise_v[a])):
            if noise_v[a][x] != 0:
                new_v.append(previous_v[x] * B_matrix[a - 1][a - 1] + noise_v[a][x])
            else:
                new_v.append(0)
        v.append(new_v)
    
    
    f_F = [] #state = 1
    f_F_new = [] #state = 2
    total_likelihood = 0
    w_original = [0.5, 0.5, 0.5, 0.5]
    w_new = [0.5, 0.5, 0.5, 0.5]
    alpha_original = [0.5, 0.5, 0.5, 0.5]
    alpha_new = [0.5, 0.5, 0.5, 0.5]
    p_original = [0.5, 0.5, 0.5, 0.5]
    p_new = [0.5, 0.5, 0.5, 0.5]
    
    for s in range(1, 3):
        current_f, current_F, current_likelihood = LDS_forward(f_1, F_1, v[1], s)
        
        if s == 1:
            f_F.append([current_f, current_F])
            alpha_original[0] = p_original[0] * current_likelihood
        
        if s == 2:
            f_F_new.append([current_f, current_F])
            alpha_new[0] = p_new[0] * current_likelihood
        
        previous_f = current_f
        previous_F = current_F
        

        for t in range(2, T + 1):
            current_f, current_F, current_likelihood = LDS_forward(previous_f, previous_F, v[t], s)
            
            if s == 1:
                f_F.append([current_f, current_F])
                p_original[t - 1] = w_original[t - 2] * w_original[t - 1] * alpha_original[t - 2] * current_likelihood
                alpha_original[t - 1] = p_original[t - 1]
            
            if s == 2:
                f_F_new.append([current_f, current_F])
                p_new[t - 1] = w_new[t - 2] * w_new[t - 1] * alpha_new[t - 2] * current_likelihood
                alpha_new[t - 1] = p_new[t - 1]
            
            previous_f = current_f
            previous_F = current_F
        
        if s == 1:
            summation = 0
            for e in range(len(p_original)):
                summation = summation + p_original[e]
            total_likelihood = total_likelihood + math.log(summation)
            
        if s == 2:
            summation = 0
            for e in range(len(p_new)):
                summation = summation + p_new[e]
            total_likelihood = total_likelihood + math.log(summation)
        
        
    
    weighted_f_F = []
    for w in range(len(f_F)):
        mean = p_original[w] * f_F[w][0] + p_new[w] * f_F_new[w][0]
        covariance = p_original[w] * f_F[w][1] + p_new[w] * f_F_new[w][1]
        weighted_f_F.append([mean, covariance])
    
    f_F_array = []
    for x in range(len(weighted_f_F)):
        temp = []
        for y in range(len(weighted_f_F[x][0])):
            temp.append(weighted_f_F[x][0][y])
    
        temp1 = []
        for z in range(len(weighted_f_F[x][1])):
            temp2 = []
            for t in range(len(weighted_f_F[x][1][z])):
                temp2.append(weighted_f_F[x][1][z][t])
            temp1.append(temp2)
    
        f_F_array.append([temp, temp1])
    
    g_G_array_weighted = []
    g_G_array_original = []
    g_G_array_new = []
    
    for s in range(1, 3):
        g_G_array = []
        g_G_array.append([f_F_array[-1][0], f_F_array[-1][1]])

        for a in range(T-2, -1, -1):
            current_g, current_G = LDS_backward(g_G_array[-1][0], g_G_array[-1][1], f_F_array[a][0], f_F_array[a][1], s)
            
            g_G_array.append([current_g, current_G])
        
        if s == 1:
            g_G_array_original = g_G_array[:]
        
        if s == 2:
            g_G_array_new = g_G_array[:]
    
    p_original = [0.5, 0.5, 0.5, 0.5]
    p_new = [0.5, 0.5, 0.5, 0.5]
    
    temp = [] 
    
    for w in range(len(g_G_array_original[-1][0])):
        mean = p_original[w] * g_G_array_original[-1][0][w] + p_new[w] * g_G_array_new[-1][0][w]
        temp.append(mean)
    
    smoothed_posterior = temp[:]
    smoothed_posterior_matrix = numpy.array(smoothed_posterior)
    
    
    
    
    
    
    h_1 = h[1]
    h_1_matrix = numpy.array(h_1)
    
    h_1_t = []
    for a in range(len(h_1)):
        h_1_t.append([h_1[a]])
    h_1_t_matrix = numpy.array(h_1_t)
    
    mean_pi_new = numpy.multiply(h_1_matrix, smoothed_posterior_matrix)
    
    sigma_pi_new_left = numpy.multiply(numpy.dot(h_1_t_matrix, h_1_t_matrix.T), smoothed_posterior_matrix)
    sigma_pi_new_right = numpy.dot(numpy.multiply(h_1_t_matrix, smoothed_posterior_matrix), (numpy.multiply(h_1_t_matrix, smoothed_posterior_matrix)).T)
    sigma_pi_new = numpy.subtract(sigma_pi_new_left, sigma_pi_new_right)
    
    
    A_new_left = numpy.array([[0] * T] * T)
    
    for x in range(0, len(h)):
        h_1 = h[x]
        
        if x == len(h) - 1:
            h_2 = [0, 0, 0, last_value]
        else:
            h_2 = h[x + 1]
        
        h_1_t = []
        for b in range(len(h_1)):
            h_1_t.append([h_1[b]])
        h_1_t_matrix = numpy.array(h_1_t)
        
        h_2_t = []
        for c in range(len(h_2)):
            h_2_t.append([h_2[c]])
        h_2_t_matrix = numpy.array(h_2_t)
        
        A_new_left = numpy.add(A_new_left, numpy.multiply(numpy.dot(h_2_t_matrix, h_1_t_matrix.T), smoothed_posterior_matrix))
            
    A_new_right = numpy.array([[0] * T] * T)
    
    for y in range(0, len(h)):
        h_1 = h[y]
        
        h_1_t = []
        for b in range(len(h_1)):
            h_1_t.append([h_1[b]])
        h_1_t_matrix = numpy.array(h_1_t)
        
        A_new_right = numpy.add(A_new_right, numpy.multiply(numpy.dot(h_1_t_matrix, h_1_t_matrix.T), smoothed_posterior_matrix))
    
    A_new_right = numpy.linalg.pinv(A_new_right)
    
    A_new = numpy.dot(A_new_left, A_new_right)
    
    
    
    
    
    
    B_new_left = numpy.array([[0] * T] * T)
    
    for x1 in range(0, len(h)):
        
        h_1 = h[x1]
        v_1 = v[x1]
        
        h_1_t = []
        for b in range(len(h_1)):
            h_1_t.append([h_1[b]])
        h_1_t_matrix = numpy.array(h_1_t)
        
        v_1_t = []
        for c in range(len(v_1)):
            v_1_t.append([v_1[c]])
        v_1_t_matrix = numpy.array(v_1_t)
        
        B_new_left = numpy.add(B_new_left, numpy.dot(v_1_t_matrix, numpy.multiply(v_1_t_matrix.T, smoothed_posterior_matrix)))
    
    B_new_right = numpy.array([[0] * T] * T)
    
    for y1 in range(0, len(h)):
        
        h_1 = []
        if y1 == len(h) - 1:
            h_1 = [0, 0, 0, last_value]
        else:
            h_1 = h[y1 + 1]
        
        
        h_1_t = []
        for b in range(len(h_1)):
            h_1_t.append([h_1[b]])
        h_1_t_matrix = numpy.array(h_1_t)
        
        B_new_right = numpy.add(B_new_right, numpy.multiply(numpy.dot(h_1_t_matrix, h_1_t_matrix.T), smoothed_posterior_matrix))
    
    B_new_right = numpy.linalg.pinv(B_new_right)
    
    B_new = numpy.dot(B_new_left, B_new_right)
    
    satisfy_probability = True
    
    for r1 in range(len(A_new)):
        for r2 in range(len(A_new[r1])):
            if A_new[r1][r2] > 1 or A_new[r1][r2] < 0:
                satisfy_probability = False
    
    for r1 in range(len(B_new)):
        for r2 in range(len(B_new[r1])):
            if B_new[r1][r2] > 1 or B_new[r1][r2] < 0:
                satisfy_probability = False
    
    if total_likelihood > max_likelihood and satisfy_probability == True:
        A_MAX = A_new
        B_MAX = B_new
        max_likelihood = total_likelihood
    
    i = i + 1

print(A_MAX)
print(B_MAX)