import logging
import random
import time

from neuralNet.interactor import NeuralNetInteractor
from spirecomm.ai.agent import Agent
from spirecomm.ai.priorities import *
from spirecomm.communication.action import *
from spirecomm.spire.card import Card
from spirecomm.spire.character import Intent, Monster, PlayerClass
from spirecomm.spire.game import Game
from spirecomm.spire.potion import Potion
from spirecomm.spire.relic import Relic
from spirecomm.spire.screen import RestOption
from utilities.scraping import Scraper


class NnAgent(Agent):
    def __init__(self, chosen_class=PlayerClass.THE_SILENT):
        self.interactor = NeuralNetInteractor()
        self.scraper = Scraper(chosen_class)
        super().__init__(chosen_class)

    def change_class(self, chosen_class: PlayerClass):
        self.scraper.change_class(chosen_class)
        return super().change_class(chosen_class)

    def get_next_combat_action(self):
        self.scraper.scrape_state(self.game)
        game_state = self.game
        priorities = self.priorities
        return super().get_next_combat_action()
    
        # Auto use potions on boss for now...
        if (
            self.game.room_type == "MonsterRoomBoss"
            and len(self.game.get_real_potions()) > 0
        ):
            potion_action = self.__use_next_potion()
            if potion_action is not None:
                return potion_action

        logging.info("Getting next game action for llm")
        logging.debug("Using state: " + str(game_state))
        return self.interactor.run_combat(game_state, priorities)

    def __use_next_potion(self):
        for potion in self.game.get_real_potions():
            if potion.can_use:
                if potion.requires_target:
                    return PotionAction(
                        True, potion=potion, target_monster=self.__get_low_hp_target()
                    )
                else:
                    return PotionAction(True, potion=potion)

    def get_card_reward_action(self):
        self.scraper.scrape_state(self.game)
        return super().get_card_reward_action()

    def get_rest_action(self):
        self.scraper.scrape_state(self.game)
        return super().get_rest_action()

    def get_screen_action(self):
        self.scraper.scrape_state(self.game)
        return super().get_screen_action()

    def get_map_choice_action(self):
        self.scraper.scrape_state(self.game)
        return super().get_map_choice_action()

    def get_next_combat_reward_action(self):
        self.scraper.scrape_state(self.game)
        return super().get_next_combat_reward_action()

    def get_next_boss_reward_action(self):
        self.scraper.scrape_state(self.game)
        return super().get_next_boss_reward_action()
