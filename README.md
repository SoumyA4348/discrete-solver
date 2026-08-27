# DiscreteSolver — Machine Learning Combinatorics Classifier & Solver

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Support%20Vector%20Classifier-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![KaTeX](https://img.shields.io/badge/KaTeX-LaTeX%20Rendering-005B94?style=flat-square)](https://katex.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

> Type a natural-language discrete math or combinatorics word problem, and instantly receive the classified operation, mathematical formula, step-by-step LaTeX rendering, and computed numerical solution.

---

## Overview

Combinatorics word problems can be ambiguous and difficult to categorize by hand (distinguishing between order-dependent permutations, combination groupings, derangements, and circular arrangements).

**DiscreteSolver** combines a trained **Support Vector Classifier (SVC)** machine learning model with a custom **Regular Expression NLP entity parser** to tokenize free-text math questions, extract numeric variables (n, r), route them to the appropriate combinatorics engine, and render clean LaTeX step-by-step solutions in real time.

---

## Features

- **Natural Language Parsing:** Accepts raw, unformatted English math word problems.
- **Support Vector Classifier (SVC):** Categorizes problem types using term frequency analysis and linear vector boundaries.
- **6 Combinatorial Operations Supported:**
  1. *Permutations without Replacement* (P(n, r) = n! / (n-r)!)
  2. *Combinations without Replacement* (C(n, r) = n! / (r!(n-r)!))
  3. *Permutations with Replacement* (n^r)
  4. *Combinations with Replacement* ((n+r-1)! / (r!(n-1)!))
  5. *Derangements (Subfactorials)* (!n)
  6. *Circular Permutations* ((n-1)!)
- **Custom NLP Entity Extractor:** Extracts parameter variables (n, r) and maps textual numbers (*"five", "three"*) to integers.
- **In-Browser LaTeX Rendering:** Utilizes KaTeX for mathematical notation and step-by-step formula breakdown.
- **Responsive Theme UI:** Clean, modern interface supporting light/dark modes.

---

## Pipeline Architecture

```
User Free-Text Input 
       |
[ Custom RegEx NLP Parser ] ---> Extracts variables (n, r) & keywords
       |
[ Scikit-Learn SVC Classifier ] ---> Identifies Mathematical Class (e.g., Combination)
       |
[ Math Engine (math_engine.py) ] ---> Computes exact numerical answer
       |
[ KaTeX Formula Generator ] ---> Renders dynamic LaTeX step-by-step solution
```

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend & Server** | Python, Flask, Jinja2 |
| **Machine Learning** | Scikit-learn (SVC), Joblib |
| **NLP & Extraction** | Custom RegEx Pattern Parser, Word-to-Number Entity Mapping |
| **Frontend & Math** | HTML5, CSS3, JavaScript, KaTeX (LaTeX Rendering Engine) |
| **Testing** | PyTest |

---

## Setup & Local Installation

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/SoumyA4348/discrete-solver.git
cd discrete-solver

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Train Model & Run Server
```bash
# Train the SVC model once on labeled problem datasets
python combinatorics_solver/load_data.py

# Launch the Flask application
python app.py
```
Navigate to [http://localhost:5000](http://localhost:5000) in your browser.

---

## Running Tests

Execute the automated test suite with `pytest`:
```bash
pytest tests/ -v
```

---

## Authors & Contributors

* **Soumya Patel** — *Machine Learning Model Training, Mathematical Engine & Full-Stack Implementation* — [@SoumyA4348](https://github.com/SoumyA4348)
* **Krish Shah** — *Co-Developer, Dataset Curation & Testing* — [@KSHAH01-can](https://github.com/KSHAH01-can)

*Developed collaboratively for academic discrete mathematics and algorithmic problem solving.*

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
