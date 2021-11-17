import pygame
from random import sample
from utils import *
from genetic import Genetic
import numpy as np


offset          = 100 #donde se muestra la pnatalla
width, height   = 1080, 600 #dimensiones del programa
n = 12 #cantidad de puntos
populationSize  = 5*n #tamaño de la poblacion
iterations = 300 #cantidad de generaciones máximas 
pygame.font.init() #inicamos pygame

textColor   = (0, 0, 0) #color de texto (blanco)
textFont    = pygame.font.SysFont("Arial", 20) #tipo de letra del display


class Point: #clase punto
    def __init__(self, x, y):
        self.x      = x #coordenada en X
        self.y      = y #coordenada en Y
        self.radius = 1 #tamaño del punto
        self.alpha  = 150 

    def Draw(self, manager, showIndex=False, highlight=False, point_index=0): #dibujamos la ventana 
        surface = pygame.Surface((self.radius *2, self.radius*2), pygame.SRCALPHA, 32)

        if highlight: #para resaltar los círculos 
            r, g, b = manager.White
            pygame.draw.circle(surface, (r, g, b, 255), (self.radius, self.radius), self.radius)
            pygame.draw.circle(surface, (r, g, b, 255), (self.radius, self.radius), self.radius, 1)


        manager.screen.blit(surface, (int(self.x-self.radius), int(self.y-self.radius))) #para dibujar los círculos

        if showIndex:
            textSurface = textFont.render(str(point_index), True, textColor) #para mostrar los índices de los círculos 
            textRectangle = textSurface.get_rect(center=(self.x, self.y))
            manager.screen.blit(textSurface, textRectangle)




