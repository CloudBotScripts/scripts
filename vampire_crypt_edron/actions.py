#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "refill_avalanche":
        rune_name, take_rune = client.hunt_config['rune_name'], client.hunt_config['take_rune']
        if not withdraw_item_from_stash(client, rune_name, take_rune, client.items[rune_name]): 
            print('Not enough runes')
            client.logout()

    else:
        global_actions.waypoint_action(client, action)
