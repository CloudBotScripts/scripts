#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "check_down_1":
        if not client.script_options['hunt_down']:
            client.jump_label('skip_down_1')

    elif action == "check_down_2":
        if not client.script_options['hunt_down']:
            client.jump_label('skip_down_2')

    elif action == "check2":
        check_hunt(client, 'continue', 'leave', time=True)

    else:
        global_actions.waypoint_action(client, action)
