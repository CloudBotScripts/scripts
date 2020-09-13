''' User defined functions

User defined functions 
These functions can be used in the waypoint actions (actions.py) or during regular intervals (persistent_actions).
'''
import time
from time import sleep
from datetime import datetime
from pytz import timezone
import json
import os, sys, random

# Use hotkey at sqm
def use_hotkey_at_sqm(client, hotkey, sqm):
    print('[Action] Use hotkey', hotkey, 'at', sqm)
    x, y = client.gameboard.sqm_to_coordinate(*sqm)
    client.hotkey(hotkey)
    sleep(0.3)
    client.click(x, y, button='left')
    sleep(1)

# Use item at sqm (item must be assigned to a hotkey in setup.json)
def use_item_at_sqm(client, item_name='sword', sqm=(0,0)):
    hotkey = client.item_hotkeys[item_name]
    use_hotkey_at_sqm(client, hotkey, sqm)

# Use item from backpack to sqm. Item must be visible.
def use_item_from_container_to_sqm(client, item_name='sword', sqm=(0,0)):
    containers = client.get_opened_containers()
    for container in containers:
        num_slots = container.get_num_slots()
        for slot in reversed(range(num_slots)):
            if item_name in container.get_item_in_slot(slot):
                print(f'[Action] Use item {item_name} in sqm {sqm}')
                client.use_slot(container, slot)
                client.move_mouse_sqm(sqm)
                client.click_sqm(*sqm)
                return

# Move item from sqm to backpack.
def get_item_from_sqm(client, sqm=(0,0), dest_container='Backpack'):
    dest = client.get_container(dest_container)
    if not dest:
        print(f'[Action] Could not find backpack {dest_container} to hold items')
    client.get_item_from_sqm(sqm, dest)

# Drop item from backpack to sqm. Item must be visible.
# use stack=True to drop a single item of the stack
def drop_item_to_sqm(client, item_name='empty potion flask', stack=False, dest_sqm=(0,0)):
    containers = client.get_opened_containers()
    for container in containers:
        num_slots = container.get_num_slots()
        for slot in reversed(range(num_slots)):
            if item_name in container.get_item_in_slot(slot):
                print('[Action] Dropping vial')
                client.drop_item_from_container(container, slot, stack=stack, sqm=dest_sqm)
                return

# Warning: Do not use with same interval of other persistents like equip_item, refill_ammo...
def drop_items(client, names=[]):
    print('[Action] Call drop items', names)
    monster_count = client.battle_list.get_monster_count()
    if monster_count < 1:
        containers = client.get_opened_containers()
        for container in containers:
            num_slots = container.get_num_slots()
            for slot in reversed(range(num_slots)):
                item_in_slot = container.get_item_in_slot(slot) 
                for name in names:
                    client.heal()
                    if name in item_in_slot:
                        print('[Action] Dropping', name)
                        client.drop_item_from_container(container, slot)
                        client.sleep(0.1, 0.12)

# Drop vials from backpack. Vials must be visible.
# Will drop only if capacity < cap and if there are no monsters on screen.
def drop_vials(client, cap=500, drop_stacks=4):
    monster_count = client.battle_list.get_monster_count()
    if monster_count < 1 and client.get_cap() <= cap:
        containers = client.get_opened_containers()
        for container in containers:
            num_slots = container.get_num_slots()
            for slot in reversed(range(num_slots)):
                if 'empty potion flask' in container.get_item_in_slot(slot):
                    print('[Action] Dropping vial')
                    client.drop_item_from_container(container, slot)
                    sleep(0.3)
                    drop_stacks -= 1
                    if drop_stacks <= 0:
                        break

# Use rune if monsters hit greater than threshold
# rune must be in items
def throw_rune_if_monsters(client, min_mp, rune_name, min_monsters_hit=3, selected_monsters='all', use_with_target_off=True):
    rune_hotkey = client.item_hotkeys.get(rune_name, 'none')
    if rune_hotkey == 'none':
        print(f'[Action] Rune {rune_name} is not configured in items')
    monster_list = client.battle_list.get_monster_list()
    if selected_monsters != 'all':
        selected_monsters = [''.join([c for c in m if c.isalpha()]) for m in selected_monsters]
        monster_list = [m for m in monster_list if m in selected_monsters]

    if len(monster_list) < min_monsters_hit:
        return
    if not use_with_target_off and not client.target_on:
        return

    creatures_sqm = client.gameboard.get_sqm_monsters()
    client.allow_sqms_active_scan(creatures_sqm) 
    reachable_creatures_sqm = [sqm for sqm in creatures_sqm if client.minimap.is_reachable(sqm)]
    best_sqm, monsters_hit = client.find_sqm_max_hit(reachable_creatures_sqm)
    hp_percentage, mp_percentage = client.status_bar.get_percentage()
    if mp_percentage > min_mp and monsters_hit >= min_monsters_hit:
        print(f'[Action] Throw rune {rune_name} in sqm {best_sqm}')
        client.hotkey(rune_hotkey)
        sleep(0.1)
        client.click_sqm(*best_sqm)
    else:
        print(f'[Action] Rune will hit {monsters_hit}')

# Set persistent interval
## Use 999999 or high number to turn off
def set_persistent_interval(client, persistent_alias, interval=60):
    for persistent in client.persistent_actions:
        if persistent.get('alias', 'none') == persistent_alias:
            persistent['interval'] = interval
            break

def set_persistent_args(client, persistent_alias, key, value):
    for persistent in client.persistent_actions:
        if persistent.get('alias', 'none') == persistent_alias:
            persistent['args'][key] = value
            break

# Attack distance until certain amount of monsters on screen, then follow
def set_target_action(client, selected_monsters='all', action='follow'):
    for monster in client.target_conf:
        if selected_monsters == 'all' or monster in selected_monsters:
            client.target_conf[monster]['action'] = action
    print(f'[Action] Set target config of monsters {selected_monsters} to {action}')

