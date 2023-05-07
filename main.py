from Agent import Agent
from time import sleep
agent = Agent()

# Set sleep time between each step, for testing
agent.set_sleep(0.05)
sleep(2)
agent.autonomous_play(random_agent=False, probability=0.8, exploration_rate_decay_factor=5)
# agent.manual_play()