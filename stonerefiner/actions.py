#Load Custom functions
from lib import *
sys.path.append('../scripts/')
import global_actions

def waypoint_action(client, action):
    if action == "check_soft":
        use_soft_boots = client.script_options.get('use_soft_boots', False)
        if use_soft_boots:
            client.jump_label('go_soft')
        else:
            client.jump_label('skip_soft')
    elif action == "fix_soft":
        client.npc_say(['soft', 'yes'])
    else:
        global_actions.waypoint_action(client, action)
