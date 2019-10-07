''' User defined functions

User defined functions 
These functions can be used in the waypoint actions (actions.py) or during regular intervals (persistent_actions).
'''
from time import sleep
from datetime import datetime
from pytz import timezone
import json
import os, sys

# Anti paralyze
def anti_paralyze(client, hotkey='f2'):
    conditions = client.condition_bar.get_condition_list()
    if 'paralyzed' in conditions:
        print('Cast anti paralyze')
        client.hotkey(hotkey)

def drop_vials(client):
    monster_count = client.battle_list.get_monster_count()
    if monster_count < 1:
        containers = client.get_opened_containers()
        for container in containers:
            num_slots = container.get_num_slots()
            for slot in reversed(range(num_slots)):
                if 'empty potion flask' in container.get_item_in_slot(slot):
                    print('Dropping vial')
                    client.drop_item_from_container(container, slot)
                    sleep(0.2)

def recover_full_mana(client, hotkey='e'):
    monster_count = client.battle_list.get_monster_count()
    hp_percentage, mp_percentage = client.status_bar.get_percentage()
    if monster_count < 1 and mp_percentage < 95:
        client.hotkey(hotkey)

# Call eat food
def eat_food(client):
    food_hotkey = 'f11'
    client.hotkey(food_hotkey)

# Cast haste
def haste(client):
    spell_hotkey = 'v'
    monster_count = client.battle_list.get_monster_count()
    conditions = client.condition_bar.get_condition_list()
    if monster_count < 1 and 'haste' not in conditions:
        client.hotkey(spell_hotkey)

# Cast utana vid
def invisibility(client):
    spell_hotkey = '8'
    client.hotkey(spell_hotkey)

# Use stealth ring
def stealth_ring(client, monster_count, monster_list=False):
    ring_hotkey_slot = 8 
    ring_hotkey = 'f8'

    # ring
    equipped_ring = client.get_name_item_in_slot(client.equips, 'ring')
    monster_count = client.battle_list.get_monster_count()

    print(equipped_ring)
    if monster_count > 4 and equipped_ring != 'stealth ring':
        print('Equip ring')
        client.hotkey(ring_hotkey)
    elif monster_count < 2 and equipped_ring == 'stealth ring':
        print('Unequip ring')
        client.hotkey(ring_hotkey)

# Cast spell if mana full
def cast_spell(client):
    spell_hotkey = 'v'
    hp_percentage, mp_percentage = client.status_bar.get_percentage()
    if mp_percentage > 98:
        client.hotkey(spell_hotkey)

# Refill ammo using hotkey
def refill_ammo(client):
    refill_hotkey_slot = 21
    refill_hotkey = 'j'

    # Stars
    #ammo_count = client.equips.get_count_item_in_slot('weapon')
    # Arrow
    ammo_count = client.equips.get_count_item_in_slot('ammunition')

    print('Ammo count', ammo_count)
    if ammo_count is None or ammo_count < 80:
        client.hotkey(refill_hotkey)

# Call refill of ammo
def refill_diamond_ammo(client, save_single_target=False):
    refill_hotkey_slot = 21
    refill_hotkey = 'j'

    diamond_hotkey_slot = 20
    diamond_hotkey = 'k'

    ammo_used = client.get_name_item_in_slot(client.equips, 'ammunition')

    # Use crystalline arrow
    if save_single_target:
        monster_list = client.battle_list.get_monster_list(filter_by=client.target_conf.keys())
        monster_count = len(monster_list)
        if monster_count == 1 and client.battle_list.is_targetting():
            if ammo_used != 'crystalline arrows': 
                client.hotkey(refill_hotkey)
            return

    # Use diamond arrows
    diamond_count = client.get_hotkey_item_count(diamond_hotkey_slot)

    # Equip diamond if has diamond arrow and is not equiped
    if diamond_count > 0: 
        if not ammo_used.startswith('diamond arrow'): 
            client.hotkey(diamond_hotkey)
    # Use regular arrows
    else:
        ammo_count = client.equips.get_count_item_in_slot('ammunition')
        if ammo_count is None or ammo_count < 70:
            client.hotkey(refill_hotkey)

def conjure_diamond_arrows(client):
    hp_percentage, mp_percentage = client.status_bar.get_percentage()
    if mp_percentage > 30:
        print('Conjure Diamond Arrows')
        client.hotkey('f4')

def lure_monsters_diamond_arrow(client, count=3, min_count=1, wait=False):
    ammo_used = client.get_name_item_in_slot(client.equips, 'ammunition')
    if ammo_used in ('diamond arrows', 'burst arrows'):
        lure_monsters(client, count, min_count, wait)
    # Regular arrows no lure
    else:
        client.target_on = True

    # Optional hunt distance
    #if monster_count > 2:
    #    for monsters in client.target_conf.values():
    #        monsters['action'] = 'follow'
    #if ammo_used != 'diamond arrows' and monster_count < 3:
    #    for monsters in client.target_conf.values():
    #        monsters['action'] = 'distance'