# Attack distance if too many monsters on screen
def distance_monster_count_above(client, selected_monsters='all', count=3):
    monster_list = client.battle_list.get_monster_list(filter_by=client.target_conf.keys())
    monster_count = len(monster_list)

    if selected_monsters != 'all':
        selected_monsters = [m.replace(' ', '') for m in selected_monsters]

    follow=True
    for monster in client.target_conf:
        if selected_monsters == 'all' or monster in selected_monsters:
            if monster_count >= count:
                follow=False
                client.target_conf[monster]['action'] = 'distance'
            else:
                client.target_conf[monster]['action'] = 'follow'
    if follow:
        print('[Action] Follow monsters')
    else:
        print('[Action] Distance attack lure')

# Attack distance until certain amount of monsters on screen, then follow
def distance_attack_lure(client, selected_monsters='all', count=4):
    monster_list = client.battle_list.get_monster_list(filter_by=client.target_conf.keys())
    monster_count = len(monster_list)

    if selected_monsters != 'all':
        selected_monsters = [m.replace(' ', '') for m in selected_monsters]


    follow=False
    for monster in client.target_conf:
        if selected_monsters == 'all' or monster in selected_monsters:
            if monster_count >= count:
                follow=True
                client.target_conf[monster]['action'] = 'follow'
            elif monster_count < 1 and not client.battle_list.is_targetting():
                client.target_conf[monster]['action'] = 'distance'
            else:
                return
    if follow:
        print('[Action] Follow monsters')
    else:
        print('[Action] Distance attack lure')

# Cast spell if monsters around
## Monsters_count is deprecated, use monster_count
def cast_spell_if_monsters(client, min_mp, spell_hotkey, monster_count=3, monsters_count=3, selected_monsters='all', dist=1, use_with_target_off=False):
    if monster_count == 3:
        print('[Action] cast_spell_if_monsters monsters_count is deprecated, use monster_count')
        monster_count = monsters_count
    monster_list = client.battle_list.get_monster_list()
    if selected_monsters != 'all':
        selected_monsters = [''.join([c for c in m if c.isalpha()]) for m in selected_monsters]
        monster_list = [m for m in monster_list if m in selected_monsters]

    if len(monster_list) < monster_count:
        return
    if not use_with_target_off and not client.target_on:
        return

    creatures_sqm = client.gameboard.get_sqm_monsters()
    hp_percentage, mp_percentage = client.status_bar.get_percentage()

    if mp_percentage > min_mp and sum(max(abs(x[0]), abs(x[1])) <= dist for x in creatures_sqm) >= monster_count:
        print(f'[Action] Cast spell in hotkey {spell_hotkey}')
        client.hotkey(spell_hotkey)

# Anti paralyze
def anti_paralyze(client, hotkey='f2'):
    conditions = client.condition_bar.get_condition_list()
    if 'paralyzed' in conditions:
        print('[Action] Cast anti paralyze')
        print('[Action] Deprecated, use "use_hotkey_if_condition"')
        client.hotkey(hotkey)

# Anti poison
def anti_poison(client, hotkey='f10'):
    conditions = client.condition_bar.get_condition_list()
    if 'poisoned' in conditions:
        print('[Action] Cast anti poison')
        print('[Action] Deprecated, use "use_hotkey_if_condition"')
        client.hotkey(hotkey)

# Equip dwarven ring then unequip it
def anti_drunk(client, item_equip, item_unequip=None, slot='ring'):
    conditions = client.condition_bar.get_condition_list()

    equip_item_count = client.get_hotkey_item_count(client.items[item_equip])
    equip_hotkey = client.item_hotkeys[item_equip]

    item_name = client.get_name_item_in_slot(client.equips, slot)

    if 'drunk' in conditions:
        if item_name != item_equip and equip_item_count > 0:
            print('[Action] Equip dwarven ring')
            client.hotkey(equip_hotkey)
    else:
        print('[Action] Item equipped', item_name)
        if item_name == item_equip:
            if item_unequip is None:
                print('[Action] Unequip dwarven ring')
                client.hotkey(equip_hotkey)
            else:
                unequip_hotkey = client.item_hotkeys[item_unequip]
                print('[Action] Equip', item_unequip)
                client.hotkey(unequip_hotkey)

# Use hotkey if condition is active
# conditions is one of ['poisoned', 'bleeding', 'cursed', 'mana', 'paralyzed', 'electrified', 'battle', 'haste', 'drunk', 'hungry', 'protected']
def use_hotkey_if_condition(client, hotkey='f10', condition='poisoned'):
    conditions = client.condition_bar.get_condition_list()
    if condition in conditions:
        print(f'[Action] Condition {condition} is active, using hotkey {hotkey}')
        client.hotkey(hotkey)

def wait(client, tmin=1, tmax=1.2):
    client.sleep(tmin, tmax, heal=True)

# Wait until mana is above mana_perc
# If hotkey is none, will not refill mana and some other way to refill mana should be active.
def wait_mana_percentage_below(client, mana_perc, hotkey=None, monster_count_below=1):
    monster_count = client.battle_list.get_monster_count()
    while monster_count < monster_count_below:
        _, mp_percentage = client.status_bar.get_percentage()
        client.heal()
        if mp_percentage > mana_perc:
            return
        if hotkey:
            client.hotkey(hotkey)
            client.sleep(0.5, 0.7)
        client.sleep(0.2, 0.3, heal=True)

def recover_full_mana(client, hotkey='e', monster_count_below=1):
    monster_count = client.battle_list.get_monster_count()
    hp_percentage, mp_percentage = client.status_bar.get_percentage()
    if monster_count < monster_count_below and mp_percentage < 95:
        client.use_potion(hotkey)

# Use hotkey
def use_hotkey(client, hotkey='f11'):
    client.hotkey(hotkey)

# Deprecated, use function use_hotkey
def eat_food(client, hotkey='f11'):
    food_hotkey = hotkey
    client.hotkey(food_hotkey)

# Cast haste
def haste(client, hotkey='v'):
    spell_hotkey = hotkey
    monster_count = client.battle_list.get_monster_count()
    conditions = client.condition_bar.get_condition_list()
    if monster_count < 1 and 'haste' not in conditions:
        client.hotkey(spell_hotkey)

