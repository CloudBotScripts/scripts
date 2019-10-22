#Load Custom functions
from lib import *

## Hotkey levitate
levitate_down = '-'
levitate_up = '='

def waypoint_action(client, action):
    if action == "start":
        print('Bot started')

    elif action == "debug":
        client.jump_label('debug')

    elif action == "check_ammo":
        if 'ammo_name' not in client.hunt_config.keys():
            client.jump_label('skip_ammo')
        else:
            ammo_name = client.hunt_config['ammo_name']
            if 'arrow' not in ammo_name and 'bolt' not in ammo_name:
                client.jump_label('skip_ammo')

    elif action == "bank":
        client.npc_say(['deposit all', 'yes'])

    elif action == "wait":
        sleep(1)

    elif action == "wait_ten_min":
        sleep(10 * 60)

    elif action == "communication_task":
        client.npc_say(['communication', 'yes'])

    elif action == "confirm":
        client.hotkey('enter')

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
        health_name, take_health = client.hunt_config['health_name'], client.hunt_config['take_health']
        if not withdraw_item_from_stash(client, health_name, take_health, client.items[health_name]): 
            print('Not enough potions')
        if not withdraw_item_from_stash(client, 'brown mushroom', 50, client.items['brown mushroom']): 
            print('Not enough mushrooms')
        if 'health_name2' in client.hunt_config.keys():
            health_name2, take_health2 = client.hunt_config['health_name2'], client.hunt_config['take_health2']
            if not withdraw_item_from_stash(client, health_name2, take_health2, client.items[health_name2]): 
                print('Not enough potions')
        if 'ammo_name' in client.hunt_config.keys():
            ammo_name, take_ammo = client.hunt_config['ammo_name'], client.hunt_config['take_ammo']
            if not withdraw_item_from_stash(client, ammo_name, take_ammo, client.items[ammo_name]): 
                print('Not enough ammo')

    elif action == "levitate_down":
        levitate(client, 'south', levitate_down)

    elif action == "levitate_up":
        levitate(client, 'north', levitate_up)

    elif action == "travel_edron":
        client.npc_say(['edron', 'yes'])

    elif action == "travel_thais":
        client.npc_say(['thais', 'yes'])

    elif action == "travel_oramond":
        client.npc_say(['oramond', 'yes'])

    elif action == "travel_krailos":
        client.npc_say(['krailos', 'yes'])

    elif action == "travel_port_hope":
        client.npc_say(['port hope', 'yes'])

    elif action == "travel_venore":
        client.npc_say(['venore', 'yes'])

    elif action == "travel_carlin":
        client.npc_say(['carlin', 'yes'])

    elif action == "travel_liberty_bay":
        client.npc_say(['liberty bay', 'yes'])

    elif action == "travel_ankrahmun":
        client.npc_say(['ankrahmun', 'yes'])

    elif action == "travel_svargrond":
        client.npc_say(['svargrond', 'yes'])

    elif action == "travel_gray_island":
        client.npc_say(['gray island', 'yes'])

    elif action == "travel_farmine":
        client.npc_say(['farmine', 'yes'])

    elif action == "travel_yalahar":
        client.npc_say(['yalahar', 'yes'])

    elif action == "travel_cormaya":
        client.npc_say(['cormaya', 'yes'])

    elif action == "travel_mistrock":
        client.npc_say(['mistrock', 'yes'])

    elif action == "travel_passage":
        client.npc_say(['passage', 'yes'])

    elif action == "travel_east":
        client.npc_say(['east', 'yes'])

    elif action == "travel_west":
        client.npc_say(['west', 'yes'])

    elif action == "travel_center":
        client.npc_say(['center', 'yes'])

    elif action == "buy_potions":
        npc_refill(client, mana=True, health=True)

    elif action == "buy_runes":
        npc_refill(client, mana=False, health=False, rune=True)

    elif action == "buy_ammo":
        npc_refill(client, ammo='ammo_name' in client.hunt_config.keys())

    elif action == "check_supplies":
        check_supplies(client, ammo='ammo_name' in client.hunt_config.keys(), logout_fail=True)

    elif action == "summon":
        hotkey = client.script_options.get('summon', False)
        if hotkey != False:
            client.hotkey(hotkey)

    elif action == "check":
        check_hunt(client, 'hunt', 'leave', ammo='ammo_name' in client.hunt_config.keys(), time=True)

    elif action == "check2":
        check_hunt(client, 'hunt2', 'leave2', ammo='ammo_name' in client.hunt_config.keys(), time=True)

    elif action == "check_time":
        check_time(client, 'train', 'start')

    elif action == "check_train":
        check_skill(client)

    elif action == "end":
        client.logout()
