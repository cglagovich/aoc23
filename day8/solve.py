def gcd(x, y):
    while y:
        x, y = y, x % y

    return int(x)

def lcm(x, y):
    return int(x * y / gcd(x, y))

def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.readlines()

    lr = [*inp[0][:-1]]

    dirs = [l.strip() for l in inp[2:]]
    m = {}
    for d in dirs:
        n, tup = d.split(' = ')
        l, r = tup[1:-1].split(', ')
        m[n] = (l, r)

    cur = 'AAA'
    end = 'ZZZ'
    step = 0

    while 1:
        lr_idx = step % len(lr)
        step +=1 
        d_idx = 0 if lr[lr_idx] == 'L' else 1

        n = m[cur][d_idx]

        # print(f'Moving from {cur} to {n}')
        cur = n
        if cur == end:
            break

    print(f'Part 1: {step}')

    curs = list(filter(lambda x: x[2] == 'A', m.keys()))
    periods = [None]*len(curs)
    print(curs)

    # Will each cur return to its start?
    step = 0
    while 1:
        lr_idx = step % len(lr)
        step +=1 
        d_idx = 0 if lr[lr_idx] == 'L' else 1

        for i in range(len(curs)):
            curs[i] = m[curs[i]][d_idx]
            if curs[i][2] == 'Z':
                if periods[i] is None:
                    periods[i] = step

        if all([x is not None for x in periods]):
            print(f'Found all periods. Breaking')
            break

    print(periods)

    lc = periods[0]
    # How to do LCM of 6 numbers??
    for i in range(1, len(periods)):
        lc = lcm(lc, periods[i])

    print(f'Part 2: {lc}')

if __name__ == '__main__':
    main()