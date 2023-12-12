from enum import Enum

class Direction(Enum):
    ABOVE = 1
    BELOW = 2
    LEFT = 3
    RIGHT = 4

class Coord:
    def __init__(self, y, x):
        assert x >= 0 and y >= 0
        self.y = y
        self.x = x

    def __repr__(self):
        return f'Coord(y={self.y}, x={self.x})'

    def right(self):
        return Coord(self.y, self.x+1)
    def left(self):
        return Coord(self.y, self.x-1)
    def up(self):
        return Coord(self.y-1, self.x)
    def down(self):
        return Coord(self.y+1, self.x)

    def dir_from(self, other):
        '''
        Return direction from other to self
        '''
        if self.x > other.x:
            assert self.y == other.y
            return Direction.LEFT
        elif self.x < other.x:
            assert self.y == other.y
            return Direction.RIGHT
        elif self.y > other.y:
            assert self.x == other.x
            return Direction.ABOVE
        elif self.y < other.y:
            assert self.x == other.x
            return Direction.BELOW
        else:
            assert False, "other {other} not directly connected to self {self}"


def move(prev, cur, cur_type):
    # Depending on direction of movement and pipe type, next location differs
    direction = cur.dir_from(prev)

    if cur_type == '|':
        if direction == Direction.ABOVE:
            return cur.down()
        elif direction == Direction.BELOW:
            return cur.up()
        else:
            assert False
    elif cur_type == '-':
        if direction == Direction.RIGHT:
            return cur.left()
        elif direction == Direction.LEFT:
            return cur.right()
        else:
            assert False
    elif cur_type == '7':
        if direction == Direction.LEFT:
            return cur.down()
        elif direction == Direction.BELOW:
            return cur.left()
        else:
            assert False
    elif cur_type == 'F':
        if direction == Direction.RIGHT:
            return cur.down()
        elif direction == Direction.BELOW:
            return cur.right()
        else:
            assert False
    elif cur_type == 'L':
        if direction == Direction.RIGHT:
            return cur.up()
        elif direction == Direction.ABOVE:
            return cur.right()
        else:
            assert False
    elif cur_type == 'J':
        if direction == Direction.ABOVE:
            return cur.left()
        elif direction == Direction.LEFT:
            return cur.up()
        else:
            assert False
    else:
        assert False

