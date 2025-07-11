

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


# New advanced check functions
def under_attack(state):
    """Check if my planets are under attack by enemy fleets"""
    return any(fleet.destination_planet in [p.ID for p in state.my_planets()] 
               for fleet in state.enemy_fleets())


def have_overwhelming_advantage(state):
    """Check if we have overwhelming advantage (2x or more)"""
    my_total = sum(planet.num_ships for planet in state.my_planets()) + \
               sum(fleet.num_ships for fleet in state.my_fleets())
    enemy_total = sum(planet.num_ships for planet in state.enemy_planets()) + \
                  sum(fleet.num_ships for fleet in state.enemy_fleets())
    return my_total > enemy_total * 2


def have_multiple_planets(state):
    """Check if we own multiple planets"""
    return len(state.my_planets()) > 1


def enemy_nearby(state):
    """Check if enemy planets are nearby"""
    if not state.my_planets() or not state.enemy_planets():
        return False
    
    min_distance = float('inf')
    for my_planet in state.my_planets():
        for enemy_planet in state.enemy_planets():
            distance = state.distance(my_planet.ID, enemy_planet.ID)
            min_distance = min(min_distance, distance)
    
    return min_distance <= 5  # Consider nearby if distance <= 5


def weak_enemy_exists(state):
    """Check if there are weak enemy planets we can easily defeat"""
    if not state.my_planets() or not state.enemy_planets():
        return False
    
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships)
    for enemy_planet in state.enemy_planets():
        distance = state.distance(strongest_planet.ID, enemy_planet.ID)
        required_ships = enemy_planet.num_ships + distance * enemy_planet.growth_rate + 1
        if strongest_planet.num_ships > required_ships * 1.5:  # Can win with margin
            return True
    return False


def should_defend_planet(state):
    """Check if any planet needs defense"""
    for my_planet in state.my_planets():
        incoming_enemy = sum(fleet.num_ships for fleet in state.enemy_fleets() 
                           if fleet.destination_planet == my_planet.ID)
        incoming_friendly = sum(fleet.num_ships for fleet in state.my_fleets() 
                              if fleet.destination_planet == my_planet.ID)
        
        if incoming_enemy > my_planet.num_ships + incoming_friendly:
            return True
    return False


def profitable_neutral_exists(state):
    """Check if there are profitable neutral planets"""
    if not state.my_planets() or not state.neutral_planets():
        return False
    
    for my_planet in state.my_planets():
        for neutral_planet in state.neutral_planets():
            if my_planet.num_ships > neutral_planet.num_ships + 5:  # Can capture with margin
                return True
    return False


def early_game(state):
    """Check if it's early game (low planet occupation)"""
    total_owned = len(state.my_planets()) + len(state.enemy_planets())
    total_planets = total_owned + len(state.neutral_planets())
    return total_owned < total_planets * 0.6  # Early if less than 60% occupied


def can_aggressive_expand(state):
    """Check if we can aggressively expand"""
    return have_largest_fleet(state) and len(state.my_fleets()) <= 2
