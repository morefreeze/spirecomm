import itertools
import datetime
import sys
<<<<<<< HEAD
<<<<<<< Updated upstream
=======
import random
import time
import os
>>>>>>> Stashed changes
=======
import random
import time
>>>>>>> 8c3cae8a3f11ae851ae8e30525126757edb61686

from spirecomm.communication.coordinator import Coordinator
from spirecomm.ai.agent import SimpleAgent
from spirecomm.ai.randomAgent import RandomAgent
from spirecomm.spire.character import PlayerClass


if __name__ == "__main__":
    agent = SimpleAgent()
    coordinator = Coordinator()
    coordinator.signal_ready()
    coordinator.register_command_error_callback(agent.handle_error)
    coordinator.register_state_change_callback(agent.get_next_action_in_game)
    coordinator.register_out_of_game_callback(agent.get_next_action_out_of_game)

    # We're running an AI, it doesn't make sense to play anything other than defect
    chosen_class = PlayerClass.DEFECT
    agent.change_class(chosen_class)
    while True:
        # result = coordinator.play_one_game(chosen_class)

        seed = str(int(time.time()))
        save_name = str(int(time.time()))
        random.seed(seed)
        # Quick and dirty grab of run files for a given ascension
        # We assume that we're in the SlayTheSpire game folder

        repo_base = os.path.join(os.getcwd(), "..")
        game_path = os.path.join(repo_base, "SlayTheSpire")
        mod_path = os.path.join(repo_base, "Mods/spirecomm")

        # print(game_path, mod_path)

        # We are located in the SlayTheSpire directory by default
        runs_path_relative = "runs/1_DEFECT"
        game_runs_path = os.path.join(game_path, runs_path_relative)

        mod_runs_path = os.path.join(mod_path, "runs")
        local_runs_path = os.path.join(mod_runs_path, save_name + "-" + seed)

        try:
            os.mkdir(mod_runs_path)
        except FileExistsError:
            pass

        try:
            os.mkdir(local_runs_path)
        except FileExistsError:
            pass

        results = coordinator.climb_till_defeat(chosen_class, seed, save_name)

        run_files = os.listdir(game_runs_path)

        run_files.sort()
        run_file_names = run_files[-len(results):]

        try:
            for file in run_file_names:
                with open(os.path.join(game_runs_path, file), "r") as source_data:
                    with open(os.path.join(local_runs_path, file), "w") as dest_data:
                        dest_data.write(source_data.read())
        except OSError:
            pass

