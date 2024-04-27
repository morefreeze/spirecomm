import json
import logging

import boto3
from bs4 import ResultSet
from click import prompt
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # required, but unused
)

import spirecomm.spire.card
from spirecomm.ai.priorities import *
from spirecomm.communication.action import *
from spirecomm.spire.character import Intent, PlayerClass
from spirecomm.spire.game import Game

# import os
# os.environ['http_proxy'] = ''
# os.environ['https_proxy'] = ''
# # Setup bedrock
# bedrock_runtime = boto3.client(
#     service_name="bedrock-runtime",
#     region_name="us-east-1",
# )


def call_local_llm(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="llama2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    results = response.choices[0].message.content
    logging.debug(f"results: {results}")
    return results


def call_claude_haiku(system_prompt, user_prompt):

    prompt_config = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                ],
            }
        ],
    }

    body = json.dumps(prompt_config)

    modelId = "anthropic.claude-3-haiku-20240307-v1:0"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get("body").read())

    results = response_body.get("content")[0].get("text")
    return results


def get_valid_targets(targets):
    target_list = []
    for target in targets:
        target_list.append(target.monster_index)
    return target_list


def get_card_to_play(name, cards):
    for card in cards:
        if card.name.lower() == name.lower():
            return card
    return None


def parse_action_from_response(response):
    start_index = response.find("{")
    end_index = response.find("}", start_index)

    if start_index != -1 and end_index != -1:
        json_string = response[start_index : end_index + 1]
        try:
            action_data = json.loads(json_string)
            return action_data
        except json.JSONDecodeError:
            pass

    return None


def build_system_prompt(game_state):

    system_prompt = f"""
You are an expert Slay the Spire player. Your goal is to analyze the given game state and generate the optimal next action to take based on the available cards, player stats, and monster targets.

Use a clear, concise, and strategic tone in your responses. Provide explanations for your chosen action to demonstrate your reasoning.

Remember that Slay the Spire is a roguelike deck-building game where the player aims to ascend a spire by defeating monsters using a deck of cards. The player must make strategic decisions on which cards to play and which targets to attack while managing their health, energy, and other resources.

Here are some key points to keep in mind:

1. Analyze the provided game state, including the player's cards, stats, and the monster targets.
2. Consider factors such as minimizing incoming damage, optimizing energy usage, and prioritizing high-impact cards.
3. If incoming damage is 0 or less than 0, then lots foucs on attacking since we will not be hurt this turn.
4. If our block is greater than incoming damage, then we will not be hurt this turn, focus on attacking.
5. Generate the next action to take based on the game state.
6. For the action, specify the card name and, if applicable, the target monster's name and index.
7. Provide a brief explanation for the action, discussing your reasoning and strategy.

Here are some Examples:

<example 1>
I will be Defending to mitigate incoming damage
{{"action":"Defend"}}
</example 1>

<example 2>
I will be using the Vulnerable debuff on Acid Slime to increase future damage
{{"action": "Bash", "target_index":1}}
</example 2>

Here is the current game state:
<game_state>
{game_state}
</game_state>

Before generating the next action, break down your thought process into the following steps:

1. Assess the immediate threats and incoming damage.
2. Identify any high-priority targets or opportunities for synergy.
3. Consider the available energy and card costs.
4. Evaluate the long-term benefits and drawbacks of each potential action.
5. Generate the action with your explanation.

Here is how the output should be formated:

<output format>
(Explanation of your the actions you will take)

If targeting a monster, the format should be:
{{"action": "CARD_NAME", "target_index": MONSTER_INDEX}}

If not targeting a monster, the format should be:
{{"action": "CARD_NAME"}}

</output format>

Please generate the next action based on the provided game state, following the specified format and including your explanation for your action.
"""
    return system_prompt


def parse_powers(powers):

    power_list = []
    for power in powers:
        power_obj = {}
        power_obj["power_id"] = power.power_id
        power_obj["power_name"] = power.power_name
        power_obj["amount"] = power.amount
        power_obj["damage"] = power.damage
        power_obj["misc"] = power.misc
        power_obj["just_applied"] = power.just_applied
        power_obj["card"] = power.card
        power_list.append(power_obj)

    return power_list


def parse_potions(potions):
    potions_list = []
    # self.potion_id = potion_id
    # self.name = name
    # self.can_use = can_use
    # self.can_discard = can_discard
    # self.requires_target = requires_target
    # self.price = price
    for potion in potions:
        potion_obj = {}
        potion_obj["potion_id"] = potion.potion_id
        potion_obj["name"] = potion.name
        potion_obj["can_use"] = potion.can_use
        potion_obj["can_discard"] = potion.can_discard
        potion_obj["requires_target"] = potion.requires_target
        potion_obj["price"] = potion.price
        potions_list.append(potion_obj)
    return potions_list


def get_player_class(player_class):
    return PlayerClass[player_class]


def get_relics(relics):

    relic_list = []
    for relic in relics:
        relic_obj = {}
        relic_obj["relic_id"] = relic.relic_id
        relic_obj["name"] = relic.name
        relic_obj["counter"] = relic.counter
        relic_obj["price"] = relic.price
        relic_list.append(relic_obj)
    return relic_list