# Equip item
def equip_item(client, hotkey='f10', selected_monsters='all', dist=10, amount=1, slot='ring'):
    monster_list = client.battle_list.get_monster_list()
    if selected_monsters != 'all':
        selected_monsters = [''.join([c for c in m if c.isalpha()]) for m in selected_monsters]
        monster_list = [m for m in monster_list if m in selected_monsters]

    creatures_sqm = client.gameboard.get_sqm_monsters()
    monster_count = len(monster_list)
    if len(creatures_sqm) >= monster_count: # Found all monsters on screen
        near_monster_count = sum(max(abs(x[0]), abs(x[1])) <= dist for x in creatures_sqm)
        monster_count =  min(monster_count, near_monster_count)
    
    item_name = client.equips.get_item_in_slot(slot)

    if monster_count >= amount and item_name == 'none':
        print('[Action] Equip item')
        client.hotkey(hotkey)
    elif monster_count < amount and item_name != 'none':
        print('[Action] Unequip item')
        client.hotkey(hotkey)

# Equip item if conditions, and equip back
def swap_equip(client, item_equip, item_unequip, selected_monsters='all', dist=10, amount=1, slot='ring', hp_perc=100):
    hp_percentage, _ = client.status_bar.get_percentage()

    monster_list = client.battle_list.get_monster_list()
    if selected_monsters != 'all':
        selected_monsters = [''.join([c for c in m if c.isalpha()]) for m in selected_monsters]
        monster_list = [m for m in monster_list if m in selected_monsters]

    creatures_sqm = client.gameboard.get_sqm_monsters()
    print('Monsters:', monster_list)
    monster_count = len(monster_list)
    if len(creatures_sqm) >= monster_count: # Found all monsters on screen
        near_monster_count = sum(max(abs(x[0]), abs(x[1])) <= dist for x in creatures_sqm)
        monster_count =  min(monster_count, near_monster_count)
    
    equip_item_count = client.get_hotkey_item_count(client.items[item_equip])
    equip_hotkey = client.item_hotkeys[item_equip]

    unequip_hotkey = client.item_hotkeys[item_unequip]

    item_name = client.equips.get_item_in_slot(slot)
    if monster_count >= amount and equip_item_count > 0 and hp_percentage < hp_perc and item_name != item_equip:
        print(f'[Action] Equip item {item_name}')
        client.hotkey(equip_hotkey)
    elif monster_count < amount and item_name != item_unequip:
        print(f'[Action] Unequip item {item_name}')
        client.hotkey(unequip_hotkey)

# Cast spell if mana full
def cast_spell(client, hotkey='v', min_mp=98):
    spell_hotkey = hotkey
    hp_percentage, mp_percentage = client.status_bar.get_percentage()
    if mp_percentage > min_mp:
        client.hotkey(spell_hotkey)

# Refill ammo using hotkey
def refill_ammo(client, ammo_name="arrow", equip_slot="ammunition", min_amount=80):
    refill_hotkey_slot = client.items[ammo_name]
    refill_hotkey = client.item_hotkeys[ammo_name]

    # Stars
    #ammo_count = client.equips.get_count_item_in_slot('weapon')
    # Arrow
    ammo_count = client.equips.get_count_item_in_slot(equip_slot)

    print('[Action] Ammo count', ammo_count)
    if ammo_count is None or ammo_count < min_amount:
        client.hotkey(refill_hotkey)

# Refill ammo using hotkey
def refill_priority_ammo(client, priority_ammo_name="spectral bolt", regular_ammo_name="infernal bolt", equip_slot="ammunition", min_amount=20):
    priority_ammo_slot = client.items[priority_ammo_name]
    priority_ammo_hotkey = client.item_hotkeys[priority_ammo_name]

    ammo_used = client.get_name_item_in_slot(client.equips, equip_slot)

    priority_ammo_count = client.get_hotkey_item_count(priority_ammo_slot)
    print(f'[Action] {priority_ammo_name} count', priority_ammo_count)
    if priority_ammo_count > 0: 
        if not ammo_used.startswith(priority_ammo_name): 
            print(f'[Action] Equip {priority_ammo_name} into {equip_slot}')
            client.hotkey(priority_ammo_hotkey)
    else:
        # Regular ammo
        ammo_count = client.equips.get_count_item_in_slot(equip_slot)
        print('Regular ammo count', ammo_count)
        if ammo_count is None or ammo_count < min_amount:
            regular_ammo_hotkey = client.item_hotkeys[regular_ammo_name]
            print(f'[Action] Equip {regular_ammo_name} into {equip_slot}')
            client.hotkey(regular_ammo_hotkey)

# Call refill of ammo
def refill_diamond_ammo(client, save_single_target=False):
    crystalline_hotkey_slot = client.items["crystalline arrow"]
    crystalline_hotkey = client.item_hotkeys["crystalline arrow"]
    diamond_hotkey_slot = client.items["diamond arrow"]
    diamond_hotkey = client.item_hotkeys["diamond arrow"]

    ammo_used = client.get_name_item_in_slot(client.equips, 'ammunition')

    # Use crystalline arrow
    if save_single_target:
        monster_list = client.battle_list.get_monster_list(filter_by=client.target_conf.keys())
        monster_count = len(monster_list)
        if monster_count == 1 and client.battle_list.is_targetting():
            if ammo_used != 'crystalline arrows': 
                client.hotkey(crystalline_hotkey)
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
            client.hotkey(crystalline_hotkey)

def conjure_diamond_arrows(client):
    hp_percentage, mp_percentage = client.status_bar.get_percentage()
    if mp_percentage > 30:
        print('[Action] Conjure Diamond Arrows')
        client.hotkey('f4')

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

