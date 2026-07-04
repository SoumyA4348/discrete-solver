# DiscreteSolver

**ML-powered combinatorics word problem solver** — type a plain-English math question, get the classified operation, formula, LaTeX rendering, and numerical answer.

> *"How many ways can 5 people be arranged in a row?"* → **Permutation → P(5,5) = 120**

---

## ✨ Features

- **Natural Language Input** — accepts plain-English combinatorics questions
- **ML Classification** — SVC model (scikit-learn) auto-classifies the problem type
- **6 Operations** — Permutations, Combinations, P/C with Replacement, Derangements, Circular Permutations
- **Custom NLP Parser** — regex-driven engine extracts mathematical variables from raw text
- **LaTeX Rendering** — KaTeX displays formulas in the browser
- **Dark/Light Theme** — clean UI with theme toggle

## 🧠 How It Works

```
User Input → NLP Parser (regex) → SVC Classifier → Math Engine → LaTeX Output
                                      ↑
                              Trained on labeled
                              combinatorics dataset
```

1. **NLP Parser** extracts key variables (n, r) from natural language using regex patterns and word mapping
2. **SVC Classifier** (scikit-learn) categorizes the operation type from the parsed text
3. **Math Engine** computes the answer using the classified formula
4. **Frontend** renders the result with KaTeX for clean mathematical notation

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| ML | scikit-learn (SVC), joblib |
| NLP | Custom regex parser |
| Frontend | HTML/CSS/JS, KaTeX |

## 🚀 Setup

```bash
pip install -r requirements.txt
python combinatorics_solver/load_data.py   # Train model (once)
python app.py                              # Run at localhost:5000
```

## 📁 Structure

```
DiscreteSolver/
├── app.py                  # Flask application
├── solver_service.py       # ML classification + math computation
├── math_engine.py          # Core combinatorics calculations
├── combinatorics_solver/   # Training data + model loader
├── templates/              # HTML templates
├── static/                 # CSS/JS assets
├── tests/                  # Test suite
└── requirements.txt
```

## 📜 License

MIT
