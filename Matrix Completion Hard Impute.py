# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 14:50:54 2020

@author: Grant
"""

import numpy
from scipy.linalg import svd

n = 6

lam = [5, 4, 3]

Z = []

for l in lam:
    Z_NEW = []
    Z_OLD = numpy.array([[8, 6, 1, 2, 3, 1], [5, 1, 6, 8, 2, 1], [3, 1, 6, 5, 3, 1], [1, 1, 2, 3, 1, 1], [2, 5, 1, 1, 3, 2], [1, 2, 1, 5, 6, 8]])
    PGZ = numpy.array([[8, 6, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0], [3, 0, 6, 0, 0, 0], [1, 1, 0, 0, 1, 0], [2, 0, 1, 0, 3, 0], [1, 2, 1, 0, 0, 0]])
    original_coordinates =[[0, 0], [0, 1], [1, 0], [2, 0], [2, 2], [3, 0], [3, 1], [3, 4], [4, 0], [4, 2], [4, 4], [5, 0], [5, 1], [5, 2]]
    
    for a in range(100):
        t_PGZ_OLD = []
        for i in range(n):
            temp = []
            for j in range(n):
                temp.append(Z_OLD[i][j])
            t_PGZ_OLD.append(temp)
        
        PGZ_OLD = numpy.array(t_PGZ_OLD)
        
        for i in range(n):
            for j in range(n):
                if [i, j] in original_coordinates:
                    continue
                else:
                    PGZ_OLD[i][j] = 0
        
        temp = numpy.add(numpy.subtract(PGZ, PGZ_OLD), Z_OLD)
        #print(temp)
    
        U, s, VT = svd(temp)
    
        new_s = []
        
        for x in range(0, n):
            if x <= l:
                new_s.append(s[x])
            else:
                new_s.append(0)
            x -= 1
            
        #print(new_s)
        
        matrix_new_s = numpy.array(new_s)
        
        Sigma = numpy.zeros((temp.shape[0], temp.shape[1]))
        
        Sigma[:temp.shape[1], :temp.shape[1]] = numpy.diag(matrix_new_s)
    
        Z_NEW = U.dot(Sigma.dot(VT))
        
        t_Z_OLD = []
        for i in range(n):
            temp = []
            for j in range(n):
                temp.append(Z_NEW[i][j])
            t_Z_OLD.append(temp)
        
        Z_OLD = numpy.array(t_Z_OLD)
    
    Z_NEW_MATRIX = []
    for i in range(n):
        temp = []
        for j in range(n):
            temp.append(int(round(Z_NEW[i][j])))
        Z_NEW_MATRIX.append(temp)
    
    Z.append(Z_NEW_MATRIX)

print(Z)