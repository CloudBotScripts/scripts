from time import sleep
from datetime import datetime

## Options
hours_leave = [9, 10]
skill_train = 'club'

## Cap to leave
cap_leave = 30

## Mana potions to take
take_mana = 10
mana_leave = 5
mana_name = 'mana potion'
depot_mana_potions = 3
hotkey_mana_potions = 4

# Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *

persistent_actions = [{'interval':60, 'action':eat_food}]

def waypoint_action(client, action):
    if action == "start":
      print('Bot started')

    elif action == "debug":
        client.jump_label('debug')

    elif action == "buy_rake":
        client.buy_items_from_npc(['rake'], [1])

    elif action == "travel_abdendriel":
        client.npc_say(["ab'dendriel", 'yes'])

    elif action == "buy_poem":
        client.npc_say(["love poem", 'yes'])

    elif action == "travel_venore":
        client.npc_say(["venore", 'yes'])

    elif action == "travel_liberty_bay":
        client.npc_say(["liberty bay", 'yes'])

    elif action == "ring":
        client.npc_say(["ring", 'yes'])

    elif action == "levitate_up_north":
        levitate(client, 'north', '=')

    elif action == "levitate_down_south":
        levitate(client, 'south', '-')

    elif action == "use_rake_north":
        container = client.get_container('Backpack')
        if container is False:
            client.logout()
        client.use_slot(container, 1)
        sleep(0.2)
        client.click_sqm(0, 1)
        sleep(0.2)

    elif action == "give_ring":
        client.npc_say(["ring", 'yes', 'yes', 'yes'])

    elif action == "errand":
        client.npc_say(["errand", 'yes'])

    elif action == "peg_leg":
        client.npc_say(["errand", 'peg leg', 'yes'])

    elif action == "travel_meriana":
        client.npc_say(['peg leg', 'yes'])

    elif action == "raymond":
        client.npc_say(['eleonore', 'mermaid'])

    elif action == "mermaid":
        client.npc_say(['raymond striker'])

    elif action == "djinn":
        client.npc_say(['eleonore', 'mermaid', 'date', 'yes'])

    elif action == "mermaid2":
        client.npc_say(['date'])

    elif action == "djinn2":
        client.npc_say(['mermaid', 'love poem', 'yes'])


    elif action == "finish":
        client.npc_say(['raymond striker', 'mermaid'])

    elif action == "end":
        client.logout()

    else:
        print('Action', action, 'is not defined')