def lure_monsters(client, count=3, min_count=1, wait=False):
    #monster_count = client.battle_list.get_monster_count()
    monster_list = client.battle_list.get_monster_list(filter_by=client.target_conf.keys())
    monster_count = len(monster_list)
    if not client.target_on and monster_count >= count:
        client.target_on = True
        print('Target on')
    elif client.target_on and monster_count < min_count:
        client.target_on = False
        print('Target off')
    elif wait and (not client.target_on and 0 < monster_count < count):
        creatures_sqm = client.gameboard.get_sqm_monsters()
        if len(creatures_sqm) > 0:
            x, y = zip(*creatures_sqm)
            if any(abs(l) >= 6 for l in x) or any(abs(l) >= 4 for l in y):
                print('Wait lure')
                client.hotkey('esc')
                sleep(0.6)

def equip_ring(client, hotkey='f10', selected_monsters='all', amount=1):
    monster_list = client.battle_list.get_monster_list()
    if selected_monsters != 'all':
        monster_list = [m for m in monster_list if m in selected_monsters]
    monster_count = len(monster_list)
    
    item_name = client.equips.get_item_in_slot('ring')
    print(item_name)

    if monster_count >= amount and item_name == 'unknown':
        print('Equip ring')
        client.hotkey(hotkey)
    elif monster_count < amount and item_name != 'unknown':
        print('Unequip ring')
        client.hotkey(hotkey)

def withdraw_item_from_stash(client, item_name, amount, hotkey_item):
    item_count = client.get_hotkey_item_count(hotkey_item)
    print(item_name, ':', item_count)
    if item_count >= amount:
        print('Already has enough', item_name)
        return True
    client.withdraw_item_from_stash(item_name, amount=amount - item_count)
    # Check if withdraw was succesfull
    item_count = client.get_hotkey_item_count(hotkey_item)
    print(item_name, ':', item_count)
    if item_count >= amount:
        print('Already has enough', item_name)
        return True
    print('Could not withdraw', amount, 'x', item_name, 'from stash')
    return False

def withdraw_item_from_depot_to_backpack(client, item_name, depot_num, backpack_name, amount, hotkey_item, stack=True):
    src = client.open_depot(depot_num)
    if not src:
        print('Could not open depot to withdraw')
        return False

    dest = client.get_container(backpack_name)
    if not dest:
        print('Could not find backpack to hold items')
        return False

    # Open depot num
    client.use_slot(src, depot_num - 1) # open depot_num
    sleep(0.5)

    # Try 5 times to withdraw item
    for i in range(5):
        item_count = client.get_hotkey_item_count(hotkey_item)
        if item_count >= amount:
            client.return_container(src)
            return True

        # Move item from src to dest
        if stack == False:
            for i in range(amount):
                client.take_item_from_slot(src, src_slot=0, dest=dest)
        else:
            while amount > 100:
                client.take_item_from_slot(src, src_slot=0, dest=dest)
                amount -= 100
            client.take_stack_from_slot(src, src_slot=0, dest=dest, amount=amount)
        sleep(0.3)

    client.return_container(src)

    print('Could not withdraw', item_name, '. Make sure this item is in the depot and that the character can hold that amount')
    return False

# Move item or container to stash
def stash_item_from_slot(client, src, src_slot):
    dest = client.open_locker()
    if not dest:
        print('Could not find locker')
        return False

    client.take_item_from_slot(src, src_slot, dest, dest_slot=1)
    return True

# Deposit all items from backpack to depot
def deposit_all_from_backpack_to_depot(client, backpack_name, depot_num):
    items = None
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../scripts/items.json")
    with open(path) as f:
        content = f.read()
        items = json.loads(content)
    if items is None:
        return False

    sort_deposit = client.script_options.get('sort_deposit', dict()) 

    src = client.get_container(backpack_name)
    if not src:
        print('Could not find backpack', backpack_name, 'with items')
        return False

    dest = client.open_depot(max([depot_num, *sort_deposit.values()]))
    if not dest:
        print('Could not open depot to deposit')
        return False

    enter = 0
    tries = 20
    while not src.is_empty() and tries > 0 and enter < 20: 
        tries -= 1
        item_name = client.get_name_item_in_slot(src, 0)
        if item_name != backpack_name.lower():
            depot_dest = depot_num
            for npc in items.keys():
                if item_name in items[npc]:
                    depot_dest = sort_deposit.get(npc, depot_num)
                    break
            client.take_item_from_slot(src, 0, dest, dest_slot=depot_dest - 1)
        else:
            enter += 1
            client.use_slot(src, 0)
            tries = 20
        sleep(0.5)

    if tries < 0 or enter >= 20:
        return False

    for i in range(enter):
        client.return_container(src)
        sleep(0.2)
    return True

