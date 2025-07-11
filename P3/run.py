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
    """Test against all opponent bots on all maps"""
    if maps_to_test is None:
        maps_to_test = list(range(1, 101))  # map1 ~ map100
    
    total_games = 0
    total_wins = 0
    results_by_opponent = {}
    
    print(f"\nAll maps test started: {len(maps_to_test)} maps x {len(opponents)} bots = {len(maps_to_test) * len(opponents)} games")
    print("=" * 80)
    
    for opponent in opponents:
        opponent_name = opponent.split('/')[1].split('.')[0]
        results_by_opponent[opponent_name] = {'wins': 0, 'losses': 0, 'details': []}
        
        print(f"\nTesting {opponent_name} vs bt_bot...")
        
        for map_num in maps_to_test:
            result = test(bot, opponent, map_num)
            total_games += 1
            
            if result['winner'] == 'bt_bot':
                total_wins += 1
                results_by_opponent[opponent_name]['wins'] += 1
                status = "WIN"
            else:
                results_by_opponent[opponent_name]['losses'] += 1
                status = "LOSS"
            
            results_by_opponent[opponent_name]['details'].append(result)
            
            # Progress report every 10 games
            if map_num % 10 == 0:
                win_rate = results_by_opponent[opponent_name]['wins'] / (results_by_opponent[opponent_name]['wins'] + results_by_opponent[opponent_name]['losses']) * 100
                print(f"  Map {map_num}: {status} (Win rate: {win_rate:.1f}%)")
    
    return total_games, total_wins, results_by_opponent


def print_detailed_results(total_games, total_wins, results_by_opponent):
    """Print detailed test results"""
    print("\n" + "=" * 80)
    print("Final Test Results")
    print("=" * 80)
    
    overall_win_rate = (total_wins / total_games) * 100 if total_games > 0 else 0
    print(f"Overall Results: {total_wins}/{total_games} wins (Win rate: {overall_win_rate:.1f}%)")
    
    print(f"\nDetailed Results by Opponent:")
    for opponent_name, stats in results_by_opponent.items():
        wins = stats['wins']
        losses = stats['losses']
        total = wins + losses
        win_rate = (wins / total) * 100 if total > 0 else 0
        
        if win_rate == 100:
            rank = "[PERFECT]"
        elif win_rate >= 90:
            rank = "[EXCELLENT]"
        elif win_rate >= 80:
            rank = "[GOOD]"
        elif win_rate >= 70:
            rank = "[OK]"
        else:
            rank = "[WARNING]"
        
        print(f"  {rank} vs {opponent_name:15}: {wins:3d}/{total:3d} wins (Win rate: {win_rate:5.1f}%)")
        
        # Show detailed info for lost games
        if losses > 0:
            print(f"     Lost games:")
            for detail in stats['details']:
                if detail['winner'] != 'bt_bot':
                    print(f"        Map {detail['map']:3d}: {detail['reason']}")
    
    print("\n" + "=" * 80)


def test_sample_maps(bot, opponents, sample_size=20):
    """Test on randomly selected maps for quick testing"""
    all_maps = list(range(1, 101))
    sample_maps = random.sample(all_maps, min(sample_size, len(all_maps)))
    sample_maps.sort()
    
    print(f"Random sample test: {sample_size} maps")
    print(f"Selected maps: {sample_maps}")
    
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
            # Visualization mode on specific maps
            maps = [71, 13, 24, 56, 7]
            for opponent, map_num in zip(opponents, maps):
                show_match(my_bot, opponent, map_num)
                
        elif mode == "test":
            # Test mode on specific maps
            maps = [71, 13, 24, 56, 7]
            for opponent, map_num in zip(opponents, maps):
                result = test(my_bot, opponent, map_num)
                status = "Victory!" if result['winner'] == 'bt_bot' else f"Defeat ({result['reason']})"
                print(f"{result['bot']} vs {result['opponent']} (Map {map_num}): {status}")
                
        elif mode == "all":
            # Test on all maps
            total_games, total_wins, results = test_all_maps(my_bot, opponents)
            print_detailed_results(total_games, total_wins, results)
            
        elif mode == "sample":
            # Random sample test
            sample_size = int(sys.argv[2]) if len(sys.argv) >= 3 else 20
            total_games, total_wins, results = test_sample_maps(my_bot, opponents, sample_size)
            print_detailed_results(total_games, total_wins, results)
            
        else:
            print("Usage:")
            print("  python run.py show    - Show visualization on specific maps")
            print("  python run.py test    - Simple test on specific maps")
            print("  python run.py all     - Full test on all maps")
            print("  python run.py sample [N] - Test on N random maps (default: 20)")
    else:
        # Default: visualization on specific maps
        maps = [71, 13, 24, 56, 7]
        for opponent, map_num in zip(opponents, maps):
            show_match(my_bot, opponent, map_num)
