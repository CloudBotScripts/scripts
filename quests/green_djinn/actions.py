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

    elif action == "talk_melfar":
        client.npc_say(["word of greeting", 'bye'])

    elif action == "talk_ubaid":
        client.npc_say(["DJANNI'HAH", 'passage', 'no', 'yes', 'yes'])

    elif action == "talk_baaleal":
        client.npc_say(["DJANNI'HAH", 'mission', 'yes'])

    elif action == "travel_venore":
        client.npc_say(["venore", 'yes'])

    elif action == "travel_carlin":
        client.npc_say(["carlin", 'yes'])

    elif action == "travel_thais":
        client.npc_say(["thais", 'yes'])

    elif action == "travel_abdendriel":
        client.npc_say(["ab'dendriel", 'yes'])

    elif action == "talk_shauna":
        client.npc_say(["job", 'water pipe', 'prisoner'])
        
    elif action == "talk_partos":
        client.npc_say(["prison", 'ankrahmun', 'supplies'])

    elif action == "travel_ankrahmun":
        client.npc_say(["ankrahmun", 'yes'])

    elif action == "talk_baaleal_2":
        client.npc_say(["DJANNI'HAH", 'mission', 'yes', 'partos', 'hail malor'])

    elif action == "talk_alesar":
        client.npc_say(["DJANNI'HAH", 'mission', 'yes'])

    elif action == "talk_malor":
        client.npc_say(["DJANNI'HAH", 'mission', 'yes'])

    elif action == "get_item":

        dest = client.get_container(client.container_conf['loot_bp'])
        if not dest:
            print('Could not find backpack to hold items')
        client.get_item_from_sqm((0,0), dest)

    elif action == "talk_orc":
        client.npc_say([])

    elif action == "talk_orc_2":
        client.npc_say(['hi', 'lamp', 'malor'])

    elif action == "end":
        client.logout()

    else:
        print('Action', action, 'is not defined')
