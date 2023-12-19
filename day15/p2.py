import time
from collections import deque

def myhash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256

    return h

def get_by_label(label, box):
    for i, lens in enumerate(box):
        if lens[0] == label:
            return i, lens
    return None, None

def print_boxes(boxes):
    for idx, box in enumerate(boxes):
        if len(box) > 0:
            print(f'Box {idx}: {box}')

def packboxes(s, boxes):
    if '=' in s:
        label, focal = s.split('=')
    elif '-' in s:
        label = s.split('-')[0]
    h = myhash(label)
    box = boxes[h]
    if '=' in s:
        # Add or replace
        label, focal = s.split('=')
        focal = int(focal)
        new_val = (label, focal)
        # Is this label already in box?
        idx, same_label = get_by_label(label, box)
        if same_label is not None:
            box.remove(same_label)
            box.insert(idx, new_val)
        else:
            box.append(new_val)
    elif '-' in s:
        # Remove
        label = s.split('-')[0]
        idx, same_label = get_by_label(label, box)
        if same_label is not None:
            box.remove(same_label)
    else:
        assert False

    print(f'After {s}')
    print_boxes(boxes)


def score_boxes(boxes):
    ret = 0
    for box_idx, box in enumerate(boxes):
        box_multiplier = 1+box_idx
        box_sum = 0
        for label_idx, label in enumerate(box):
            label_multiplier = 1+label_idx
            focal = label[1]
            box_sum += focal * label_multiplier
        ret += box_sum * box_multiplier

    return ret

def main():
    start = time.time()
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.read().strip()

    res = 0

    steps = inp.split(',')
    boxes = [deque() for _ in range(256)]
    # Box is a deque of tuples (label, focal)
    
    for step in steps:
        packboxes(step, boxes)

    res = score_boxes(boxes)

    print(f'Part 2: {res}')
    print(f'Part 2 latency: {time.time() - start:.5f}')

if __name__ == '__main__':
    main()