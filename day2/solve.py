from functools import reduce

def main():
    with open('input.txt') as f:
        lines = f.readlines()

    # Find max number of reds, greens, and blues across sets for a game
    max_map = {'red': 12, 'green': 13, 'blue': 14}

    game_sum = 0
    power_sum = 0
    for line in lines:
        game, sets = line.split(':')
        game_num = int(game.split(' ')[-1])
        set_map = {'red': 0, 'green': 0, 'blue': 0}
        for set in sets.split(';'):
            if len(set) == 0:
                continue
            
            for color in set_map.keys():
                if color in set:
                    c = set.split(color)[0]
                    c = c.split(',')[-1]
                    c = int(c.strip())
                    set_map[color] = max(set_map[color], c)

        if all([set_map[k] <= max_map[k] for k in max_map.keys()]):
            game_sum += game_num

        power_sum += reduce((lambda x, y: x*y), set_map.values())


    print(f'Part1: {game_sum}')
    print(f'Part2: {power_sum}')


if __name__ == '__main__':
    main()