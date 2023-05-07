import pygame
import sys
from Policy import Policy
from time import sleep

class Maze:
    points = 0 # Points the agents earns

    # Define the size of the grid and the size of each cell
    num_rows = 0
    num_cols = 0
    cell_size = 0

    # Define the colors to use for elements in the maze
    wall_color = (0, 0, 0)
    empty_color = (255, 255, 255)
    water_color = (0,191,255)
    enemy_color = (220,20,60)

    reward_color = (0,250,154)

    # Images for objects 
    tile_image = pygame.image.load('images/tile.png')
    agent_image = pygame.image.load('images/agent.png')
    water_image = pygame.image.load('images/water_tile.png')   
    enemy_image = pygame.image.load('images/enemy.png')

    finish_flags_image = pygame.image.load('images/finish_flags.png')
    finish_line_image = pygame.image.load('images/finish_line.png')

    # Variables for the pygame screen
    width = 0
    height = 0
    screen = None
    font = None # Font of text on cells
    small_font = None

    maze = []
    
    # Define the starting position of the agent
    default_agent_row, default_agent_col = 4,3
    agent_row, agent_col = default_agent_row, default_agent_col

    policy = Policy()

    def __init__(self, num_rows=6, num_cols=6, cell_size=150):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size = cell_size

        # Generate 2D list of maze
        for i in range(num_rows):
            row = []
            for j in range(num_cols):
                # Outer wall cells
                if i == 0 or i == num_rows - 1 or j == 0 or j == num_cols - 1:
                    row.append({"id":1, "reward":-999, "terminal":None, "value":0})
                else:
                    # Empty cells
                    # Contains the following: [cell ID, reward, Terminal, state value]
                    # The contents are updated
                    row.append({"id":0, "reward":-1, "terminal":False, "value":0})
            self.maze.append(row)

        # Water
        self.maze[2][4]["id"] = 2 # Edit grid cell ID. 2 = water
        self.maze[2][3]["id"] = 2
        self.maze[2][4]["reward"] = -10
        self.maze[2][3]["reward"] = -10

        # Enemy
        self.maze[4][2]["id"] = 3 # Edit grid cell ID. 3 = enemy
        self.maze[4][2]["reward"] = -2

        # Finish lines
        self.maze[4][1]["id"] = 4 # Edit grid cell ID. 4 = 1st finish with +10 score
        self.maze[1][4]["id"] = 5 # Edit grid cell ID. 5 = 2nd finish with +40 score
        self.maze[4][1]["reward"] = 10 
        self.maze[1][4]["reward"] = 40
        self.maze[4][1]["terminal"] = True
        self.maze[1][4]["terminal"] = True

        # Create the Pygame window
        self.width = num_cols * cell_size
        self.height = num_rows * cell_size
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Grid-Based Maze')

        # Set fonts for texts that will show on Pygame
        self.font = pygame.font.SysFont('Arial', 22)
        self.small_font = pygame.font.SysFont('Arial', 16)


    def generate_object(self, x, y, image, size=1.0):

        """
        Generate objects and show them on the Pygame screen.

        :param x: x-coordinate of the object's top-left corner
        :param y: y-coordinate of the object's top-left corner
        :param image: image of the object to be displayed
        :param size: size of the object (default: 1/full size)
        """

        center = (x + self.cell_size // 2, y + self.cell_size // 2)
        image = pygame.transform.scale(image, (self.cell_size * size, self.cell_size * size))
        image_rect = image.get_rect()
        image_rect.center = center
        self.screen.blit(image, image_rect)           


    def draw_maze(self, run=False, exploration_rate=False):
        """
        Draws the maze in the game window with different elements such as cells, walls, water, enemies, finish flags, and finish line.
        Also, it generates the lines between the cells to create a roster, draws reward at each state, and visualizes the points.
        """
        for row in range(self.num_rows):
            for col in range(self.num_rows):
                x = col * self.cell_size
                y = row * self.cell_size
                if self.maze[row][col]["id"] == 0:
                    # Generate normal grid cells
                    self.generate_object(x, y, self.tile_image)                 
                if self.maze[row][col]["id"] == 1:
                    # Generate black walls on outer edges
                    pygame.draw.rect(self.screen, self.wall_color, (x, y, self.cell_size, self.cell_size))
                if self.maze[row][col]["id"] == 2: 
                    # Generate water on grid cell
                    self.generate_object(x, y, self.water_image)
                if self.maze[row][col]["id"] == 3:
                    # Generate normal grid cell and enemy ontop
                    self.generate_object(x, y, self.tile_image) 
                    self.generate_object(x, y, self.enemy_image, 0.8)
                if self.maze[row][col]["id"] == 4:
                    # Generate normal grid cell and finish flags on top
                    self.generate_object(x, y, self.tile_image) 
                    self.generate_object(x, y, self.finish_flags_image, 0.6)
                if self.maze[row][col]["id"] == 5:
                    # Generate normal grid cell and finish line on top
                    self.generate_object(x, y, self.tile_image) 
                    self.generate_object(x, y, self.finish_line_image)

                # Draw lines between grid cells, to create a roster
                pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x + self.cell_size, y), 2)
                pygame.draw.line(self.screen, (0, 0, 0), (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)
                pygame.draw.line(self.screen, (0, 0, 0), (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 2)
                pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x, y + self.cell_size), 2)

                # Visualize the reward and the value of the state
                self.visualize_state_utilities(row, col)

        # Visualization of the amount of points gathered
        self.visualize_points()
        
        if run:
            self.visualize_run(run)

        if exploration_rate:
            self.visualize_exploration_rate(exploration_rate) 

        # Update display
        pygame.display.update()       


    def visualize_state_utilities(self, row, col):
        """
        Visualize the state value and reward of a non-wall state in the maze.
        """
        x = col * self.cell_size
        y = row * self.cell_size
        
        # Draw reward and state value at each state
        if self.maze[row][col]["id"] != 1:
            reward = self.maze[row][col]["reward"]
            text = self.small_font.render(str(reward), True, (50,205,50))
            text_rect = text.get_rect(center=(x+self.cell_size//7, y+self.cell_size//7))
            self.screen.blit(text, text_rect)

            value = self.maze[row][col]["value"]
            text = self.font.render("V = "+str(value), True, self.reward_color)
            text_rect = text.get_rect(center=(x+self.cell_size//2, y+self.cell_size//2))
            self.screen.blit(text, text_rect)


    def visualize_points(self):
        """
        Display number representing the points earned
        """       
        text = self.font.render("Points: " + str(self.points), True, (0,255,127))
        text_rect = text.get_rect(center=(0+self.cell_size//2, 0+self.cell_size//2))
        self.screen.blit(text, text_rect)
    

    def visualize_run(self, run):
        """
        Display number representing the current r un
        """        
        # Visualization of the amount of points gathered
        text = self.font.render("Run: " + str(run), True, (138,43,226))
        text_rect = text.get_rect(center=(self.cell_size//2, 0.2*self.cell_size+self.cell_size//2))
        self.screen.blit(text, text_rect)      


    def visualize_convergence(self):
        """
        Display text that notifies if convergence has been reached
        """
        message = "Reached convergence! Showing optimal route"
        text = self.font.render(message, True, (138,43,226))
        text_rect = text.get_rect(center=(self.num_cols/2.4*self.cell_size+self.cell_size//2, 0+self.cell_size//2))
        self.screen.blit(text, text_rect)

        # Update display
        pygame.display.update()

    def visualize_exploration_rate(self, exploration_rate):
        """
       Display number representing the exploration rate
        """
        text = self.font.render("Exploration rate: " + str(exploration_rate), True, (138,43,226))
        text_rect = text.get_rect(center=((self.num_cols-1.5)*self.cell_size+self.cell_size//2, \
                                          0.4*self.cell_size+self.cell_size//2))
        self.screen.blit(text, text_rect)

        # Update display
        pygame.display.update()        

    
    def generate_agent(self):
        """
        Generate the agent on the maze
        """
        x = self.agent_col * self.cell_size
        y = self.agent_row * self.cell_size

        center = (x + self.cell_size // 2, y + self.cell_size // 2)
        image = pygame.transform.scale(self.agent_image, (self.cell_size//2, self.cell_size//1.9))
        image_rect = image.get_rect()
        image_rect.center = center
        self.screen.blit(image, image_rect)

        # Update the display
        pygame.display.update()        


    def generate_maze(self, reset=False, run=False, exploration_rate=False):
        """
        Generates and displays the maze and the agent.

        :param reset: a boolean indicating whether to reset the agent position and points earned
        :param run: None or a number representing the current run
        """        
        if reset:
            self.agent_row, self.agent_col = self.default_agent_row, self.default_agent_col
            self.points = 0
        self.draw_maze(run, exploration_rate)
        self.generate_agent()
        
 

    def is_valid_move(self, row, col):
        """
        Check if move doesn't cause agent to collide with wall, otherwise agents stays on same state.
        """
        return self.maze[row][col]["id"] != 1


    def shut_down(self):
        pygame.quit()
        sys.exit()
    

    def update_values(self):
        max_value, _ = self.policy.select_action(self)
        
        x, y = self.agent_row, self.agent_col             
        if self.maze[x][y]["terminal"] == False:
            self.maze[x][y]["value"] = max_value         


    def step(self, action, convergence=False):
        """
        Perform one step in the maze by taking the given action and updating the agent's position.
        Also updates the amount of points. In case convergence has been reached, this is displayed.

        :param action: The action to take (0 = left, 1 = right, 2 = up, 3 = down)
        :param convergence: A flag indicating if this step is part of convergence testing
        """        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f"Terminating game. Total points: {self.points}!")
                self.shut_down()
        if action == 0 and self.is_valid_move(self.agent_row, self.agent_col - 1):  # Move left
            self.agent_col -= 1
            # print("Moved left")
        elif action == 1 and self.is_valid_move(self.agent_row, self.agent_col + 1):  # Move right
            self.agent_col += 1
            # print("Moved right")
        elif action == 2 and self.is_valid_move(self.agent_row - 1, self.agent_col):  # Move up
            self.agent_row -= 1
            # print("Moved up")
        elif action == 3 and self.is_valid_move(self.agent_row + 1, self.agent_col):  # Move down
            self.agent_row += 1       
            # print("Moved down")

        # Update points with the gained reward
        reward = self.maze[self.agent_row][self.agent_col]["reward"]
        self.points += reward
        # print(f"Gained reward of {reward} points\n")

        if convergence:
            self.visualize_convergence()

        # End program if convergence and we reach terminal state
        if convergence and self.maze[self.agent_row][self.agent_col]["terminal"] == True:
            print(f"Reached finish line with total points of {self.points}!")
            self.generate_maze()
            sleep(3)
            self.shut_down()


    # For manual testing of the game using keyboard |w,a,s,d| or |up,down,left,right| keys
    def manual_play(self):
        """
        This function allows for manual testing of the game.
        This is done using keyboard keys |w,a,s,d| or |up,down,left,right| to move the agent in the maze. 
        """
        self.generate_maze()
        while True:
            for event in pygame.event.get():
                legal_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, 
                            pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
                self.update_values()

                if event.type == pygame.QUIT:
                    print(f"Terminating game. Total points: {self.points}!")
                    self.shut_down()
                elif event.type == pygame.KEYDOWN and event.key in legal_keys:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.is_valid_move(self.agent_row - 1,self.agent_col):
                            self.agent_row -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if self.is_valid_move(self.agent_row + 1,self.agent_col):
                            self.agent_row += 1
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.is_valid_move(self.agent_row,self.agent_col - 1):
                            self.agent_col -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.is_valid_move(self.agent_row,self.agent_col + 1):
                            self.agent_col += 1  

                    # Update points with the reward
                    reward = self.maze[self.agent_row][self.agent_col]["reward"]
                    self.points += reward
                    print(f"Gained reward of {reward} points")

                    # Clear the screen and update the maze and agent position
                    self.generate_maze()

                    # If terminal state reached
                    if self.maze[self.agent_row][self.agent_col]["terminal"] == True:
                        print(f"Reached finish line with total points of {self.points}!")
                        # self.shut_down()