# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 10:39:39 2020

@author: Grant
"""

import numpy
from scipy.linalg import svd

n = 3

lam = [0.5, 0.4, 0.3]

Z = []

for l in lam:
    Z_NEW = []
    Z_OLD = numpy.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    PGZ = numpy.array([[8, 6, 0], [5, 0, 0], [3, 0, 6]])
    original_coordinates =[[0, 0], [0, 1], [1, 0], [2, 0], [2, 2]]
    
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
    
        U, s, VT = svd(temp)
    
        new_s = []
    
        for x in s:
            new_s.append(max(x - l, 0))
    
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
    
