# Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *

def waypoint_action(client, action):
    if action == "start":
      print('Bot started')
      client.jump_label('ank')

    elif action == "travel_edron":
        client.npc_say(['edron', 'yes'])

    elif action == "travel_kazordoon":
        client.npc_say(['kazordoon', 'yes'])

    elif action == "travel_darashia":
        client.npc_say(['darashia', 'yes'])

    elif action == "travel_ankrahmun":
        client.npc_say(['ankrahmun', 'yes'])

    elif action == "travel_venore":
        client.npc_say(['venore', 'yes'])

    elif action == "travel_thais":
        client.npc_say(['thais', 'yes'])

    elif action == "travel_port_hope":
        client.npc_say(['port hope', 'yes'])

    elif action == "travel_liberty_bay":
        client.npc_say(['liberty bay', 'yes'])

    elif action == "travel_yalahar":
        client.npc_say(['yalahar', 'yes'])

    elif action == "honey":
        client.buy_items_from_npc(['sample of sand wasp honey'], [1])

    elif action == "jug":
        client.buy_items_from_npc(['jug of embalming fluid'], [1])

    elif action == "venorean_spice":
        client.buy_items_from_npc(['sample of venorean spice'], [1])

    elif action == "royal_satin":
        client.buy_items_from_npc(['piece of royal satin'], [1])

    elif action == "rum":
        client.buy_items_from_npc(['rum flask of rum'], [1])

    elif action == "angus":
        client.npc_say(['join', 'yes', 'yes'])

    elif action == "angus2":
        client.npc_say(['pickaxe', 'yes'])

    elif action == "wyrdin":
        client.npc_say(['mission', 'yes'])

    elif action == "karith":
        client.npc_say(['darashia', 'yes', 'thais', 'yes', 'venore', 'yes', 'ankrahmun', 'yes', 'liberty bay', 'yes'])

    elif action == "end":
        client.logout()

    else:
        print('Action', action, 'is not defined')