class Manager(object):
    size            = (width, height) #tamaño del programa 
    fps             = 2500 #cantidad de cuadros por segundo 
    screen          = pygame.display.set_mode(size) #tamaño de la pantalla
    clock           = pygame.time.Clock() #reloj del juego
    scaler          = 1 #escala del juego
    max_radius      = 15 #radio máximo
    Black           = (0, 0, 0) #color negro
    White           = (255, 255, 255) #color blanco
    Gray            = (100, 100, 100) #color gris
    Highlight       = (51, 153, 255) #resaltar
    generations     = iterations #número de generaciones 
    col_size        = populationSize #numero de población por generación
    actual_gen      = 0 #generación actual 
    LineThickness   = 4 #grosor de las aristas 
    showIndex       = True #mostrar los índices
    n_points        = n #cantidad de puntos 
    genetic         = Genetic([sample(list(range(n)), n) for i in range(populationSize)], populationSize) #la muestra del algoritmo genético
    contador = 0 #contador para las generaciones sin mejoras 
    PossibleCombinations = Factorial(n_points) #todas las posibles combinaciones

    Order           = [i for i in range(n_points)] #orden de los puntos 

    def __init__(self, Points = [Point(np.random.randint(offset, width-offset), np.random.randint(offset, height-offset)) for i in range(n_points)]):
        self.Points          = Points #los puntos iniciales
        self.recordDistance  = Distancia_tot(self.Points) #distancia record
        self.OptimalRoutes   = self.Points.copy() #rutas optimas
        self.currentList     = self.Points.copy() #puntos iniciales


    def ResetGenetic(self): #para resetear el algoritmo
        self.genetic = Genetic([sample(list(range(n)), n) for i in range(populationSize)], populationSize)


    def SetFps(self): #para setear los FPS
        return self.clock.tick(self.fps)/1000.0

    def UpdateCaption(self): #para indicar los FPS a los que corre el programa 
        frameRate = int(self.clock.get_fps())
        pygame.display.set_caption("TSP - Fps : {}".format(frameRate))


    def GeneticAlgorithm(self): #aplicación del algoritmo genético
        self.genetic.CalculateFitness(self.Points)#se calcula la fitness para los puntps 
        self.genetic.NaturalSelection()#se hace una selección natural
        self.contador = self.contador + 1 #este el contador de generaciones sin cambios
        for i in range(self.n_points):
            self.currentList[i] = self.Points[self.genetic.current[i]] #actualizamos la lista de puntos 
        if self.genetic.record < self.recordDistance: #evaluamos si se mejroa la distancia 
            self.contador = 0 #el contador de mejoras se actualiza
            for i in range(self.n_points): 
                self.OptimalRoutes[i] = self.Points[self.genetic.fitest[i]] #se actuaalizan las rutas 
                
                
            self.recordDistance = self.genetic.record #se actualiza la distancia record
        self.actual_gen= self.actual_gen + 1   #se completa una generación


        self.DrawLines(True) #se dibujan las aritas 
    
        

    def RandomPoints(self): #generar puntos aleatorios 
        self.Points = [Point(np.random.randint(offset, width-offset), np.random.randint(offset, height-offset)) for i in range(self.n_points)] #se generan los puntos aleatorios
        self.recordDistance  = Distancia_tot(self.Points) #se actualiza la distancia record
        self.OptimalRoutes   = self.Points.copy() #se actualizan las rutas optimas
        self.currentList     = self.Points.copy() #se actualiza la lista de puntos 


    def ShowText(self, selectedIndex, started = True): #para mostrar texto en la pantalla 
        textColor   = (255, 255, 255) #color negro
        textFont    = pygame.font.SysFont("Times", 20) #tipo y tamaño de letra 
        textFont2    = pygame.font.SysFont("Arial Black", 40) #segundo tipo y tamaño de letra 

        textSurface1 = textFont.render("Mejor distancia encontrada hasta ahora : " + str(round(self.recordDistance,2)), False, textColor) #muestra la mejor distancia
        textSurface2 = textFont.render("Algoritmo Genético", False, textColor) #el algoritmo que se usa 
        textSurface3 = textFont.render("Generación: " + str(int(self.actual_gen/self.col_size)), False, textColor) #la generación actual
        textSurface4 = textFont.render("Puntos: " + str(self.n_points), False, textColor) #ka cabtudad de ountos 
        textSurface5 = textFont.render("Generaciones sin mejora: " + str(int(self.contador/self.col_size)), False, textColor) #las generaciones sin mejoras 

        #ubicaciones de los textos en pantalla 
        self.screen.blit(textSurface1, (70, 70))
        self.screen.blit(textSurface2, (70, 35))
        self.screen.blit(textSurface3, (300, 35))
        self.screen.blit(textSurface4, (450, 35))
        self.screen.blit(textSurface5, (600, 35))

    def DrawShortestPath(self): #función que dibuja el camino más corto entre los puntos 
        if len(self.OptimalRoutes) > 0: #si tenemos más de una ruta optima 
            for n in range(self.n_points): #recorremos todos los posibles puntos 
                i = (n+1)%self.n_points #y el siguiente 
                pygame.draw.line(self.screen, self.Highlight, #dibujamos las aristas en pantalla
                                (self.OptimalRoutes[n].x, self.OptimalRoutes[n].y), #sus coordenadas en X
                                (self.OptimalRoutes[i].x, self.OptimalRoutes[i].y), #sus coordenadas en Y
                                self.LineThickness)
                self.OptimalRoutes[n].Draw(self, self.showIndex, True, n) #dibujamos las rutas optimas 

    def DrawPoints(self, selected_index = 0): #función para dibujar los puntos 
        for point in self.Points: #recorremos todos los puntos 
            point.radius = self.scaler #con unradio igual a la escala
            point.Draw(self) #los dibujamos 

    def DrawLines(self, drawCurrent=False): #función para dibujar las lineas (posibles combinaciones )
        if drawCurrent == True:
            for i, point in enumerate(self.currentList): #recorremos la lista enumerada de puntos actuales 
                j = (i+1)%len(self.currentList) #y sus consecutivos 
                pygame.draw.line(self.screen, self.Gray, (point.x, point.y), (self.currentList[j].x, self.currentList[j].y), 1) #dibujamos las aristas entre ellos 
        else:
            for i, point in enumerate(self.Points): #recorremos la lista enumera de puntos totales
                j = (i+1)%len(self.Points) #y sus consectuvios 
                pygame.draw.line(self.screen, self.Gray, (point.x, point.y), (self.Points[j].x, self.Points[j].y), 1) #dibujamos las aristas entre ellos

    def Background(self): #función para colorear el fondo
        self.screen.fill(self.Black)
