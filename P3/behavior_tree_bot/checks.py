def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def is_my_planet_under_attack(state):
    if not state.enemy_fleets():
        return False
    my_planet_ids = [p.ID for p in state.my_planets()]
    for fleet in state.enemy_fleets():
        if fleet.destination_planet in my_planet_ids:
            return True
    return False

def is_best_value_target_available(state):
    if not state.not_my_planets():
        return False
    # Simple check, can be improved with more complex logic
    return True
