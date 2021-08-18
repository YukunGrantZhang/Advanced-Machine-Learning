# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 10:35:50 2020

@author: Grant
"""

num_variables = 8

import numpy

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

A = [[1, 0, 0, 0], [0.1, 1, 0, 0], [0, 0.1, 1, 0], [0, 0, 0.1, 1]]

B = [[0.2, 0, 0, 0], [0, 0.2, 0, 0], [0, 0, 0.2, 0], [0, 0, 0, 0.2]]

a_s = [0.1, 0.1, 0.1, 0.1]
covariances = [0.05, 0.05, 0.05, 0.05]

def get_probability(probability, graph, source_number, source_state, destination_number, destination_state):
    source_index = 0
    for a in range(len(graph.adj)):
        for b in range(len(graph.adj[a])):
            if graph.adj[a][b].source_number_state == source_number and graph.adj[a][b].source_types_state == source_state:
                source_index = a
    #print(source_index)
    
    for c in range(len(graph.adj[source_index])):
        if graph.adj[source_index][c].destination_number_state == destination_number and graph.adj[source_index][c].destination_types_state == destination_state:
            if graph.adj[source_index][c].destination_types_state == 1:
                i_dash = graph.adj[source_index][c].destination_number_state
                i = graph.adj[source_index][c].source_number_state
                
                return A[i_dash - 1][i - 1] * probability
            if graph.adj[source_index][c].destination_types_state == 2:
                j = graph.adj[source_index][c].destination_number_state
                i = graph.adj[source_index][c].source_number_state
                
                return B[j - 1][i - 1] * probability
    
    for d in range(len(graph.adj[source_index])):
        if graph.adj[source_index][d].destination_types_state == 1:
            i_dash = graph.adj[source_index][d].destination_number_state
            i = graph.adj[source_index][d].source_number_state
                
            new_probability = A[i_dash - 1][i - 1] * probability
            
            return get_probability(new_probability, graph, graph.adj[source_index][d].destination_number_state, graph.adj[source_index][d].destination_types_state, destination_number, destination_state)
    
    return 0

summation_alpha = 0

def alpha(h_number, graph):
    global summation_alpha
    global B
    global a_s
    global covariances
    
    mean = (B[h_number - 1][h_number - 1] - numpy.random.normal(0, covariances[h_number - 1], 1)[0])
    
    p_vt_st = numpy.random.normal(mean, covariances[h_number - 1], 1)[0]
    
    print(mean)
    
    general_p = p_vt_st
    
    #general_p = get_probability(1, hidden_markov_network, h_number, 1, h_number, 2)
    #print(general_p)
    
    if h_number == 1:
        summation_alpha = summation_alpha + general_p
        return general_p
    
    summation = 0
    for a in range(1, h_number):
        summation = summation + get_probability(1, graph, a, 1, a + 1, 1) * alpha(a, graph)
    
    summation_alpha = summation_alpha + summation
    return general_p * summation

T = 4

summation_beta = 0

def beta(h_number_minus, graph):
    global summation_beta
    global B
    global a_s
    global covariances
    
    mean = (B[h_number_minus - 1][h_number_minus - 1] - numpy.random.normal(0, covariances[h_number_minus - 1], 1)[0])
    
    p_vt_st = numpy.random.normal(mean, covariances[h_number_minus - 1], 1)[0]
    
    print(mean)
    
    general_p = p_vt_st
    
    if h_number_minus == 4:
        summation_beta = summation_beta + 1
        return 1
    
    #general_p = get_probability(1, graph, h_number_minus + 1, 1, h_number_minus + 1, 2)
    
    summation_beta = summation_beta + general_p * get_probability(1, graph, h_number_minus, 1, h_number_minus + 1, 1) * beta(h_number_minus + 1, graph)
    return general_p * get_probability(1, graph, h_number_minus, 1, h_number_minus + 1, 1) * beta(h_number_minus + 1, graph)
    
print(get_probability(1, hidden_markov_network, 1, 1, 4, 2))
print(alpha(4, hidden_markov_network))
print(summation_alpha)
print()
print(beta(1, hidden_markov_network))
print(summation_beta)

converge = False
convergence_criteria = 0.00001

a_1_new = 0

while converge == False:
    a_1_new_previous = a_1_new
    A_previous = A[:]
    B_previous = B[:]
    
    for count in range(1, T + 1):
        denominator = 0
        for a in range(1, T + 1):
            summation_alpha = 0
            summation_beta = 0
        
            alpha(a, hidden_markov_network)
            beta(a, hidden_markov_network)
        
            denominator = denominator + summation_alpha * summation_beta
        print(denominator)
    
        numerator = 0
        summation_alpha = 0
        summation_beta = 0
        alpha(count, hidden_markov_network)
        beta(count, hidden_markov_network)
        numerator = summation_alpha * summation_beta
    
        a_1_new = numerator / denominator * (1 / T)
    
        print("A1 New",a_1_new)
    
        brackets = (numpy.random.normal(0, covariances[count - 1], 1)[0])**2
    
        covariances[count - 1] = 1 / a_1_new * a_1_new * brackets
    
    for x in range(0, T):
        for y in range(0, T):
            if A[x][y] == 0 or A[x][y] == 1:
                continue
            
            i_dash = x + 1
            i = y + 1
            
            numerator = 0
            summation_alpha = 0
            summation_beta = 0
            alpha(i, hidden_markov_network)
            beta(i_dash, hidden_markov_network)
            
            
            mean = (B[i_dash - 1][i_dash - 1] - numpy.random.normal(0, covariances[i_dash - 1], 1)[0])
    
            p_vt_st = numpy.random.normal(mean, covariances[i_dash - 1], 1)[0]
    
            print(mean)
            
            numerator = summation_alpha * p_vt_st * get_probability(1, hidden_markov_network, i, 1, i_dash, 1) * summation_beta
            print("Numerator",numerator)
            
            denominator = 0
            for r in range(T):
                summation_alpha = 0
                summation_beta = 0
                alpha(i, hidden_markov_network)
                i_dash = r + 1
                beta(i_dash, hidden_markov_network)
                
                mean = (B[i_dash - 1][i_dash - 1] - numpy.random.normal(0, covariances[i_dash - 1], 1)[0])
    
                p_vt_st = numpy.random.normal(mean, covariances[i_dash - 1], 1)[0]
    
                print(mean)
                
                
                denominator = denominator + summation_alpha * p_vt_st * get_probability(1, hidden_markov_network, i, 1, i_dash, 1) * summation_beta
            print("Denominator",denominator)
            
            A[x][y] = numerator / denominator
    
    print()
    
    for v in range(0, T):
        for h in range(0, T):
            if B[v][h] == 0:
                continue
            
            j = v + 1
            i = h + 1
            
            numerator = 1
            summation_alpha = 0
            summation_beta = 0
            alpha(i, hidden_markov_network)
            beta(i, hidden_markov_network)
            numerator = numerator * summation_alpha * summation_beta
            
            summation_alpha = 0
            summation_beta = 0
            alpha(j, hidden_markov_network)
            beta(j, hidden_markov_network)
            numerator = numerator * summation_alpha * summation_beta
            
            print("Numerator",numerator)
            
            denominator = 0
            for r in range(T):
                summation_alpha = 0
                summation_beta = 0
                i = r + 1
                alpha(i, hidden_markov_network)
                beta(i, hidden_markov_network)
                denominator = denominator + summation_alpha * summation_beta
            print("Denominator",denominator)
            
            B[v][h] = numerator / denominator
    
    converge = True
    for d in range(T):
        for e in range(T):
            if abs(A[d][e] - A_previous[d][e]) > convergence_criteria:
                converge = False

print(a_1_new)
print(A)
print(B)
print(covariances)