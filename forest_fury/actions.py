#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "refill":
        # No stash for free acc
        pass

    elif action == "check_time":
        check_time(client, 'exit', 'start')

    elif action == "check_floor":
        check_hunt(client, 'upper', 'skip_floor', 
                mana='mana_name' in client.hunt_config.keys(),
                health='health_name' in client.hunt_config.keys(),
                rune='rune_name' in client.hunt_config.keys(), 
                ammo='ammo_name' in client.hunt_config.keys(), 
                other=client.script_options['upper_level'])

    elif action == "check_lower":
        check_hunt(client, 'lower', 'skip_lower', 
                mana='mana_name' in client.hunt_config.keys(),
                health='health_name' in client.hunt_config.keys(),
                rune='rune_name' in client.hunt_config.keys(), 
                ammo='ammo_name' in client.hunt_config.keys(), 
                other=client.script_options['lower_level'])

    else:
        global_actions.waypoint_action(client, action)
