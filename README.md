# Maze Solver
The project consists of a maze game with an agent that learns to navigate the maze and reach the goal using reinforcement learning.

- **Maze**: This class is responsible for initializing the maze and updating it based on the actions taken by the agent.
- **Agent**: The Agent class creates an agent to navigate a maze and optimize its actions. It includes methods for the agent to act, generate exploration rate, track value changes, and play autonomously.
- **Policy**: This class is responsible for selecting actions for the agent based on the current state of the maze using an epsilon-greedy algorithm with a specified exploration rate.
<br>

### Initializing
In the **main class**, the agent class is imported. There it can be used for either autonomous play using reinforcement learning, or manual play to test the maze.
<br>

### Probability
The maze can be a stochastic environment, using the `probability` parameter. If set on 0.7, it means there's only a 70% chance the agent will actually take said action. <br> 
This means that in an MDP maze simulation, the agent may not always move to the intended next state, but may instead move to another state with some probability. This can be useful for avoiding getting stuck in a suboptimal terminal state and instead exploring more of the maze to potentially find a better terminal state. By incorporating stochasticity into the agent's actions, it has more opportunity to explore states that can be very useful to uncover.
<br>

### Exploration
I've noticed that adding a lot of exploration at the start can be very useful in speeding up convergence. For that reason there's also a parameter for exploration priority, `exploration_rate_decay_factor`. The exploration_rate_decay_factor is another parameter in the Agent class which determines the exploration priority. This parameter can be set between 0 and 5 (or higher). A higher value (e.g. 5) indicates a higher amount of exploration and will only slow down much later, when most states have been uncovered, which can help the agent discover more states and improve its performance. A lower value (e.g. 0) means that the agent will prioritize exploitation of the already known states rather than exploring new ones.

### Demo
In this video demo, the simulation is demonstrated.

<a href="https://github.com/ayoub-z/Maze-solver/blob/master/Maze%20simulation.mp4"><img src="https://github.com/ayoub-z/Maze-solver/blob/master/images/demo_image.png" alt="alt text" width="300"/></a>
