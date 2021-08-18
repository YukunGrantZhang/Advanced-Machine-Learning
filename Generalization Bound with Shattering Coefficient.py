# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 11:18:09 2020

@author: Grant
"""

import math

N = 500 #shattering coefficient Number of function combinations for a given class
n = 50000 #number of sample data points
d = 0.05 #chance for error to occur

e = 2*((math.log(2*m) + math.log(d))/(n))**(1/2) #difference between true risk R(f) and empirical risk Rn(f)

print(e)