def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.readlines()

    '''
    Dumb way first. There are 2 ways to begin from S. Take both of them
    and record the step # in a dict.
    Coord system: (x,y), top-left is (0,0), increases with down-right
    '''

    # Find position of starting S
    for y_s, line in enumerate(inp):
        x_s = line.find('S')
        if x_s > -1:
            break
    start = Coord(y=y_s, x=x_s)
    print(start)

    possible_next = [start.down(), start.right()]
    if start.x > 0:
        possible_next.append(start.left())
    if start.y > 0:
        possible_next.append(start.up())
    print(possible_next)

    valid_starts = []
    for pn in possible_next:
        try:
            pipe = inp[pn.y][pn.x]
            n = move(start, pn, pipe)
            print(f'For possible next {pn} ({pipe}), chose to move to {n}({inp[n.y][n.x]})')
            valid_starts.append(pn)
        except:
            pass
    print(f'Valid starts: {valid_starts}')

    # Iterate over starts to find loop
    scores = {(start.y, start.x): 0} # (y,x) -> score 

    for n in valid_starts:
        print(f'Running from start {n}')
        # with open(f'debug.out', 'a') as f:
        #     f.write('------------------\nRunning from start {n}\n')
        prev = start
        steps = 1
        while 1:
            pipe = inp[n.y][n.x]
            if steps > scores.get((n.y,n.x), float('inf')) or pipe == 'S':
                # Trying to assign a higher score to something that's already been seen.
                # Either completing the loop a second time or hitting other direction's scores.
                break
            scores[(n.y,n.x)] = steps
            next = move(prev, n, inp[n.y][n.x])
            # print(f'Moved from {n} ({inp[n.y][n.x]}) to {next} ({inp[next.y][next.x]})')
            # with open(f'debug.out', 'a') as f:
                # f.write(f'Moved from {n} ({inp[n.y][n.x]}) to {next} ({inp[next.y][next.x]})\n')
            prev, n = n, next
            steps += 1

    # print(f'scores: {scores}')

    # Print debug map
    debug_out = [[0 for i in range(len(inp[0]))] for i in range(len(inp))]
    for y in range(len(inp)):
        for x in range(len(inp[0])):
            c = (y, x)
            if c in scores:
                debug_out[y][x] = scores[c]

    # for y in range(len(inp)):
    #     print(debug_out[y])
    #     with open('debug.out', 'a') as f:
    #         f.write(str(debug_out[y]))
    #         f.write('\n')

    '''
    Part 2
    Given our scores map, we know the location of all pipes which are
    part of the loop. The plan is to scan from left to right, from top to bottom,
    and keep track whether we are inside the loop or not. While we are
    inside the loop and we encounter spaces that are not the loop, set that
    space to a 1. Take the sum the end.

    You swap positions when you finish a horizontal line segment.
    Examples:
    |   -> change inside status
    F-7 -> don't change inside status
    L-7 -> change inside status
    L-J -> don't change inside status
    F-J -> change inside status

    Replace S in inp with whatever it actually represents.
    Find this based on the valid starts we got from part 1
    '''

    start_directions = set(vs.dir_from(start) for vs in valid_starts)
    if start_directions == {Direction.ABOVE, Direction.LEFT}:
        '''
        .S-
        .|.
        '''
        replacement = 'F'
    elif start_directions == {Direction.ABOVE, Direction.RIGHT}:
        '''
        -S.
        .|.
        '''
        replacement = '7'
    elif start_directions == {Direction.BELOW, Direction.LEFT}:
        '''
        .|.
        .S-
        ...
        '''
        replacement = 'L'
    elif start_directions == {Direction.BELOW, Direction.RIGHT}:
        '''
        .|.
        -S.
        ...
        '''
        replacement = 'J'
    else:
        assert False

    start_line = inp[start.y]
    inp[start.y] = start_line[:start.x] + replacement + start_line[start.x+1:]

    for line in inp:
        print(line)

    insides = set()
    vert_pipes = ['|']
    horiz_begins = ['F', 'L']
    horiz_ends = ['7', 'J']
    horiz_swaps = ['FJ', 'L7']
    horiz_keeps = ['F7', 'LJ']
    max_y = len(inp)
    max_x = len(inp[0].strip())
    print(f'max_y: {max_y}, max_x:{max_x}')
    for y in range(max_y):
        inside = False
        seg_begin = None
        seg_end = None
        for x in range(max_x):
            inp_at = inp[y][x]
            if (y, x) in scores:
                # (y,x) is a location in the loop
                if inp_at in vert_pipes:
                    # We just switched our inside status
                    inside = not inside # invert inside
                elif inp_at in horiz_begins:
                    seg_begin = inp_at
                elif inp_at in horiz_ends:
                    seg_end = inp_at
                    assert seg_begin is not None, "Should only encounter horiz end if we had a begin"
                    seg = seg_begin + seg_end
                    if seg in horiz_swaps:
                        # This type of segment means we switch inside status
                        inside = not inside
                    elif seg in horiz_keeps:
                        # This type of segment means we keep status
                        pass
                    else:
                        assert False, f'Invalid horizontal segment {seg}'
                    seg_begin = None
                    seg_end = None
                else:
                    assert inp_at == '-', f'Input should be - but is {inp_at}'
            else:
                if inside:
                    insides.add((y, x))

        
    out_str = ''
    for y in range(max_y):
        for x in range(max_x):
            if (y,x) in scores: 
                out_str += inp[y][x]
            elif (y,x) in insides:
                out_str += '@'
            else:
                out_str += '.'
        out_str += '\n'
    with open('debug.out', 'w') as f:
        f.write(out_str)

    print(f'Found these inside spaces: {insides}')
    print(f'Part 2: {len(insides)}')
            




    max_steps = max([max(x) for x in debug_out])

    print(f'Part 1: {max_steps}')


if __name__ == '__main__':
    main()