def lure_monsters(client, count=3, min_count=1, wait=False):
    #monster_count = client.battle_list.get_monster_count()
    monster_list = client.battle_list.get_monster_list(filter_by=client.target_conf.keys())
    monster_count = len(monster_list)
    if not client.target_on and monster_count >= count:
        client.target_on = True
        print('[Action] Target on')
    elif client.target_on and monster_count < min_count:
        client.target_on = False
        print('[Action] Target off')
    elif wait and (not client.target_on and 0 < monster_count < count):
        client.hotkey('esc')
        creatures_sqm = client.gameboard.get_sqm_monsters()
        reachable_creatures_sqm = [sqm for sqm in creatures_sqm if client.minimap.is_reachable(sqm)]
        if len(monster_list) > 0 and len(reachable_creatures_sqm) > 0:
            x, y = zip(*reachable_creatures_sqm)
            if any(abs(l) >= 5 for l in x) or any(abs(l) >= 4 for l in y):
                print('[Action] Wait lure')
                client.heal()
                client.sleep(0.2)

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

def wait_lure(client, direction_movement='all', lure_amount=3, dist=3, max_wait=2, min_left_behind=1):
    def monsters_around(creatures_sqm, dist=2):
        return sum(max(abs(x[0]), abs(x[1])) <= dist for x in creatures_sqm)

    def dist_sqm(sqm):
        return max(abs(sqm[0]), abs(sqm[1]))

    # Indicate how many monsters will be left behind if continue walking. 
    # monsters are left behind if they are opposite to the direction char is going to
    # directions: n, e, s, w
    def monsters_left_behind(creatures_sqm, direction_movement='all'):
        if direction_movement == 'n':
            return sum(m[1] < 0 and dist_sqm(m) > dist for m in creatures_sqm) 
        elif direction_movement == 's':
            return sum(m[1] > 0 and dist_sqm(m) > dist for m in creatures_sqm) 
        elif direction_movement == 'e':
            return sum(m[0] < 0 and dist_sqm(m) > dist for m in creatures_sqm) 
        elif direction_movement == 'w':
            return sum(m[0] > 0 and dist_sqm(m) > dist for m in creatures_sqm) 
        else:
            return len(creatures_sqm)

    wait_start = time.time()
    while time.time() < wait_start + max_wait:
        client.heal()
        creatures_sqm = client.gameboard.get_sqm_monsters()
        reachable_creatures_sqm = [sqm for sqm in creatures_sqm if client.minimap.is_reachable(sqm)]
        m_around = monsters_around(reachable_creatures_sqm, dist=dist)
        if client.battle_list.get_monster_count() < min_left_behind:
            print('[Action] Not enough monsters around to lure')
            break

        if m_around < lure_amount:
            m_left_behind = monsters_left_behind(reachable_creatures_sqm, direction_movement=direction_movement)
            print('[Action] Monsters left behind', m_left_behind)
            if m_left_behind >= min_left_behind:
                print('[Action] Waiting lure')
            else:
                break
        else:
            print(f'[Action] Lured {m_around} monsters')
            break

def withdraw_item_from_stash(client, item_name, amount, hotkey_item=None):
    item_count = client.get_hotkey_item_count(client.items[item_name])
    print(item_name, ':', item_count)
    if item_count >= amount:
        print('[Action] Already has enough', item_name)
        return True
    client.withdraw_item_from_stash(item_name, amount=amount - item_count)
    # Check if withdraw was succesfull
    item_count = client.get_hotkey_item_count(client.items[item_name])
    print(item_name, ':', item_count)
    if item_count >= amount:
        print('[Action] Already has enough', item_name)
        return True
    print('[Action] Could not withdraw', amount, 'x', item_name, 'from stash')
    return False

def withdraw_item_from_depot_to_backpack(client, item_name, depot_num, backpack_name, amount, stack=True):
    src = client.open_depot(depot_num)
    if not src:
        print('[Action] Could not open depot to withdraw')
        return False

    dest = client.get_container(backpack_name)
    if not dest:
        print('[Action] Could not find backpack to hold items')
        return False

    # Open depot num
    client.use_slot(src, depot_num - 1) # open depot_num
    sleep(0.5)

    # Try 5 times to withdraw item
    for i in range(5):
        item_count = client.get_hotkey_item_count(client.items[item_name])
        if item_count >= amount:
            client.return_container(src)
            print('[Action] Withdrawn', item_name)
            return True

        # Move item from src to dest
        if stack == False:
            for i in range(max(0, amount - item_count)):
                client.take_item_from_slot(src, src_slot=0, dest=dest)
                sleep(0.2)
        else:
            while max(0, amount - item_count) > 100:
                client.take_item_from_slot(src, src_slot=0, dest=dest)
                amount -= 100
                sleep(0.1)
            client.take_stack_from_slot(src, src_slot=0, dest=dest, amount=amount - item_count)
            sleep(0.2)
        sleep(0.3)

    client.return_container(src)

    print('[Action] Could not withdraw', item_name, '. Make sure this item is in the depot and that the character can hold that amount')
    return False

# Move item or container to stash
def stash_item_from_slot(client, src, src_slot):
    dest = client.open_locker()
    if not dest:
        print('[Action] Could not find locker')
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
        print('Failed to load item list')
        return False

    sort_deposit = client.script_options.get('sort_deposit', dict()) 

    src = client.get_container(backpack_name)
    if not src:
        print('[Action] Could not find backpack', backpack_name, 'with items')
        return False

    dest = client.open_depot(max([depot_num, *sort_deposit.values()]))
    if not dest:
        print('[Action] Could not open depot to deposit')
        return False

    enter = 0
    tries = 32
    while not src.is_empty() and tries > 0 and enter < 20: 
        tries -= 1
        item_name = client.get_name_item_in_slot(src, 0)
        if item_name != backpack_name.lower():
            depot_dest = depot_num
            for npc in items.keys():
                if item_name in items[npc]:
                    depot_dest = sort_deposit.get(npc, depot_num)
                    break
            print(f'[Action] Deposit item {item_name} to depot {depot_num}')
            client.take_item_from_slot(src, 0, dest, dest_slot=depot_dest - 1)
        else:
            enter += 1
            client.use_slot(src, 0)
            sleep(0.4)
            tries = 32
        sleep(0.4)

    if tries < 0 or enter >= 20:
        return False

    for i in range(enter):
        client.return_container(src)
        sleep(0.4)
    return True

