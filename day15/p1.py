import time   

def myhash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256

    return h


def main():
    start = time.time()
    inp_f = 'input.txt'
    with open(inp_f) as f:
        inp = f.read().strip()

    res = 0

    steps = inp.split(',')
    
    for step in steps:
        res += myhash(step)

    print(f'Part 1: {res}')
    print(f'Part 1 latency: {time.time() - start:.5f}')

if __name__ == '__main__':
    main()