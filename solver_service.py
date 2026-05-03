import re
from typing import List, Dict, Any, Tuple
import math_engine

NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "twenty": 20, "dozen": 12
}

FORMULAS = {
    "permutations": r"\frac{n!}{(n - r)!}",
    "combinations": r"\frac{n!}{r!(n - r)!}",
    "permutations_with_replacement": r"n^r",
    "combinations_with_replacement": r"\frac{(n + r - 1)!}{r!(n - 1)!}",
    "derangements": r"!n = n! \sum_{i=0}^{n} \frac{(-1)^i}{i!}",
    "circular_permutations": r"(n - 1)!",
}

LABELS = {
    "permutations": "Permutations",
    "combinations": "Combinations",
    "permutations_with_replacement": "Permutations (W. Replacement)",
    "combinations_with_replacement": "Combinations (W. Replacement)",
    "derangements": "Derangements",
    "circular_permutations": "Circular Permutations",
}

def extract_numbers(text: str) -> List[int]:
    """Extracts integers from text, including word-based numbers."""
    text_lower = text.lower()
    for word, num in NUMBER_WORDS.items():
        text_lower = re.sub(rf'\b{word}\b', str(num), text_lower)
    return [int(num) for num in re.findall(r'\d+', text_lower)]

class SolverService:
    def __init__(self, model: Any = None):
        self.model = model

    def solve_question(self, question: str) -> Dict[str, Any]:
        """
        Parses a question, predicts the operation, and calculates the result.
        """
        if self.model is None:
            raise ValueError("ML model not loaded.")

        try:
            operation = self.model.predict([question])[0]
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")

        numbers = extract_numbers(question)
        if not numbers:
            raise ValueError("No numbers found in your question. Please include values for calculation.")

        # Determine n and r based on operation and extracted numbers
        if len(numbers) >= 2:
            val1, val2 = numbers[0], numbers[1]
        else:
            val1 = val2 = numbers[0]

        if operation == "combinations_with_replacement":
            r, n = val1, val2
        else:
            n, r = max(val1, val2), min(val1, val2)

        if len(numbers) == 1:
            n = r = val1

        if n > 10000 or r > 10000:
            raise ValueError("Numbers are too large (max 10,000). Please enter smaller numbers.")

        # Calculate result
        answer, expression = self._calculate(operation, n, r)

        return {
            "operation": operation,
            "operation_label": LABELS.get(operation, operation),
            "formula": FORMULAS.get(operation, ""),
            "expression": expression,
            "n": n,
            "r": r,
            "answer": answer,
        }

    def _calculate(self, operation: str, n: int, r: int) -> Tuple[int, str]:
        if operation == "permutations":
            return math_engine.calculate_permutations(n, r), fr"P({n}, {r})"
        elif operation == "combinations":
            return math_engine.calculate_combinations(n, r), fr"\binom{{{n}}}{{{r}}}"
        elif operation == "permutations_with_replacement":
            return math_engine.calculate_permutations_with_replacement(n, r), fr"{n}^{{{r}}}"
        elif operation == "combinations_with_replacement":
            return math_engine.calculate_combinations_with_replacement(n, r), fr"\binom{{{n} + {r} - 1}}{{{r}}}"
        elif operation == "derangements":
            return math_engine.calculate_derangements(n), fr"!{n}"
        elif operation == "circular_permutations":
            return math_engine.calculate_circular_permutations(n), fr"({n} - 1)!"
        else:
            raise ValueError(f"Unknown operation: '{operation}'")
