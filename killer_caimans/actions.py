#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "use_elevator":
        client.use_lever((1, 0))
    elif action == "jump_travel_back":
        client.jump_label('travel_back')
    elif action == "jump_elevator_gohunt":
        client.jump_label('elevator_gohunt')
    elif action == "gohunt_14":
        conditional_jump_floor(client, 14, 'continue_gohunt_14', 'skip_gohunt_14')
    elif action == "gohunt_12":
        conditional_jump_floor(client, 12, 'continue_gohunt_12', 'gohunt_10')
    elif action == "back_14":
        conditional_jump_floor(client, 14, 'continue_back_14', 'skip_back_14')
    elif action == "back_12":
        conditional_jump_floor(client, 12, 'continue_back_12', 'back_10')
    elif action == "levitate_north_up":
        levitate(client, 'north', client.spells['exani hur up'])
    elif action == "levitate_west_up":
        levitate(client, 'west', client.spells['exani hur up'])
    elif action == "levitate_south_down":
        levitate(client, 'south', client.spells['exani hur down'])
    elif action == "levitate_east_down":
        levitate(client, 'east', client.spells['exani hur down'])

    elif action == "check_down":
        check_hunt(client, 'continue', 'leave', time=True)

    else:
        global_actions.waypoint_action(client, action)