def npc_refill(client, mana=False, health=False, ammo=False, rune=False):
    buy_list_names = []
    buy_list_count = []
    if mana:
        mana_count = client.get_hotkey_item_count(client.hunt_config['hotkey_mana_potions'])
        buy_list_names.append(client.hunt_config['mana_name'])
        buy_list_count.append(client.hunt_config['take_mana'] - mana_count)
    if health:
        health_count = client.get_hotkey_item_count(client.hunt_config['hotkey_health_potions'])
        buy_list_names.append(client.hunt_config['health_name'])
        buy_list_count.append(client.hunt_config['take_health'] - health_count)

        if 'hotkey_health_potions2' in client.hunt_config.keys():
            health_count2 = client.get_hotkey_item_count(client.hunt_config['hotkey_health_potions2'])
            buy_list_names.append(client.hunt_config['health_name2'])
            buy_list_count.append(client.hunt_config['take_health2'] - health_count2)
    if rune:
        rune_count = client.get_hotkey_item_count(client.hunt_config['hotkey_runes'])
        buy_list_names.append(client.hunt_config['rune_name'])
        buy_list_count.append(client.hunt_config['take_rune'] - rune_count)
    if ammo:
        ammo_count = client.get_hotkey_item_count(client.hunt_config['hotkey_ammo'])
        buy_list_names.append(client.hunt_config['ammo_name'])
        buy_list_count.append(client.hunt_config['take_ammo'] - ammo_count)

    print('Buying', list(zip(buy_list_names, buy_list_count)))
    success = client.buy_items_from_npc(buy_list_names, buy_list_count)
    if not success:
        print('Failed to buy one or more items')

def check_hunt(client, success, fail, mana=True, health=True, cap=True, rune=False, ammo=False, time=False, other=True):
    mana_check = health_check = cap_check = ammo_check = rune_check = time_check = True
    if mana:
        mana_count = client.get_hotkey_item_count(client.hunt_config['hotkey_mana_potions'])
        mana_check = mana_count > client.hunt_config['mana_leave']
    if health:
        health_count = client.get_hotkey_item_count(client.hunt_config['hotkey_health_potions'])
        health_check = health_count > client.hunt_config['health_leave']
        if 'hotkey_health_potions2' in client.hunt_config.keys():
            health_count2 = client.get_hotkey_item_count(client.hunt_config['hotkey_health_potions2'])
            health_check2 = health_count2 > client.hunt_config['health_leave2']
            health_check = health_check and health_check2
    if rune:
        rune_count = client.get_hotkey_item_count(client.hunt_config['hotkey_runes'])
        rune_check = rune_count > client.hunt_config['rune_leave']
    if ammo:
        ammo_count = client.get_hotkey_item_count(client.hunt_config['hotkey_ammo'])
        ammo_check = ammo_count > client.hunt_config['ammo_leave']
    if cap:
        cap_check = client.get_cap() > client.hunt_config['cap_leave']
    if time:
        cest = timezone('Europe/Berlin')
        time_check = datetime.now(cest).hour not in client.script_options['hours_leave']

    print('Check Hunt results:')
    print('Mana:', mana_check)
    print('Health:', health_check)
    print('Ammo:', ammo_check)
    print('Rune:', rune_check)
    print('Cap:', cap_check)
    print('Time:', time_check)
    if all((mana_check, health_check, cap_check, ammo_check, rune_check, time_check, other)):
        client.jump_label(success)
    else:
        client.jump_label(fail)

def check_time(client, train, repeat):
    cest = timezone('Europe/Berlin')
    hour = datetime.now(cest).hour

    if hour in client.script_options['hours_leave']:
        client.jump_label(train)
    else:
        client.jump_label(repeat)

def check_skill(client):
    skill = client.script_options['skill_train']
    if skill == 'sword':
        client.jump_label('sword')
    elif skill == 'axe':
        client.jump_label('axe')
    elif skill == 'club':
        client.jump_label('club')
    elif skill == 'distance':
        client.jump_label('distance')
    elif skill == 'magic':
        client.jump_label('magic')