def get_player_stats(game):

    player_stats = {}
    player_stats["current_action"] = game.current_action
    player_stats["current_hp"] = game.current_hp
    player_stats["max_hp"] = game.max_hp
    player_stats["floor"] = game.floor
    player_stats["act"] = game.act
    player_stats["gold"] = game.gold
    player_stats["class"] = "IRONCLAD"  # TODO Hard coded
    player_stats["relics"] = get_relics(game.relics)
    player_stats["potions"] = parse_potions(game.potions)
    player_stats["block"] = game.player.block
    player_stats["energy"] = game.player.energy
    player_stats["orbs"] = game.player.orbs
    player_stats["powers"] = parse_powers(game.player.powers)

    return player_stats


def parse_cards(cards):
    card_list = []

    for card in cards:
        card_object = {}
        card_object["name"] = card.name
        card_object["cost"] = card.cost
        card_object["type"] = card.type
        card_object["rarity"] = card.rarity
        card_object["upgrades"] = card.upgrades
        card_object["has_target"] = card.has_target
        card_object["is_playable"] = card.is_playable
        card_object["exhausts"] = card.exhausts
        card_object["misc"] = card.misc
        card_object["price"] = card.price
        card_list.append(card_object)

    return card_list


def parse_monsters(monsters):
    monster_list = []

    for monster in monsters:
        monster_object = {}
        monster_object["name"] = monster.name
        monster_object["max_hp"] = monster.max_hp
        monster_object["current_hp"] = monster.current_hp
        monster_object["intent"] = monster.intent
        monster_object["is_gone"] = monster.is_gone
        monster_object["half_dead"] = monster.half_dead
        monster_object["move_id"] = monster.move_id
        monster_object["last_move_id"] = monster.last_move_id
        monster_object["second_last_move_id"] = monster.second_last_move_id
        monster_object["move_base_damage"] = monster.move_base_damage
        monster_object["move_adjusted_damage"] = monster.move_adjusted_damage
        monster_object["move_hits"] = monster.move_hits
        monster_object["monster_index"] = monster.monster_index
        monster_object["powers"] = parse_powers(monster.powers)
        monster_object["block"] = monster.block
        monster_list.append(monster_object)

    return monster_list


# Translate game state to NN readable format
def game_state_to_action(gameState: Game, priorities: Priority) -> str:
    # TODO will turn to something for a prompt
    playable_cards = [card for card in gameState.hand if card.is_playable]
    zero_cost_cards = [card for card in playable_cards if card.cost == 0]
    zero_cost_attacks = [card for card in zero_cost_cards if card.type == spirecomm.spire.card.CardType.ATTACK]
    zero_cost_non_attacks = [card for card in zero_cost_cards if card.type != spirecomm.spire.card.CardType.ATTACK]
    nonzero_cost_cards = [card for card in playable_cards if card.cost != 0]
    aoe_cards = [card for card in playable_cards if priorities.is_card_aoe(card)]

    available_monsters = [
        monster for monster in gameState.monsters if monster.current_hp > 0 and not monster.half_dead and not monster.is_gone
    ]

    incoming_damage = 0
    for monster in gameState.monsters:
        if not monster.is_gone and not monster.half_dead:
            if monster.move_adjusted_damage is not None:
                incoming_damage += monster.move_adjusted_damage * monster.move_hits
        elif monster.intent == Intent.NONE:
            incoming_damage += 5 * gameState.act

    # Can't do anything
    if len(playable_cards) == 0:
        return EndTurnAction()

    try:
        data_prompt = f"""
        Cards in your hands:
        <cards>
        Zero cost cards: {parse_cards(zero_cost_cards)}
        Zero cost attacks: {parse_cards(zero_cost_attacks)}
        Zero cost non-attacks: {parse_cards(zero_cost_non_attacks)}
        Non-zero cost cards: {parse_cards(nonzero_cost_cards)}   
        AOE cards: {parse_cards(aoe_cards)}
        </cards>

        Available monster targets: 
        <targets>
        {parse_monsters(available_monsters)}
        </targets>

        Incoming damage:
        <incoming_damage>
        {incoming_damage}
        </incoming_damage>

        Player Stats: 
        <player_stats>
        {get_player_stats(gameState)}
        </player_stats>
        """
        logging.info("Data Prompt:")
        logging.info(data_prompt)
    except Exception as e:
        logging.error(e)

    system_prompt = build_system_prompt(data_prompt)
    user_prompt = "Please generate the next action based on the provided game state, following the specified format and including your explanation for your action. I can only do one action at a time."

    # response = call_claude_haiku(system_prompt, user_prompt)
    response = call_local_llm(system_prompt, user_prompt)

    logging.info(f"LLM Response:\n{response}")

    # Return Action
    try:
        action = parse_action_from_response(response)
        card_name = action["action"]
        card_to_play = get_card_to_play(card_name, playable_cards)
        valid_targets = get_valid_targets(available_monsters)

        if "target_index" in action:
            target_index = action["target_index"]

            # check if can target with card
            if not card_to_play.has_target:
                return PlayCardAction(card=card_to_play)

            # Check if valid target
            if target_index not in valid_targets:
                target_index = valid_targets[0]

            return PlayCardAction(card=card_to_play, target_index=target_index)
        else:
            # check if card has a target
            if card_to_play.has_target:
                target_index = valid_targets[0]
                return PlayCardAction(card=card_to_play, target_index=target_index)

            return PlayCardAction(card=card_to_play)
    except Exception as e:
        logging.error(e)

    # Shouldn't get here...
    return EndTurnAction()


# Translate NN output format to readable game state
def NN_output_to_action(networkOutput: str) -> Action:
    return EndTurnAction()
