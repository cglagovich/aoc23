import time

def is_valid(line, groups, starts):
    '''
    O(n) validation check
    line:       ???.###
    attempt:    #.#.###
    groups: 1,1,3
    starts: 0,2,4
    '''
    # Check for overlapping groups
    group_idxs = []
    group_valids = []
    for g, s in zip(groups, starts):
        group_idxs.extend(range(s, s+g+1))
        group_valids.extend(range(s, s+g))
    # print(f'group_idxs: {group_idxs}')
    overlap = len(group_idxs) > len(set(group_idxs))
    if overlap:
        # print(f'failing due to overlapping groups')
        return False

    # Check that no groups run off the edge
    for g, s in zip(groups, starts):
        if s+g > len(line):
            return False

    # Create attempt string
    attempt = [None]*len(line)
    for i in range(len(line)):
        if i in group_valids:
            attempt[i] = '#'
        else:
            attempt[i] = '.'
    # print(f'attempt: {attempt}')

    # Check attempt against line
    for i in range(len(line)):
        if attempt[i] == '#' and line[i] == '.':
            return False
        if attempt[i] == '.' and line[i] == '#':
            return False

    # print(f'----')
    # print(groups)
    # print(line)
    # print(''.join(attempt))
    return True



def possible_starts(line, groups):
    # groups: (1,1,3)
    max_len = len(line)
    next = tuple([0]*len(groups))
    yield next
    while True:
        # Add with carrying
        updated = list(next)
        updated[-1] += 1
        # Carry from -1 to -len
        for i in range(1, len(groups)+1):
            if updated[-i] > max_len-1:
                if (i+1) > len(groups):
                    return
                updated[-(i+1)] += 1
                updated[-i] = updated[-(i+1)]
                if i < len(groups):
                    updated[-i] += groups[-(i+1)]
            else:
                break
        next = tuple(updated)
        yield next


def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = [a.strip() for a in f.readlines()]

    start = time.time()
    res = 0
    for line in inp:
        s, g = line.split(' ')
        s = s.strip()
        gs = tuple(int(a) for a in g.split(','))
        s = '?'.join([s]*5)
        gs = gs * 5

        print(f'Solving line {line}')
        print(s)
        print(gs)


        # valid = is_valid(s, gs, (0,1,4))
        combinations = 0
        for ps in possible_starts(s, gs):
            # print(ps)
            if is_valid(s, gs, ps):
                combinations += 1
                # print(f'Valid combination {ps}')
        res += combinations
        print(f'Found {combinations} combinations for line {s} {g}')

    duration = time.time() - start
    print(f'Part 1: {res}')
    print(f'Part 1 latency: {duration:.5f}s')

if __name__ == '__main__':
    main()