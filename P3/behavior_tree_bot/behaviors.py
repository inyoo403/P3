import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack(state):
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)
    enemy_planets = sorted(state.enemy_planets(), key=lambda p: p.num_ships)

    if not my_planets or not enemy_planets:
        return False

    # Try to attack from each of my planets
    for my_planet in my_planets:
        # Find a target that can be taken over by this planet
        for target_planet in enemy_planets:
            required_ships = target_planet.num_ships + state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                # Update my planet's ship count for this turn's planning
                my_planet = my_planet._replace(num_ships=my_planet.num_ships - required_ships)
                return True # Issued one order this turn
    return False

def spread(state):
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)
    neutral_planets = sorted(state.neutral_planets(), key=lambda p: p.num_ships)

    if not my_planets or not neutral_planets:
        return False

    for my_planet in my_planets:
        for target_planet in neutral_planets:
            required_ships = target_planet.num_ships + 1
            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = my_planet._replace(num_ships=my_planet.num_ships - required_ships)
                return True # Issued one order this turn
    return False