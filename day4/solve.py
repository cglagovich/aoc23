def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        lines = f.readlines()

    cards = [[[int(digit) for digit in card_side.split(' ') if len(digit)>0] for card_side in line.split(':')[1].strip().split('|')] for line in lines]
    # print(cards)

    scores = [int(2**(sum([1 if num in card[0] else 0 for num in card[1]])-1)) for card in cards]
    # print(scores)
    score = sum(scores)
    print(f'Part 1: {score}')

    score = 0
    card_idx_to_copies = {i: 1 for i in range(len(scores))}
    for idx, card in enumerate(cards):
        copy_range = sum([1 if num in card[0] else 0 for num in card[1]])
        local_copies = card_idx_to_copies[idx]
        # For each card in copy range, increase num copies by local copies
        for i in range(idx+1,idx+1+copy_range):
            card_idx_to_copies[i] += local_copies


        # local_score = local_copies * scores[idx]
    
    score = sum(card_idx_to_copies.values())

    print(f'Part 2: {score}')

        

if __name__ == '__main__':
    main()