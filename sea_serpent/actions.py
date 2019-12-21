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
        check_hunt(client, 'hunt_north', 'leave_north', 
                mana='mana_name' in client.hunt_config.keys(),
                health='health_name' in client.hunt_config.keys(),
                ammo='ammo_name' in client.hunt_config.keys(), 
                rune='rune_name' in client.hunt_config.keys(), 
                time=True)

    elif action == "check_south":
        check_hunt(client, 'hunt_south', 'leave_south', 
                mana='mana_name' in client.hunt_config.keys(),
                health='health_name' in client.hunt_config.keys(),
                ammo='ammo_name' in client.hunt_config.keys(), 
                rune='rune_name' in client.hunt_config.keys(), 
                time=True)
            
    elif action == "check_south_down":
        check_hunt(client, 'hunt_south_down', 'leave_south_down',
                mana='mana_name' in client.hunt_config.keys(),
                health='health_name' in client.hunt_config.keys(),
                ammo='ammo_name' in client.hunt_config.keys(), 
                rune='rune_name' in client.hunt_config.keys(), 
                time=True)

    else:
        global_actions.waypoint_action(client, action)
