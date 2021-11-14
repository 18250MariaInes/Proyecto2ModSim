from math import sqrt
from random import randint, uniform

def Distance(a, b):
    return sqrt( (b.x-a.x)*(b.x-a.x) + (b.y-a.y)*(b.y-a.y) )

def SumDistance(points):
    s = 0
    for i in range(len(points)):
        dist = Distance(points[i], points[(i+1) % len(points)])
        s += dist
    return s

def PickSelection(myList, probabilities):
    i = 0
    r = uniform(0, 1)

    while r > 0:
        r -= probabilities[i]
        i += 1
    i -= 1
    return myList[i].copy()

def Factorial(n):
    if n == 1:
        return 1
    else:
        return n * Factorial(n - 1)
