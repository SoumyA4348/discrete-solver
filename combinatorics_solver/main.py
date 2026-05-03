import sys
import os
import re
import joblib

# Add the parent directory to sys.path to import math_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import math_engine

def extract_numbers(text: str):
    """Use Regular Expressions to find all numbers in the text."""
    # \d+ matches 1 or more digits
    numbers = [int(num) for num in re.findall(r'\d+', text)]
    if len(numbers) >= 2:
        return numbers[0], numbers[1]
    elif len(numbers) == 1:
        # Only one number found (e.g. "arrange 5 people in a line")
        # Treat as choosing all items: n = r = that number
        return numbers[0], numbers[0]
    return 0, 0

def solve_word_problem(text: str):
    print("COMBINATORICS SOLVER")
    print(f"User Question: '{text}'\n")
    
    print("[1] NLP Extraction layer...")
    
    # Load our trained ML model to predict the operation
    try:
        model_path = os.path.join(os.path.dirname(__file__), "combinatorics_model.joblib")
        model = joblib.load(model_path)
        prediction = model.predict([text])
        operation = prediction[0]
        print("    -> ML Model loaded successfully.")
    except Exception as e:
        print("    -> Error loading ML model. Please run load_data.py first!")
        return

    # Extract numbers using RegEx
    val1, val2 = extract_numbers(text)
    
    # Heuristic to assign n and r based on the operation
    if operation == "combinations_with_replacement":
        # C(n+r-1, r): n = number of categories (types/bins), r = items to pick.
        # In most word problems the category count (bins/flavors/boxes) appears
        # as the SECOND number, e.g. "15 candies among 5 children" → n=5, r=15.
        # We use the first extracted number as r and the second as n.
        r = val1
        n = val2
    else:
        # For permutations and standard combinations, we normally choose 'r' from 'n'
        # so n is the larger number
        n = max(val1, val2)
        r = min(val1, val2)
        
    print(f"    -> Identified [n]: {n}")
    print(f"    -> Identified [r]: {r}")
    print(f"    -> ML Predicted Operation: {operation}\n")
    
    # Calculate using our Math Engine
    print("[2] Math Engine layer...")
    
    if operation == "permutations":
        answer = math_engine.calculate_permutations(n, r)
    elif operation == "combinations":
        answer = math_engine.calculate_combinations(n, r)
    elif operation == "permutations_with_replacement":
        answer = math_engine.calculate_permutations_with_replacement(n, r)
    elif operation == "combinations_with_replacement":
        answer = math_engine.calculate_combinations_with_replacement(n, r)
    else:
        answer = "Unknown operation"
        
    print(f"    -> Called function for: {operation}")
    print(f"\n[DONE] Result: There are {answer} ways to do this!")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Welcome to the Discrete Math Combinatorics Solver!")
    print("Type your word problem below, or type 'exit' to quit.")
    print("="*50)
    
    while True:
        user_input = input("\n[Enter your question] (or 'exit'): ")
        
        if user_input.strip().lower() in ['exit', 'quit']:
            print("Thanks for using the solver! Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        print("-" * 50)
        solve_word_problem(user_input)
        print("-" * 50)