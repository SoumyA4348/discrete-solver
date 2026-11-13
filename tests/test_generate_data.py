import os
import sys

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "combinatorics_solver"))
import generate_data


def test_generated_set_is_balanced_unique_and_disjoint_from_eval():
    df = generate_data.generate()
    assert df["operation"].value_counts().nunique() == 1
    assert df["question"].str.lower().is_unique
    held_out = pd.read_csv(os.path.join(generate_data._DIR, "eval_questions.csv"))["question"].str.lower()
    assert not set(df["question"].str.lower()) & set(held_out)


def test_generation_is_deterministic():
    assert generate_data.generate().equals(generate_data.generate())
