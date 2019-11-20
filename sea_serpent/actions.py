#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

## Hotkey levitate
levitate_down = '-'
levitate_up = '='

def waypoint_action(client, action):
    if action == "check_tasks":
        if not client.script_options.get('task', False):
            client.jump_label('skip_tasks')

    elif action == "get_tasks":
        client.npc_say(['tasks', 'yes', 'promotion', 'tasks', 'sea serpent', 'yes'])

    elif action == "check_hunt":
        if client.script_options['respawn'] == 'north':
            client.jump_label('go_north')
        elif client.script_options['respawn'] == 'south':
            client.jump_label('go_south')
        else:
            client.jump_label('go_south_down')

    elif action == "check_north":
        check_hunt(client, 'hunt_north', 'leave_north', ammo=ammo, time=True)

    elif action == "check_south":
        check_hunt(client, 'hunt_south', 'leave_south', ammo=ammo, time=True)
            
    elif action == "check_south_down":
        check_hunt(client, 'hunt_south_down', 'leave_south_down', ammo=ammo, time=True)

    elif action == "levitate_south_down":
        levitate(client, 'south', levitate_down)
    elif action == "levitate_east_down":
        levitate(client, 'east', levitate_down)
    elif action == "levitate_west_down":
        levitate(client, 'west', levitate_down)
    elif action == "levitate_north_down":
        levitate(client, 'north', levitate_down)
    elif action == "levitate_south_up":
        levitate(client, 'south', levitate_up)
    elif action == "levitate_east_up":
        levitate(client, 'east', levitate_up)
    elif action == "levitate_west_up":
        levitate(client, 'west', levitate_up)
    elif action == "levitate_north_up":
        levitate(client, 'north', levitate_up)

    else:
        global_actions.waypoint_action(client, action)
