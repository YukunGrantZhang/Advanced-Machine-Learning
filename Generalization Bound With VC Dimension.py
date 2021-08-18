# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 13:55:25 2020

@author: Grant
"""

import math

ec = 0.5 #Euler Coefficienct
dimension = 3 #Dimension of hyperplane
Radius = 10 #data points restricted to a circle with radius R
margin = 0.1 #linear hyperplane with margin
vcd = min(dimension, 2*(Radius)**2/(margin)**2) + 1 #VC Dimension
n = 50000 #number of sample data points
delta = 0.05 #chance for error to occur

e = 2*((vcd*math.log(2*ec*n/vcd) - math.log(delta))/(n))**(1/2) #difference between true risk R(f) and empirical risk Rn(f)

print(e)