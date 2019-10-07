#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "refill":
        # No stash for free acc
        pass

    elif action == "buy_potions":
        npc_refill(client, mana=True, health=True)

    elif action == "check_time":
        check_time(client, 'exit', 'start')

    elif action == "check_floor":
        check_hunt(client, 'upper', 'skip_floor', other=client.script_options['upper_level'])

    elif action == "check_lower":
        check_hunt(client, 'lower', 'skip_lower', other=client.script_options['lower_level'])

    else:
        global_actions.waypoint_action(client, action)
