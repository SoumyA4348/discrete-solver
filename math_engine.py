import math
from typing import Union

def calculate_permutations(n: int, r: int) -> int:
    """
    Calculates nPr (Permutation) - The number of ways to arrange 'r' items from a set of 'n'.
    Order matters. Formula: n! / (n-r)!
    
    :param n: Total number of items in the set.
    :param r: Number of items to arrange.
    :return: Number of permutations. Returns 0 for invalid inputs.
    """
    if r > n or n < 0 or r < 0:
        return 0
    return math.perm(n, r)

def calculate_combinations(n: int, r: int) -> int:
    """
    Calculates nCr (Combination) - The number of ways to choose 'r' items from a set of 'n'.
    Order does NOT matter. Formula: n! / (r! * (n-r)!)
    
    :param n: Total number of items in the set.
    :param r: Number of items to choose.
    :return: Number of combinations. Returns 0 for invalid inputs.
    """
    if r > n or n < 0 or r < 0:
        return 0
    return math.comb(n, r)

def calculate_permutations_with_replacement(n: int, r: int) -> int:
    """
    Calculates Permutation with replacement.
    Order matters, items can be repeated. Formula: n^r
    
    :param n: Number of options for each choice.
    :param r: Number of choices made.
    :return: Number of permutations with replacement. Returns 0 for invalid inputs.
    """
    if n < 0 or r < 0:
        return 0
    return n ** r

def calculate_combinations_with_replacement(n: int, r: int) -> int:
    """
    Calculates Combination with replacement.
    Order does NOT matter, items can be repeated. Formula: (n+r-1)! / (r! * (n-1)!)
    
    :param n: Number of options to choose from.
    :param r: Number of items to choose.
    :return: Number of combinations with replacement. Returns 0 for invalid inputs.
    """
    if n <= 0 or r < 0:
        return 0
    return math.comb(n + r - 1, r)

def calculate_derangements(n: int) -> int:
    """
    Calculates the number of derangements of n items (subfactorial !n).
    A derangement is a permutation where no element appears in its original position.
    
    :param n: Number of items.
    :return: Number of derangements. Returns 0 for invalid inputs.
    """
    if n < 0:
        return 0
    if n == 0:
        return 1
    d = 0 if n == 1 else 1 # Subfactorial !1=0, !2=1
    if n == 1: return 0
    if n == 2: return 1
    
    # Using the iterative approach for !n = (n-1)(!(n-1) + !(n-2))
    # or the simple iterative: d(i) = i*d(i-1) + (-1)^i
    d = 1
    for i in range(1, n + 1):
        d = i * d + (-1)**i
    return d

def calculate_circular_permutations(n: int) -> int:
    """
    Calculates circular permutations of n items.
    The number of unique ways to arrange n items in a circle.
    Formula: (n - 1)!
    
    :param n: Number of items.
    :return: Number of circular permutations. Returns 0 for invalid inputs.
    """
    if n <= 0:
        return 0
    return math.factorial(n - 1)

# Testing the code
if __name__ == "__main__":
    print("Testing Math Engine...")
    print(f"Permutations of 5 items picking 3 (5P3): {calculate_permutations(5, 3)}")           # Should be 60
    print(f"Combinations of 5 items picking 3 (5C3): {calculate_combinations(5, 3)}")           # Should be 10
    print(f"Permutations w/ replacement of 2 items picking 3: {calculate_permutations_with_replacement(2, 3)}") # Should be 8
    print(f"Combinations w/ replacement of 4 items picking 2: {calculate_combinations_with_replacement(4, 2)}") # Should be 10
    print(f"Derangements of 4 items: {calculate_derangements(4)}") # Should be 9
    print(f"Circular permutations of 5 items: {calculate_circular_permutations(5)}") # Should be 24
