import numpy as np

def Distancia(a, b):
    return np.sqrt( (b.x-a.x)*(b.x-a.x) + (b.y-a.y)*(b.y-a.y) ) #esta función caclula al distancia entre 2 puntos

def Distancia_tot(puntos): #calcula la distancia total
    total = 0
    for i in range(len(puntos)):
        dist = Distancia(puntos[i], puntos[(i+1) % len(puntos)]) #sumamos todas las distancias
        total += dist 
    return total #distancia total

def Escoger(lista, prob):
    i = 0
    r = np.random.uniform(0, 1)

    while r > 0:
        r -= prob[i]
        i += 1
    i -= 1
    return lista[i].copy()

def Factorial(n): #funcion que calcula el factorail de un número
    if n == 1: 
        return 1
    else:
        return n * Factorial(n - 1) #calculamos de forma iterativa