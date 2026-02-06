document.addEventListener('DOMContentLoaded', () => {
    console.log("🔥 NEW GAME.JS LOADED - v2.1 Streak & Hangman");
    const wordDisplay = document.getElementById('word-display');
    const input = document.getElementById('command-input');
    const log = document.getElementById('message-log');
    const breachList = document.getElementById('breach-stages');
    const restartBtn = document.getElementById('restart-btn');
    const hintBtn = document.getElementById('hint-btn');
    const themeToggle = document.getElementById('theme-toggle');

    let isGameOver = false;

    // Breach stages match Python logic
    const BREACH_STAGES = [
        "Secure",
        "Firewall Weakened",
        "Encryption Broken",
        "Credentials Exposed",
        "Unauthorized Access",
        "SYSTEM COMPROMISED"
    ];

    // --- THEME & STREAK MANAGEMENT ---
    let currentTheme = localStorage.getItem('theme') || 'minimal';
    let winStreak = parseInt(localStorage.getItem('secure_access_win_streak') || "0");
    const streakDisplay = document.getElementById('streak-display');

    // Initial Streak Render
    if (streakDisplay) streakDisplay.innerText = winStreak;

    function appliesTheme(theme) {
        if (theme === 'cyber') {
            document.body.classList.add('theme-cyber');
            themeToggle.innerHTML = "<span>🟢 Cyber</span>";
        } else {
            document.body.classList.remove('theme-cyber');
            themeToggle.innerHTML = "<span>⚪ Minimal</span>";
        }
    }

    // Apply immediately
    appliesTheme(currentTheme);

    themeToggle.addEventListener('click', () => {
        currentTheme = currentTheme === 'minimal' ? 'cyber' : 'minimal';
        localStorage.setItem('theme', currentTheme);
        appliesTheme(currentTheme);
    });

    // --- AMBIENT MOTION CONTROL ---
    const gridOverlay = document.querySelector('.cyber-grid-overlay');
    let motionTimeout;

    function pauseAmbientMotion() {
        if (currentTheme !== 'cyber') return;
        if (gridOverlay) {
            gridOverlay.classList.add('paused');

            clearTimeout(motionTimeout);
            motionTimeout = setTimeout(() => {
                gridOverlay.classList.remove('paused');
            }, 1200); // Resume after 1.2s idle
        }
    }

    // Attach pause triggers
    if (gridOverlay) {
        input.addEventListener('keydown', pauseAmbientMotion);
        hintBtn.addEventListener('click', pauseAmbientMotion);
        restartBtn.addEventListener('click', pauseAmbientMotion);
    }

    // --- LOGIC ---

    // --- TYPEWRITER LOGIC ---
    let activeTypewriters = [];

    function cancelAllTypewriters() {
        activeTypewriters.forEach(t => {
            clearInterval(t.interval);
            if (t.element) {
                t.element.innerText = `> ${t.fullText}`;
                t.element.classList.remove('typewriter-caret');
            }
        });
        activeTypewriters = [];
    }

    function logMessage(msg, type = 'sys-msg') {
        const p = document.createElement('p');
        p.className = type;
        log.appendChild(p);

        // Check for reduced motion
        const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        // Only animate system messages, and only if allowed
        if (type === 'sys-msg' && !prefersReduced) {
            p.classList.add('typewriter-caret'); // Add blinker
            p.innerText = '> ';

            let i = 0;
            const interval = setInterval(() => {
                p.innerText = `> ${msg.substring(0, i + 1)}`;
                i++;
                if (i >= msg.length) {
                    clearInterval(interval);
                    p.classList.remove('typewriter-caret'); // Remove blinker when done
                    // Remove from active list
                    activeTypewriters = activeTypewriters.filter(t => t.interval !== interval);
                }
                log.scrollTop = log.scrollHeight; // Keep scrolling
            }, 20); // 20ms per char

            activeTypewriters.push({ interval, element: p, fullText: msg });
        } else {
            // Instant render
            p.innerText = `> ${msg}`;
        }

        log.scrollTop = log.scrollHeight;
    }

    // Interrupt logic: Cancel animation on input
    input.addEventListener('input', cancelAllTypewriters);

    // Visual FX Helpers
    function triggerShake() {
        // Only main container shakes on error
        const container = document.querySelector('.terminal-container');
        container.classList.remove('anim-shake'); // reset
        void container.offsetWidth; // force reflow
        container.classList.add('anim-shake');
    }

    function triggerSuccess() {
        const container = document.querySelector('.terminal-container');
        container.classList.add('anim-success-sweep');
        setTimeout(() => container.classList.remove('anim-success-sweep'), 1000);
    }

    function triggerFailure() {
        document.body.classList.add('anim-fail');
    }

    function resetVisuals() {
        document.body.classList.remove('anim-fail');
    }

    async function startGame() {
        try {
            resetVisuals();
            const res = await fetch('/api/start', { method: 'POST' });
            const state = await res.json();

            log.innerHTML = '';
            updateUI(state);
            logMessage("SYSTEM INITIALIZED. READY.", "sys-msg");

            isGameOver = false;
            input.disabled = false;
            input.value = '';
            input.focus();
            restartBtn.style.display = 'none';
        } catch (e) {
            logMessage("CONNECTION ERROR: SERVER OFFLINE.", "err-msg");
        }
    }

    async function sendGuess(guess) {
        if (!guess) return;
        try {
            const res = await fetch('/api/guess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ guess })
            });
            const state = await res.json();

            // Determine result for animation *before* UI update
            // We check if masked word changed or if breach level increased
            updateUI(state, true);
        } catch (e) {
            logMessage("TRANSMISSION ERROR.", "err-msg");
        }
    }

    async function reqHint() {
        if (isGameOver) return;
        try {
            const res = await fetch('/api/hint', { method: 'POST' });
            const state = await res.json();
            updateUI(state);
        } catch (e) {
            logMessage("HINT RETRIEVAL FAILED.", "err-msg");
        }
    }

    let lastBreachLevel = 0;
    let lastMaskedWord = "";

    function updateUI(data, isGuess = false) {
        const state = data.status;

        // --- Letter Reveal Animation Logic ---
        // Compare new masked word with old to find revealed chars
        const newWord = state.masked_word; // "A _ _ L E"

        // Simple innerText update, but could be fancier with span-per-char for animation
        // For 'Minimal' theme, we just update text. 
        // Improvement: We can re-render to spans if we want per-letter pop-in.
        if (state.masked_word !== lastMaskedWord) {
            wordDisplay.innerHTML = state.masked_word
                .split(' ')
                .map(char => `<span class="${char !== '_' ? 'anim-pop' : ''}">${char}</span>`)
                .join(' ');
        }

        lastMaskedWord = state.masked_word;

        // --- Breach Feedback ---
        if (state.breach_level > lastBreachLevel) {
            triggerShake();
            logMessage(`ALERT: BREACH LEVEL ${state.breach_level}`, "err-msg");
        }
        lastBreachLevel = state.breach_level;

        // --- Breach List ---
        breachList.innerHTML = '';
        BREACH_STAGES.forEach((stage, idx) => {
            const li = document.createElement('li');
            li.innerText = stage;
            if (idx < state.breach_level) li.classList.add('passed');
            if (idx === state.breach_level) li.classList.add('active');
            breachList.appendChild(li);
        });

        // --- Minimal Hangman Update ---
        // Breach Levels: 0=Safe, 1-5=Danger
        const potatoParts = [
            'man-head',   // Lvl 1
            'man-body',   // Lvl 2
            'man-arm-l',  // Lvl 3
            'man-arm-r',  // Lvl 4
            ['man-leg-l', 'man-leg-r'] // Lvl 5 (Both legs)
        ];

        // Reset all first
        document.querySelectorAll('.hangman-part').forEach(el => el.style.opacity = '0');

        // Reveal based on level
        for (let i = 0; i < state.breach_level; i++) {
            if (i < potatoParts.length) {
                const partId = potatoParts[i];
                if (Array.isArray(partId)) {
                    partId.forEach(id => document.getElementById(id).style.opacity = '1');
                } else {
                    const el = document.getElementById(partId);
                    if (el) el.style.opacity = '1';
                }
            }
        }

        // --- Stats ---
        document.getElementById('hints-count').innerText = state.hints_used;
        document.getElementById('breach-level-display').innerText = state.breach_level;

        // --- Message ---
        if (state.message) {
            let type = 'sys-msg';
            if (state.won) type = 'win-msg';
            else if (state.game_over) type = 'err-msg';
            else if (state.message.includes("ERROR") || state.message.includes("REJECTED")) type = 'err-msg';

            // Filter redundant messages if handled by specific anims/logs
            if (!state.message.includes("BREACH LEVEL INCREASED")) {
                logMessage(state.message, type);
            }
        }

        // --- End Game ---
        if (state.game_over) {
            isGameOver = true;
            input.disabled = true;

            // STREAK LOGIC
            if (state.won) {
                winStreak++;
                triggerSuccess();
            } else {
                winStreak = 0;
                triggerFailure();
                if (data.target_word) {
                    logMessage(`TARGET WAS: ${data.target_word}`, 'err-msg');
                }
            }
            // Save & Update Streak
            localStorage.setItem('secure_access_win_streak', winStreak);
            if (streakDisplay) streakDisplay.innerText = winStreak;

            // Optional Polish: Delay end-state UI by 600ms
            setTimeout(() => {
                restartBtn.style.display = 'block';
            }, 600);
        }
    }

    // Event Listeners
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isGameOver) {
            const val = input.value.trim();
            if (val) {
                logMessage(`> ${val}`, 'user-msg');
                sendGuess(val);
                input.value = '';
            }
        }
    });

    hintBtn.addEventListener('click', reqHint);
    restartBtn.addEventListener('click', startGame);

    // Initial Start
    startGame();
});