# Will reach npc and say 'hi' already. So don't put 'hi' in list of words.
def talk_npc(client, list_words):
    client.npc_say(list_words)

def npc_refill(client, mana=False, health=False, ammo=False, rune=False, food=False):
    buy_list_names = []
    buy_list_count = []
    if mana:
        mana_name, take_mana = client.hunt_config['mana_name'], client.hunt_config['take_mana']
        mana_count = client.get_hotkey_item_count(client.items[mana_name])
        buy_list_names.append(mana_name)
        buy_list_count.append(take_mana - mana_count)
    if health:
        health_name, take_health = client.hunt_config['health_name'], client.hunt_config['take_health']
        health_count = client.get_hotkey_item_count(client.items[health_name])
        buy_list_names.append(health_name)
        buy_list_count.append(take_health - health_count)

        if 'health_name2' in client.hunt_config.keys():
            health_name2, take_health2 = client.hunt_config['health_name2'], client.hunt_config['take_health2']
            health_count2 = client.get_hotkey_item_count(client.items[health_name2])
            buy_list_names.append(health_name2)
            buy_list_count.append(take_health2 - health_count2)
    if rune:
        rune_name, take_rune = client.hunt_config['rune_name'], client.hunt_config['take_rune']
        rune_count = client.get_hotkey_item_count(client.items[rune_name])
        buy_list_names.append(rune_name)
        buy_list_count.append(take_rune - rune_count)

        if 'rune_name2' in client.hunt_config.keys():
            rune_name2, take_rune2 = client.hunt_config['rune_name2'], client.hunt_config['take_rune2']
            rune_count2 = client.get_hotkey_item_count(client.items[rune_name2])
            buy_list_names.append(rune_name2)
            buy_list_count.append(take_rune2 - rune_count2)
    if ammo:
        ammo_name, take_ammo = client.hunt_config['ammo_name'], client.hunt_config['take_ammo']
        ammo_count = client.get_hotkey_item_count(client.items[ammo_name])
        buy_list_names.append(ammo_name)
        buy_list_count.append(take_ammo - ammo_count)
        
    if food:
        food_name, take_food = client.hunt_config['food_name'], client.hunt_config['take_food']
        food_count = client.get_hotkey_item_count(client.items[food_name])
        buy_list_names.append(food_name)
        buy_list_count.append(take_food - food_count)

    print('[Action] Buying', list(zip(buy_list_names, buy_list_count)))
    say = None
    if (mana or health) and not rune and not ammo and not food:
        print('[Action] Buying only potions')
        say = ['potions']
    elif rune and not mana and not health and not ammo and not food:
        print('[Action] Buying only runes')
        say = ['runes']
    success = client.buy_items_from_npc(buy_list_names, buy_list_count, say=say)
    if not success:
        print('[Action] Failed to buy one or more items')

def buy_items_npc(client, item_list_name, item_list_count):
    print('[Action] Buying', list(zip(item_list_name, item_list_count)))
    success = client.buy_items_from_npc(item_list_name, item_list_count)
    if not success:
        print('[Action] Failed to buy one or more items')

def use_imbuing_shrine(client, sqm=None):
    imbuements = client.script_options['imbuements']
    for imbuement in imbuements:
        print('[Action] Checking', imbuement)
        active_imbuements = client.get_imbuements_equip(imbuement['equip_slot'])
        print('Active', active_imbuements)
        if active_imbuements:
            if imbuement['name'] in active_imbuements:
                print('Imbuement', imbuement['name'], 'active')
            else:
                print('Equip', imbuement['equip_slot'], 'has no', imbuement['name'], 'active')
                shrine = client.use_imbuing_shrine(imbuement['equip_slot'], sqm=sqm)
                if shrine:
                    shrine.imbue_item(imbuement['type'], imbuement['name'].split()[0])
                else:
                    print('Imbuing shrine not found')

def time_leave(client):
    cest = timezone('Europe/Berlin')
    now = datetime.now(cest)
    print('Current time', now)
    for h in client.script_options.get('hours_leave', []):
        hour_leave = datetime(now.year, now.month, now.day, round(h - (h%1)), round(60 * (h % 1)), 0, tzinfo=now.tzinfo)
        delta_mins = (now - hour_leave).total_seconds() / 60
        if 0 < delta_mins < 60:
            print('Now:', now, 'Leave check:', hour_leave)
            return True
    return False

def check(client, mana=True, health=True, cap=True, rune=False, ammo=False, time=False, other=True):
    mana_check = health_check = cap_check = ammo_check = rune_check = time_check = True
    if mana:
        mana_name, take_mana = client.hunt_config['mana_name'], client.hunt_config['take_mana']
        mana_count = client.get_hotkey_item_count(client.items[mana_name])
        mana_check = mana_count > client.hunt_config['mana_leave']
    if health:
        health_name, take_health = client.hunt_config['health_name'], client.hunt_config['take_health']
        health_count = client.get_hotkey_item_count(client.items[health_name])
        health_check = health_count > client.hunt_config['health_leave']
        if 'health_name2' in client.hunt_config.keys():
            health_name2, take_health2 = client.hunt_config['health_name2'], client.hunt_config['take_health2']
            health_count2 = client.get_hotkey_item_count(client.items[health_name2])
            health_check2 = health_count2 > client.hunt_config['health_leave2']
            health_check = health_check and health_check2
    if rune:
        rune_name, take_rune = client.hunt_config['rune_name'], client.hunt_config['take_rune']
        rune_count = client.get_hotkey_item_count(client.items[rune_name])
        rune_check = rune_count > client.hunt_config['rune_leave']
        if 'rune_name2' in client.hunt_config.keys():
            rune_name2, take_rune2 = client.hunt_config['rune_name2'], client.hunt_config['take_rune2']
            rune_count2 = client.get_hotkey_item_count(client.items[rune_name2])
            rune_check2 = rune_count2 > client.hunt_config['rune_leave2']
            rune_check = rune_check and rune_check2
    if ammo:
        ammo_name, take_ammo = client.hunt_config['ammo_name'], client.hunt_config['take_ammo']
        ammo_count = client.get_hotkey_item_count(client.items[ammo_name])
        ammo_check = ammo_count > client.hunt_config['ammo_leave']
    if cap:
        cap_check = client.get_cap() > client.hunt_config['cap_leave']
    if time:
        time_check = not time_leave(client)

    print('[Action] Check results:')
    print('[Action] Mana:', mana_check)
    print('[Action] Health:', health_check)
    print('[Action] Ammo:', ammo_check)
    print('[Action] Rune:', rune_check)
    print('[Action] Cap:', cap_check)
    print('[Action] Time:', time_check)
    if all((mana_check, health_check, cap_check, ammo_check, rune_check, time_check, other)):
        return True
    return False

