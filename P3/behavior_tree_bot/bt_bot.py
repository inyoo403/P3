#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import spread, attack
from behavior_tree_bot.checks import if_neutral_planet_available
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

def setup_behavior_tree():
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    # Spread to neutral planets if available
    spread_plan = Sequence(name='Spread Strategy')
    neutral_check = Check(if_neutral_planet_available)
    spread_action = Action(spread)
    spread_plan.child_nodes = [neutral_check, spread_action]

    # Otherwise, attack the enemy
    attack_action = Action(attack)

    root.child_nodes = [spread_plan, attack_action]

    logging.info('\n' + root.tree_to_string())
    return root


# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
