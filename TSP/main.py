import pygame
from manager import *
from random import randint
from UI.setup import *
from utils import Distancia_tot

pygame.init() #iniciamos pygame 

manager = Manager() #creamos una isntancia del manager

selectedIndex = 2 

#definimos variables interactivas 

pause = True 
started = False 
rightMouseClicked = False
GenerateToggle = False
reset = False

PauseButton.state = pause #para pausar el juego
ResetButton.state = reset  #para resetearlo 
RandomButton.state = GenerateToggle #botones


showUI = False
run = True
while run: #mientras se corra el programa 
    manager.Background() #colocamos un background
    
    delta_time = manager.SetFps() #colocamos los FPS definidos en manager
    manager.UpdateCaption() #se actualiza la barra

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #para salir del juego
            run = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE: #para salir del juego
                run = False
            if event.key == pygame.K_SPACE: #para pausar el juego
                pause = not pause
                started = True
            if event.key == pygame.K_n: #para generar nuevos puntos aleatorios
                manager.RandomPoints() #generamos puntos aleatorios 
                GenerateToggle = False
                RandomButton.state = False 
                reset = False 
                ResetButton.state = False 
                temp = manager.Points.copy() #copiamos esos puntos
                manager = Manager(temp) #definimos la nueva temp
                manager.OptimalRoutes = manager.Points.copy() #buscamos las rutas optimas 
                manager.recordDistance = Distancia_tot(manager.Points) #acutalizamos la distancias 
                manager.ResetGenetic() #reseteamos el algoritmo 
            if event.key == pygame.K_r: #para resetear los puntos 
                reset = False
                ResetButton.state = False
                temp = manager.Points.copy() #reseteamos los puntos
                manager = Manager(temp) #definimos la temp
                manager.OptimalRoutes = manager.Points.copy() #buscamos las rutas optimas 
                manager.recordDistance = Distancia_tot(manager.Points) #actualizamos la distancia
                manager.ResetGenetic() #reseteamos el algoritmo

        if event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1:
                rightMouseClicked = True
    if int(manager.actual_gen/manager.col_size) > manager.generations or (int(manager.contador/manager.col_size) > 49): #criterio de paro 
    #si se completan todas las generaciones indicadas o si pasan 50 generaciones sin actualizaciones de la distancia mínima 
        pause = True
        


    #Para ejecutar el algoritmo genético
    if selectedIndex == 2:
        if pause == False: #corre el algoritmo
            manager.GeneticAlgorithm() 
        manager.DrawPoints()#dibuja los puntos
        manager.DrawShortestPath() #dibuja los caminos
    

    manager.ShowText(selectedIndex, started) #muestra los textos

    # UI de videojuego con Pygame
    if showUI:
        panel.Render(manager.screen)
        if pause != PauseButton.state:
            PauseButton.state = pause
        
        #Menu de acciones a realizar, reiniciar, pausar y nuevo
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
            manager.recordDistance = Distancia_tot(manager.Points)
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

    # conteo de iteraciones
    manager.scaler += 1
    if manager.scaler > manager.max_radius:
        manager.scaler = manager.max_radius

    pygame.display.flip()
    rightMouseClicked = False
pygame.quit()
