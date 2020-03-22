#Load Custom functions
import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):

    if action == "check_supplies":
        check_supplies(client, logout_fail=True)

    elif action == "bless_thais":
        client.npc_say(['spiritual', 'yes'])

    elif action == "bless_carlin":
        client.npc_say(['embrace', 'yes'])

    elif action == "bless_abdendriel":
        client.npc_say(['suns', 'yes'])

    elif action == "travel_eremo":
        client.npc_say(['eremo', 'yes'])

    elif action == "bless_eremo":
        client.npc_say(['solitude', 'yes'])

    elif action == "travel_passage":
        client.npc_say(['passage', 'yes'])

    elif action == "buy_ticket":
        client.npc_say(['ticket', 'yes'])

    elif action == "bless_kaz1":
        client.npc_say(['phoenix', 'yes'])

    elif action == "bless_kaz2":
        client.npc_say(['phoenix', 'yes'])

    elif action == "check_enhanced":
        print(client.script_options)
        if client.script_options['enhanced']:
            client.jump_label('enhanced')
        else:
            client.jump_label('go_train_edron')

    elif action == "bless_enhanced":
        client.say('hi')
        client.say('enhanced')
        client.say('yes')

    elif action == "travel_camp":
        client.npc_say(['passage', 'camp', 'yes'])
        client.sleep(2)

    elif action == "check_svargrond_to_camp":
        conditional_jump_position(client, [[32224,31381,7]], label_jump='okolnir_to_camp')
        conditional_jump_position(client, [[32332,31227,7]], label_jump='tyrsung_to_camp')
        conditional_jump_position(client, [[32256,31197,7]], label_jump='svargrond_to_camp')
        conditional_jump_position(client, [[32021,31294,7]], label_jump='in_camp')

    elif action == "travel_back_camp":
        client.npc_say(['passage', 'svargrond', 'yes'])
        client.sleep(2)

    elif action == "check_camp_to_svargrond":
        conditional_jump_position(client, [[32224,31381,7]], label_jump='okolnir_to_svargrond')
        conditional_jump_position(client, [[32332,31227,7]], label_jump='tyrsung_to_svargrond')
        conditional_jump_position(client, [[32021,31294,7]], label_jump='camp_to_svargrond')
        conditional_jump_position(client, [[32256,31197,7]], label_jump='in_svar')

    else:
        global_actions.waypoint_action(client, action)
