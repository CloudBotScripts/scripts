#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):

    def use_pick_south():
        pick_hotkey = client.item_hotkeys["pick"]

        x, y = client.gameboard.sqm_to_coordinate(0, -1)
        client.hotkey(pick_hotkey)
        sleep(0.3)
        client.click(x, y, button='left')
        sleep(0.5)

    def use_fishing_rod_south():
        x, y = client.gameboard.sqm_to_coordinate(0, -1)
        client.hotkey('O')
        sleep(0.3)
        client.click(x, y, button='left')
        sleep(1)

    def get_sqm_type_south():
        x, y = client.gameboard.sqm_to_coordinate(0, -1)
        client.keyDown('shift')
        sleep(0.1)
        client.click(x, y, button='left')
        sleep(0.1)
        client.keyDown('shift')
        sleep(0.1)
        client.click(x, y, button='left')
        sleep(0.1)
        client.keyUp('shift')
        sleep(0.4)
        client.hotkey('alt', 'd')
        sleep(0.4)
        client.hotkey('tab')
        sleep(0.6)

        # get last 4 server messages
        log = client.copy_server_log()

        look_results = [line for line in log if 'You' in line and 'see' in line]
        sleep(1)
        if 'fragile' in look_results[-1]:
            print('[Action] Closed ice hole')
            return 'closed'
        elif 'movement of' in look_results[-1]:
            print('[Action] Fish in ice hole')
            return 'fish'
        elif 'ice hole' in look_results[-1]:
            print('[Action] Empty ice hole')
            return 'empty'
        else:
            return 'other'

    if action == "fish_south":
        type_sqm = get_sqm_type_south() 
        if type_sqm == 'closed':
            use_pick_south()
            sleep(1)
            type_sqm = get_sqm_type_south() 

        if type_sqm == 'fish':
            worm_hotkey = client.items["worm"]
            worm_count = client.get_hotkey_item_count(worm_hotkey)
            for i in range(30):
                use_fishing_rod_south()
                new_worm_count = client.get_hotkey_item_count(worm_hotkey)
                if new_worm_count < worm_count:
                    print('Catched fish')
                    break
            # Move fish to Loot backpack
            src = client.get_container(client.container_conf['main_bp'])
            if not src:
                print('Could not find backpack with items')
            dest = client.get_container(client.container_conf['loot_bp'])
            if not src:
                print('Could not find backpack with items')

            name_item = client.get_name_item_in_slot(src, 0)
            print('Item backpack', name_item)
            if name_item in ('fish', 'northern pike', 'rainbow trout', 'green perch'):
                client.take_item_from_slot(src, 0, dest, dest_slot=0)

    elif action == "buy_worms":
        worm_hotkey = client.items["worm"]
        worm_count = client.get_hotkey_item_count(worm_hotkey)
        client.buy_items_from_npc(['worm'], [200 - worm_count])

    elif action == "refill":
        food_hotkey = client.items["brown mushroom"]
        if not withdraw_item_from_stash(client, 'brown mushroom', client.hunt_config['food_amount'], food_hotkey): 
            print('Not enough mushrooms')

    elif action == "check_worms":
        worm_hotkey = client.items["worm"]
        worm_count = client.get_hotkey_item_count(worm_hotkey)
        if worm_count > 100:
            client.jump_label('skip_worms')

    elif action == "check":
        worm_hotkey = client.items["worm"]
        worm_count = client.get_hotkey_item_count(worm_hotkey)
        if worm_count < 100 or client.get_cap() < client.hunt_config['cap_leave']:
            client.jump_label('leave')
        else:
            client.jump_label('hunt')


    elif action == "check_supplies":
        worm_hotkey = client.items["worm"]
        worm_count = client.get_hotkey_item_count(worm_hotkey)
        if worm_count < 100:
            client.logout()

    elif action == "wait":
        sleep(300)

    elif action == "exit":
      print('Logout')
      client.logout()

    else:
        global_actions.waypoint_action(client, action)
