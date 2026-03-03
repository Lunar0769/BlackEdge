/* ─── BlackEdge — Dynamic Frontend ──────────────────────── */

let currentStream = null;

/* ── Preset query helper ──────────────────────────────────── */
function setQuery(text) {
    document.getElementById('queryInput').value = text;
}

/* ── Tab switching ────────────────────────────────────────── */
function switchTab(btn, tabId) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + tabId).classList.add('active');
}

/* ── Main analysis runner ─────────────────────────────────── */
async function runAnalysis() {
    const query = document.getElementById('queryInput').value.trim();
    if (!query) { shakeInput(); return; }

    // Cancel any in-flight stream
    if (currentStream) { currentStream.abort(); }

    resetUI();
    setStatus('active');
    setRunBtn(true);

    // Show result panel
    document.getElementById('resultPlaceholder').style.display = 'none';
    document.getElementById('resultSections').style.display = 'block';

    // Clear text areas
    ['researchContent', 'analysisContent', 'decisionContent', 'criticContent'].forEach(id => {
        document.getElementById(id).innerHTML = '';
        document.getElementById(id).classList.remove('cursor');
    });

    const controller = new AbortController();
    currentStream = controller;

    try {
        const resp = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query }),
            signal: controller.signal,
        });

        if (!resp.ok) throw new Error(`Server error ${resp.status}`);

        const reader = resp.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop(); // keep incomplete line

            let event = null;
            for (const line of lines) {
                if (line.startsWith('event: ')) {
                    event = line.slice(7).trim();
                } else if (line.startsWith('data: ') && event) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        handleEvent(event, data);
                    } catch (_) { }
                    event = null;
                }
            }
        }

        setStatus('done');
    } catch (err) {
        if (err.name !== 'AbortError') {
            console.error(err);
            setStatus('error');
            showError(err.message);
        }
    } finally {
        setRunBtn(false);
        currentStream = null;
    }
}

/* ── Event handler ────────────────────────────────────────── */
function handleEvent(event, data) {
    if (event === 'step') {
        const { step, status, label, content } = data;
        updateStep(step, status, label, content);

        // Live-type into the active panel
        if (status === 'done' && content) {
            const targets = {
                researcher: 'researchContent',
                analyst: 'analysisContent',
                trader: 'decisionContent',
                critic: 'criticContent'
            };
            if (targets[step]) {
                const el = document.getElementById(targets[step]);
                el.classList.remove('cursor');

                let textToType = content;
                if (step === 'critic') {
                    try {
                        const parsed = JSON.parse(content);
                        textToType = `## Critic Score: ${parsed.score}/10\n\n**Summary:**\n${parsed.summary}\n\n`;
                        if (parsed.weaknesses && parsed.weaknesses.length) {
                            textToType += "**Weaknesses:**\n" + parsed.weaknesses.map(w => `- ${w}`).join('\n') + "\n";
                        }
                        if (parsed.missing_factors && parsed.missing_factors.length) {
                            textToType += "**Missing factors:**\n" + parsed.missing_factors.map(w => `- ${w}`).join('\n');
                        }
                    } catch (e) { }
                }

                typeText(el, textToType);
                // Auto-switch tab to match current step
                const tabMap = { researcher: 'research', analyst: 'analysis', trader: 'decision', critic: 'critic' };
                const tabBtn = document.querySelector(`.tab[data-tab="${tabMap[step]}"]`);
                if (tabBtn) switchTab(tabBtn, tabMap[step]);
            }
        }
    } else if (event === 'result') {
        // Final result received - no score card to render
    } else if (event === 'error') {
        showError(data.message);
        setStatus('error');
    }
}

/* ── Pipeline step updater ────────────────────────────────── */
function updateStep(step, status, label, content) {
    const el = document.getElementById(`step-${step}`);
    const statusEl = document.getElementById(`status-${step}`);
    if (!el || !statusEl) return;

    el.classList.remove('loading', 'done');

    if (status === 'loading') {
        el.classList.add('loading');
        statusEl.innerHTML = '<span class="dot-spin"></span>';
    } else if (status === 'done') {
        el.classList.add('done');
        statusEl.innerHTML = '<span class="dot-done">✅</span>';
    } else if (status === 'error') {
        statusEl.innerHTML = '<span class="dot-error">❌</span>';
    }
}

/* ── Animated typewriter text ─────────────────────────────── */
function typeText(el, text, speed = 4) {
    el.innerHTML = '';
    el.classList.add('cursor');
    let index = 0;

    function tick() {
        if (index < text.length) {
            // Batch chars for speed
            const chunk = Math.min(speed, text.length - index);
            const currentString = text.slice(0, index + chunk);
            el.innerHTML = typeof marked !== 'undefined' ? marked.parse(currentString) : currentString;
            index += chunk;
            el.scrollTop = el.scrollHeight;
            requestAnimationFrame(tick);
        } else {
            el.classList.remove('cursor');
            el.innerHTML = typeof marked !== 'undefined' ? marked.parse(text) : text;
        }
    }
    requestAnimationFrame(tick);
}

