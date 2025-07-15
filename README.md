# bt_bot

## 1. Overview

The original bot used a simple attack-and-expand logic. This version has been fully redesigned for strategic adaptability. It evaluates threats, identifies opportunities, and dynamically adjusts its behavior using a multi-layered behavior tree structure.

## 2. Core Features & Enhancements

### bt_bot.py: Behavior Tree Overhaul

The main logic is rebuilt with an 8-level priority-based behavior tree inside the `setup_behavior_tree()` function.  
The root node is:  
`Selector(name='Master Strategic Controller')`  
This ensures the most critical actions are always executed first.

**Priority Order:**
1. Emergency Defense Protocol  
2. Overwhelming Assault  
3. Opportunistic Strike  
4. Defensive Reinforcement  
5. Early Game Strategy  
6. Mid-Late Game Strategy  
7. Basic Expansion Strategy  
8. Fallback Attack → `attack_weakest_enemy_planet`

**Branching Logic:**
- **Emergency Defense:**  
  Calls `defend_weakest_planet()` immediately if `under_attack()` returns `True`.

- **Overwhelming Assault:**  
  Triggers `aggressive_multi_attack()` when `have_overwhelming_advantage()` is `True`.

- **Early Game Strategy:**  
  If `early_game()` is `True`, the bot expands cautiously using `strategic_spread()`.

---

### behaviors.py: Strategic Action Functions

Six high-level action functions support advanced decision-making:

- `smart_attack_calculation()`  
  Chooses targets by balancing distance, ship cost, and growth rate.

- `defend_weakest_planet()`  
  Detects the most vulnerable friendly planet and reinforces it.

- `aggressive_multi_attack()`  
  Launches simultaneous attacks when a major advantage is detected.

- `strategic_spread()`  
  Prioritizes capturing neutral planets with high growth vs. ship cost.

- `reinforce_front_line()`  
  Shifts support fleets from rear to frontline planets.

- `opportunistic_attack()`  
  Exploits windows when enemy planets are left unguarded.

---

### checks.py: Game State Evaluation

Nine condition-checking functions help the bot make precise decisions:

- `under_attack()`  
  Returns `True` if enemy fleets are targeting friendly planets.

- `have_overwhelming_advantage()`  
  Checks if total ships exceed enemy’s by more than 2x.

- `should_defend_planet()`  
  Compares incoming enemy forces to current defense.

- `early_game()`  
  True if most planets are still unoccupied.

- `weak_enemy_exists()`  
  Finds lightly defended enemy planets.

- `profitable_neutral_exists()`  
  Filters neutral planets by ROI (growth vs. capture cost).

- `have_multiple_planets()`  
  Checks if bot controls more than one planet.

- `enemy_nearby()`  
  Detects nearby enemy planets.

- `can_aggressive_expand()`  
  Validates if the bot has the largest fleet and few active missions.

---

### bt_bot.log

INFO:root:
Selector: Master Strategic Controller
| Sequence: Emergency Defense Protocol
| | Check: under_attack
| | Action: defend_weakest_planet
| Sequence: Overwhelming Assault
| | Check: have_overwhelming_advantage
| | Action: aggressive_multi_attack
| Sequence: Opportunistic Strike
| | Sequence: Perfect Attack Opportunity
| | | Check: weak_enemy_exists
| | | Action: opportunistic_attack
| Sequence: Defensive Reinforcement
| | Check: should_defend_planet
| | Check: have_multiple_planets
| | Action: reinforce_front_line
| Selector: Early Game Strategy
| | Sequence: Early Strategic Expansion
| | | Check: early_game
| | | Check: profitable_neutral_exists
| | | Action: strategic_spread
| | Sequence: Early Normal Expansion
| | | Check: early_game
| | | Check: if_neutral_planet_available
| | | Action: spread_to_weakest_neutral_planet
| Selector: Mid-Late Game Strategy
| | Sequence: Aggressive Expansion
| | | Check: can_aggressive_expand
| | | Action: smart_attack_calculation
| | Sequence: Nearby Enemy Assault
| | | Check: enemy_nearby
| | | Check: have_largest_fleet
| | | Action: smart_attack_calculation
| | Sequence: Standard Advantage Attack
| | | Check: have_largest_fleet
| | | Action: smart_attack_calculation
| Sequence: Basic Expansion Strategy
| | Check: if_neutral_planet_available
| | Action: strategic_spread
| Action: attack_weakest_enemy_planet

---

## 3. How to Run

### Prerequisites
- Java JDK  
- Python

### Execution

Make sure all files (`bt_bot.py`, `behaviors.py`, `checks.py`) are in the correct directory.  
Run your game engine or simulation framework as usual — `bt_bot.py` should be imported and used as the main agent controller.

---

## Team Contributions

- **Inho Yoo**  
  - Redesigned the entire behavior tree structure and overall strategy (`bt_bot.py`)
  - Developed intelligent action functions for strategic decision-making (`behaviors.py`)
  - Implemented advanced game state check functions (`checks.py`)

- **Daisy Fragoso**  
  - Analyzed the `opponent_bot` structure for benchmarking and evaluation
  - Identified and improved weaknesses in the modified `behaviors.py` and proposed improvements
  - Optimized the bot's control logic and behavior tree structure
