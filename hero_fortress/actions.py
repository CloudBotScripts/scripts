#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "check2":
        check_hunt(client, 'continue', 'leave2', time=True)

    else:
        global_actions.waypoint_action(client, action)
