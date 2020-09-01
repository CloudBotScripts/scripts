#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "openChest":
        client.use_sqm(1, 0)

    elif action == "takeMissions":
        client.npc_say(['mission', 'trolls', 'yes', 'log book', 'yes'])
	
    elif action == "doneLogBook":
        client.npc_say(['log book', 'yes', 'trolls', 'yes'])

    elif action == "escape":
        client.hotkey('esc')

    elif action == 'gotoPartDone':
        client.jump_label('firstPartDone')

    elif action == 'checkEQ':
         mana_count = client.get_hotkey_item_count(2)
         if mana_count > 10:
            client.jump_label('normalMonsters')
         else:
            client.jump_label('easyMonsters')

    elif action == 'dropAmmo':
        client.drop_item_from_container(client.equips, 'ammunition')

    elif action == 'buyEquips':
        if client.get_name_item_in_slot(client.equips, 'weapon') == 'dagger':
            client.drop_item_from_container(client.equips, 'weapon')
            sleep(1)
            client.drop_item_from_container(client.equips, 'weapon')

            client.buy_items_from_npc(['sabre'], [1])

    elif action == 'checkerNormal':
        if client.cap() < 50 or client.get_hotkey_item_count(3) < 3:
            client.jump_label('leaveNormal')
        else:
            client.jump_label('atNormalM')

    else:
        global_actions.waypoint_action(client, action)

