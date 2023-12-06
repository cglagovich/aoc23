from tqdm import tqdm

def src_to_dst(src, mappings):
    # Perform mappping and return dst
    # mapping: [(dst_start, src_start, range_len), ...]
    dst = src
    for (dst_start, src_start, range_len) in mappings:
        if (src >= src_start) and (src < src_start + range_len):
            dst = (src - src_start) + dst_start

    return dst

def range_to_ranges(src_range, mappings):
    # A range of inputs is mapped to ranges of outputs
    src_start, src_len = src_range
    src_end = src_start + src_len - 1 # inclusive
    outputs = []
    src_used = []
    for (dst_start, map_src_start, range_len) in mappings:
        # find a mapping which spans a portion of the range
        map_src_end = map_src_start + range_len - 1 # inclusive
        if src_start <= map_src_end and src_end >= map_src_start:
            # We have overlapping ranges
            # Overlapping area
            max_start = max(src_start, map_src_start)
            min_end = min(src_end, map_src_end)
            # max_start to min_end is a newly mapped range
            out_start = max_start - map_src_start + dst_start
            out_len = min_end - max_start + 1
            outputs.append([out_start, out_len])
            src_used.append([max_start, out_len])

    # Return ranges. Note that a range is unchanged if it was not mapped
    src_used = sorted(src_used, key=lambda x: x[0])
    unchanged = []
    start = src_start
    for i in range(len(src_used)):
        if start < src_used[i][0]:
            unchanged.append([src_start, src_used[i][0]])
        # Update start to end of last used range
        start = src_used[i][0] + src_used[i][1]
    if start < src_end:
        unchanged.append([start, (src_end - start + 1)])

    return outputs + unchanged

def main():
    inp_f = 'input.txt'
    with open(inp_f) as f:
        lines = f.readlines()

    maps = [] # List of list of tuples, [map0, map1...]
    for line in lines:
        if 'seeds' in line:
            seeds = [int(seed.strip()) for seed in line.split(':')[1].strip().split(' ')]
        elif 'map' in line:
            maps.append([])
        elif len(line.split(' ')) > 1:
            maps[-1].append(tuple([int(map_item.strip()) for map_item in line.split(' ')]))

    # Part 1
    locations = []
    for s in seeds:
        dst = s
        for map in maps:
            dst = src_to_dst(dst, map)
        locations.append(dst)

    print(f'Part 1: {min(locations)}')

    inp_ranges = [seeds[i*2:(i+1)*2] for i in range(len(seeds)//2)]
    for i, map in enumerate(maps):
        out_ranges = []
        for inp in inp_ranges:
            out_ranges.extend(range_to_ranges(inp, map))
        
        inp_ranges = out_ranges

    loc_sorted = sorted(inp_ranges, key=lambda x: x[0])

    print(f'Part 2: {loc_sorted[0][0]}')



if __name__ == '__main__':
    main()