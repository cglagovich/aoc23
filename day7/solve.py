import functools

'''
How do you map a hand to a key?

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

key = <num_matches><hand>

Replace AKQJT with edcba

5 of a kind -> 7
4 of a kind -> 6
full house -> 5
3 of a kind -> 4
two pair -> 3
one pair -> 2
high card -> 1
'''

def hand_to_key(h, jokers=False):
    def char_count(h):
        d = {}
        for c in h:
            if c not in d:
                d[c] = 1
            else:
                d[c] += 1
        return d

    def n_of_a_kind(d, jokers=False):
        if jokers:
            k = max([v if k != 'J' else 0 for k, v in d.items()])
            j = d.get('J', 0)
            k += j
            k = min(k, 5)
        else:
            k = max(d.values())
        return k

    def full_house(d, jokers=False):
        if jokers:
            j = d.get('J', 0)
            d_j = [d[k] if k != 'J' else 0 for k in d.keys()]
            counts_no_j = sorted(d_j, reverse=True)
            ret = (counts_no_j[0] + counts_no_j[1] + j) >= 5
        else:
            counts = sorted(d.values(), reverse=True)
            ret = counts[0] == 3 and counts[1] == 2

        return ret

    def two_pair(d, jokers=False):
        counts = sorted(d.values(), reverse=True)
        ret = counts[0] == 2 and counts[1] == 2
        if jokers and not ret and counts[0] <= 2:
            j = d.get('J', 0)
            ret = (counts[0] + counts[1] + j) >= 4
        return ret


    res = ''
    d = char_count(h)
    n_kind = n_of_a_kind(d, jokers=jokers)

    if n_kind == 5:
        # 5 of a kind
        res += '7'
    elif n_kind == 4:
        # 4 of a kind
        res += '6'
    elif full_house(d, jokers=jokers):
        # full house
        res += '5'
    elif n_kind == 3:
        # 3 of a kind
        res += '4'
    elif two_pair(d, jokers=jokers):
        # two pair
        res += '3'
    elif n_kind == 2:
        res += '2'
    elif n_kind == 1:
        res += '1'
    else:
        assert False, f"Can't have n_kind {n_kind} > 5"

    res += h
    # Replace AKQJT with edcba
    res = res.replace('A', 'e')
    res = res.replace('K', 'd')
    res = res.replace('Q', 'c')
    if jokers:
        res = res.replace('J', '0')
    else:
        res = res.replace('J', 'b')
    res = res.replace('T', 'a')

    assert len(res) == 6

    return res

def tally_bids(sorted_hands):
    res = 0
    for i, h in enumerate(sorted_hands):
        res += (i+1) * h[1]
    return res

def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.readlines()

    hands = [[i.strip() for i in i.split(' ')] for i in inp]
    hands = [[h0, int(h1)] for h0, h1 in hands]

    hands_keys = list(map(lambda x: [hand_to_key(x[0]), x[1]], hands))

    hands_ranked = sorted(hands_keys, key=lambda x: x[0])

    res = tally_bids(hands_ranked)
    print(f'Part 1: {res}')

    hands_keys = list(map(lambda x: [hand_to_key(x[0], jokers=True), x[1]], hands))

    hands_ranked = sorted(hands_keys, key=lambda x: x[0])

    res = tally_bids(hands_ranked)
    print(f'Part 2: {res}')


if __name__ == '__main__':
    main()