/* ── Score gauge renderer ─────────────────────────────────── */
function renderFinalScore(evaluation) {
    if (!evaluation) return;

    const scoreCard = document.getElementById('scoreCard');
    scoreCard.style.display = 'block';
    scoreCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    const score = evaluation.score || 0;
    const fill = document.getElementById('gaugeFill');
    const numEl = document.getElementById('scoreNumber');
    const summaryEl = document.getElementById('scoreSummary');
    const weakEl = document.getElementById('weaknessList');

    // Animate gauge (arc total ~173px)
    const offset = 173 - (173 * score / 10);
    fill.style.strokeDashoffset = offset;

    // Color-code score number
    numEl.style.color = score >= 7 ? '#10b981' : score >= 5 ? '#f59e0b' : '#ef4444';
    numEl.textContent = score;

    summaryEl.textContent = evaluation.summary || '';

    // Weaknesses
    weakEl.innerHTML = '';
    const items = [...(evaluation.weaknesses || []), ...(evaluation.missing_factors || [])];
    if (items.length) {
        items.slice(0, 4).forEach(w => {
            const div = document.createElement('div');
            div.className = 'weakness-item';
            div.textContent = w;
            weakEl.appendChild(div);
        });
    }
}

/* ── Memory panel ─────────────────────────────────────────── */
function toggleMemory() {
    const panel = document.getElementById('memoryPanel');
    const overlay = document.getElementById('memoryOverlay');
    const isOpen = panel.classList.contains('open');

    if (isOpen) {
        panel.classList.remove('open');
        overlay.classList.remove('open');
    } else {
        panel.classList.add('open');
        overlay.classList.add('open');
        loadMemory();
    }
}

async function loadMemory() {
    const weakEl = document.getElementById('commonWeaknesses');
    const failEl = document.getElementById('recentFailures');
    const countEl = document.getElementById('failCount');

    weakEl.innerHTML = '<li class="loading-text">Loading…</li>';
    failEl.innerHTML = '<div class="loading-text">Loading…</div>';

    try {
        const r = await fetch('/api/memory');
        const data = await r.json();

        const weaknesses = data.common_weaknesses || [];
        weakEl.innerHTML = weaknesses.length
            ? weaknesses.map(w => `<li>${w}</li>`).join('')
            : '<li class="loading-text">No weaknesses logged yet.</li>';

        const failures = data.recent_mistakes || [];
        countEl.textContent = failures.length;
        failEl.innerHTML = failures.length
            ? failures.reverse().map(f => `
        <div class="failure-item">
          <div class="failure-query">${escHtml((f.query || '').slice(0, 100))}…</div>
          <div class="failure-summary">${escHtml(f.summary || '')}</div>
          <div class="failure-score">Score: ${f.score}/10</div>
        </div>`).join('')
            : '<div class="loading-text">No failures logged yet. 🎉</div>';
    } catch {
        weakEl.innerHTML = '<li class="loading-text">Error loading memory.</li>';
    }
}

async function clearMemory() {
    if (!confirm('Clear all failure memory? This cannot be undone.')) return;
    await fetch('/api/clear_memory', { method: 'POST' });
    loadMemory();
}

/* ── UI helpers ───────────────────────────────────────────── */
function setStatus(state) {
    const dot = document.getElementById('statusDot');
    dot.className = 'status-dot';
    dot.classList.add(state);
    dot.title = state.charAt(0).toUpperCase() + state.slice(1);
}

function setRunBtn(disabled) {
    const btn = document.getElementById('runBtn');
    btn.disabled = disabled;
    btn.querySelector('.btn-text').textContent = disabled ? 'Analysing…' : 'Analyse';
    btn.querySelector('.btn-icon').textContent = disabled ? '⏳' : '⚡';
}

function resetUI() {
    // Reset all pipeline steps
    ['rag', 'researcher', 'analyst', 'trader', 'critic'].forEach(step => {
        const el = document.getElementById(`step-${step}`);
        const statusEl = document.getElementById(`status-${step}`);
        if (el) el.classList.remove('loading', 'done');
        if (statusEl) statusEl.innerHTML = '<span class="dot-idle"></span>';
    });

    // Clear tabs
    ['researchContent', 'analysisContent', 'decisionContent', 'criticContent'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.innerHTML = '';
            el.classList.remove('cursor');
        }
    });
}

function showError(msg) {
    const el = document.getElementById('researchContent');
    el.textContent = '❌ Error: ' + msg;
    switchTab(document.querySelector('.tab[data-tab="research"]'), 'research');
}

function shakeInput() {
    const el = document.getElementById('queryInput');
    el.style.animation = 'none';
    el.offsetHeight; // reflow
    el.style.animation = 'shake 0.4s ease';
    setTimeout(() => el.style.animation = '', 500);
}

function escHtml(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
}

/* ── Keyboard shortcut: Ctrl+Enter ───────────────────────── */
document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') runAnalysis();
});

/* Add shake keyframe programmatically */
const style = document.createElement('style');
style.textContent = `@keyframes shake {
  0%,100% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}`;
document.head.appendChild(style);
