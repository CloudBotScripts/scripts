import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "check_teleport":
        check_hunt(client, 'continue', 'skip_teleport', ammo='ammo_name' in client.hunt_config.keys(), time=True)

    else:
        global_actions.waypoint_action(client, action)