def check_supplies(client, mana=True, health=True, cap=True, imbuement=True, rune=False, ammo=False, logout_fail=True):
    mana_check = health_check = cap_check = ammo_check = rune_check = imbuement_check = True
    print('Check Supplies results:')
    if mana:
        mana_count = client.get_hotkey_item_count(client.hunt_config['hotkey_mana_potions'])
        mana_check = mana_count >= 0.9 * client.hunt_config['take_mana']
        print('Mana:', mana_check, mana_count, '/', client.hunt_config['take_mana'])
    if health:
        health_count = client.get_hotkey_item_count(client.hunt_config['hotkey_health_potions'])
        health_check = health_count >= 0.9 * client.hunt_config['take_health']
        print('Health:', health_check, health_count, '/', client.hunt_config['take_health'])
        if 'hotkey_health_potions2' in client.hunt_config.keys():
            health_count2 = client.get_hotkey_item_count(client.hunt_config['hotkey_health_potions2'])
            health_check2 = health_count2 >=  0.9 * client.hunt_config['take_health2']
            health_check = health_check and health_check2
            print('Health2:', health_check2, health_count2, '/', client.hunt_config['take_health2'])
    if rune:
        rune_count = client.get_hotkey_item_count(client.hunt_config['hotkey_runes'])
        rune_check = rune_count >= 0.9 * client.hunt_config['take_rune']
        print('Rune:', rune_check, rune_count, '/', client.hunt_config['take_rune'])
    if cap:
        cap_check = client.get_cap() > 1.1 * client.hunt_config['cap_leave']
        print('Cap:', cap_check, client.get_cap(), '/', client.hunt_config['cap_leave'])
    if ammo:
        ammo_count = client.get_hotkey_item_count(client.hunt_config['hotkey_ammo'])
        ammo_check = ammo_count >= 0.9 * client.hunt_config['take_ammo']
        print('Ammo:', ammo_check, ammo_count, '/', client.hunt_config['take_ammo'])
    if imbuement:
        imbuement_check = check_imbuements(client)
        print('Imbuements:', imbuement_check)

    if not all((mana_check, health_check, ammo_check)):
        import cv2
        cv2.imwrite('hotkey_fail.png', client.img.screen)

    if not (cap_check):
        import cv2
        cv2.imwrite('cap_fail.png', client.img.screen)

    if not all((mana_check, health_check, cap_check, ammo_check, imbuement_check, rune_check)):
        print('Log out')
        client.logout()

# Function to levitate
def levitate(client, direction, hotkey):
    minimap = client.minimap.refresh()
    if minimap is None:
        return 
    map_status = hash(minimap.tostring())

    key = {'south':'s', 'north':'w', 'east':'d', 'west':'a'}[direction]
    sqms = {'south':(0,-1), 'north':(0,1), 'east':(1,0), 'west':(-1,0)}
    sqm = sqms[direction]
    if not client.minimap.is_sqm_walkable(sqm):
        client.press(key)
        sleep(0.5)
        new_minimap = client.minimap.refresh()
        if new_minimap is None:
            return 
        new_map_status = hash(new_minimap.tostring())

        if map_status == new_map_status:
            client.hotkey('ctrl', key)
            sleep(0.3)
            client.hotkey(hotkey)
            sleep(0.3)
    else:
        client.hotkey('ctrl', key)
        sleep(0.3)
        client.hotkey(hotkey)
        sleep(0.3)

def check_imbuements(client):
    if 'imbuements' in client.script_options.keys():
        imbuements = client.script_options['imbuements']
        equip_slots = list(set([imbuement['equip_slot'] for imbuement in imbuements]))
        print('Equip slots:', equip_slots)
        active_imbuements = client.get_imbuements_equips(equip_slots)
        print('Active imbuements:', active_imbuements)

        for imbuement in imbuements:
            equip_slot = imbuement['equip_slot']
            equip_imbuements = active_imbuements[equip_slot]
            if equip_imbuements:
                if imbuement['name'] in equip_imbuements:
                    print(equip_slot, ': imbuement', imbuement['name'], 'active')
                else:
                    print('Equip', imbuement['equip_slot'], 'has no', imbuement['name'], 'active')
                    return False
    return True

def use_imbuing_shrine(client, sqm=(0,1)):
    imbuements = client.script_options['imbuements']
    for imbuement in imbuements:
        print('Checking', imbuement)
        active_imbuements = client.get_imbuements_equip(imbuement['equip_slot'])
        print('Active', active_imbuements)
        if active_imbuements:
            if imbuement['name'] in active_imbuements:
                print('Imbuement', imbuement['name'], 'active')
            else:
                print('Equip', imbuement['equip_slot'], 'has no', imbuement['name'], 'active')
                shrine = client.use_imbuing_shrine(sqm, imbuement['equip_slot'])
                if shrine:
                    shrine.imbue_item(imbuement['type'], imbuement['name'].split()[0])
                else:
                    print('Imbuing shrine not found')





