import pygame
import numpy as np
import time


class GameOfLife:
    def __init__(self, nxC=75, nyC=75, screenDim=(1000, 1000)):
        # Número de celdas por eje
        self.nxC = nxC
        self.nyC = nyC
        # Dimensiones de pantalla
        self.screenDim = screenDim
        # Dimensiones de celda
        self.dimCW = screenDim[0] / nxC
        self.dimCH = screenDim[1] / nyC
        # Dimensiones de celda
        self.oldGameState = np.zeros((nxC, nyC), dtype=int).reshape((nxC, nyC))
        self.newGameState = np.zeros((nxC, nyC), dtype=int).reshape((nxC, nyC))

    def random_state(self):
        # Establecemos un estado inicial aleatorio
        self.oldGameState = np.random.randint(0, 2, (self.nxC, self.nyC))

    def alive_neighbours(self, x, y):
        # Calculamos el número de vecinos directos que estan vivos.
        n_neigh = self.oldGameState[(x - 1) % nxC, (y - 1) % nyC] + \
                self.oldGameState[x % nxC, (y - 1) % nyC] + \
                self.oldGameState[(x + 1) % nxC, (y - 1) % nyC] + \
                self.oldGameState[(x - 1) % nxC, y % nyC] + \
                self.oldGameState[(x + 1) % nxC, y % nyC] + \
                self.oldGameState[(x - 1) % nxC, (y + 1) % nyC] + \
                self.oldGameState[x % nxC, (y + 1) % nyC] + \
                self.oldGameState[(x + 1) % nxC, (y + 1) % nyC]
        return n_neigh

    def play(self):
        pygame.init()

        # Creación de la pantalla.
        screen = pygame.display.set_mode(self.screenDim)
        # Color del fondo = Casi negro, casi oscuro.
        bg = 25, 25, 25
        # Pintamos el fondo con el color elegido.
        screen.fill(bg)

        # Control de la ejecución del juego.
        pauseExect = False

        # Bucle de ejecución
        while True:

            self.newGameState = np.copy(self.oldGameState)

            screen.fill(bg)
            time.sleep(0.01)

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
                    celX = int(np.floor(posX / self.dimCW))
                    celY = int(np.floor(posY / self.dimCH))
                    self.newGameState[celX, celY] = not mouseClick[2]

            for y in range(0, nyC):
                for x in range(0, nxC):

                    if not pauseExect:

                        n_neigh = self.alive_neighbours(x, y)

                        # Rule #1: Una célula muerta con exactamente 3 células
                        # vecinas vivas, "revive" (es decir, al turno siguiente
                        # estará viva).
                        if self.oldGameState[x, y] == 0 and n_neigh == 3:
                            self.newGameState[x, y] = 1

                        # Rule #2: Una célula viva con 2 o 3 células vecinas
                        # vivas sigue viva, en otro caso muere.
                        elif self.oldGameState[x, y] == 1 and (n_neigh < 2 or
                                                               n_neigh > 3):
                            self.newGameState[x, y] = 0

                    # Creamos el polígono de cada celda a dibujar.
                    poly = [(x * self.dimCW, y * self.dimCH),
                            ((x + 1) * self.dimCW,  y * self.dimCH),
                            ((x + 1) * self.dimCW, (y + 1) * self.dimCH),
                            (x * self.dimCW, (y + 1) * self.dimCH)]

                    # Dibujamos la celda para cada par de x e y.
                    if self.newGameState[x, y] == 0:
                        pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
                    else:
                        pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

            # Actualizamos el estado del juego.
            self.oldGameState = np.copy(self.newGameState)

            # Actualizamos la pantalla.
            pygame.display.flip()


if __name__ == "__main__":
    # Ancho y alto de la pantalla.
    width, height = 1000, 1000
    screenDim = (width, height)

    # Número de celdas.
    nxC, nyC = 75, 75

    game = GameOfLife(nxC=nxC, nyC=nyC, screenDim=screenDim)
    game.random_state()
    game.play()
