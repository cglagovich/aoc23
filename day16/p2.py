import time   
from collections import Counter, namedtuple

Coordinate = namedtuple('Coordinate', ['r', 'c'])
Beam = namedtuple('Beam', ['coord', 'dir'])

mappings = {
    '.': {k: k for k in 'ENWS'},
    '|': {'N': 'N', 'S': 'S', 'E': 'NS', 'W': 'NS'},
    '-': {'E': 'E', 'W': 'W', 'S': 'EW', 'N': 'EW'},
    '\\': {'N': 'W', 'S': 'E', 'W': 'N', 'E': 'S'},
    '/': {'N': 'E', 'S': 'W', 'E': 'N', 'W': 'S'}
    }

def move_pos(pos, dir):
    if dir == 'E':
        return Coordinate(r=pos.r, c=pos.c+1)
    elif dir == 'W':
        return Coordinate(r=pos.r, c=pos.c-1)
    elif dir == 'N':
        return Coordinate(r=pos.r-1, c=pos.c)
    elif dir == 'S':
        return Coordinate(r=pos.r+1, c=pos.c)
    else:
        assert False


def check_bounds(pos, max_r, max_c):
    return pos.r >= 0 and pos.c >= 0 and pos.r < max_r and pos.c < max_c

def print_energized(energized, max_r, max_c):
    ret = [['.' for _ in range(max_c)] for _ in range(max_r)]
    for item in energized:
        r, c = item.coord
        ret[r][c] = '#'

    ret = '\n'.join([''.join(s) for s in ret])
    print(ret)

def get_energy(start, board, max_r, max_c):
    energized = set()
    nodes = [start]
    while len(nodes) > 0:
        n = nodes.pop()
        if n in energized:
            continue
        energized.add(n)
        pos = n.coord
        dir = n.dir
        
        t = board[pos.r][pos.c]
        moves = mappings[t][dir]
        for move_dir in moves:
            next_n = move_pos(pos, move_dir)
            if check_bounds(next_n, max_r, max_c):
                nodes.append(Beam(coord=next_n, dir=move_dir))
    unique_energized = {e.coord for e in energized}
    return len(unique_energized)


def main():
    start = time.time()
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.readlines()

    gameboard = [i.strip() for i in inp]
    max_r = len(gameboard)
    max_c = len(gameboard[0])
    print('\n'.join(gameboard))

    starts = [Beam(Coordinate(r=r, c=0), 'E') for r in range(max_r)] \
        + [Beam(Coordinate(r=0, c=c), 'S') for c in range(max_c)] \
        + [Beam(Coordinate(r=r, c=max_c-1), 'W') for r in range(max_r)] \
        + [Beam(Coordinate(r=max_r-1, c=c), 'N') for c in range(max_c)]

    max_energy = 0
    for s in starts:
        energy = get_energy(s, gameboard, max_r, max_c)
        max_energy = max(max_energy, energy)

    print(f'Part 1: {max_energy}')
    print(f'Part 1 latency: {time.time() - start:.5f}')

if __name__ == '__main__':
    main()