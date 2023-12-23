import time   
from collections import namedtuple

Coord = namedtuple("Coordinate", ('r', 'c'))

def dig(start, direc, steps):
    def move(start, direc):
        return {
            'U': Coord(start.r-1, start.c),
            'D': Coord(start.r+1, start.c),
            'R': Coord(start.r, start.c+1),
            'L': Coord(start.r, start.c-1)
        }[direc]

    cur = Coord(start.r, start.c)
    new_digs = []
    for _ in range(steps):
        cur = move(cur, direc)
        new_digs.append(cur)
    return new_digs

def volume(border):
    def vertical_neighbor(border, e):
        up_row = border.setdefault(e.r-1, [])
        down_row = border.setdefault(e.r+1, [])
        if Coord(e.r-1, e.c) in up_row:
            return 'UP'
        elif Coord(e.r+1, e.c) in down_row:
            return 'DOWN'
        else:
            assert False, 'Beginning # must have come from above or below'

    def empty_spaces_backwards(edges, idx):
        if idx == 0:
            return 0
        empty = edges[idx].c - edges[idx-1].c - 1
        assert empty >= 1
        return empty

    v = 0
    for row in sorted(border.keys()):
        '''
        .#.##.###.#.#.#. -> .##########.###.
        Switch insideness when encountering a single hash or a long path which opens, just like pipe puzzle
        '''

        row_vol = 0
        in_vol = False
        came_from = None
        going_to = None
        edges = sorted(list(set(border[row])), key=lambda x: x.c)
        print(f'For row {row}, we have the border nodes {edges}')
        for idx, e in enumerate(edges):
            row_vol += 1
            if Coord(e.r, e.c-1) not in edges:
                # First in a string, or solo
                if in_vol:
                        row_vol += empty_spaces_backwards(edges, idx)
                if Coord(e.r, e.c+1) not in edges:
                    # Solo
                    in_vol = not in_vol
                else:
                    # Begins string
                    came_from = vertical_neighbor(border, e)
            else:
                if Coord(e.r, e.c+1) not in edges:
                    # Ends a string
                    going_to = vertical_neighbor(border, e)
                    if going_to == came_from:
                        # No change to in_vol status
                        pass
                    else:
                        in_vol = not in_vol
        v += row_vol


        # Print row and volume
        p = ['.' for _ in range(edges[-1].c - edges[0].c+1)]
        for e in edges:
            p[e.c - edges[0].c] = '#'
        print(f'Working on row {"".join(p)}')
        print(f'row_vol: {row_vol}')

    return v
                    




def main():
    start = time.time()
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.readlines()

    cur = Coord(0,0)
    border = {0: [cur]}

    # Trace border
    for line in inp:
        direc, steps = line.split(' ')[:2]
        steps = int(steps)
        print(f'{direc} {steps}')

        new_digs = dig(cur, direc, steps)
        for d in new_digs:
            val = border.setdefault(d.r, [])
            val.append(d)
        cur = new_digs[-1]

    # Print digs
    pattern = [['.' for _ in range(1000)] for _ in range(1000)]
    offset = 200
    for k, v in border.items():
        for node in v:
            pattern[node.r+offset][node.c+offset] = '#'
    with open('debug.txt', 'w') as f:
        f.write('\n'.join([''.join(a) for a in pattern]))


    # Fill in by scanning
    ret = volume(border)

    print(f'Part 1: {ret}')
    print(f'Part 1 latency: {time.time() - start:.5f}')

if __name__ == '__main__':
    main()