#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "use_elevator":
        client.use_lever((1, 0))
        
    elif action == "levitate_north_up":
        levitate(client, 'north', client.spells['exani hur up'])
    elif action == "levitate_west_up":
        levitate(client, 'west', client.spells['exani hur up'])
    elif action == "levitate_south_down":
        levitate(client, 'south', client.spells['exani hur down'])
    elif action == "levitate_east_down":
        levitate(client, 'east', client.spells['exani hur down'])

    elif action == "refill":
        if not withdraw_item_from_stash(client, 'brown mushroom', 50, client.items['brown mushroom']): 
            print('Not enough mushrooms')
        health_name, take_health = client.hunt_config['health_name'], client.hunt_config['take_health']
        if not withdraw_item_from_stash(client, health_name, take_health, client.items[health_name]): 
            print('Not enough health potions')

    elif action == "check_down":
        check_hunt(client, 'continue', 'leave', time=True)

    else:
        global_actions.waypoint_action(client, action)
