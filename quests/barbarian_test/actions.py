# Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "get_mission":
        client.npc_say(["test"])

    elif action == "mead":
        prev_cap = client.get_cap()
        client.npc_say(["mead", "yes"])
        sleep(1.0)

        if client.get_cap() >= prev_cap:
            print('Finished test 1')
            client.jump_label('second_test')

        containers = client.get_opened_containers()
        has_item = False
        for container in containers:
            num_slots = container.get_num_slots()
            for slot in reversed(range(num_slots)):
                if 'honeycomb' in container.get_item_in_slot(slot):
                    print('Has honeycomb')
                    has_item = True
        if not has_item:
            print('Failed quest, no honeycomb')
            client.logout()

    elif action == "drink":
        for i in range(20):
            client.use_sqm(-1,0)
            sleep(1.0)
        client.jump_label('mead')

    elif action == "fill_mead":
        containers = client.get_opened_containers()
        has_item = False
        for container in containers:
            num_slots = container.get_num_slots()
            for slot in reversed(range(num_slots)):
                print(client.get_name_item_in_slot(container, slot))
                if 'mead horn' in client.get_name_item_in_slot(container, slot):
                    print('Fill mead horn')
                    sleep(0.2)
                    client.use_slot(container, slot)
                    sleep(0.2)
                    client.click_sqm(-1, 0)
                    sleep(0.2)
                    has_item = True
        if not has_item:
            print('Did not find mead horn')
            client.logout()

    elif action == "use_mead_bear":
        containers = client.get_opened_containers()
        has_item = False
        for container in containers:
            num_slots = container.get_num_slots()
            for slot in reversed(range(num_slots)):
                print(client.get_name_item_in_slot(container, slot))
                if 'mead horn' in client.get_name_item_in_slot(container, slot):
                    print('Fill mead horn')
                    sleep(0.2)
                    client.use_slot(container, slot)
                    sleep(0.2)
                    client.click_sqm(0, 1)
                    sleep(0.7)
                    client.use_sqm(0, 1)
                    has_item = True

        if not has_item:
            print('Did not find mead horn')
            client.logout()

    elif action == "bear_complete":
        client.npc_say(["bear", "yes"])

    elif action == "mamooth":
        client.hotkey('f6')
        sleep(0.5)
        client.hotkey('f6')
        sleep(0.5)
        client.hotkey('f6')
        sleep(0.5)
        client.use_sqm(0, 1)

    elif action == "mamooth_complete":
        client.npc_say(["push", "yes"])

    else:
        global_actions.waypoint_action(client, action)

