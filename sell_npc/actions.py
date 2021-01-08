#Load Custom functions
from lib import *
import global_actions

def waypoint_action(client, action):

    def withdraw_items_to_backpack(backpack, depot):
        # Returns true if withdraw was successful

        dest = client.get_container(backpack)
        if not dest:
            print('Could not find backpack', backpack, 'to hold items')
            return False

        # Open up to last backpack
        tries = 20
        while not dest.is_empty() and tries:
            tries -= 1 
            client.use_slot(dest, 0)
            sleep(0.3)
            client.use_slot(dest, 1)
            sleep(0.3)
            client.hotkey('esc')

        # Try 3 times to open depot
        for tries in range(3):
            client.reach_locker()
            src = client.open_depot(depot)
            if src:
                client.use_slot(src, depot - 1)
                sleep(1)
                break
        else:
            print('Failed to reach locker')
            return False

        # Withdraw items until no backpack slots or no cap
        withdraw_any = False
        if client.get_cap() < 800:
            print('[Action] Need at least 800 cap to sell items')
            return False

        prev_cap = 100000
        for i in range(15):
            print('cap:', client.get_cap())
            if client.get_cap() >= prev_cap:
                print('[Action] Could not withdraw more items')
                break
            prev_cap = client.get_cap()

            if client.get_cap() < 200:
                print('[Action] Low cap')
                return withdraw_any

            dest = client.get_container(backpack)
            if not dest:
                print('Could not find backpack', backpack, 'to hold items')
                return withdraw_any

            if src.is_empty(): 
                print('Depot is empty')
                return withdraw_any

            # Withdraw 19 items to current backpack
            items = 19
            while items > 0:
                items -= 1
                client.take_item_from_slot(src, 0, dest)
                sleep(0.2)
            withdraw_any = True

            # Go back one backpack
            client.return_container(dest)

        print('Withdrawed more than 250 items')
        return True

    if action == 'check_sell_edron':
        if not client.script_options['lailene'] and not client.script_options['alexander'] and not client.script_options['telas']:
            client.jump_label('end_edron') 

    elif action == 'check_sell_edron_tower':
        if not client.script_options['lailene'] and not client.script_options['alexander']:
            client.jump_label('goto_telas') 

    elif action == 'check_sell_rashid':
        if not client.script_options['rashid']:
            client.jump_label('skip_sell_rashid') 

    elif action == 'check_sell_djinn':
        if not client.script_options['green_djinn'] and not client.script_options['blue_djinn']:
            client.jump_label('skip_sell_djinn') 

    elif action == 'check_djinn_type':
        if client.script_options['green_djinn']:
            client.jump_label('green_djinn') 
        elif client.script_options['blue_djinn']:
            client.jump_label('blue_djinn') 
        else:
            client.jump_label('end_djinn') 

    elif action == 'check_sell_flint':
        if not client.script_options['flint']:
            client.jump_label('skip_sell_flint') 

    elif action == 'check_sell_lailene':
        if not client.script_options['lailene']:
            client.jump_label('skip_sell_lailene') 

    elif action == 'check_sell_alexander':
        if not client.script_options['alexander']:
            client.jump_label('skip_sell_alexander') 

    elif action == 'check_sell_telas':
        if not client.script_options['telas']:
            client.jump_label('skip_sell_telas') 

    elif action == 'check_sell_tamoril':
        if not client.script_options['tamoril']:
            client.jump_label('skip_sell_tamoril') 

    elif action == 'check_sell_esrik':
        if not client.script_options['esrik']:
            client.jump_label('skip_sell_esrik') 

    elif action == "travel_darashia": # Only for carpet
        client.npc_say(['darashia', 'yes']) 

    elif action == "repeat_flint":
        client.jump_label('start_flint')
        
    elif action == "flint":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['flint_depot'])
        if not withdraw:
            client.jump_label('end_flint')

    elif action == "repeat_djinn":
        client.jump_label('start_djinn')
        
    elif action == "djinn":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['djinn_depot'])
        if not withdraw:
            client.jump_label('end_djinn')

    elif action == "repeat_edron":
        client.jump_label('start_edron')
        
    elif action == "edron":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['edron_depot'])
        if not withdraw:
            client.jump_label('end_edron')
            
    elif action == "skip_edron":
        client.jump_label('skip_edron')
            
    elif action == "repeat_farmine":
        client.jump_label('start_farmine')
        
    elif action == "farmine":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['esrik_depot'])
        if not withdraw:
            client.jump_label('end_farmine')

    elif action == "use_elevator":
        client.use_lever((1,0))

    elif action == "repeat_yalahar":
        client.jump_label('start_yalahar')
        
    elif action == "yalahar":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['tamoril_depot'])
        if not withdraw:
            client.jump_label('end_yalahar')

    elif action == "check_rashid":
        if not client.script_options['rashid']:
            client.jump_label('end_rashid')
        weekday = datetime.utcnow().weekday()
        # Adjust date to sever save 
        if 0 < datetime.utcnow().hour + 1 < 10:
            weekday -= 1 # still before server save
            weekday %= 7

        if weekday == 0:
            client.jump_label('goto_svargrond_depot')
        elif weekday == 1:
            client.jump_label('goto_liberty_bay_depot')
        elif weekday == 2:
            client.jump_label('goto_port_hope_depot')
        elif weekday == 3:
            client.jump_label('goto_ankrahmun_depot')
        elif weekday == 4:
            client.jump_label('goto_darashia_depot')
        elif weekday == 5:
            client.jump_label('goto_edron_depot')
        elif weekday == 6:
            client.jump_label('goto_carlin_depot')

    elif action == "end_rashid":
        client.jump_label('end_rashid')

    elif action == "repeat_rashid_svargrond":
        client.jump_label('start_rashid_svargrond')
        
    elif action == "rashid_svargrond":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['rashid_depot'])
        if not withdraw:
            client.jump_label('end_rashid_svargrond')

    elif action == "repeat_rashid_carlin":
        client.jump_label('start_rashid_carlin')
        
    elif action == "rashid_carlin":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['rashid_depot'])
        if not withdraw:
            client.jump_label('end_rashid_carlin')

    elif action == "repeat_rashid_liberty_bay":
        client.jump_label('start_rashid_liberty_bay')
        
    elif action == "rashid_liberty_bay":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['rashid_depot'])
        if not withdraw:
            client.jump_label('end_rashid_liberty_bay')

    elif action == "repeat_rashid_port_hope":
        client.jump_label('start_rashid_port_hope')
        
    elif action == "rashid_port_hope":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['rashid_depot'])
        if not withdraw:
            client.jump_label('end_rashid_port_hope')

    elif action == "repeat_rashid_ankrahmun":
        client.jump_label('start_rashid_ankrahmun')
        
    elif action == "rashid_ankrahmun":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['rashid_depot'])
        if not withdraw:
            client.jump_label('end_rashid_ankrahmun')

    elif action == "repeat_rashid_darashia":
        client.jump_label('start_rashid_darashia')
        
    elif action == "rashid_darashia":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['rashid_depot'])
        if not withdraw:
            client.jump_label('end_rashid_darashia')

    elif action == "repeat_rashid_edron":
        client.jump_label('start_rashid_edron')
        
    elif action == "rashid_edron":
        withdraw = withdraw_items_to_backpack(backpack=client.script_options['backpack_name'], depot=client.script_options['rashid_depot'])
        if not withdraw:
            client.jump_label('end_rashid_edron')

    elif action == "stash_all":
        client.reach_locker()
        stash_item_from_slot(client, client.equips, 'backpack')

    else:
        global_actions.waypoint_action(client, action)
