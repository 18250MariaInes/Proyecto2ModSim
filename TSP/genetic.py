from utils import *
from random import randint
import numpy as np

#Diccionario de conceptos

#Genes: es un punto representado con sus coordenadas (x, y)

#Cromosomas: son las rutas entre puntos 

#Fitness: una función que determina que tan buena es una ruta en este caso que tan pequeña es su distancia

#Mutacion: esta es la forma en que introducimos la varaición, cambiando aleatoriamente dos ciudades

#Selección natural, determina que individuos sobreviven y cuales no para la siguiente generación

#Población: es la colección de todas las posibles rutas 


class Genetic:
    def __init__(self, poblacion=[], poblacion_size=0):
        self.poblacion = poblacion #la cantidad de puntos
        self.size = poblacion_size #el tamaño de cada generación
        self.fitness = [0 for i in range(poblacion_size)]
        self.record = float("inf") #distancia minima
        self.currentDist = float("inf") #distancia actual
        self.current = None #poblacion actual
        self.fitest = [] #la lista de la mejor población
        self.fitestIndex = 0 #indice de la lista 
        self.mutation_rate = 0.9 #la probabilidad de mutar

    def CalculateFitness(self, puntos): #funcion que indica que tan buena es una ruta 
        for i in range(self.size): #en el tamaño de la generación
            nodos = [] 
            for j in self.poblacion[i]:
                nodos.append(puntos[j]) #tomamos los nodos
            dist = Distancia_tot(nodos) #calculamos la distancia total 
            if dist < self.currentDist: #evaluamos si la distancia es mejor
                self.current = self.poblacion[i] #actualizamos la población

            if dist < self.record: #evaluamos que la distancia sea mejor 
                self.record = dist #actualizamos el recrod
                self.fitest = self.poblacion[i] #actualizamos la población
                self.fitestIndex = i#actualizamos el índice
            self.fitness[i] = 1/ (dist+1) #actualizamos fitness de cada punto
        self.NormalizarFitness() #normalizamos la fitness

    def NormalizarFitness(self):
        s = 0
        for i in range(self.size):
            s += self.fitness[i] #sumamos todas las fitness
        for i in range(self.size):
            self.fitness[i] = self.fitness[i]/s #normalizamos todas las fitness

    def Mutar(self, genes): #la función que muta los gentes 
        for i in range(len(self.poblacion[0])): #para tida ka oiblación
            if np.random.uniform(0,1) < self.mutation_rate: #decidimos si muta o no
                a = randint(0, len(genes)-1) #seleccionamos un gen al azar
                b = randint(0, len(genes)-1) #seleccionamos un gen al azar
                genes[a], genes[b] = genes[b], genes[a] #se cambian de lugar los genes 

    def CrossOver(self, gen1, gen2):
        start = randint(0, len(gen1)-1) #seleccionamos el inicio de una cadena de genes
        end   = randint(start-1, len(gen2)-1) #seleccionamos el final de la cadena de genes
        try:
            end = randint(start+1, len(gen2)-1) #probamos que el final exista
        except:
            pass
        nuevos_genes = gen1[start:end] #generamos la nueva listas de genes
        for i in range(len(gen2)):
            p = gen2[i] #seleccionamos un gen de la lista
            if p not in nuevos_genes: #si no está 
                nuevos_genes.append(p) #lo agregamos
        return nuevos_genes #devolvemos los nuevos genes 

    def NaturalSelection(self):
        poblacion_siguiente = [] #lista de población siguiente
        for i in range(self.size):
            generacion1 = Escoger(self.poblacion, self.fitness) #escogemos población con buenas fitness (prob)
            generacion2 = Escoger(self.poblacion, self.fitness) #escogemos otra problación con buena fitness (prob)
            genes = self.CrossOver(generacion1, generacion2) #cruzamos los genes
            self.Mutar(genes) #mutamos esos genes
            poblacion_siguiente.append(genes) #generamos la población siguiente
        self.poblacion = poblacion_siguiente #actualizamos la población
