import pygame
#from point import *
from manager import *
from random import randint
from UI.setup import *
from utils import SumDistance

pygame.init()

manager = Manager()

selectedIndex = 2

pause = True
started = False
rightMouseClicked = False
GenerateToggle = False
reset = False

PauseButton.state = pause
ResetButton.state = reset
RandomButton.state = GenerateToggle

showUI = False
run = True
while run:
    manager.Background()

    delta_time = manager.SetFps()
    manager.UpdateCaption()

    # handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                pause = not pause
                started = True
            if event.key == pygame.K_n:
                manager.RandomPoints()
                GenerateToggle = False
                RandomButton.state = False
                reset = False
                ResetButton.state = False
                temp = manager.Points.copy()
                manager = Manager(temp)
                manager.OptimalRoutes = manager.Points.copy()
                manager.recordDistance = SumDistance(manager.Points)
                manager.ResetGenetic()
            if event.key == pygame.K_r:
                reset = False
                ResetButton.state = False
                temp = manager.Points.copy()
                manager = Manager(temp)
                manager.OptimalRoutes = manager.Points.copy()
                manager.recordDistance = SumDistance(manager.Points)
                manager.ResetGenetic()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rightMouseClicked = True


    # Choose one method between the 3 below: bruteForce, lexicagraphic order, genetic algorithm
    if selectedIndex == 2:
        if pause == False:
            manager.GeneticAlgorithm()
        manager.DrawPoints()
        manager.DrawShortestPath()
    

    manager.ShowText(selectedIndex, started)

    # UI
    if showUI:
        panel.Render(manager.screen)
        #AlgorithmChoice.Render(manager.screen, rightMouseClicked)
        if pause != PauseButton.state:
            PauseButton.state = pause

        PauseButton.Render(manager.screen, rightMouseClicked)
        ResetButton.Render(manager.screen, rightMouseClicked)
        RandomButton.Render(manager.screen, rightMouseClicked)

        pause = PauseButton.state
        reset = ResetButton.state

        if reset == True:
            reset = False
            ResetButton.state = False
            temp = manager.Points.copy()
            manager = Manager(temp)
            manager.OptimalRoutes = manager.Points.copy()
            manager.recordDistance = SumDistance(manager.Points)
            manager.ResetGenetic()

        GenerateToggle = RandomButton.state
        if GenerateToggle == True:
            manager.RandomPoints()
            GenerateToggle = False
            RandomButton.state = False

        if pause == True:
            PauseButton.text = "Continuar"
        else:
            PauseButton.text = "Pausar"

    # point scale animation increment
    manager.scaler += 1
    if manager.scaler > manager.max_radius:
        manager.scaler = manager.max_radius

    pygame.display.flip()
    rightMouseClicked = False
pygame.quit()
