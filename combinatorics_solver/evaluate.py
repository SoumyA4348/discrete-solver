import os
import sys
from collections import Counter

import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver_service import SolverService

_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(_DIR, "combinatorics_model.joblib")


def evaluate(model):
    """Scores the full pipeline on held-out questions: operation, n and r, and the final answer."""
    df = pd.read_csv(os.path.join(_DIR, "eval_questions.csv"))
    train = pd.concat([pd.read_csv(os.path.join(_DIR, name)) for name in ("dataset.csv", "train_generated.csv")
                       if os.path.exists(os.path.join(_DIR, name))], ignore_index=True)
    overlap = set(df["question"].str.lower()) & set(train["question"].str.lower())
    if overlap:
        raise SystemExit(f"Held-out questions also appear in the training data: {sorted(overlap)}")

    service = SolverService(model)
    predicted = model.predict(df["question"])
    op_ok = nr_ok = answer_ok = 0
    failures = Counter()
    for row, pred in zip(df.itertuples(), predicted):
        expected, _ = service._calculate(row.operation, row.n, row.r)
        op_ok += pred == row.operation
        try:
            result = service.solve_question(row.question)
        except ValueError:
            failures["no answer"] += 1
            continue
        if (result["n"], result["r"]) == (row.n, row.r):
            nr_ok += 1
        if result["answer"] == expected:
            answer_ok += 1
        elif pred != row.operation:
            failures["wrong operation"] += 1
        else:
            failures["wrong n or r"] += 1

    total = len(df)
    print(f"Held-out questions: {total}")
    print(f"  operation correct:  {op_ok}/{total} ({op_ok / total:.0%})")
    print(f"  n and r correct:    {nr_ok}/{total} ({nr_ok / total:.0%})")
    print(f"  final answer right: {answer_ok}/{total} ({answer_ok / total:.0%})")
    print(f"  failures: {dict(failures)}")
    print("\n" + classification_report(df["operation"], predicted, zero_division=0))
    labels = sorted(df["operation"].unique())
    short = ["".join(w[0] for w in l.split("_")).upper() for l in labels]
    print("Confusion matrix (rows = true, columns = predicted):")
    print(pd.DataFrame(confusion_matrix(df["operation"], predicted, labels=labels), index=short, columns=short))
    print("  " + ", ".join(f"{s} = {l}" for s, l in zip(short, labels)))

    folds = cross_val_score(model, train["question"], train["operation"], cv=5)
    print(f"\n5-fold cross-validation on the training set: {folds.mean():.0%} (+/- {folds.std():.0%})")


if __name__ == "__main__":
    evaluate(joblib.load(MODEL_PATH))
