import tqdm
import numpy as np
import time
from numba import njit
from functools import lru_cache, wraps

def np_cache(function):
    @lru_cache()
    def cached_wrapper(hashable_array):
        array = np.array(hashable_array)
        return function(array)

    @wraps(function)
    def wrapper(array):
        return cached_wrapper(tuple(tuple(a) for a in array))

    # copy lru_cache attributes over too
    wrapper.cache_info = cached_wrapper.cache_info
    wrapper.cache_clear = cached_wrapper.cache_clear

    return wrapper

# def transpose(puzzle):
#     cols = [[] for _ in range(len(puzzle[0]))]
#     for row in puzzle:
#         for idx, char in enumerate(row):
#             cols[idx].append(char)

#     c = []
#     for col in cols:
#         c.append(''.join(col))
#     return c

def get_weight(row):
    tot = 0
    for i, char in enumerate(row):
        weight = len(row) - i
        if char == 'O':
            tot += weight
    return tot

def reverse_puzzle(puzzle):
    res = []
    for row in puzzle:
        res.append(''.join(reversed(row)))
    return res

def shift_left(row):
    n = [None]*len(row)
    for i in range(len(row)):
        n[i] = row[i]
        if n[i] == 'O':
            for j in range(1, i+1):
                if n[i-j] == '.':
                    n[i-j] = 'O'
                    n[i-j+1] = '.'
                else:
                    break
    return ''.join(n)

# @njit
def _shift_left(row):
    for i in range(len(row)):
        if row[i] == 'O':
            for j in range(1, i+1):
                if row[i-j] == '.':
                    # Swap 
                    row[i-j] = 'O'
                    row[i-j+1] = '.'
                else:
                    break

# @np_cache
# @njit
def _shift_puzzle_left(puzzle):
    # puzzle = np.array(puzzle)
    for r in range(puzzle.shape[0]):
        _shift_left(puzzle[r,:])

def shift_puzzle_left(puzzle):
    res = []
    for row in puzzle:
        res.append(list(shift_left(row)))

    res = np.array(res)

    return res

def spin(puzzle):
    # North, West, South, East

    # North
    # Transpose, shift left (output transposed)
    # puzzle = transpose(puzzle)
    puzzle = puzzle.transpose()
    # puzzle = shift_puzzle_left(puzzle)
    # breakpoint()
    _shift_puzzle_left(puzzle)

    # West
    # Transpose, shift left (output normal)
    # puzzle = transpose(puzzle)
    puzzle = puzzle.transpose()
    # puzzle = shift_puzzle_left(puzzle)
    _shift_puzzle_left(puzzle)

    # South
    # Transpose, reverse, shift left (output transposed, reversed)
    # puzzle = transpose(puzzle)
    puzzle = puzzle.transpose()
    puzzle = np.flip(puzzle, axis=1)
    # puzzle = shift_puzzle_left(puzzle)
    _shift_puzzle_left(puzzle)

    # East
    # reverse, transpose, reverse, shift left (output reversed)
    puzzle = np.flip(puzzle, axis=1)
    puzzle = puzzle.transpose()
    # puzzle = transpose(puzzle, reverse=False)
    puzzle = np.flip(puzzle, axis=1)
    # puzzle = shift_puzzle_left(puzzle)
    _shift_puzzle_left(puzzle)
    puzzle = np.flip(puzzle, axis=1)
    # puzzle = reverse_puzzle(puzzle)
    # return
    return puzzle

def print_puzzle(puzzle):
    ret = ''
    for row in puzzle:
        ret += row
        ret += '\n'

    print(ret)

def print_np(puzzle):
    ret = ''
    for row in puzzle:
        r = list(row)
        r = ''.join(r)
        ret += r
        ret += '\n'

    print(ret)

def get_weight_np(puzzle):
    n_rows = puzzle.shape[0]
    ret = 0
    for i, row in enumerate(puzzle):
        for char in row:
            if char == 'O':
                ret += (n_rows - i)
    return ret

def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.readlines()
    
    start = time.time() 
    puzzle = []
    for line in inp:
        puzzle.append(list(line.strip()))

    puzzle = np.array(puzzle)

    # print_puzzle(puzzle)
    # print_np(puzzle)
    puzzle_cache = {}
    for i in tqdm.tqdm(range(1000)):
        puzzle = spin(puzzle)
        # print(f'Spin {i}')
        # print_np(puzzle)

        weight = get_weight_np(puzzle)

        puzzle_hashable = tuple(tuple(a) for a in puzzle)
        match = puzzle_cache.setdefault(puzzle_hashable, [])
        match.append((i, weight))
        if len(match) > 1:
            print(f'Found match during iteration [{i}]. Matches {match}')
        else:
            print("### NO MATCH for idx {i}")


    # We got the cache. Now find it for 1B
    goal = 1_000_000_000-1
    ret = None

    for value in puzzle_cache.values():
        if len(value) >= 2:
            base_idx, weight = value[0]
            next_idx, _ = value[1]
            period = next_idx - base_idx
            if (goal - base_idx) % period == 0:
                ret = weight
                print(f'Found match for 1B. base_idx {base_idx}, period {period}, weight {weight}')
                break







    print(f'Part 1: {ret}')
    print(f'Part 1 latency: {time.time() - start:.5f}')

if __name__ == '__main__':
    main()