def check_hunt(client, success, fail=None, mana=True, health=True, cap=True, rune=False, ammo=False, time=False, other=True):
    mana=mana and 'mana_name' in client.hunt_config.keys()
    health=health and 'health_name' in client.hunt_config.keys()
    ammo=ammo and 'ammo_name' in client.hunt_config.keys()
    rune=rune and 'rune_name' in client.hunt_config.keys()
    if check(client, mana, health, cap, rune, ammo, time, other):
        client.jump_label(success)
    elif fail:
        client.jump_label(fail)

def check_time(client, train, repeat):
    cest = timezone('Europe/Berlin')
    if time_leave(client):
        print('[Action] Go train')
        client.jump_label(train)
    else:
        print('[Action] Skip train', datetime.now(cest), 'not in hours_leave:', client.script_options['hours_leave'])
        client.jump_label(repeat)

# Add vip members to a group called "Blacklist" and hide offline vips
# Will jump label if any player in group Blacklist is appearing
def check_blacklist_player_online(client, label_jump):
    result = client.get_windows_by_names(['VIP'])
    if result:
        vip = result[0]
        if 'Blacklist' in vip.recognize_text_content():
            print('[Action] Players in blacklist are online')
            print('[Action] Jump label:', label_jump)
            client.jump_label(label_jump)
    else:
        print('[Action] Could not find VIP window')

# Target off if monster on screen
## Retro safe must be on
def stop_target_player_on_screen(client):
    if not client.retro_safe:
        print('[Action] Retro safe must be set to true')
        return
    if client.target_on and client.retro_safe and client.player_battle_list.has_creature():
        print('[Action] Stop target 2s due to player on screen')
        if client.battle_list.is_targetting():
            client.hotkey('esc')
            sleep(0.1)
        client.attack_timeout = time.time() + 2

def check_kill_count(client, monster_name, kill_amount, label_jump, label_skip):
    result = client.get_windows_by_names(['QuestTracker'])
    if result:
        tracker = result[0]
        tracker_text = tracker.recognize_text_content()
        if monster_name in tracker_text:
            print('[Action] Monster found')
            print('Tracker_Text:', tracker_text)
            current_killcount = tracker_text[tracker_text.find("hunted")+6:tracker_text.find(kill_amount, tracker_text.find(monster_name)-len(kill_amount), tracker_text.find(monster_name))]
            print('[Action] Hunted ', current_killcount, '/', str(kill_amount), ' ', monster_name)
            if int(current_killcount) > int(kill_amount):
                print('[Action] Kill Count reached, Jump label:', label_jump)
                client.jump_label(label_jump)
            else:
                print('[Action] Kill Count not reached, Jump label:', label_skip)
                client.jump_label(label_skip)
        else:
            print('[Action] Could not find Monster Name')
    else:
        print('[Action] Could not find Quest Tracker window')

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
    client.turn_chat_off()
    mana_check = health_check = cap_check = ammo_check = rune_check = imbuement_check = True
    print('[Action] Check Supplies results:')
    if mana:
        mana_name, take_mana = client.hunt_config['mana_name'], client.hunt_config['take_mana']
        mana_count = client.get_hotkey_item_count(client.items[mana_name])
        mana_check = mana_count >= 0.9 * take_mana
        print('[Action] Mana:', mana_check, mana_count, '/', take_mana)
    if health:
        health_name, take_health = client.hunt_config['health_name'], client.hunt_config['take_health']
        health_count = client.get_hotkey_item_count(client.items[health_name])
        health_check = health_count >= 0.9 * take_health
        print('[Action] Health:', health_check, health_count, '/', take_health)
        if 'health_name2' in client.hunt_config.keys():
            health_name2, take_health2 = client.hunt_config['health_name2'], client.hunt_config['take_health2']
            health_count2 = client.get_hotkey_item_count(client.items[health_name2])
            health_check2 = health_count2 >=  0.9 * take_health2
            health_check = health_check and health_check2
            print('[Action] Health2:', health_check2, health_count2, '/', take_health2)
    if rune:
        rune_name, take_rune = client.hunt_config['rune_name'], client.hunt_config['take_rune']
        rune_count = client.get_hotkey_item_count(client.items[rune_name])
        rune_check = rune_count >= 0.9 * take_rune
        print('[Action] Rune:', rune_check, rune_count, '/', take_rune)
        if 'rune_name2' in client.hunt_config.keys():
            rune_name2, take_rune2 = client.hunt_config['rune_name2'], client.hunt_config['take_rune2']
            rune_count2 = client.get_hotkey_item_count(client.items[rune_name2])
            rune_check2 = rune_count2 >=  0.9 * take_rune2
            rune_check = rune_check and rune_check2
            print('[Action] Rune2:', rune_check2, rune_count2, '/', take_rune2)
    if cap:
        cap_check = client.get_cap() > client.hunt_config['cap_leave']
        print('[Action] Cap:', cap_check, client.get_cap(), '/', client.hunt_config['cap_leave'])
    if ammo:
        ammo_name, take_ammo = client.hunt_config['ammo_name'], client.hunt_config['take_ammo']
        ammo_count = client.get_hotkey_item_count(client.items[ammo_name])
        ammo_check = ammo_count >= 0.9 * take_ammo
        print('[Action] Ammo:', ammo_check, ammo_count, '/', take_ammo)
    if imbuement:
        imbuement_check = check_imbuements(client)
        print('[Action] Imbuements:', imbuement_check)

    if not all((mana_check, health_check, cap_check, ammo_check, imbuement_check, rune_check)):
        print('[Action] Log out, missing supplies')
        client.logout()

