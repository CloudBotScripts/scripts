#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *

## Hotkey levitate
levitate_down = '-'
levitate_up = '='

def waypoint_action(client, action):

    if action == "start":
        print('Bot started')

    elif action == "debug":
        client.jump_label('debug')
        #client.jump_label('travel_camp')

    elif action == "wait":
        sleep(2)

    elif action == "check_supplies":
        check_supplies(client, logout_fail=True)

    elif action == "bless_thais":
        client.npc_say(['spiritual', 'yes'])

    elif action == "travel_carlin":
        client.npc_say(['carlin', 'yes'])

    elif action == "bless_carlin":
        client.npc_say(['embrace', 'yes'])

    elif action == "bless_abdendriel":
        client.npc_say(['suns', 'yes'])

    elif action == "travel_edron":
        client.npc_say(['edron', 'yes'])

    elif action == "travel_cormaya":
        client.npc_say(['cormaya', 'yes'])

    elif action == "travel_eremo":
        client.npc_say(['eremo', 'yes'])

    elif action == "bless_eremo":
        client.npc_say(['solitude', 'yes'])

    elif action == "travel_passage":
        client.npc_say(['passage', 'yes'])

    elif action == "travel_kazordoon":
        client.npc_say(['kazordoon', 'yes'])

    elif action == "buy_ticket":
        client.npc_say(['ticket', 'yes'])

    elif action == "bless_kaz1":
        client.npc_say(['phoenix', 'yes'])

    elif action == "bless_kaz2":
        client.npc_say(['phoenix', 'yes'])

    elif action == "check_enhanced":
        print(client.script_options)
        if client.script_options['enhanced']:
            client.jump_label('enhanced')
        else:
            client.jump_label('go_train_edron')

    elif action == "travel_port_hope":
        client.npc_say(['port hope', 'yes'])

    elif action == "travel_east":
        client.npc_say(['east', 'yes'])

    elif action == "travel_banuta":
        client.npc_say(['banuta', 'yes'])

    elif action == "travel_venore":
        client.npc_say(['venore', 'yes'])

    elif action == "travel_svargrond":
        client.npc_say(['svargrond', 'yes'])

    elif action == "travel_camp":
        client.npc_say(['passage', 'camp', 'yes'])
        client.jump_label('in_camp')

    elif action == "levitate_north_up":
        levitate(client, 'north', levitate_up)

    elif action == "levitate_south_down":
        levitate(client, 'south', levitate_down)

    elif action == "bless_enhanced":
        client.say('hi')
        client.say('enhanced')
        client.say('yes')

    elif action == "travel_back_camp":
        client.npc_say(['passage', 'svargrond', 'yes'])

    elif action == "check_skill":
        check_skill(client)

    elif action == "end":
        sleep(10)
        client.logout()

    else:
        print('Action', action, 'is not defined')
