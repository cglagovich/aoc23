from re import A


def num_wins(t, d):
        # there are two (t_early * t-t_early), (t_late * t-t_late) which both equal d
    max_t = int(d**.5)
    while True:
        if max_t * (t-max_t) <= d:
            break
        max_t -= 1
    t_early = max_t + 1
    # print(t_early)
    t_late = t - max_t
    # print(t_late)
    num_wins = t_late - t_early
    # print(f'(t,d) {(t,d)}. num_wins = {num_wins}, t_early={t_early}')
    return num_wins


def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.readlines()
    x = [list(filter(lambda x: x is not None, [int(x.strip()) if len(x.strip()) != 0 else None for x in inp[i].split(':')[1].split(' ')])) for i in range(2)]
    races = list(zip(x[0], x[1]))

    mult = 1
    for t, d in races:
        mult *= num_wins(t,d)
    print(f'Part 1: {mult}')

    t = [str(d) for d in x[0]]
    t = int(''.join(t))
    print(t)
    d = [str(y) for y in x[1]]
    d = int(''.join(d))
    print(d)

    mult = num_wins(t,d)
    print(mult)


if __name__ == '__main__':
    main()