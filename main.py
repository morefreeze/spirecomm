import itertools
import datetime
import sys
import random
import time

from spirecomm.communication.coordinator import Coordinator
from spirecomm.ai.agent import SimpleAgent
from spirecomm.ai.randomAgent import RandomAgent
from spirecomm.spire.character import PlayerClass


if __name__ == "__main__":
    seed = str(int(time.time()))
    save_name = str(int(time.time()))
    random.seed(seed)
    agent = SimpleAgent()
    coordinator = Coordinator()
    coordinator.signal_ready()
    coordinator.register_command_error_callback(agent.handle_error)
    coordinator.register_state_change_callback(agent.get_next_action_in_game)
    coordinator.register_out_of_game_callback(agent.get_next_action_out_of_game)

    # We're running an AI, it doesn't make sense to play anything other than defect
    chosen_class = PlayerClass.DEFECT
    agent.change_class(chosen_class)
    # result = coordinator.play_one_game(chosen_class)
    result = coordinator.climb_till_defeat(chosen_class, seed, save_name)
