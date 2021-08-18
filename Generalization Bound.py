# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:25:07 2020

@author: Grant
"""

import math

m = 500 #number of functions in a class
n = 50000 #number of sample data points
d = 0.05 #chance for error to occur

e = ((math.log(2*m) + math.log(1/d))/(2*n))**(1/2) #difference between true risk R(f) and empirical risk Rn(f)

print(e)