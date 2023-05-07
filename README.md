The project consists of a maze game with an agent that learns to navigate the maze and reach the goal using reinforcement learning.

- **Maze**: This class is responsible for initializing the maze and updating it based on the actions taken by the agent.
- **Agent**: The Agent class creates an agent to navigate a maze and optimize its actions. It includes methods for the agent to act, generate exploration rate, track value changes, and play autonomously.
- **Policy**: This class is responsible for selecting actions for the agent based on the current state of the maze using an epsilon-greedy algorithm with a specified exploration rate.

In the **main class**, the agent class is imported. There it can be used for either autonomous play using reinforcement learning, or manual play to test the maze.

<br>
In this video demo, the simulation is demonstrated.

<a href="https://github.com/ayoub-z/Maze-solver/blob/master/Maze%20simulation.mp4"><img src="https://github.com/ayoub-z/Maze-solver/blob/master/images/demo_image.png" alt="alt text" width="300"/></a>
