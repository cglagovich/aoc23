def main():
    with open('input.txt') as f:
        lines = f.readlines()

    digits = [str(c) for c in list(range(10))]

    sum = 0
    for line in lines:
        first = None
        second = None
        for c in line:
            if c in digits:
                if first is None:
                    first = c
                second = c
        num = int(first + second)
        print(num)
        sum += num

    print(f"Answer is {sum}")


if __name__ == '__main__':
    main()