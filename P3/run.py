import subprocess
import os, sys
import random


def show_match(bot, opponent_bot, map_num):
    """
        Runs an instance of Planet Wars between the two given bots on the specified map. After completion, the
        game is replayed via a visual interface.
    """
    command = 'java -jar tools/PlayGame.jar maps/map' + str(map_num) + '.txt 1000 1000 log.txt ' + \
              '"python ' + bot + '" ' + \
              '"python ' + opponent_bot + '" ' + \
              '| java -jar tools/ShowGame.jar'
    print(command)
    os.system(command)


def test(bot, opponent_bot, map_num):
    """ Runs an instance of Planet Wars between the two given bots on the specified map. """
    bot_name, opponent_name = bot.split('/')[1].split('.')[0], opponent_bot.split('/')[1].split('.')[0]
    command = 'java -jar tools/PlayGame.jar maps/map' + str(map_num) +'.txt 1000 1000 log.txt ' + \
              '"python ' + bot + '" ' + \
              '"python ' + opponent_bot + '" '

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    result = {'bot': bot_name, 'opponent': opponent_name, 'map': map_num, 'winner': None, 'reason': None}

    while True:
        return_code = p.poll()  # returns None while subprocess is running
        line = p.stdout.readline().decode('utf-8')
        if '1 timed out' in line:
            result['winner'] = opponent_name
            result['reason'] = f'{bot_name} timed out'
            break
        elif '2 timed out' in line:
            result['winner'] = bot_name
            result['reason'] = f'{opponent_name} timed out'
            break
        elif '1 crashed' in line:
            result['winner'] = opponent_name
            result['reason'] = f'{bot_name} crashed'
            break
        elif '2 crashed' in line:
            result['winner'] = bot_name
            result['reason'] = f'{opponent_name} crashed'
            break
        elif 'Player 1 Wins!' in line:
            result['winner'] = bot_name
            result['reason'] = 'normal victory'
            break
        elif 'Player 2 Wins!' in line:
            result['winner'] = opponent_name
            result['reason'] = 'normal victory'
            break

        if return_code is not None:
            break
    
    return result


def test_all_maps(bot, opponents, maps_to_test=None):
    """모든 맵에서 모든 opponent_bots와 테스트"""
    if maps_to_test is None:
        maps_to_test = list(range(1, 101))  # map1 ~ map100
    
    total_games = 0
    total_wins = 0
    results_by_opponent = {}
    
    print(f"\n🎮 모든 맵 테스트 시작: {len(maps_to_test)}개 맵 × {len(opponents)}개 봇 = {len(maps_to_test) * len(opponents)}게임")
    print("=" * 80)
    
    for opponent in opponents:
        opponent_name = opponent.split('/')[1].split('.')[0]
        results_by_opponent[opponent_name] = {'wins': 0, 'losses': 0, 'details': []}
        
        print(f"\n🤖 {opponent_name} vs bt_bot 테스트 중...")
        
        for map_num in maps_to_test:
            result = test(bot, opponent, map_num)
            total_games += 1
            
            if result['winner'] == 'bt_bot':
                total_wins += 1
                results_by_opponent[opponent_name]['wins'] += 1
                status = "✅"
            else:
                results_by_opponent[opponent_name]['losses'] += 1
                status = "❌"
            
            results_by_opponent[opponent_name]['details'].append(result)
            
            # 진행상황 표시 (매 10게임마다)
            if map_num % 10 == 0:
                win_rate = results_by_opponent[opponent_name]['wins'] / (results_by_opponent[opponent_name]['wins'] + results_by_opponent[opponent_name]['losses']) * 100
                print(f"  Map {map_num}: {status} (승률: {win_rate:.1f}%)")
    
    return total_games, total_wins, results_by_opponent


