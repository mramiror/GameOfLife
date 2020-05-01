import pygame
import numpy as np
import time
# import matplotlib.pyplot as plt

pygame.init()

size = width, height = 600, 600

nxC = 60
nyC = 60

dimCW = width / nxC
dimCH = height / nyC

bg = 25, 25, 25

screen = pygame.display.set_mode(size)
screen.fill(bg)

gameState = np.random.randint(0, 2, (nxC, nyC))

# gameState = np.zeros((nxC, nyC))

# gameState[20, 20] = 1
# gameState[20, 19] = 1
# gameState[20, 21] = 1

# gameState[31, 31] = 1
# gameState[32, 32] = 1
# gameState[32, 33] = 1
# gameState[31, 33] = 1
# gameState[30, 33] = 1

while 1:
    pygame.event.get()
    screen.fill(bg)
    gameStateNew = np.copy(gameState)

    for x in range(0, nxC):
        for y in range(0, nyC):
            # Se calcula el numero de vecinos de la célula (8 en total)
            n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                gameState[(x) % nxC, (y - 1) % nyC] + \
                gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                gameState[(x - 1) % nxC, (y) % nyC] + \
                gameState[(x + 1) % nxC, (y) % nyC] + \
                gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                gameState[(x) % nxC, (y + 1) % nyC] + \
                gameState[(x + 1) % nxC, (y + 1) % nyC]

            # Una célula muerta con exactamente 3 células vecinas vivas "nace" (es decir, al turno siguiente estará viva).
            if gameState[x, y] == 0:
                if n_neigh == 3:
                    gameStateNew[x, y] = 1
            # Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere (por "soledad" o "superpoblación").
            else:
                if n_neigh < 2 or n_neigh > 3:
                    gameStateNew[x, y] = 0

            poly = [((x) * dimCW, (y) * dimCH),
                    ((x + 1) * dimCW,     (y) * dimCH),
                    ((x + 1) * dimCW,     (y + 1) * dimCH),
                    ((x) * dimCW, (y + 1) * dimCH)]
            # plt.matshow(gameState)
            # plt.show()

            pygame.draw.polygon(screen, (128, 128, 128), poly, int(abs(1 - gameState[x, y])))
    gameState = np.copy(gameStateNew)

    time.sleep(0.1)
    pygame.display.flip()