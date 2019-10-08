#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "refill":
        if not withdraw_item_from_stash(client, 'brown mushroom', 50, client.items['brown mushroom']): 
            print('Not enough mushrooms')
        health_name, take_health = client.hunt_config['health_name'], client.hunt_config['take_health']
        if not withdraw_item_from_stash(client, health_name, take_health, client.items[health_name]): 
            print('Not enough health potions')
        gem_name, take_gem = client.hunt_config['gem_name'], client.hunt_config['take_gem']
        if not withdraw_item_from_stash(client, gem_name, take_gem, client.items[gem_name]): 
            print('Not enough small rubies')
            client.logout()

    elif action == "use_gem_north":
        x, y = client.gameboard.sqm_to_coordinate(0, 1)
        gem_name = client.hunt_config['gem_name']
        client.hotkey(client.item_hotkeys[gem_name])
        sleep(0.3)
        client.click(x, y, button='left')
        sleep(1)

    elif action == "skip_mountain":
        client.jump_label('after_mountain')

    elif action == "skip_portal":
        client.jump_label('after_portal')

    elif action == "skip_portal_2":
        client.jump_label('after_portal_2')

    else:
        global_actions.waypoint_action(client, action)
