import numpy as np
import pygame_gui
import pygame

# Define colors as constants
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BACKGROUND_COLOR = (200, 200, 255)

def sum_neighbours_torus(gameState: np.ndarray, x: int, y: int, neighborhood: str = "Moore") -> int:
    """
    Calculates the sum of values of neighboring cells using a toroidal topology.

    Args:
        gameState (np.ndarray): matrix representing the current state of the game.
        x (int): x-coordinate of the current cell.
        y (int): y-coordinate of the current cell.

    Returns:
        int: the sum of values of neighboring cells.
    """
    # Get the dimensions of the gameState matrix
    No_x_cel, No_y_cel = gameState.shape
    
    # Initialize the sum of neighbors to zero
    sum = 0
    sum_neuman_diff = 0
    
    # Sum the values of neighbors around cell [x, y]
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Calculate the indices of the neighboring cell using the modulo operator
            neighbour_x = (x + i) % No_x_cel
            neighbour_y = (y + j) % No_y_cel
            
            # Add the value of the neighboring cell to the sum variable
            sum += gameState[neighbour_x, neighbour_y]
            if abs(i) == abs(j):
                sum_neuman_diff += gameState[neighbour_x, neighbour_y]
    
    # Subtract the value of cell [x, y] from the total sum of neighbors
    sum -= gameState[x, y]
    
    if neighborhood == "Neumann":
        return sum - sum_neuman_diff
    else:
        return sum

def get_game_params():
    pygame.init()

    # Define window parameters
    WINDOW_SIZE = (400, 300)
    BG_COLOR = (255, 255, 255)

    # Create the window
    pygame.display.set_caption("Conway's Game of Life")
    window_surface = pygame.display.set_mode(WINDOW_SIZE)

    # Create the GUI event manager
    ui_manager = pygame_gui.UIManager(WINDOW_SIZE)

    # Create text input elements
    x_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((100, 50), (200, 50)),
        manager=ui_manager
    )

    y_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((100, 120), (200, 50)),
        manager=ui_manager
    )

    # Create the "Accept" button
    ok_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((150, 200), (100, 50)),
        text="Accept",
        manager=ui_manager
    )

    # Create the text
    font = pygame.font.Font(None, 30)
    text = font.render("Select Game Size", True, (0, 0, 0))
    text_rect = text.get_rect(center=(200, 30))

    # Main window loop
    is_running = True
    clock = pygame.time.Clock()

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == ok_button:
                        # Get input values
                        try:
                            No_x_cel = int(x_input.get_text())
                            No_y_cel = int(y_input.get_text())
                            return No_x_cel, No_y_cel
                        except ValueError:
                            print("Error: Enter valid integers")
            ui_manager.process_events(event)

        ui_manager.update(time_delta)

        window_surface.fill(BG_COLOR)

        window_surface.blit(text, text_rect)
        
        ui_manager.draw_ui(window_surface)

        pygame.display.update()

    pygame.quit()
    return No_x_cel, No_y_cel

class GameOfLife:
    def __init__(self, initGameState: np.ndarray) -> None:
        """
        Initializes the Game of Life.

        Args:
            initGameState (np.ndarray): matrix representing the initial state of the game.
        """
        self.gameState    = initGameState
        self.h_size       = initGameState.shape[0]
        self.v_size       = initGameState.shape[1]
        self.neighborhood = "Moore"

    def update(self):
        """
        Updates the game state using the rules of the Game of Life.
        """
        newgameState = np.copy(self.gameState)

        for y in range(0, self.h_size):
            for x in range(0, self.v_size):      
                # States
                n_neigh = sum_neighbours_torus(self.gameState, x, y, neighborhood=self.neighborhood)
                
                # Rule 1: If you are dead and have 3 live neighbors: You live!
                if (self.gameState[x,y] == 0  and n_neigh == 3):
                    newgameState[x,y] = 1

                # Rule 2: If you are alive and have fewer than two neighbors: you die of loneliness
                if (self.gameState[x,y] == 1  and n_neigh < 2):
                    newgameState[x,y] = 0

                # Rule 3: If you are alive and have more than 3 neighbors you die from overpopulation
                if (self.gameState[x,y] == 1  and n_neigh > 3):
                    newgameState[x,y] = 0
        
        self.gameState = newgameState

    def draw(self, screen, cel_width, cel_heigth):
        """
        Draws the current state of the game on the screen.

        Args:
        screen (pygame.Surface): the screen surface on which the game will be drawn.
        cel_width (int): the width of each cell.
        cel_height (int): the height of each cell.
        """

        screen.fill(BACKGROUND_COLOR)

        for y in range(0, self.h_size):
            for x in range(0, self.v_size):
                # Cells
                poly = [((x)    * cel_width , y     * cel_heigth),
                        ((x+1)  * cel_width , y     * cel_heigth),
                        ((x+1)  * cel_width , (y+1) * cel_heigth),
                        ((x)    * cel_width , (y+1) * cel_heigth)]
                
                if self.gameState[x,y] == 0:
                    pygame.draw.polygon(screen, RED , poly, 1)
                else:
                    pygame.draw.polygon(screen, BLUE, poly, 0)
                    pygame.draw.polygon(screen, RED , poly, 1)
