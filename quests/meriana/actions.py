import sys
sys.path.append('../scripts/')
from lib import *
import global_actions

def waypoint_action(client, action):
    if action == "buy_rake":
        client.buy_items_from_npc(['rake'], [1])

    elif action == "buy_poem":
        client.npc_say(["love poem", 'yes'])

    elif action == "ring":
        client.npc_say(["ring", 'yes'])

    elif action == "use_rake_north":
        use_item_at_sqm(client, 'rake', (0,1))

    elif action == "give_ring":
        client.npc_say(["ring", 'yes', 'yes', 'yes'])

    elif action == "errand":
        client.npc_say(["errand", 'yes'])

    elif action == "peg_leg":
        client.npc_say(["errand", 'peg leg', 'yes'])

    elif action == "travel_meriana":
        client.npc_say(['peg leg', 'yes'])

    elif action == "raymond":
        client.npc_say(['eleonore', 'mermaid'])

    elif action == "mermaid":
        client.npc_say(['raymond striker'])

    elif action == "djinn":
        client.npc_say(['eleonore', 'mermaid', 'date', 'yes'])

    elif action == "mermaid2":
        client.npc_say(['date'])

    elif action == "djinn2":
        client.npc_say(['mermaid', 'love poem', 'yes'])

    elif action == "finish":
        client.npc_say(['raymond striker', 'mermaid'])

    else:
        global_actions.waypoint_action(client, action)
