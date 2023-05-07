import numpy as np

class Policy():

    def select_action(self, maze, probability=1.0, exploration_rate=0.0, random_agent=False):
        """
        Select an action for the agent based on the current state of the maze, 
        using an epsilon-greedy algorithm with a specified exploration rate.
        Exploration rate is a percentage, representing the chance of taking a random action to explore.

        :param maze: the current maze object
        :param probability: probability of selecting the best action based on value (default: 1.0)
        :param exploration_rate: probability of selecting a random action (default: 0.0)
        :param random_agent: whether or not the agent is random (default: False)
        :return: a tuple containing the value of the best next state, and the action towards that state
        """

        x, y = [maze.agent_row, maze.agent_col]

        values = np.zeros(4)
        for i, (dx, dy) in enumerate([(0,-1), (0,1), (-1,0), (1,0)]):
            next_value = maze.maze[x+dx][y+dy]["reward"] + maze.maze[x+dx][y+dy]["value"]
            values[i] = next_value

        max_value = max(values)

        if random_agent:
            # Take a random action
            next_action = np.random.choice([0, 1, 2, 3])
        else:
            if np.random.rand() < exploration_rate:
                # Take a random action
                next_action = np.random.choice([0, 1, 2, 3])
            else:
                # In case there are multiple best actions with equal values, 
                # put them all in list and pick random one
                max_indices = np.where(values == np.max(values))[0]

                # Pick best action of within probability
                if np.random.rand() < probability:
                    next_action = np.random.choice(max_indices)
                else:
                    # Take a random action, besides the best action
                    non_max_indices = [i for i in [0, 1, 2, 3] if i not in max_indices]
                    next_action = np.random.choice(non_max_indices)
        return max_value, next_action