

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


# 새로운 고급 체크 함수들
def under_attack(state):
    """내 행성이 적 함대의 공격을 받고 있는지 확인"""
    return any(fleet.destination_planet in [p.ID for p in state.my_planets()] 
               for fleet in state.enemy_fleets())


def have_overwhelming_advantage(state):
    """압도적인 우위를 가지고 있는지 확인 (2배 이상)"""
    my_total = sum(planet.num_ships for planet in state.my_planets()) + \
               sum(fleet.num_ships for fleet in state.my_fleets())
    enemy_total = sum(planet.num_ships for planet in state.enemy_planets()) + \
                  sum(fleet.num_ships for fleet in state.enemy_fleets())
    return my_total > enemy_total * 2


def have_multiple_planets(state):
    """여러 행성을 소유하고 있는지 확인"""
    return len(state.my_planets()) > 1


def enemy_nearby(state):
    """가까운 거리에 적 행성이 있는지 확인"""
    if not state.my_planets() or not state.enemy_planets():
        return False
    
    min_distance = float('inf')
    for my_planet in state.my_planets():
        for enemy_planet in state.enemy_planets():
            distance = state.distance(my_planet.ID, enemy_planet.ID)
            min_distance = min(min_distance, distance)
    
    return min_distance <= 5  # 거리 5 이하면 가까운 것으로 판단


def weak_enemy_exists(state):
    """내가 쉽게 이길 수 있는 약한 적 행성이 있는지 확인"""
    if not state.my_planets() or not state.enemy_planets():
        return False
    
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships)
    for enemy_planet in state.enemy_planets():
        distance = state.distance(strongest_planet.ID, enemy_planet.ID)
        required_ships = enemy_planet.num_ships + distance * enemy_planet.growth_rate + 1
        if strongest_planet.num_ships > required_ships * 1.5:  # 여유있게 이길 수 있으면
            return True
    return False


def should_defend_planet(state):
    """방어가 필요한 행성이 있는지 확인"""
    for my_planet in state.my_planets():
        incoming_enemy = sum(fleet.num_ships for fleet in state.enemy_fleets() 
                           if fleet.destination_planet == my_planet.ID)
        incoming_friendly = sum(fleet.num_ships for fleet in state.my_fleets() 
                              if fleet.destination_planet == my_planet.ID)
        
        if incoming_enemy > my_planet.num_ships + incoming_friendly:
            return True
    return False


def profitable_neutral_exists(state):
    """수익성 있는 중립 행성이 있는지 확인"""
    if not state.my_planets() or not state.neutral_planets():
        return False
    
    for my_planet in state.my_planets():
        for neutral_planet in state.neutral_planets():
            if my_planet.num_ships > neutral_planet.num_ships + 5:  # 여유있게 점령 가능
                return True
    return False


def early_game(state):
    """게임 초기인지 확인 (총 행성 수가 적음)"""
    total_owned = len(state.my_planets()) + len(state.enemy_planets())
    total_planets = total_owned + len(state.neutral_planets())
    return total_owned < total_planets * 0.6  # 60% 미만이 점령된 상태면 초기


def can_aggressive_expand(state):
    """공격적으로 확장할 수 있는 상황인지 확인"""
    return have_largest_fleet(state) and len(state.my_fleets()) <= 2
