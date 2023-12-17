def rows(puzzle):
    return puzzle

def cols(puzzle):
    cols = [[] for _ in range(len(puzzle[0]))]
    for row in puzzle:
        for idx, char in enumerate(row):
            cols[idx].append(char)

    c = []
    for col in cols:
        c.append(''.join(col))
    return c

def sym_axis(rows):
    '''
    0 #...##..# 0
    1 #....#..# 1
    2 ..##..### 2
    3v#####.##.v3
    4^#####.##.^4
    5 ..##..### 5
    6 #....#..# 6
    '''
    # d = {} # row -> row_idx
    # for idx, r in enumerate(rows):
    #     d[r] = idx
    
    # Try all possible axes
    # Define axis as column which axis is before
    for ax in range(len(rows)-1):
        match = True
        end_range = (ax+1)*2-1
        for i in range(ax+1):
            reflect = end_range - i
            if reflect >= 0 and reflect < len(rows):
                # print(f'for axis {ax} mapping {i} to {reflect}')
                if not rows[i] == rows[reflect]:
                    match = False
                
        if match:
            print(f'Found reflection at ax {ax}')
            return ax
    return None


def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.readlines()
    
    res = 0
    puzzle = []
    for line in inp:
        # breakpoint()
        if line.strip() != '':
            puzzle.append(line.strip())
        else:
            # Got a full puzzle
            print(f'Got puzzle')
            r = rows(puzzle)
            # Check for row symmetry
            r_axis = sym_axis(r)
            if r_axis is not None:
                res += 100*(r_axis+1)
            else:
                c = cols(puzzle)
                c_axis = sym_axis(c)
                if c_axis is not None:
                    res += (c_axis + 1)
                else:
                    assert False, "Should have gotten r or c match"



            # Done
            puzzle = []

    print(f'Part 1: {res}')

if __name__ == '__main__':
    main()