import numpy as np

"""
Sample Math File for LaptagBernstein
------------------------------------
Define a function analyze
Must have an array as an argument
This is the function that will be called
Make sure to return an array of an array of x values and an array of y values
"""

def analyze(arrays):
	#getting the arrays from the argument
    arrayX = arrays[0]
    arrayY = arrays[1]

    #doing some math
    for val in arrayX:
    	arrayX[val] = arraX[val] % 2
    for val in arrayY:
    	arrayY[val] = arrayY[val]**2

    #returning array of the values
    return [freq[idx], ny[idx]]
