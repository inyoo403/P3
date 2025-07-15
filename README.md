# P3 Behavior Trees for Plant Wars

## Overview
Python AI bot that plays, a strategy game, Planet Wars. The objective of the game is to conquer planets using ships. The bot uses our implmented Behavior Trees for context awareness and structured decisions in real time. The game is implented in java with our behavior tree in Python.

## Project Structure
Behavior_tree_bot -> bt_bot.py, behaviors.py, checks.py, 
</br>bt_nodes.py
</br>planet_wars.py
</br>run.py

## Behavior.py (explanation)
attack_weakest_enemy_planet(state)
</br>Attacks the enemy planet with the fewest ships using half the ships from player 1 strongest planet, but only if no fleet is already in flight. 
</br></br>

spread_to_weakest_neutral_planet(state)
</br>Sends ships to conquer the weakest neutral planet, only if no fleets are already in flight. 
</br></br>

smart_attack_calculation(state)
</br>Attacks the most efficient enemy planet by calculating how many ships is need, based on planet growth rate, travel distance, and current number of ships.
</br></br>

defend_weakest_planet(state)
</br>Finds the most vulnerable of player 1 planets and defends against from a stronger planet
</br></br>

aggressive_multi_attack(state)
</br>If there is a stronger advantage, this will cause up to 3 attacks to happen against enemies planets
</br></br>

strategic_spread(state)
</br>Expands to neutral plants with high value
</br></br>

reinforce_front_line(state)
</br>Reinforces front-line planets that are closer to the enemies and weak. 
</br></br>

opportunistic_attack(state)
</br>If the enemy has no fleets in flight, this launches an attack on the easiest enemy planet. 


## bt_bot.py
Defines and executes our behavior tree bot in an strategic behavior in the priority of emergency defense, aggressive attack, opportunistic attack, defensive reinforcement if needed, strategic expansion, mid-late game strategy (fleet advantage+aggressive expansion, aggressive attack, then general advantage situation attack), basic expansion strategy (when neutral planets exist), lastly basic attack.

## checks.py
Contains state-based check functions, returning True or False for each function if the conditions are met. 

basic checks = if_neutral_planet_available(state), have_largest_fleet(state), 

advanced checks = under_attack(state), have_overwhelming_advantage(state), have_multiple_planets(state), enemy_nearby(state), weak_enemy_exists(state), should_defend_planet(state), profitiable_neutral_exists(state), early_game(state), can_aggressive_expand(state),