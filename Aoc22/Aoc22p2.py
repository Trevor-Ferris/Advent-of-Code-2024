"""
Advent of Code day 22 part 2
Written by Trevor Ferris
2/5/2024
Notes: Slow as hell but pretty easy. Also I noticed that each value is the same so theres probably a better algo I could use
"""
"""                   PART TWO THOUGHT PROCESS
        GOAL: find the highest number of bananas from a list of prices
        1. The actual price is equal to the last digit of the price (%10)
        2. The monkey looks for a set of 4 numbers and then immediately sells
        3. Each price can only sell one time
        4. The sequence is the same for each price
        
        STEPS
        1. Run the part 1 calcs
        2. While running it record a running total of the diffs
        3. The first time a given diff happens record that price into a dict of diffs
        4. Run through the dict and find the diff that has the highest sum"""

from time import time

PRICE_FILENAME = "Aoc22/input.txt"
PRUNE_MOD = 16777216
NUM_SECRETS = 2000
M1 = 64
M2 = 2048
D1 = 32
DIFF_LEN = 4

def load_prices(file_name):
    with open(file_name, "r") as price_file:
        return [int(line.rstrip("\n")) for line in price_file]

def prune(price: int) -> int:
    return price % PRUNE_MOD

def mix(price: int, n_price: int) -> int:
    return price ^ n_price

def init_diff_dict() -> dict[tuple[int, int, int, int]: list]:
    """Initializes a dictionary containing each possible set of diffs"""

    diff_dict = {}
    for w in range(-9, 10):
        for x in range(-9, 10):
            for y in range(-9, 10):
                for z in range(-9, 10):
                    diff_dict[(w, x, y, z)] = []
    return diff_dict

def calc_secret(prices: int) -> int:
    """Calculates the sequence of price differences that result in the highest value
    
    Calculates the first 2000 secret numbers of the prices recording price changes 
    when a new series of 4 changes happens, records the price at the location

    Args:
        prices: the list of prices from the file

    Returns:
        The highest sum of prices from any of the recorded price changes
    """

    diff_dict = init_diff_dict()
    for price in prices:
        diffs, used_diffs = [], []
        prev_price = price
        for x in range(NUM_SECRETS):
            price = prune(mix(price, price * M1))
            price = prune(mix(price, price // D1))
            price = prune(mix(price, price * M2))
            diffs.append(price % 10 - prev_price % 10)
            if len(diffs) > DIFF_LEN:                    
                diffs = diffs[1:]
            if len(diffs) >= DIFF_LEN:
                if tuple(diffs) not in used_diffs:
                    diff_dict[tuple(diffs)].append(price % 10)
                    used_diffs.append(tuple(diffs))
            prev_price = price
    return max(sum(diff) for diff in diff_dict.values())

def main():
    start_time = time()
    prices = load_prices(PRICE_FILENAME)
    print("Calculating best sequence")
    print(f"Highest value: {(calc_secret(prices))}")
    end_time = time()
    print(f"Time: {end_time - start_time}")

if __name__ == ("__main__"):
    main()