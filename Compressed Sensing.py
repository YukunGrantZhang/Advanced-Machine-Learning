# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 10:50:36 2020

@author: Grant
"""

from random import randrange
import numpy as np
import numpy.linalg as la
import scipy.linalg as spla

d = 1000
e = 0.1
delta = 0.01
s = 0.5

k = int(s * math.log(d / (e*delta)) / e**2)

W = []
m = 0
s = 2**(1/2)

for i in range(k):
    temp = []
    
    for j in range(d):
        temp.append(np.random.normal(0, s))
    
    W.append(temp)

W_matrix = numpy.array(W)

x_bar = []
for i in range(k):    
    x_bar.append(randrange(256))

print(x_bar)
x_bar_matrix = numpy.array(x_bar)

W_matrix_inverse = np.linalg.pinv(W_matrix)
x = numpy.dot(W_matrix_inverse, x_bar_matrix)

for i in range(len(x)):
    x[i] = int(x[i])
    if x[i] < 0:
        x[i] = 255 - abs(x[i])
print(x)
