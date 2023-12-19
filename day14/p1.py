import time

def transpose(puzzle):
    cols = [[] for _ in range(len(puzzle[0]))]
    for row in puzzle:
        for idx, char in enumerate(row):
            cols[idx].append(char)

    c = []
    for col in cols:
        c.append(''.join(col))
    return c

def shift_left(row):
    n = [None]*len(row)
    for i in range(len(row)):
        n[i] = row[i]
        if n[i] == 'O':
            # breakpoint()
            for j in range(1, i+1):
                if n[i-j] == '.':
                    n[i-j] = 'O'
                    n[i-j+1] = '.'
                else:
                    break
    return ''.join(n)

def get_weight(row):
    tot = 0
    for i, char in enumerate(row):
        weight = len(row) - i
        if char == 'O':
            tot += weight
    return tot         

def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.readlines()
    
    start = time.time()
    res = 0
    puzzle = []
    for line in inp:
        puzzle.append(line.strip())

    c = transpose(puzzle)
    # print(c)

    # Deal by row
    shifted = []
    for r in c:
        sl = shift_left(r)

        weight = get_weight(sl)
        res += weight




    print(f'Part 1: {res}')
    print(f'Part 1 latency: {time.time() - start:.5f}')

if __name__ == '__main__':
    main()