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

    elif action == "check_runes":
        if 'rune_name' not in client.hunt_config.keys():
            client.jump_label('skip_runes')

    elif action == "bank":
        client.npc_say(['deposit all', 'yes'])

    elif action == "wait":
        client.sleep(1)

    elif action == "wait_ten_min":
        client.sleep(10 * 60)

    elif action == "target_off":
        client.target_on = False

    elif action == "target_on":
        client.target_on = True

    elif action == "communication_task":
        client.npc_say(['communication', 'yes'])

    elif action == "confirm":
        client.hotkey('enter')

    elif action == "sell":
        client.sell_all_to_npc()

    elif action == "check_imbuements":
        if check_imbuements(client):
            client.jump_label('skip_imbuement')

    elif action == "check_sell_gems":
        if not client.script_options.get('sell_gems', False):
            client.jump_label('skip_sell_gems')

    elif action == "check_sell_loot":
        if not client.script_options.get('sell_loot', False):
            client.jump_label('skip_sell_loot')

    elif action == "use_imbuing_shrine":
        use_imbuing_shrine(client)

    elif action == "use_imbuing_shrine_north":
        use_imbuing_shrine(client, sqm=(0,1))

    elif action == "use_lever_east":
        client.use_lever((1, 0))

    elif action == "deposit":
        client.reach_locker()
        deposit_all_from_backpack_to_depot(client, client.container_conf['loot_bp'], 2)

    elif action == "refill":
        if 'health_name' in client.hunt_config.keys():
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

    elif action == "refill_gem":
        gem_name, take_gem = client.hunt_config['gem_name'], client.hunt_config['take_gem']
        if not withdraw_item_from_stash(client, gem_name, take_gem, client.items[gem_name]): 
            print('Not enough small amethysts')
            client.logout()

    elif action == "levitate_down":
        levitate(client, 'south', levitate_down)
    elif action == "levitate_up":
        levitate(client, 'north', levitate_up)

    elif action == "levitate_south_up":
        levitate(client, 'south', client.spells['exani hur up'])
    elif action == "levitate_south_down":
        levitate(client, 'south', client.spells['exani hur down'])
    elif action == "levitate_east_up":
        levitate(client, 'east', client.spells['exani hur up'])
    elif action == "levitate_east_down":
        levitate(client, 'east', client.spells['exani hur down'])
    elif action == "levitate_west_up":
        levitate(client, 'west', client.spells['exani hur up'])
    elif action == "levitate_west_down":
        levitate(client, 'west', client.spells['exani hur down'])
    elif action == "levitate_north_up":
        levitate(client, 'north', client.spells['exani hur up'])
    elif action == "levitate_north_down":
        levitate(client, 'north', client.spells['exani hur down'])


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

    elif action == "travel_abdendriel":
        client.npc_say(['ab\'dendriel', 'yes'])

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

    elif action == "travel_banuta":
        client.npc_say(['banuta', 'yes'])

    elif action == "travel_alchemist":
        client.npc_say(['pass', 'alchemist'])

    elif action == "travel_cemetery":
        client.npc_say(['pass', 'cemetery'])

    elif action == "travel_magician":
        client.npc_say(['pass', 'magician'])

    elif action == "buy_ticket":
        client.npc_say(['ticket', 'yes'])

    elif action == "use_gem_north":
        x, y = client.gameboard.sqm_to_coordinate(0, 1)
        gem_name = client.hunt_config['gem_name']
        client.hotkey(client.item_hotkeys[gem_name])
        sleep(0.3)
        client.click(x, y, button='left')
        sleep(1)

    elif action == "skip_portal":
        client.jump_label('after_portal')

    elif action == "skip_portal_2":
        client.jump_label('after_portal_2')

    elif action == "buy_potions":
        npc_refill(client, mana=True, health='health_name' in client.hunt_config.keys())

    elif action == "buy_runes":
        if 'rune_name' in client.hunt_config.keys():
            npc_refill(client, mana=False, health=False, rune=True)

    elif action == "buy_ammo":
        npc_refill(client, ammo='ammo_name' in client.hunt_config.keys())

    elif action == "buy_food":
        npc_refill(client, food='food_name' in client.hunt_config.keys())

    elif action == "check_supplies":
        check_supplies(client, 
                mana='mana_name' in client.hunt_config.keys(),
                health='health_name' in client.hunt_config.keys(),
                ammo='ammo_name' in client.hunt_config.keys(), 
                rune='rune_name' in client.hunt_config.keys(), 
                logout_fail=True)

    elif action == "summon":
        hotkey = client.script_options.get('summon', False)
        if hotkey != False:
            client.hotkey(hotkey)

    elif action == "check":
        check_hunt(client, 'hunt', 'leave', 
                mana='mana_name' in client.hunt_config.keys(),
                health='health_name' in client.hunt_config.keys(),
                ammo='ammo_name' in client.hunt_config.keys(), 
                rune='rune_name' in client.hunt_config.keys(), 
                time=True)

    elif action == "check2":
        check_hunt(client, 'hunt2', 'leave2', 
                mana='mana_name' in client.hunt_config.keys(),
                health='health_name' in client.hunt_config.keys(),
                rune='rune_name' in client.hunt_config.keys(), 
                ammo='ammo_name' in client.hunt_config.keys(), 
                time=True)

    elif action == "check_time":
        check_time(client, 'train', 'start')

    elif action == "check_train":
        check_skill(client)

    elif action == "check_level_8":
        if client.get_level() >= 8:
            client.jump_label('end')
        else:
            client.jump_label('continue_dawnport')

    elif action == "end":
        client.logout()

    else:
        print('Action:', action, 'does not exist')
