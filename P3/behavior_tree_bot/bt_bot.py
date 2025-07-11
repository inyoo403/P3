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

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# 고급 전략을 가진 새로운 BT - 모든 opponent_bots를 이기도록 설계
def setup_behavior_tree():

    # 최상위 전략 선택기
    root = Selector(name='Master Strategic Controller')

    # 1. 긴급 방어 전략 (최우선)
    emergency_defense = Sequence(name='Emergency Defense Protocol')
    under_attack_check = Check(under_attack)
    defend_action = Action(defend_weakest_planet)
    emergency_defense.child_nodes = [under_attack_check, defend_action]

    # 2. 압도적 우위 시 적극적 다중 공격
    overwhelming_attack = Sequence(name='Overwhelming Assault')
    overwhelming_check = Check(have_overwhelming_advantage)
    multi_attack_action = Action(aggressive_multi_attack)
    overwhelming_attack.child_nodes = [overwhelming_check, multi_attack_action]

    # 3. 기회주의적 공격 (적 함대가 비어있을 때)
    opportunistic_strike = Sequence(name='Opportunistic Strike')
    no_enemy_fleets_and_weak_enemy = Sequence(name='Perfect Attack Opportunity')
    weak_enemy_check = Check(weak_enemy_exists)
    opportunistic_action = Action(opportunistic_attack)
    no_enemy_fleets_and_weak_enemy.child_nodes = [weak_enemy_check, opportunistic_action]
    opportunistic_strike.child_nodes = [no_enemy_fleets_and_weak_enemy]

    # 4. 방어가 필요한 상황에서의 방어 강화
    defensive_reinforcement = Sequence(name='Defensive Reinforcement')
    need_defense_check = Check(should_defend_planet)
    multiple_planets_check = Check(have_multiple_planets)
    reinforce_action = Action(reinforce_front_line)
    defensive_reinforcement.child_nodes = [need_defense_check, multiple_planets_check, reinforce_action]

    # 5. 게임 초기 전략적 확장
    early_game_strategy = Selector(name='Early Game Strategy')
    
    # 5a. 게임 초기 + 수익성 높은 중립 행성 확장
    early_expansion = Sequence(name='Early Strategic Expansion')
    early_game_check = Check(early_game)
    profitable_neutral_check = Check(profitable_neutral_exists)
    strategic_spread_action = Action(strategic_spread)
    early_expansion.child_nodes = [early_game_check, profitable_neutral_check, strategic_spread_action]
    
    # 5b. 게임 초기 + 일반 중립 행성 확장
    early_normal_expansion = Sequence(name='Early Normal Expansion')
    early_game_check2 = Check(early_game)
    neutral_available_check = Check(if_neutral_planet_available)
    normal_spread_action = Action(spread_to_weakest_neutral_planet)
    early_normal_expansion.child_nodes = [early_game_check2, neutral_available_check, normal_spread_action]
    
    early_game_strategy.child_nodes = [early_expansion, early_normal_expansion]

    # 6. 중후반 전략 (우위 상황)
    mid_late_game_strategy = Selector(name='Mid-Late Game Strategy')
    
    # 6a. 함대 우위 + 공격적 확장
    aggressive_expansion = Sequence(name='Aggressive Expansion')
    can_expand_check = Check(can_aggressive_expand)
    smart_attack_action = Action(smart_attack_calculation)
    aggressive_expansion.child_nodes = [can_expand_check, smart_attack_action]
    
    # 6b. 적이 가까이 있을 때 적극적 공격
    nearby_enemy_attack = Sequence(name='Nearby Enemy Assault')
    enemy_nearby_check = Check(enemy_nearby)
    largest_fleet_check = Check(have_largest_fleet)
    smart_attack_action2 = Action(smart_attack_calculation)
    nearby_enemy_attack.child_nodes = [enemy_nearby_check, largest_fleet_check, smart_attack_action2]
    
    # 6c. 일반적인 우위 상황 공격
    standard_advantage_attack = Sequence(name='Standard Advantage Attack')
    largest_fleet_check2 = Check(have_largest_fleet)
    smart_attack_action3 = Action(smart_attack_calculation)
    standard_advantage_attack.child_nodes = [largest_fleet_check2, smart_attack_action3]
    
    mid_late_game_strategy.child_nodes = [aggressive_expansion, nearby_enemy_attack, standard_advantage_attack]

    # 7. 기본 확장 전략 (중립 행성이 있을 때)
    basic_expansion = Sequence(name='Basic Expansion Strategy')
    neutral_available_check2 = Check(if_neutral_planet_available)
    strategic_spread_action2 = Action(strategic_spread)
    basic_expansion.child_nodes = [neutral_available_check2, strategic_spread_action2]

    # 8. 최후의 수단 - 기본 공격
    fallback_attack = Action(attack_weakest_enemy_planet)

    # 전체 BT 구조 조립
    root.child_nodes = [
        emergency_defense,           # 1. 긴급 방어
        overwhelming_attack,         # 2. 압도적 우위 공격
        opportunistic_strike,        # 3. 기회주의적 공격
        defensive_reinforcement,     # 4. 방어 강화
        early_game_strategy,         # 5. 게임 초기 전략
        mid_late_game_strategy,      # 6. 중후반 전략
        basic_expansion,             # 7. 기본 확장
        fallback_attack              # 8. 최후의 수단
    ]

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
