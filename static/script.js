// ── Example questions for the chips ──────────────────────────
const EXAMPLES = [
  "How many ways can 5 people stand in a line?",
  "How many ways can a committee of 3 be chosen from 10 people?",
  "How many 4-digit PINs are possible if digits can be repeated?",
  "How many ways can you distribute 15 identical candies among 5 children?",
  "How many 5-card hands can be dealt from a deck of 52 cards?",
  "How many 3-letter passwords can be made using 26 letters with repeats?",
];

// ── Populate chips on load ────────────────────────────────────
(function buildChips() {
  const row = document.getElementById("chips-row");
  EXAMPLES.forEach((q) => {
    const chip = document.createElement("button");
    chip.className = "chip";
    chip.textContent = q;
    chip.title = q;
    chip.onclick = () => {
      document.getElementById("question-input").value = q;
      document.getElementById("question-input").focus();
    };
    row.appendChild(chip);
  });
})();

// ── Handle "Enter" to submit (Shift+Enter for newline) ────────
document.getElementById("question-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSolve();
  }
});

// ── Count-up animation ─────────────────────────────────────────
function countUp(el, target, duration = 900) {
  const start = performance.now();
  const startVal = 0;

  function tick(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(startVal + (target - startVal) * eased);
    el.textContent = current.toLocaleString();
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// ── Main solve handler ────────────────────────────────────────
async function handleSolve() {
  const question = document.getElementById("question-input").value.trim();
  const btn = document.getElementById("solve-btn");
  const resultPanel = document.getElementById("result-panel");
  const errorBox = document.getElementById("error-box");

  // Clear previous state
  resultPanel.classList.remove("visible");
  resultPanel.style.display = "none";
  errorBox.classList.remove("visible");

  if (!question) {
    showError("Please enter a word problem before clicking Solve.");
    return;
  }

  // Loading state
  btn.classList.add("loading");

  try {
    const response = await fetch("/solve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      showError(data.error || "An unknown error occurred.");
      return;
    }

    // Populate result
    document.getElementById("result-badge").textContent = data.operation_label;
    document.getElementById("stat-n").textContent = data.n;
    document.getElementById("stat-r").textContent = data.r;
    document.getElementById("stat-formula").textContent = data.formula;

    // Show panel then animate number
    resultPanel.style.display = "block";
    void resultPanel.offsetWidth; // force reflow for transition
    resultPanel.classList.add("visible");

    // Use a wrapper span so gradient clip re-renders correctly on all browsers
    const answerEl = document.getElementById("answer-number");
    answerEl.innerHTML = '<span id="answer-inner">0</span>';
    const innerEl = document.getElementById("answer-inner");
    setTimeout(() => countUp(innerEl, data.answer), 150);

  } catch (err) {
    showError("Could not connect to the server. Is Flask running?");
  } finally {
    btn.classList.remove("loading");
  }
}

function showError(msg) {
  const box = document.getElementById("error-box");
  document.getElementById("error-text").textContent = msg;
  box.classList.add("visible");
}
