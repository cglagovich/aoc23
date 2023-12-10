def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.readlines()

    inp =[[int(a.strip()) for a in x.split(' ')] for x in inp]
    print(inp)

    res = 0
    res2 = 0
    for series in inp:
        s = series
        diffs = []
        while 1:
            cur_diffs = []
            for i in range(1, len(s)):
                cur_diffs.append(s[i] - s[i-1])
            diffs.append(cur_diffs)
            s = cur_diffs
            if all(x == s[0] for x in s):
                break
        print(f'original series {series}')
        print(f'diffs: {diffs}')
        next_item = sum([d[-1] for d in diffs]) + series[-1]
        print(f'next item: {next_item}')

        res += next_item

        sub = 0
        for diff in diffs[::-1]:
            sub = diff[0] - sub
        prev_item = series[0] - sub
        print(f'previous item: {prev_item}')

        res2 += prev_item

    print(f'Part 1: {res}')
    print(f'Part 2: {res2}')

if __name__ == '__main__':
    main()