#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):

    if action == "check_hydras":
        if not client.script_options.get('hunt_hydras', False):
            client.jump_label('skip_hydras')

    else:
        global_actions.waypoint_action(client, action)