def check_imbuements(client):
    if 'imbuements' in client.script_options.keys():
        imbuements = client.script_options['imbuements']
        if len(imbuements) < 1:
            return True
        equip_slots = list(set([imbuement['equip_slot'] for imbuement in imbuements]))
        print('Equip slots:', equip_slots)
        active_imbuements = client.get_imbuements_equips(equip_slots)
        print('Active imbuements:', active_imbuements)

        for imbuement in imbuements:
            client.heal()
            client.sleep(0.3, 0.4)
            equip_slot = imbuement['equip_slot']
            equip_imbuements = active_imbuements.get(equip_slot, None)
            if equip_imbuements:
                if imbuement['name'] in equip_imbuements:
                    print(equip_slot, ': imbuement', imbuement['name'], 'active')
                else:
                    print('Equip', imbuement['equip_slot'], 'has no', imbuement['name'], 'active')
                    return False
    return True

def stop_target_no_supplies(client, mana=True, health=True, cap=True, rune=False, ammo=False, time=False, other=True):
    if check(client, mana, health, cap, rune, ammo, time, other):
        if not client.target_on:
            print('[Action] Start target supplies ok')
            client.target_on = True
    else:
        if client.target_on:
            print('[Action] Stop target no supplies')
            client.target_on = False

# Stop looting
def stop_looting(client, selected_monsters='all', cap=0):
    print('[Action] stop_looting')

    if selected_monsters != 'all':
        selected_monsters = [m.replace(' ', '') for m in selected_monsters]

    for monster in client.target_conf:
        if selected_monsters == 'all' or monster in selected_monsters:
            print('[Action] {} in selected_monsters list'.format(monster))
            if client.get_cap() > cap:
                client.target_conf[monster]['loot'] = True
            else:
                client.target_conf[monster]['loot'] = False

# Jump to label
def jump_to_label(client, label):
  print('[Action] Jump to label:', label)
  client.jump_label(label)

# Jump random label
# Ex: call jump_to_random_label("labels":["label1", "label2"])
def jump_to_random_label(client, labels):
  label = random.choice(labels)
  print('[Action] Jump to random label:', label)

  client.jump_label(label)

# Conditional jump monsters on screen
# selected_monsters is 'all' or a list e.g. ['Tarantula', 'Giant Spider']
def conditional_jump_monsters_on_screen(client, label_jump, label_skip=None, selected_monsters='all', amount=1, turn_target_off=False):
    monster_list = client.battle_list.get_monster_list()
    if selected_monsters != 'all':
        monster_list = [m for m in monster_list if m in selected_monsters]
    monster_count = len(monster_list)
    if monster_count >= amount:
        print('[Action] Jump due to monsters on screen ', label_jump)
        if turn_target_off:
            client.target_on = False
        client.jump_label(label_jump)
    elif label_skip:
        print('[Action] Skip jump, not enough monsters on screen', label_skip)
        client.jump_label(label_skip)

# Conditional jump using script_options variable value
def conditional_jump_script_options_value(client, var_name, label_jump_map):
    value = client.script_options.get(var_name, False)
    if value:
        print(f'[Action] Value of variable {var_name} is {value}')
        if value not in label_jump_map:
            print(f'[Action] Value {value} is not on label_jump_map')
            client.jump_label(label_jump_map[value])
    else:
        print('[Action] Variable {var_name} does not exist')

# Conditional jump using script_options variable true or false
def conditional_jump_script_options(client, var_name, label_jump, label_skip=None):
    if client.script_options.get(var_name, False):
        print('[Action] true condition jump to ', label_jump)
        client.jump_label(label_jump)
    elif label_skip:
        print('[Action] false condition jump to ', label_skip)
        client.jump_label(label_skip)
    # else, just continues to next waypoint

# Conditional jump if character pos is in coords list 
def conditional_jump_position(client, coords, label_jump, label_skip=None):
    cur_coord = client.minimap.get_current_coord()
    print(f'[Action] current coord {cur_coord}')
    if cur_coord not in ('Unreachable', 'Out of range'):
        if list(cur_coord) in coords:
            print(f'[Action] current coord {cur_coord} is in list')
            client.jump_label(label_jump)
        elif label_skip:
            print(f'[Action] current coord {cur_coord} is not in list')
            client.jump_label(label_skip)

# Conditional jump if character pos is in coords list 
def conditional_jump_floor(client, floor, label_jump, label_skip=None):
    cur_floor = client.minimap.get_floor()
    if cur_floor == floor:
        print('[Action] current floor is', floor)
        client.jump_label(label_jump)
    elif label_skip:
        print('[Action] current floor is not', floor)
        client.jump_label(label_skip)

# Conditional jump if item count == x
def conditional_jump_item_count(client, item_name, amount, label_jump, label_skip=None):
    item_count = client.get_hotkey_item_count(client.items[item_name])
    if item_count == amount:
        print('[Action] {} count is {}'.format(item_name, amount))
        client.jump_label(label_jump)
    elif label_skip:
        print('[Action] {} count is not {}'.format(item_name, amount))
        client.jump_label(label_skip)

# Conditional jump if item count < x
def conditional_jump_item_count_below(client, item_name, amount, label_jump, label_skip=None):
    item_count = client.get_hotkey_item_count(client.items[item_name])
    if item_count < amount:
        print('[Action] {} count is {}'.format(item_name, amount))
        client.jump_label(label_jump)
    elif label_skip:
        print('[Action] {} count is not {}'.format(item_name, amount))
        client.jump_label(label_skip)

