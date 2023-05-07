from Maze import Maze
from Policy import Policy
from time import sleep
import math

class Agent():

    maze = None
    policy = Policy()
    sleep_t = 0 # To add delay when visualizing maze
    epsilon = 0.01

    num_rows = 6
    num_cols = 6
    cell_size = 150


    def __init__(self, num_rows=6, num_cols=6, cell_size=150):

        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size = cell_size


    def set_sleep(self, sleep):
        self.sleep_t = sleep


    def act(self, best_action, convergence=False):
        self.maze.step(best_action, convergence)


    def get_exploration_rate(self, value_changes_list, decay_factor):
        """
        Calculates the exploration rate based on the number of unoptimal states. 
        The exploration rate starts at 1.0 and gradually decays as the agent learns 
        to navigate the maze more efficiently.

        :param: value_changes_list (list): A list of value changes that keeps track up the latest updated value change.

        :return: float: The exploration rate, between 0 and 1.
        """

        flattened_value_changes = [item for sublist in value_changes_list for item in sublist]
        total_num_states = (self.maze.num_rows-2) * (self.maze.num_cols-2)
        unoptimal_states = len([value_change for value_change in flattened_value_changes if value_change != 0])
        max_exploration_rate = 1.0
        k = decay_factor  # decay factor

        x = unoptimal_states / total_num_states
        exploration_rate = 1 - max_exploration_rate * pow(math.e, -k * x)

        # Drop the exploration rate drastically when the number of unoptimal states approaches 0
        if unoptimal_states == 0:
            exploration_rate = 0
        return exploration_rate
    
    def generate_value_changes_tracker(self):
        """
        Generate a 2D matrix, which is a copy of the maze, in which the last value change of each state is saved.
        The matrix contains 1's for each state that will be updated, and 0's for terminal states and outer walls that are ignored.
        :return: a 2D matrix of integers
        """        

        # Initialize value_changes with 1's for all states
        value_changes = [[1 for _ in range(self.num_cols)] for _ in range (self.num_rows)]

        # Set value changes of irrelevant states to 0, so they are ignored/seen as optimal states already.
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                # If it's a terminal state, mark it as irrelevant
                if self.maze.maze[i][j]["terminal"]:
                    value_changes[i][j] = 0
                # If it's just an outer wall, mark it as irrelevant
                if self.maze.maze[i][j]["id"] == 1:
                    value_changes[i][j] = 0
        return value_changes

    def autonomous_play(self, random_agent=False, probability=1, exploration_rate_decay_factor=5):
        """
        Play the game autonomously until convergence, where the maximum value change of all states 
        is below the threshold epsilon. The method will loop until convergence is achieved. 

        :param random_agent: a flag to control whether the agent takes random actions 
        :param probability: a value between 0 and 1 representing the probability of selecting the best action
        """

        # Create a new maze, reset convergence flag and run counter
        self.maze = Maze(self.num_rows,self.num_cols,self.cell_size)
        convergence = False
        run = 0

        # Create a 2D matrix to track changes in state values
        value_changes = self.generate_value_changes_tracker()

        while True: # Loop until convergence
            
            # Increment the run counter
            run += 1
            # Generate the visualization of the maze, reset agent position and points earned
            self.maze.generate_maze(reset=True, run=run)

            # Reset the delta, exploration rate
            delta = 0
            exploration_rate = self.get_exploration_rate(value_changes, exploration_rate_decay_factor)
            exploration_rate = round(exploration_rate, 2)

            # Visualize exploration_rate
            self.maze.visualize_exploration_rate(exploration_rate)
            sleep(0.5)

            while True: # Loop until terminal state

                # Current coordinates of agent
                x, y = self.maze.agent_row, self.maze.agent_col

                # Value of state we landed on
                v = self.maze.maze[x][y]["value"]
                self.maze.update_values()

                # Find best action from current state, and act it out
                _, best_action = self.policy.select_action(self.maze, probability, exploration_rate, random_agent)
                self.act(best_action, convergence)

                # Updated value of current state
                v_prime = self.maze.maze[x][y]["value"]
                # Record value change
                value_changes[x][y] = abs(v-v_prime)

                # Generate the new updated maze, where agent took best next action
                self.maze.generate_maze(run=run, exploration_rate=exploration_rate)

                # Visualize convergence
                if convergence:
                    self.maze.visualize_convergence()
                sleep(self.sleep_t)

                # End run if we land on a terminal state
                x_new, y_new = self.maze.agent_row, self.maze.agent_col
                if self.maze.maze[x_new][y_new]["terminal"] == True:
                    break

            # Update delta with biggest value change of all states
            flattened_value_changes = [item for sublist in value_changes for item in sublist]
            delta = max(flattened_value_changes)

            if delta < self.epsilon:
                # Set convergence flag to True and reset probability to 1
                convergence = True
                probability = 1

                # Visualize convergence and exploration rate
                self.maze.visualize_convergence()
                self.maze.visualize_exploration_rate(round(exploration_rate, 2))

                # Pause for 3 seconds, and set sleep between each step to 1
                sleep(3)
                self.set_sleep(1)

    def manual_play(self):
        self.maze = Maze(self.num_rows,self.num_cols,self.cell_size)
        self.maze.manual_play()