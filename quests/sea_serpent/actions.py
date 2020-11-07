from time import sleep
from datetime import datetime
import clipboard

## Options
hours_leave = [9, 10]
skill_train = 'club'

## Cap to leave
cap_leave = 30

## Mana potions to take
take_mana = 10
mana_leave = 5
mana_name = 'mana potion'
depot_mana_potions = 3
hotkey_mana_potions = 4

# Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *

persistent_actions = [{'interval':60, 'action':eat_food}]

def waypoint_action(client, action):
    if action == "start":
      print('Bot started')

    elif action == "debug":
        client.jump_label('debug')

    elif action == "give_fish_captain":
        client.npc_say(["mission", 'yes', 'bait', 'bait', 'bait', 'bait', 'hunt', 'yes'])

    elif action == "buy_bait":
        bait_count = client.get_hotkey_item_count(client.items['bait'])
        if bait_count < 1:
            client.buy_items_from_npc(['bait'], [10])

    elif action == "set_bait":
        container = client.get_container('Backpack')
        if container is False:
            print('Backpack not found')
            client.logout()
        sleep(0.4)
        client.use_slot(container, 0)
        sleep(0.4)
        client.click_sqm(0, 1)
        sleep(0.2)

    elif action == "go_up":
        client.press('d')
        sleep(0.7)

    elif action == "go_down":
        client.press('s')
        sleep(0.7)

    elif action == "telescope":
        # open server messages
        client.hotkey('alt', 'd')
        sleep(0.2)
        client.hotkey('tab')
        sleep(0.2)

        keep = True
        while keep:
            keep = False
            client.use_sqm(-1, 0)
            sleep(0.4)

            # get last server messages
            s = client.copy_server_log()

            last_messages = s[::-1]
            for message in last_messages:
                print(message)
                if 'sea serpent in sight' in message:
                    keep = True
                    break
                elif 'you lost it' in message:
                    keep = True
                    break
                elif 'straight ahead of you' in message:
                    client.jump_label('straight')
                    break
                elif 'the starboard side' in message:
                    client.jump_label('starboard')
                    break
                elif 'the larboard side' in message:
                    client.jump_label('larboard')
                    break
                elif 'gain speed' in message:
                    client.jump_label('speed')
                    break
                elif 'right location' in message:
                    client.jump_label('finish')
                    break
                else:
                    print('Message does not match')
            else:
                print('Failed to get message')
                exit()

    elif action == "repeat":
        client.jump_label('repeat_bait')

    elif action == "straight":
        client.npc_say(["straight"])

    elif action == "starboard":
        client.npc_say(["starboard"])

    elif action == "larboard":
        client.npc_say(["larboard"])

    elif action == "speed":
        client.npc_say(["speed"])

    elif action == "passage":
        client.npc_say(["passage", 'yes'])

    elif action == "travel_venore":
        client.npc_say(["venore", 'yes'])

    elif action == "travel_edron":
        client.npc_say(["edron", 'yes'])

    elif action == "end":
        client.logout()

    else:
        print('Action', action, 'is not defined')
