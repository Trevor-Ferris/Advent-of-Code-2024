"""
Advent of Code day 7 part 2
Written by Trevor Ferris
1/17/2025
"""

BRIDGE_FILENAME = "Aoc7/input.txt"

def load_bridge(file_name):
    inFile = open(file_name, 'r')
    results, nums = [], []
    for line in inFile:
        (result, num_list) = line.split(':')
        nums.append(list(map(int, num_list.split())))
        results.append(int(result))
    return (results, nums)

def calc_after(nums):
    pos_res = []
    for i in range(1, len(nums)):
        prev_res = pos_res.copy()
        pos_res.clear()
        if i == 1:
            pos_res.append(int(str(nums[0]) + str(nums[1])))
            pos_res.append(nums[0] + nums[1])
            pos_res.append(nums[0] * nums[1])
        else:
            for res in prev_res:
                pos_res.append(int(str(res) + str(nums[i])))
                pos_res.append(res + nums[i])
                pos_res.append(res * nums[i])
    return pos_res

def check_results(results, nums):
    total_corr = 0
    for index, result in enumerate(results):
        pos_res = calc_after(nums[index])
        if result in pos_res:
            total_corr += result
    return total_corr

if __name__ == ('__main__'):
    (results, nums) = load_bridge(BRIDGE_FILENAME)
    print("Calibrating...")
    print("Calibration result:", check_results(results, nums))
