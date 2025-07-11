import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


# 새로운 고급 행동 함수들
def smart_attack_calculation(state):
    """정교한 계산을 통한 공격"""
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True)
    enemy_planets = [planet for planet in state.enemy_planets()
                    if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    
    if not my_planets or not enemy_planets:
        return False
    
    # 공격 효율성을 계산하여 최적의 공격 선택
    best_attacks = []
    for my_planet in my_planets:
        for enemy_planet in enemy_planets:
            distance = state.distance(my_planet.ID, enemy_planet.ID)
            required_ships = enemy_planet.num_ships + distance * enemy_planet.growth_rate + 1
            
            if my_planet.num_ships > required_ships:
                # 효율성 = 적 행성 성장률 / 필요한 함선 수
                efficiency = enemy_planet.growth_rate / required_ships
                best_attacks.append((efficiency, my_planet, enemy_planet, required_ships))
    
    if best_attacks:
        # 가장 효율적인 공격 실행
        best_attacks.sort(reverse=True)
        _, my_planet, enemy_planet, required_ships = best_attacks[0]
        return issue_order(state, my_planet.ID, enemy_planet.ID, required_ships)
    
    return False


def defend_weakest_planet(state):
    """가장 취약한 행성을 방어"""
    my_planets = state.my_planets()
    if len(my_planets) <= 1:
        return False
    
    # 각 행성의 위험도 계산
    planet_risks = []
    for planet in my_planets:
        incoming_enemy = sum(fleet.num_ships for fleet in state.enemy_fleets() 
                           if fleet.destination_planet == planet.ID)
        incoming_friendly = sum(fleet.num_ships for fleet in state.my_fleets() 
                              if fleet.destination_planet == planet.ID)
        
        net_strength = planet.num_ships + incoming_friendly - incoming_enemy
        planet_risks.append((net_strength, planet))
    
    planet_risks.sort()  # 가장 취약한 순으로 정렬
    
    # 가장 취약한 행성이 실제로 위험한 상황인지 확인
    weakest_strength, weakest_planet = planet_risks[0]
    if weakest_strength >= 0:  # 위험하지 않으면 방어 불필요
        return False
    
    # 도움을 줄 수 있는 가장 강한 행성 찾기
    helper_planets = [(p.num_ships, p) for _, p in planet_risks[1:] if p.num_ships > 10]
    if not helper_planets:
        return False
    
    helper_planets.sort(reverse=True)
    helper_strength, helper_planet = helper_planets[0]
    
    # 필요한 만큼 지원
    needed_ships = min(helper_strength // 2, abs(weakest_strength) + 5)
    return issue_order(state, helper_planet.ID, weakest_planet.ID, needed_ships)


def aggressive_multi_attack(state):
    """압도적 우위 시 다중 공격"""
    my_planets = [p for p in state.my_planets() if p.num_ships > 20]
    enemy_planets = [p for p in state.enemy_planets() 
                    if not any(f.destination_planet == p.ID for f in state.my_fleets())]
    
    if len(my_planets) < 2 or not enemy_planets:
        return False
    
    # 여러 행성에서 동시에 공격
    attacks_made = 0
    for my_planet in my_planets:
        if attacks_made >= 3:  # 최대 3개 공격
            break
            
        for enemy_planet in enemy_planets:
            distance = state.distance(my_planet.ID, enemy_planet.ID)
            required_ships = enemy_planet.num_ships + distance * enemy_planet.growth_rate + 1
            
            if my_planet.num_ships > required_ships * 1.5:  # 여유있게 공격 가능
                issue_order(state, my_planet.ID, enemy_planet.ID, required_ships)
                enemy_planets.remove(enemy_planet)
                attacks_made += 1
                break
    
    return attacks_made > 0


def strategic_spread(state):
    """전략적 중립 행성 확장"""
    my_planets = state.my_planets()
    neutral_planets = [p for p in state.neutral_planets() 
                      if not any(f.destination_planet == p.ID for f in state.my_fleets())]
    
    if not my_planets or not neutral_planets:
        return False
    
    # 중립 행성을 가치별로 정렬 (성장률 대비 점령 비용)
    neutral_values = []
    for neutral in neutral_planets:
        min_cost = float('inf')
        closest_planet = None
        
        for my_planet in my_planets:
            distance = state.distance(my_planet.ID, neutral.ID)
            cost = neutral.num_ships + distance + 1
            if cost < min_cost and my_planet.num_ships > cost:
                min_cost = cost
                closest_planet = my_planet
        
        if closest_planet:
            value = neutral.growth_rate / min_cost if min_cost > 0 else 0
            neutral_values.append((value, neutral, closest_planet, min_cost))
    
    if neutral_values:
        # 가장 가치있는 중립 행성 점령
        neutral_values.sort(reverse=True)
        _, neutral, my_planet, cost = neutral_values[0]
        return issue_order(state, my_planet.ID, neutral.ID, cost)
    
    return False


def reinforce_front_line(state):
    """전선 행성 강화"""
    my_planets = state.my_planets()
    enemy_planets = state.enemy_planets()
    
    if len(my_planets) <= 1 or not enemy_planets:
        return False
    
    # 전선 행성들 식별 (적과 가장 가까운 행성들)
    front_line_planets = []
    for my_planet in my_planets:
        min_enemy_distance = min(state.distance(my_planet.ID, enemy.ID) for enemy in enemy_planets)
        front_line_planets.append((min_enemy_distance, my_planet))
    
    front_line_planets.sort()  # 가까운 순으로 정렬
    
    # 가장 전선에 있는 행성이 약하면 강화
    if len(front_line_planets) >= 2:
        front_distance, front_planet = front_line_planets[0]
        
        # 후방 행성 중 여유있는 것 찾기
        rear_planets = [(p.num_ships, p) for _, p in front_line_planets[1:] if p.num_ships > 15]
        
        if rear_planets and front_planet.num_ships < 20:
            rear_planets.sort(reverse=True)
            rear_strength, rear_planet = rear_planets[0]
            reinforcement = min(rear_strength // 3, 15)
            return issue_order(state, rear_planet.ID, front_planet.ID, reinforcement)
    
    return False


def opportunistic_attack(state):
    """기회주의적 공격 (적 함대가 비어있을 때)"""
    if state.enemy_fleets():  # 적 함대가 움직이고 있으면 대기
        return False
    
    my_planets = state.my_planets()
    enemy_planets = state.enemy_planets()
    
    if not my_planets or not enemy_planets:
        return False
    
    # 가장 쉽게 이길 수 있는 적 행성 찾기
    easy_targets = []
    for my_planet in my_planets:
        for enemy_planet in enemy_planets:
            distance = state.distance(my_planet.ID, enemy_planet.ID)
            required_ships = enemy_planet.num_ships + 1
            
            if my_planet.num_ships > required_ships * 2:  # 압도적으로 이길 수 있음
                easy_targets.append((required_ships, my_planet, enemy_planet))
    
    if easy_targets:
        easy_targets.sort()  # 가장 적은 비용 순
        required_ships, my_planet, enemy_planet = easy_targets[0]
        return issue_order(state, my_planet.ID, enemy_planet.ID, required_ships)
    
    return False
