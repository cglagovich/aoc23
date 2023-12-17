import time
import functools

# zeros = [0] * 10000

# @functools.lru_cache()
def is_valid(line, groups, starts, n_groups, line_len):
    '''
    O(n) validation check
    line:       ???.###
    attempt:    #.#.###
    groups: 1,1,3
    starts: 0,2,4
    '''

    for i in range(n_groups-1):
        # Check that starts are increasing
        if starts[i+1] <= starts[i]:
            return False, None
        # Check that there's no overlap
        if starts[i] + groups[i] >= starts[i+1]:
            return False, i+1
        
    # # Check for overlapping groups
    # group_idxs = []
    # group_valids = []
    # for g, s in zip(groups, starts):

    #     group_idxs.extend(range(s, s+g+1))
    #     group_valids.extend(range(s, s+g))
    # # print(f'group_idxs: {group_idxs}')
    # overlap = len(group_idxs) > len(set(group_idxs))
    # if overlap:
    #     # print(f'failing due to overlapping groups')
    #     return False

    # Check that no groups run off the edge
    for i, (g, s) in enumerate(zip(groups, starts)):
        if s+g > line_len:
            return False, i


    group_valid_bitmask = [0]*line_len
    ones = [1]*line_len
    for g, s in zip(groups, starts):
        group_valid_bitmask[s:s+g] = ones[s:s+g]

    # Create attempt string
    attempt = [None]*line_len
    for i in range(line_len):
        if group_valid_bitmask[i] == 1:
            attempt[i] = '#'
        else:
            attempt[i] = '.'
    # print(f'attempt: {attempt}')

    # Check attempt against line
    for i in range(line_len):
        if attempt[i] == '#' and line[i] == '.':
            return False, None
        if attempt[i] == '.' and line[i] == '#':
            return False, None

    # print(f'----')
    # print(groups)
    # print(line)
    # print(''.join(attempt))
    return True, None

def next_hash_or_mark(idx, hash_or_mark, len_line):
    if idx >= len_line:
        # Early out if we can't do anything valid
        return idx
    try:
        next_hash = hash_or_mark[idx:].index(1)
        # breakpoint()
        return idx + next_hash
    except:
        return idx

def next_start(cur_start, groups, n_groups, line_len, first_fail, hash_or_mark):
    # Add with carrying
    # If we know which group failed first, let's increment that group instead of last one
    # if first_fail is not None:
        # breakpoint()
        # cur_start[first_fail] += 1
    # else:
    cur_start[-1] += 1
    # Align cur_start to next valid point
    # cur_start = align_up_to_valid(cur_start, line_len, hash_or_mark)
    # print(f'Before carrying: {cur_start}')
    # Carry from -1 to -len
    for i in range(1, n_groups+1):
        if cur_start[-i] > line_len-1:
            if (i+1) > n_groups:
                return False
            prev_incr = 1
            cur_start[-(i+1)] = next_hash_or_mark(cur_start[-(i+1)]+prev_incr, hash_or_mark, line_len)
            if i < n_groups:
                cur_start[-i] = cur_start[-(i+1)] + groups[-(i+1)]
            else:
                cur_start[-i] = next_hash_or_mark(cur_start[-(i+1)], hash_or_mark, line_len)
        else:
            break

    
    # if new_start[2] == 10:
    #     breakpoint()

    # cur_start = new_start
    return cur_start

def align_up_to_valid(starts, line_len, hash_or_mark):#, line):
    # breakpoint()
    for i in range(len(starts)):
        if starts[i] >= line_len:
            return starts
        while hash_or_mark[starts[i]] == 0:
            starts[i]+=1
            if starts[i] >= line_len:
                return starts
    # for i in range(starts):
    #     if starts[i] >= line_len:
    #         return starts
    #     while line[starts[i]] == '.':
    #         starts[i] += 1
    #         if starts[i] >= line_len:
    #             return starts
    return starts

def num_combinations(line, groups):
    '''
    memoization gameplan:
    (0,0,0)
        (0,0,1), (0,0,2), (0,0,3), (0,0,4), (0,0,5)
    (0,1,0)
        (0,1,1), (0,1,2), (0,1,3), (0,1,4), (0,1,5)
    (0,2,0)
        (0,2,1), (0,2,2), (0,2,3), (0,2,4), (0,2,5)
    
    As we explore the end of a line, we can recall data we have previously processed.
    If (0,0,3) til the end had 2 valid combinations, then we know that any valid
    combination with (x,x,3) will have 2 valid combinations til the end.

    If we looked at possible_starts = (0,0,0)...(0,0,7)
    and then we start looking at (0,1,2), we know that rom (0,1,2)...(0,1,7)
    there are the same number of valid combinations as from (0,0,2)...(0,0,7)
    '''
    n_groups = len(groups)
    line_len = len(line)

    hash_or_mark = [1 if s in ['#', '?'] else 0 for s in line]

    combinations = 0
    starts = [0]*n_groups
    # Pick good starts!
    for i in range(n_groups):
        if i == 0: continue
        starts[i] = starts[i-1] + groups[i-1] + 1

    starts = align_up_to_valid(starts, line_len, hash_or_mark)
    # print('---')
    # print(line)

    while True:

        valid, first_fail = is_valid(line, groups, starts, n_groups, line_len)
        if valid:
            combinations += 1
        # print(f'{starts}')
            # print(f'Valid combination {ps}')
        starts = next_start(starts, groups, n_groups, line_len, first_fail, hash_or_mark)
        if not starts:
            break
    return combinations


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

        # print(f'Solving line {line}')
        # print(s)
        # print(gs)


        # valid = is_valid(s, gs, (0,1,4))
        combinations = num_combinations(s, gs)
        res += combinations
        # print(f'Found {combinations} combinations for line {s} {g}')

    duration = time.time() - start
    print(f'Part 1: {res}')
    print(f'Part 1 latency: {duration:.5f}s')

if __name__ == '__main__':
    main()