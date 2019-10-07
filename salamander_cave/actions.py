# Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *

persistent_actions = []

def waypoint_action(client, action):
    if action == "start":
      print('Bot started')

    elif action == "bank":
        client.npc_say(['deposit all', 'yes'])

    elif action == "sell":
        client.sell_all_to_npc()

    elif action == "deposit":
        client.reach_locker()
        deposit_all_from_backpack_to_depot(client, client.container_conf['loot_bp'], 2)

    elif action == "buy_potions":
        npc_refill(client, mana=True, health=False)

    # Check
    elif action == "check_supplies":
        check_supplies(client, health=False, logout_fail=True)

    elif action == "check_time":
        check_time(client, 'logout', 'start')

    elif action == "check":
        check_hunt(client, 'hunt', 'leave', health=False, time=True)

    elif action == "end":
        client.logout()

    else:
        print('Action', action, 'is not defined')
