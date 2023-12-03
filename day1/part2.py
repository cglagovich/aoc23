def number_word_to_digit(substr):
    # Given some str, return the digit for whichever number word is contained
    # Assert there is only one number word
    digit_mapping = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

    digits = []
    for k, v in digit_mapping.items():
        if k in substr:
            digits.append(str(v))

    assert len(digits) <= 1, "input should only have one number word:" + substr
    return None if len(digits) == 0 else digits[0]



def main():
    with open('input.txt') as f:
        lines = f.readlines()

    digits = [str(c) for c in list(range(10))]

    # In part 2, let's work from the front and then the back since we might have strings like "eightwo"
    # which should be parsed as 82
    sum = 0
    for line in lines:
        first = None
        second = None

        # Get first digit
        left_substr = ""
        for c in line:
            left_substr += c
            word_digit = number_word_to_digit(left_substr)
            if c in digits:
                first = c
                break
            elif word_digit is not None:
                first = word_digit
                break

        right_substr = ""
        for c in reversed(line):
            right_substr = c + right_substr
            word_digit = number_word_to_digit(right_substr)
            if c in digits:
                second = c
                break
            elif word_digit is not None:
                second = word_digit
                break

        # Get second digit
        num = int(first + second)
        print(num)
        sum += num

    print(f"Answer is {sum}")


if __name__ == '__main__':
    main()