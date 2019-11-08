#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *

def waypoint_action(client, action):
    if action == "start":
      print('Bot started')

    elif action == "debug":
        #client.jump_label('refill')
        pass

    elif action == "bank":
        client.npc_say(['deposit all', 'yes'])

    elif action == "sell":
        client.sell_all_to_npc()

    elif action == "check_imbuements":
        if check_imbuements(client):
            client.jump_label('skip_imbuement')

    elif action == "use_imbuing_shrine":
        use_imbuing_shrine(client)

    elif action == "deposit":
        client.reach_locker()
        deposit_all_from_backpack_to_depot(client, client.container_conf['loot_bp'], 2)

    elif action == "refill":
        if not withdraw_item_from_stash(client, client.hunt_config['rune_name'], client.hunt_config['take_rune'], client.hunt_config['hotkey_runes']): 
            print('Not enough runes')
            client.logout()
        if not withdraw_item_from_stash(client, 'brown mushroom', 50, 11): 
            print('Not enough mushrooms')
        if not withdraw_item_from_stash(client, client.hunt_config['health_name'], client.hunt_config['take_health'], client.hunt_config['hotkey_health_potions']): 
            print('Not enough potions')

    elif action == "buy_potions":
        npc_refill(client, mana=True, health=True)

    elif action == "check_supplies":
        check_supplies(client, ammo=False, imbuement=False, logout_fail=True)

    elif action == "check":
        check_hunt(client, 'hunt', 'leave', time=True)

    elif action == "check_time":
        check_time(client, 'train', 'start')

    elif action == "check_train":
        client.jump_label(client.script_options['skill_train'])

    elif action == "end":
        client.logout()

    else:
        print('Action', action, 'is not defined')