# Conditional jump if level > x
def conditional_jump_level_above(client, lvl, label_jump, label_skip=None):
    level = client.get_level()
    if level > lvl:
        print('[Action] Level {} reached. Jumping to label {}'.format(lvl, label_jump))
        client.jump_label(label_jump)
    elif label_skip:
        print('[Action] Level {} not reached. Jumping to label {}'.format(lvl, label_skip))
        client.jump_label(label_skip)

# Alert if player on screen (will send max one alert every 5 mins)
## Retro safe must be on
def alert_player_on_screen(client):
    if not client.retro_safe:
        print('[Action] Retro safe must be set to true')
        return
    if client.retro_safe and client.player_battle_list.has_creature():
        if time.time() > client.last_alert_time + 5:
            print('[Action] Player on screen, sending alert')
            players = ', '.join(client.player_battle_list.get_player_list())
            client.send_alert_message(f"Player on screen: {players}")

# Blacklist coords so that bot think it is a wall.
# coords_barrier is a list of barriers [[x,y,z],[x2,y2,z2],...]
def blacklist_coords(client, coords_barrier):
    client.minimap.add_barrier_coords(coords_barrier)

# Wall activates only during target for distance hunting. The block_side indicates which side of the barrier blocks.
# If target crosses barrier, will disable barrier to continue targeting
# Example: target_wall([x,y,z], 3, 1): wall starting in (x,y,z) with 3 sqm width that blocks from both sides
#   target_wall([x,y,z], height=3): wall starting in (x,y,z) with default 1sqm wigth and 3 sqm height that blocks from both sides
#   target_wall([x,y,z], 2, 3): wall starting in (x,y,z) with 2 sqm width and  3 sqm height
#   target_wall([x,y,z], 1, 3, block_side='east'): wall starting in (x,y,z) with 1 sqm width and  3 sqm height that 
#      blocks player coming from right (east) to left (west)  | <---
def target_wall(client, barrier_coord, width=1, height=1, block_side='all'):
    cur_coord = client.minimap.get_current_coord()
    if cur_coord in ('Unreachable', 'Out of range'):
        return
    if cur_coord[2] != barrier_coord[2]:
        return
    target_coord = client.get_target_coord()
    if not target_coord or target_coord in ('Unreachable', 'Out of range'):
        return

    def block_west(c): 
        return c[0] < barrier_coord[0]
    def block_east(c): 
        return c[0] >= barrier_coord[0] + width 
    def block_south(c): 
        return c[1] > barrier_coord[1]
    def block_north(c): 
        return c[1] <= barrier_coord[1] - height

    activate = False
    if block_side in ('east', 'all'):
        activate |= (block_east(cur_coord) and block_east(target_coord))
    if block_side in ('north', 'all'):
        activate |= (block_north(cur_coord) and block_north(target_coord))
    if block_side in ('west', 'all'):
        activate |= (block_west(cur_coord) and block_west(target_coord))
    if block_side in ('south', 'all'):
        activate |= (block_south(cur_coord) and block_south(target_coord))

    x,y,z = barrier_coord
    barriers = [[x+dx,y-dy,z] for dy in range(height) for dx in range(width)]
    if activate:
        client.minimap.add_barrier_coords(barriers)
    else:
        client.minimap.remove_barrier_coords(barriers)

# Add barriers if char is inside area defined by top_left, bottom_right
# Careful not to overlap barriers with other calls of this function
def dynamic_barrier(client, top_left, bottom_right, coords_barrier, monster_count=2):
    if not client.battle_list.is_targetting():
        return
    m_count = client.battle_list.get_monster_count()
    cur_coord = client.minimap.get_current_coord()
    if cur_coord not in ('Unreachable', 'Out of range'):
        x,y,z = cur_coord
        if z == top_left[2] and (top_left[0] < x < bottom_right[0]) and (top_left[1] < y < bottom_right[1]) and m_count >= monster_count:
            client.minimap.add_barrier_coords(coords_barrier)
        else:
            client.minimap.remove_barrier_coords(coords_barrier)

# Add barriers that activate given monster count
# Careful not to overlap barriers with other calls of this function
def dynamic_barrier_coords(client, coords_barrier, monster_count=2):
    if not client.battle_list.is_targetting():
        return
    m_count = client.battle_list.get_monster_count()
    cur_coord = client.minimap.get_current_coord()
    if m_count >= monster_count:
        client.minimap.add_barrier_coords(coords_barrier)
    else:
        client.minimap.remove_barrier_coords(coords_barrier)

# Add barriers in the border of the rectangles. rectangles is a list with top left and bottom right of the rectangles.
def dynamic_barrier_rectangles(client, rectangles, monster_count=2, allow_in=False):
    cur_coord = client.minimap.get_current_coord()
    if cur_coord in ('Unreachable', 'Out of range'):
        return

    monster_list = client.battle_list.get_monster_list(filter_by=client.target_conf.keys())
    m_count = len(monster_list)

    def inside_barrier(top_left, bottom_right):
        char_inside = (cur_coord[0] > top_left[0] and cur_coord[0] < bottom_right[0] and cur_coord[1] > top_left[1] and cur_coord[1] < bottom_right[1])
        if char_inside:
            print('Character inside', top_left, bottom_right)
        return char_inside

    activate = False
    coords_barrier = []
    for top_left, bottom_right in rectangles:
        if cur_coord[2] != top_left[2]:
            continue

        # Activate barrier if allow_in is disabled
        if inside_barrier(top_left, bottom_right) or not allow_in:
            activate = True
        z = top_left[2]
        for x in range(top_left[0], bottom_right[0] + 1):
            for y in (top_left[1], bottom_right[1]):
                coords_barrier.append((x,y,z))
        for y in range(top_left[1], bottom_right[1] + 1):
            for x in (top_left[0], bottom_right[0]):
                coords_barrier.append((x,y,z))

    if client.battle_list.is_targetting() and m_count >= monster_count and activate:
        if activate:
            print('Activate barriers')
        client.minimap.add_barrier_coords(coords_barrier)
    else:
        client.minimap.remove_barrier_coords(coords_barrier)
