#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "lever":
        print('Check lever')
        status = client.reach_stand((33171,31897,8))
        print('status', status)
        sleep(3)
        cur_coord = client.minimap.get_current_coord() 
        if cur_coord != (33171,31897,8):
            status = client.use_ladder_at_coord((33172,31896,8))
            print('Use ladder:', status)
            status = client.reach_stand((33171,31897,8))
    else:
        global_actions.waypoint_action(client, action)
