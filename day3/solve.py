from functools import reduce

def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        lines = f.readlines()

    # Pad input
    arr = ['.'+line.strip()+'.' for line in lines]
    pad_line = '.'*len(arr[0])
    arr.insert(0, pad_line)
    arr.append(pad_line)
    
    # Find each number in each line. Keep it around if you find a symbol nearby
    # What are the symbols?
    digits = [str(x) for x in range(10)]
    symbols = ['*', '@', '#', '$', '+', '%', '/', '&', '=', '-']
    stop_chars = symbols + ['.']

    part_sum = 0
    gear_map = {}

    for r in range(1, len(arr)-1):
        curr_num = 0
        num_range = [0,0]
        for c in range(len(arr[r])):
            e = arr[r][c]
            if e in digits:
                if curr_num == 0:
                    num_range[0] = c
                curr_num = curr_num*10 + int(e)
            
            if e in stop_chars:
                if curr_num == 0:
                    continue
                
                num_range[1] = c-1
                # print(f'Found {curr_num} at indices {num_range}')

                # Check for symbol touching
                valid = False
                for r_check in range(r-1, r+2):
                    for c_check in range(num_range[0]-1, num_range[1]+2):
                        if arr[r_check][c_check] in symbols:
                            valid = True

                        if arr[r_check][c_check] == '*':
                            if (r_check, c_check) not in gear_map:
                                gear_map[(r_check, c_check)] = [curr_num]
                            else:
                                gear_map[(r_check, c_check)].append(curr_num)
                        
                if valid:
                    part_sum += curr_num
                    print(f'Valid number {curr_num} at {[r, num_range[0]]}')


                curr_num = 0
                num_range = [0,0]

    # Find gears with exactly two neighbors
    gear_ratio_sum = 0
    for k, v in gear_map.items():
        if len(v) == 2:
            gear_ratio_sum += v[0] * v[1]
            
    print(f'Part 1: {part_sum}')
    print(f'Part 2: {gear_ratio_sum}')

    assert part_sum == 539590
    assert gear_ratio_sum == 80703636




if __name__ == '__main__':
    main()