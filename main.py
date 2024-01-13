import pygame
import sys
import numpy as     np
from utils   import get_game_params, GameOfLife

# Obteniendo Parámetros del juego
No_x_cel, No_y_cel = get_game_params()

# Define los colores
WHITE                 = (255, 255, 255)
BACKGROUND_COLOR      = (200, 200, 255)

# Define el tamaño de la pantalla
SCREEN_WIDTH          = 800
SCREEN_HEIGHT         = 600

# Inicializa Pygame
pygame.init()
pygame.display.set_caption("El Juego de la Vida de Conway")

# Crear la pantalla base
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)

# Crea la superficie del área de juego
game_surface = pygame.Surface((580, 580))
game_surface.fill(BACKGROUND_COLOR)

# Dibuja la superficie del área de juego en el centro de la pantalla
screen.blit(game_surface, (10, 10))

# Dibujar un rectángulo detrás de los botones
control_surface = pygame.Surface((190, 580))
control_surface.fill(BACKGROUND_COLOR)

# Boton de Pausa en Panel
pause_image        = pygame.image.load("image/stop.png")
play_image         = pygame.image.load("image/play.png")
pause_button_size  = 30
pause_image        = pygame.transform.scale(pause_image, (pause_button_size, pause_button_size))
play_image         = pygame.transform.scale(play_image, (pause_button_size, pause_button_size))
pause_button_image = play_image
is_paused          = True

# Boton de Salvar Estado:
save_image        = pygame.image.load("image/save_false.png")
saved_image       = pygame.image.load("image/saved.png")
save_button_size  = 50
save_image        = pygame.transform.scale(save_image, (save_button_size, save_button_size))
saved_image       = pygame.transform.scale(saved_image, (save_button_size, save_button_size))
save_button_image = save_image

# Boton de recargar estado salvado
reload_button_image        = pygame.image.load("image/reload.png")
reload_button_size         = 30
reload_button_image        = pygame.transform.scale(reload_button_image, (reload_button_size, reload_button_size))

# Boton de generar estado Aleatorio
random_button_image        = pygame.image.load("image/random.png")
random_button_size         = 30
random_button_image        = pygame.transform.scale(random_button_image, (random_button_size, random_button_size))

# Boton de seleccionar Vecindad
moore_image              = pygame.image.load("image/moore.png")
neumann_image            = pygame.image.load("image/neumann.png")
neighborhood_button_size = 100
moore_image              = pygame.transform.scale(moore_image, (neighborhood_button_size, neighborhood_button_size))
neumann_image            = pygame.transform.scale(neumann_image, (neighborhood_button_size, neighborhood_button_size))
neighborhood_image       = moore_image
neighborhood             = "Moore"

# Ajustar las dimensiones de la matriz de juego para que sean múltiplos de las dimensiones de la pantalla
cel_width  = game_surface.get_width()  // No_x_cel
cel_heigth = game_surface.get_height() // No_y_cel
No_x_cel   = game_surface.get_width()  // cel_width
No_y_cel   = game_surface.get_height() // cel_heigth

# Inicializar parámetros del juego
gameState  = np.zeros((No_x_cel, No_y_cel))
game       = GameOfLife(gameState)
game.draw(screen=game_surface, cel_heigth=cel_heigth, cel_width=cel_width)
saved_gameState = np.copy(game.gameState)

# Inicializar control FPS
clock  = pygame.time.Clock()

while True:

    # Checar si el estado actual es igual a el estado salvado
    if np.all(game.gameState == saved_gameState):
        state_is_save = True
        save_button_image = saved_image
    else:
        state_is_save = False
        save_button_image = save_image

    # Checar eventos
    for event in pygame.event.get():
        # En caso de cerrar ventana
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Click con el mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Permitir al usuario pausar el juego si toca el boton de pausa
            if pause_button_rect.collidepoint(event.pos):
                is_paused = not is_paused
                if not is_paused:
                    pause_button_image = pause_image
                else:
                    pause_button_image = play_image
            

        # Si el juego está en pausa y Click con el mouse
        if is_paused and event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Permitir al usuario salvar el estado acutal de la matriz si toca el boton de salvar
            if save_button_rect.collidepoint(event.pos):
                saved_gameState   = np.copy(game.gameState)

            # Permitir al usuario recargue la posición guardada
            if reload_button_rect.collidepoint(event.pos):
                game.gameState = np.copy(saved_gameState)
            
            # Permitir que el usuario genere un estado aleatorio
            if random_button_rect.collidepoint(event.pos):
                random_gameState = np.random.binomial(1, 0.2, (No_x_cel, No_y_cel))
                game.gameState = np.copy(random_gameState)

            # Permitir al usuario modificar la matriz de juego
            if (pos[0] > 10 and pos[0]<=590) & (pos[1]>10 and pos[1]<590):
                x, y = int((pos[0]-10) // cel_width), int((pos[1]-10) // cel_heigth)
                if x < No_x_cel and y < No_y_cel:
                    game.gameState[x, y] = 1 - game.gameState[x, y]

            # Permitir al usuario cambiar el tipo de vecindad
            if neighborhood_button_rect.collidepoint(event.pos):
                if neighborhood == "Moore":
                    neighborhood       = "Neumann"
                    neighborhood_image = neumann_image
                    game.neighborhood  = "Neumann"
                elif neighborhood == "Neumann":
                    neighborhood       = "Moore"
                    neighborhood_image = moore_image
                    game.neighborhood    = "Moore"

    # Dibujar el botón de pausa
    pause_button_rect  = pygame.Rect(605, 30, pause_button_size, pause_button_size)

    # Dibujar el boton de salvar
    save_button_rect  = pygame.Rect(665-20, 20, save_button_size, save_button_size)

    # Dibujar boton de reload 
    reload_button_rect  = pygame.Rect(665+40, 30, reload_button_size, reload_button_size)

    # Dibujar boton de random
    random_button_rect  = pygame.Rect(665+80, 30, random_button_size, random_button_size)

    # Dibujar el botón de Vecindad
    neighborhood_button_rect  = pygame.Rect(645, 150, neighborhood_button_size, neighborhood_button_size)

    if not is_paused:
        game.update()
        game.draw(screen=game_surface, cel_heigth=cel_heigth, cel_width=cel_width)
    else:
        game.draw(screen=game_surface, cel_heigth=cel_heigth, cel_width=cel_width)

    # Actualizar la pantalla
    screen.fill(WHITE)
    screen.blit(game_surface, (10, 10))
    screen.blit(control_surface, (600, 10))
    screen.blit(pause_button_image, pause_button_rect)
    screen.blit(save_button_image, save_button_rect)
    screen.blit(reload_button_image, reload_button_rect)
    screen.blit(random_button_image, random_button_rect)
    screen.blit(neighborhood_image, neighborhood_button_rect)    
    

    pygame.display.update()
    clock.tick(10)
