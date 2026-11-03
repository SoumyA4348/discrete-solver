import sys
import os
import pytest

# Add parent directory to path to import math_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import math_engine

def test_permutations():
    assert math_engine.calculate_permutations(5, 3) == 60
    assert math_engine.calculate_permutations(5, 5) == 120
    assert math_engine.calculate_permutations(5, 0) == 1
    assert math_engine.calculate_permutations(5, 6) == 0
    assert math_engine.calculate_permutations(-1, 2) == 0

def test_combinations():
    assert math_engine.calculate_combinations(5, 3) == 10
    assert math_engine.calculate_combinations(5, 5) == 1
    assert math_engine.calculate_combinations(5, 0) == 1
    assert math_engine.calculate_combinations(5, 6) == 0
    assert math_engine.calculate_combinations(-1, 2) == 0

def test_permutations_with_replacement():
    assert math_engine.calculate_permutations_with_replacement(2, 3) == 8
    assert math_engine.calculate_permutations_with_replacement(5, 2) == 25
    assert math_engine.calculate_permutations_with_replacement(5, 0) == 1
    assert math_engine.calculate_permutations_with_replacement(0, 5) == 0
    assert math_engine.calculate_permutations_with_replacement(-1, 2) == 0

def test_combinations_with_replacement():
    assert math_engine.calculate_combinations_with_replacement(4, 2) == 10
    assert math_engine.calculate_combinations_with_replacement(1, 5) == 1
    assert math_engine.calculate_combinations_with_replacement(4, 0) == 1
    assert math_engine.calculate_combinations_with_replacement(0, 2) == 0

def test_derangements():
    assert math_engine.calculate_derangements(0) == 1
    assert math_engine.calculate_derangements(1) == 0
    assert math_engine.calculate_derangements(2) == 1
    assert math_engine.calculate_derangements(3) == 2
    assert math_engine.calculate_derangements(4) == 9
    assert math_engine.calculate_derangements(5) == 44
    assert math_engine.calculate_derangements(-1) == 0


def test_derangements_larger_values():
    assert math_engine.calculate_derangements(10) == 1334961
    assert math_engine.calculate_derangements(-5) == 0

def test_derangements_match_brute_force():
    from itertools import permutations
    for n in range(7):
        expected = sum(
            all(p[i] != i for i in range(n)) for p in permutations(range(n))
        )
        assert math_engine.calculate_derangements(n) == expected

def test_circular_permutations():
    assert math_engine.calculate_circular_permutations(5) == 24
    assert math_engine.calculate_circular_permutations(1) == 1
    assert math_engine.calculate_circular_permutations(0) == 0
    assert math_engine.calculate_circular_permutations(-1) == 0