def print_detailed_results(total_games, total_wins, results_by_opponent):
    """상세한 결과 출력"""
    print("\n" + "=" * 80)
    print("🏆 최종 테스트 결과")
    print("=" * 80)
    
    overall_win_rate = (total_wins / total_games) * 100 if total_games > 0 else 0
    print(f"📊 전체 결과: {total_wins}/{total_games} 승 (승률: {overall_win_rate:.1f}%)")
    
    print(f"\n📈 상대별 상세 결과:")
    for opponent_name, stats in results_by_opponent.items():
        wins = stats['wins']
        losses = stats['losses']
        total = wins + losses
        win_rate = (wins / total) * 100 if total > 0 else 0
        
        if win_rate == 100:
            emoji = "🏆"
        elif win_rate >= 90:
            emoji = "🥇"
        elif win_rate >= 80:
            emoji = "🥈"
        elif win_rate >= 70:
            emoji = "🥉"
        else:
            emoji = "⚠️"
        
        print(f"  {emoji} vs {opponent_name:15}: {wins:3d}/{total:3d} 승 (승률: {win_rate:5.1f}%)")
        
        # 패배한 게임이 있으면 상세 정보 표시
        if losses > 0:
            print(f"     ❌ 패배 게임들:")
            for detail in stats['details']:
                if detail['winner'] != 'bt_bot':
                    print(f"        Map {detail['map']:3d}: {detail['reason']}")
    
    print("\n" + "=" * 80)


def test_sample_maps(bot, opponents, sample_size=20):
    """랜덤하게 선택된 맵들에서 테스트 (빠른 테스트용)"""
    all_maps = list(range(1, 101))
    sample_maps = random.sample(all_maps, min(sample_size, len(all_maps)))
    sample_maps.sort()
    
    print(f"🎲 랜덤 샘플 테스트: {sample_size}개 맵")
    print(f"선택된 맵들: {sample_maps}")
    
    return test_all_maps(bot, opponents, sample_maps)


if __name__ == '__main__':
    path = os.getcwd()
    opponents = ['opponent_bots/easy_bot.py',
                 'opponent_bots/spread_bot.py',
                 'opponent_bots/aggressive_bot.py',
                 'opponent_bots/defensive_bot.py',
                 'opponent_bots/production_bot.py']

    my_bot = 'behavior_tree_bot/bt_bot.py'
    
    if len(sys.argv) >= 2:
        mode = sys.argv[1].lower()
        
        if mode == "show":
            # 기존 시각화 모드 (특정 맵들)
            maps = [71, 13, 24, 56, 7]
            for opponent, map_num in zip(opponents, maps):
                show_match(my_bot, opponent, map_num)
                
        elif mode == "test":
            # 기존 테스트 모드 (특정 맵들)
            maps = [71, 13, 24, 56, 7]
            for opponent, map_num in zip(opponents, maps):
                result = test(my_bot, opponent, map_num)
                status = "승리!" if result['winner'] == 'bt_bot' else f"패배 ({result['reason']})"
                print(f"{result['bot']} vs {result['opponent']} (Map {map_num}): {status}")
                
        elif mode == "all":
            # 모든 맵에서 테스트
            total_games, total_wins, results = test_all_maps(my_bot, opponents)
            print_detailed_results(total_games, total_wins, results)
            
        elif mode == "sample":
            # 랜덤 샘플 테스트
            sample_size = int(sys.argv[2]) if len(sys.argv) >= 3 else 20
            total_games, total_wins, results = test_sample_maps(my_bot, opponents, sample_size)
            print_detailed_results(total_games, total_wins, results)
            
        else:
            print("사용법:")
            print("  python run.py show    - 특정 맵들에서 시각화")
            print("  python run.py test    - 특정 맵들에서 간단 테스트")
            print("  python run.py all     - 모든 맵에서 전체 테스트")
            print("  python run.py sample [N] - N개 랜덤 맵에서 테스트 (기본값: 20)")
    else:
        # 기본값: 특정 맵들에서 시각화
        maps = [71, 13, 24, 56, 7]
        for opponent, map_num in zip(opponents, maps):
            show_match(my_bot, opponent, map_num)
