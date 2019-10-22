#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *

def waypoint_action(client, action):

    if action == "start":
      print('Bot started')

    # City and Refill
    elif action == "bank":
        client.npc_say(['deposit all', 'yes'])

    elif action == "sell":
        client.sell_all_to_npc()

    elif action == "deposit":
        client.reach_locker()
        deposit_all_from_backpack_to_depot(client, client.container_conf['loot_bp'], 2)

    elif action == "refill":
        if not withdraw_item_from_stash(client, 'brown mushroom', 100, 11): 
            print('Not enough mushrooms')

    elif action == "travel_east":
        client.npc_say(['east', 'yes'])

    elif action == "travel_center":
        client.npc_say(['center', 'yes'])

    elif action == "check_task":
        if not client.script_options['get_task']:
            client.jump_label('skip_task')

    elif action == "get_task":
        client.npc_say(['task', 'tarantula', 'yes'])

    elif action == "buy_potions":
        npc_refill(client, mana=True, health=True)

    elif action == "check_supplies":
        check_supplies(client, logout_fail=True)

    elif action == "check":
        check_hunt(client, 'hunt', 'leave', time=True)

    elif action == "check_time":
        check_time(client, 'train', 'start')

    elif action == "check_train":
        client.jump_label(client.script_options['skill_train'])

    elif action == "end":
        sleep(4)
        client.logout()
    else:
        print('Action', action, 'is not defined')
