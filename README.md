# DiscreteSolver

A web app that solves combinatorics word problems using a trained ML classifier. Type a plain-English question and get the formula, LaTeX expression, and numerical answer.

## Features

- Natural language input — e.g. *"How many ways can 5 people be arranged in a row?"*
- ML model (SVC) classifies the problem type automatically
- Supports 6 operations: Permutations, Combinations, Permutations/Combinations with Replacement, Derangements, Circular Permutations
- Renders formulas with KaTeX
- Light / dark theme toggle
- Built with Flask + scikit-learn

## Setup

```bash
pip install -r requirements.txt
```

Train the model (only needed once):

```bash
python combinatorics_solver/load_data.py
```

Run the app:

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

## Tech Stack

- Python, Flask, scikit-learn (SVC), joblib
- HTML/CSS/JS, KaTeX for math rendering
