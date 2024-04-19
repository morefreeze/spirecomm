import logging

from neuralNet.dataConverter import *
from spirecomm.communication.action import *
from spirecomm.spire.game import Game


class NeuralNetInteractor:

    def __init__(self):
        pass

    def __run_combat_in_NN(self, nnCombatIpnut: str) -> str:
        # This is where you will run LLM
        return ""

    def run_combat(self, gameState: Game, priorities) -> Action:
        next_action = game_state_to_action(gameState, priorities)

        return next_action
