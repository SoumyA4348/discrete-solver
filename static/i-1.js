document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initHelpModal();
    initCounter();
    initToolButtons();
    initChips();
});

// ── Theme ──────────────────────────────────────────────────────
function initTheme() {
    const btn = document.getElementById('theme-toggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setTheme(prefersDark ? 'dark' : 'light');
    btn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        setTheme(current === 'dark' ? 'light' : 'dark');
    });
}
function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    const icon = document.querySelector('.theme-icon');
    if (icon) icon.textContent = t === 'dark' ? '☀️' : '🌙';
}

// ── Help modal ─────────────────────────────────────────────────
function initHelpModal() {
    const overlay = document.getElementById('help-modal');
    document.getElementById('help-toggle').addEventListener('click', () => overlay.classList.add('visible'));
    document.getElementById('close-help').addEventListener('click', () => overlay.classList.remove('visible'));
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.classList.remove('visible'); });
}

// ── Character counter + Enter to submit ───────────────────────
function initCounter() {
    const input = document.getElementById('question-input');
    const counter = document.getElementById('input-counter');
    input.addEventListener('input', () => {
        const n = input.value.length;
        counter.textContent = `${n} / 200`;
        counter.classList.toggle('limit', n >= 190);
    });
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSolve(); }
    });
}

// ── Tool buttons ───────────────────────────────────────────────
function initToolButtons() {
    const input = document.getElementById('question-input');
    const counter = document.getElementById('input-counter');

    document.getElementById('clear-btn').addEventListener('click', () => {
        input.value = '';
        counter.textContent = '0 / 200';
        counter.classList.remove('limit');
        input.focus();
    });

    document.getElementById('copy-btn').addEventListener('click', async () => {
        const el = document.getElementById('answer-inner');
        const text = el ? el.textContent : '';
        if (!text || text === '0') { showToast('No result yet!'); return; }
        try { await navigator.clipboard.writeText(text); showToast('Copied!'); }
        catch { showToast('Copy failed.'); }
    });

    const shareBtn = document.getElementById('share-btn');
    if (shareBtn) {
        shareBtn.addEventListener('click', () => {
            const el = document.getElementById('answer-inner');
            const result = el ? el.textContent : '--';
            if (navigator.share) {
                navigator.share({ title: 'Discrete Solver', text: `Result: ${result}`, url: location.href });
            } else { showToast('Sharing not supported here'); }
        });
    }

    document.getElementById('error-close').addEventListener('click', () => {
        document.getElementById('error-box').classList.remove('visible');
    });
}

// ── Example chips ──────────────────────────────────────────────
function initChips() {
    const examples = [
        'How many ways can 5 people stand in a line?',
        'In how many ways can a committee of 3 be chosen from 10 people?',
        'How many 4-digit PINs are possible if digits can repeat?',
        'How many ways can you distribute 15 identical candies among 5 children?',
        'How many 5-card hands can be dealt from a deck of 52 cards?',
        'If 5 people check their hats, how many ways can none of them get their own hat back?',
        'How many ways to seat 5 people around a circular table?',
    ];
    const row = document.getElementById('chips-row');
    const input = document.getElementById('question-input');
    const counter = document.getElementById('input-counter');
    examples.forEach(text => {
        const chip = document.createElement('button');
        chip.className = 'chip';
        chip.textContent = text;
        chip.title = text;
        chip.addEventListener('click', () => {
            input.value = text;
            counter.textContent = `${text.length} / 200`;
            input.focus();
        });
        row.appendChild(chip);
    });
}

// ── Count-up animation ─────────────────────────────────────────
function countUp(el, target, duration = 900) {
    const start = performance.now();
    (function tick(now) {
        const p = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased).toLocaleString();
        if (p < 1) requestAnimationFrame(tick);
    })(start);
}

// ── Main solve handler ─────────────────────────────────────────
async function handleSolve() {
    const question = document.getElementById('question-input').value.trim();
    const btn = document.getElementById('solve-btn');
    const resultPanel = document.getElementById('result-panel');
    const errorBox = document.getElementById('error-box');

    resultPanel.classList.remove('visible');
    resultPanel.style.display = 'none';
    errorBox.classList.remove('visible');
    document.getElementById('answer-expr').innerHTML = '';
    document.getElementById('answer-equals').style.display = 'none';

    if (!question) { showError('Please enter a word problem first.'); return; }

    btn.classList.add('loading');
    try {
        const res = await fetch('/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question }),
        });
        const data = await res.json();
        if (!res.ok || data.error) { showError(data.error || 'Unknown error.'); return; }

        document.getElementById('result-badge').textContent = data.operation_label;
        document.getElementById('stat-n').textContent = data.n;
        document.getElementById('stat-r').textContent = data.r;
        // Render LaTeX formula using KaTeX
        katex.render(data.formula, document.getElementById('stat-formula'), {
            throwOnError: false,
            displayMode: true
        });

        if (data.expression) {
            katex.render(data.expression, document.getElementById('answer-expr'), {
                throwOnError: false,
                displayMode: true
            });
            document.getElementById('answer-equals').style.display = 'inline-block';
        }

        resultPanel.style.display = 'block';
        void resultPanel.offsetWidth;
        resultPanel.classList.add('visible');

        const answerEl = document.getElementById('answer-number');
        answerEl.innerHTML = '<span id="answer-inner">0</span>';
        const inner = document.getElementById('answer-inner');
        setTimeout(() => countUp(inner, data.answer), 150);

    } catch (e) {
        showError('Cannot connect to server. Is Flask running?');
    } finally {
        btn.classList.remove('loading');
    }
}

function showError(msg) {
    document.getElementById('error-text').textContent = msg;
    document.getElementById('error-box').classList.add('visible');
}

function showToast(msg) {
    let t = document.getElementById('_toast');
    if (!t) {
        t = document.createElement('div');
        t.id = '_toast';
        Object.assign(t.style, {
            position:'fixed', bottom:'24px', left:'50%', transform:'translateX(-50%)',
            background:'#1e1b4b', color:'#c7d2fe', padding:'10px 20px',
            borderRadius:'8px', zIndex:'999', fontSize:'14px', boxShadow:'0 4px 20px rgba(0,0,0,0.4)'
        });
        document.body.appendChild(t);
    }
    t.textContent = msg;
    t.style.display = 'block';
    clearTimeout(t._tid);
    t._tid = setTimeout(() => { t.style.display = 'none'; }, 3000);
}