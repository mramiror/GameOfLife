import pygame
import numpy as np
import time

pygame.init()

# Ancho y alto de la pantalla.
width, height = 1000, 1000
# Creación de la pantalla.
screen = pygame.display.set_mode((height, width))

# Color del fondo = Casi negro, casi oscuro.
bg = 25, 25, 25
# Pintamos el fondo con el color elegido.
screen.fill(bg)

# Número de celdas.
nxC, nyC = 75, 75
# Dimensiones de la celda
dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas. Vivas = 1; Muertas = 0;
gameState = np.zeros((nxC, nyC))

# Autómata palo.
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Autómata movil.
gameState[31, 31] = 1
gameState[32, 32] = 1
gameState[32, 33] = 1
gameState[31, 33] = 1
gameState[30, 33] = 1

# Control de la ejecución del juego.
pauseExect = False

# Bucle de ejecución
while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    # Registramos eventos de teclado y ratón.
    ev = pygame.event.get()

    for event in ev:
        # Detectamos si se presiona una tecla.
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        # Detectamos si se presiona el ratón.
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0, nyC):
        for x in range(0, nxC):

            if not pauseExect:

                # Calculamos el número de vecinos directos (8 en total).
                n_neigh =   gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                            gameState[x       % nxC, (y - 1) % nyC] + \
                            gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                            gameState[(x - 1) % nxC, y       % nyC] + \
                            gameState[(x + 1) % nxC, y     % nyC] + \
                            gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                            gameState[x       % nxC, (y + 1) % nyC] + \
                            gameState[(x + 1) % nxC, (y + 1) % nyC]
                
                # Rule #1:  Una célula muerta con exactamente 3 células vecinas vivas, "revive" (es decir, al turno siguiente estará viva).
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                # Rule #2: Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere (por "soledad" o "superpoblación").
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Creamos el polígono de cada celda a dibujar.
            poly = [(x     * dimCW,    y * dimCH),
                    ((x + 1) * dimCW,  y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    (x     * dimCW,   (y + 1) * dimCH)]

            # Dibujamos la celda para cada par de x e y.
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    
    # Actualizamos el estado del juego.
    gameState = np.copy(newGameState)

    # Actualizamos la pantalla.
    pygame.display.flip()