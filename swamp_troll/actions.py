#Load Custom functions
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

    elif action == "buy_potions":
        npc_refill(client, mana=True, health=True)

    # Check
    elif action == "check_supplies":
        check_supplies(client, logout_fail=True)

    elif action == "check":
        check_hunt(client, 'hunt', 'leave')

    elif action == "check_time":
        check_time(client, 'train', 'start')

    elif action == "check_train":
        client.jump_label(skill_train)

    elif action == "wait":
        sleep(2)

    elif action == "end":
      client.logout()

    else:
        print('Action', action, 'is not defined')
