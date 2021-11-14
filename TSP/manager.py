import pygame
import random
from random import randint, sample
#from point import Point
from utils import *
from genetic import Genetic

offset          = 100
width, height   = 1080, 600
populationSize  = 500
n = 10
colony_size = 10
iterations = 300
pygame.font.init()

textColor   = (0, 0, 0)
textFont    = pygame.font.SysFont("Arial", 20)

class Point:
    def __init__(self, x, y):
        self.x      = x
        self.y      = y
        self.radius = 1
        self.alpha  = 150

    def Draw(self, manager, showIndex=False, highlight=False, point_index=0):
        surface = pygame.Surface((self.radius *2, self.radius*2), pygame.SRCALPHA, 32)

        if highlight:
            r, g, b = manager.White
            pygame.draw.circle(surface, (r, g, b, 255), (self.radius, self.radius), self.radius)
            pygame.draw.circle(surface, (r, g, b, 255), (self.radius, self.radius), self.radius, 1)


        manager.screen.blit(surface, (int(self.x-self.radius), int(self.y-self.radius)))

        if showIndex:
            textSurface = textFont.render(str(point_index), True, textColor)
            textRectangle = textSurface.get_rect(center=(self.x, self.y))
            manager.screen.blit(textSurface, textRectangle)

    def GetTuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Manager(object):
    size            = (width, height)
    fps             = 30
    screen          = pygame.display.set_mode(size)
    clock           = pygame.time.Clock()
    scaler          = 1
    max_radius      = 15
    Black           = (0, 0, 0)
    White           = (255, 255, 255)
    Gray            = (100, 100, 100)
    Highlight       = (51, 153, 255)
    LineThickness   = 4
    showIndex       = True
    n_points        = n
    genetic         = Genetic([sample(list(range(n)), n) for i in range(populationSize)], populationSize)
    PossibleCombinations = Factorial(n_points)

    Order           = [i for i in range(n_points)]
    counter         = 0

    def __init__(self, Points = [Point(randint(offset, width-offset), randint(offset, height-offset)) for i in range(n_points)]):
        self.Points          = Points
        self.recordDistance  = SumDistance(self.Points)
        self.OptimalRoutes   = self.Points.copy()
        self.currentList     = self.Points.copy()


    def ResetGenetic(self):
        self.genetic = Genetic([sample(list(range(n)), n) for i in range(populationSize)], populationSize)


    def SetFps(self):
        return self.clock.tick(self.fps)/1000.0

    def UpdateCaption(self):
        frameRate = int(self.clock.get_fps())
        pygame.display.set_caption("TSP - Fps : {}".format(frameRate))

    def Counter(self):
        self.counter += 1
        if self.counter > self.PossibleCombinations:
            self.counter = self.PossibleCombinations

    def GeneticAlgorithm(self):
        self.genetic.CalculateFitness(self.Points)
        self.genetic.NaturalSelection()

        # self.Counter()
        for i in range(self.n_points):
            self.currentList[i] = self.Points[self.genetic.current[i]]
        if self.genetic.record < self.recordDistance:
            for i in range(self.n_points):
                self.OptimalRoutes[i] = self.Points[self.genetic.fitest[i]]
            self.recordDistance = self.genetic.record

        # print(self.OptimalRoutes)

        self.DrawLines(True)

    def RandomPoints(self):
        self.Points = [Point(randint(offset, width-offset), randint(offset, height-offset)) for i in range(self.n_points)]
        self.recordDistance  = SumDistance(self.Points)
        self.OptimalRoutes   = self.Points.copy()
        self.currentList     = self.Points.copy()


    def ShowText(self, selectedIndex, started = True):
        textColor   = (255, 255, 255)
        textFont    = pygame.font.SysFont("Times", 20)
        textFont2    = pygame.font.SysFont("Arial Black", 40)

        textSurface1 = textFont.render("Mejor distancia encontrada hasta ahora : " + str(round(self.recordDistance,2)), False, textColor)
        textSurface2 = textFont.render("Algoritmo Genético", False, textColor)

        self.screen.blit(textSurface1, (70, 70))
        self.screen.blit(textSurface2, (70, 35))

    def DrawShortestPath(self):
        if len(self.OptimalRoutes) > 0:
            for n in range(self.n_points):
                _i = (n+1)%self.n_points
                pygame.draw.line(self.screen, self.Highlight,
                                (self.OptimalRoutes[n].x, self.OptimalRoutes[n].y),
                                (self.OptimalRoutes[_i].x, self.OptimalRoutes[_i].y),
                                self.LineThickness)
                self.OptimalRoutes[n].Draw(self, self.showIndex, True, n)

    def DrawPoints(self, selected_index = 0):
        for point in self.Points:
            point.radius = self.scaler
            point.Draw(self)

    def DrawLines(self, drawCurrent=False):
        if drawCurrent == True:
            for i, point in enumerate(self.currentList):
                _i = (i+1)%len(self.currentList)
                pygame.draw.line(self.screen, self.Gray, (point.x, point.y), (self.currentList[_i].x, self.currentList[_i].y), 1)
        else:
            for i, point in enumerate(self.Points):
                _i = (i+1)%len(self.Points)
                pygame.draw.line(self.screen, self.Gray, (point.x, point.y), (self.Points[_i].x, self.Points[_i].y), 1)

    def Background(self):
        self.screen.fill(self.Black)
