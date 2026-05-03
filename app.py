import sys
import os
import joblib
from flask import Flask, request, jsonify, render_template

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from solver_service import SolverService

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "combinatorics_solver", "combinatorics_model.joblib")
MAX_QUESTION_LENGTH = 300

solver_service = None

def load_model():
    global solver_service
    try:
        model = joblib.load(MODEL_PATH)
        solver_service = SolverService(model)
        print("[OK] ML model loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Could not load ML model: {e}")
        print("   Run combinatorics_solver/load_data.py first!")
        solver_service = SolverService(None)

load_model()

@app.route("/")
def index():
    return render_template("i-1.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    if len(question) > MAX_QUESTION_LENGTH:
        return jsonify({"error": f"Question too long (max {MAX_QUESTION_LENGTH} characters)."}), 400

    try:
        result = solver_service.solve_question(question)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
