"""
Advent of Code day 22 part 1
Written by Trevor Ferris
2/5/2024
"""

from typing import Iterator
from time import time

PRICE_FILENAME = "Aoc22/inputtest.txt"
PRUNE_MOD = 16777216
NUM_SECRETS = 2000
M1 = 64
M2 = 2048
D1 = 32

def load_prices(file_name: str) -> list[str]:
    with open(file_name, "r") as price_file:
        return [int(line.rstrip("\n")) for line in price_file]

def prune(price: int) -> int:
    return price % PRUNE_MOD

def mix(price: int, n_price: int) -> int:
    return price ^ n_price

def calc_secret(prices: int) -> Iterator[int]:
    for price in prices:
        for x in range(NUM_SECRETS):
            price = prune(mix(price, price * M1))
            price = prune(mix(price, price // D1))
            price = prune(mix(price, price * M2))
        yield price

def main():
    start_time = time()
    prices = load_prices(PRICE_FILENAME)
    print(f"Total of secret prices: {sum(calc_secret(prices))}")
    end_time = time()
    print(f"Time: {end_time - start_time}")

if __name__ == ("__main__"):
    main()