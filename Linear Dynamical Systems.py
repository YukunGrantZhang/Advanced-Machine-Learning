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

def LDS_forward(f, F, v_array):
    global A
    global B
    
    global v_bias
    global h_bias
    
    global matrix_sigma_v
    global matrix_sigma_h
    
    A_matrix = numpy.array(A)
    B_matrix = numpy.array(B)
    
    f_matrix = numpy.array(f)
    F_matrix = numpy.array(F)
    
    v_bias_matrix = numpy.array(v_bias)
    h_bias_matrix = numpy.array(h_bias)
    
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

def LDS_backward(g, G, f, F):
    global A
    global B
    
    global v_bias
    global h_bias
    
    global matrix_sigma_v
    global matrix_sigma_h
    
    A_matrix = numpy.array(A)
    B_matrix = numpy.array(B)
    
    v_bias_matrix = numpy.array(v_bias)
    h_bias_matrix = numpy.array(h_bias)
    
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
    
n = 10000

max_likelihood = -10000000000

A_MAX = []
B_MAX = []

while i < n:
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
        for s in B[w1 - 1]:
            if s != 0:
                temp.append(numpy.random.normal(v_bias_series[w1], sigma_v_series[w1], 1)[0])
            else:
                temp.append(0)
        noise_v.append(temp)
        
        
        temp = []
        for s in A[w1 - 1]:
            if s != 0:
                temp.append(numpy.random.normal(h_bias_series[w1], sigma_h_series[w1], 1)[0])
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
        v.append(noise_v[a])
    
    
    
    
    
    current_f, current_F, current_likelihood = LDS_forward(f_1, F_1, v[1])
    f_F = []
    f_F.append([current_f, current_F])

    previous_f = current_f
    previous_F = current_F
    total_likelihood = 0
    total_likelihood = total_likelihood + math.log(current_likelihood)

    for t in range(2, T + 1):
        current_f, current_F, current_likelihood = LDS_forward(previous_f, previous_F, v[t])
        total_likelihood = total_likelihood + math.log(current_likelihood)
        f_F.append([current_f, current_F])
        previous_f = current_f
        previous_F = current_F

    f_F_array = []
    for x in range(len(f_F)):
        temp = []
        for y in range(len(f_F[x][0])):
            temp.append(f_F[x][0][y])
    
        temp1 = []
        for z in range(len(f_F[x][1])):
            temp2 = []
            for t in range(len(f_F[x][1][z])):
                temp2.append(f_F[x][1][z][t])
            temp1.append(temp2)
    
        f_F_array.append([temp, temp1])

    g_G_array = []
    g_G_array.append([f_F_array[-1][0], f_F_array[-1][1]])

    for a in range(T-2, -1, -1):
        current_g, current_G = LDS_backward(g_G_array[-1][0], g_G_array[-1][1], f_F_array[a][0], f_F_array[a][1])
        g_G_array.append([current_g, current_G])

    smoothed_posterior = g_G_array[-1][0]
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