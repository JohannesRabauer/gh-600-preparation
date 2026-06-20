/**
 * GH-600 Study Progress Tracker
 * Persists study progress in localStorage, renders animated progress rings,
 * tracks session time, and provides domain-level checkboxes.
 */
(function () {
  'use strict';

  const STORAGE_KEY = 'gh600_progress';
  const SESSION_KEY = 'gh600_session_start';

  // --- State ---
  function loadState() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { completed: {}, totalTime: 0 };
    } catch { return { completed: {}, totalTime: 0 }; }
  }

  function saveState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  // --- Session Timer ---
  function initSession() {
    if (!sessionStorage.getItem(SESSION_KEY)) {
      sessionStorage.setItem(SESSION_KEY, Date.now().toString());
    }
  }

  function getSessionMinutes() {
    const start = parseInt(sessionStorage.getItem(SESSION_KEY) || Date.now(), 10);
    return Math.round((Date.now() - start) / 60000);
  }

  // --- Progress Ring SVG ---
  function createRingSVG(percent) {
    const size = 120;
    const stroke = 8;
    const radius = (size - stroke) / 2;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference * (1 - percent / 100);

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', size);
    svg.setAttribute('height', size);
    svg.setAttribute('viewBox', `0 0 ${size} ${size}`);

    const bg = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    bg.setAttribute('cx', size / 2);
    bg.setAttribute('cy', size / 2);
    bg.setAttribute('r', radius);
    bg.setAttribute('fill', 'none');
    bg.setAttribute('stroke', 'var(--gh-glass-border, rgba(200,200,200,0.3))');
    bg.setAttribute('stroke-width', stroke);

    const fill = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    fill.setAttribute('cx', size / 2);
    fill.setAttribute('cy', size / 2);
    fill.setAttribute('r', radius);
    fill.setAttribute('fill', 'none');
    fill.setAttribute('stroke', 'var(--gh-primary, #6366f1)');
    fill.setAttribute('stroke-width', stroke);
    fill.setAttribute('stroke-linecap', 'round');
    fill.setAttribute('stroke-dasharray', circumference);
    fill.setAttribute('stroke-dashoffset', circumference);
    fill.style.transition = 'stroke-dashoffset 1s ease-out';
    fill.style.transform = 'rotate(-90deg)';
    fill.style.transformOrigin = '50% 50%';

    svg.appendChild(bg);
    svg.appendChild(fill);

    // Animate after paint
    requestAnimationFrame(() => {
      requestAnimationFrame(() => { fill.setAttribute('stroke-dashoffset', offset); });
    });

    return svg;
  }

  // --- Render ---
  function render() {
    const state = loadState();
    const checkboxes = document.querySelectorAll('.domain-checkbox');
    const totalItems = checkboxes.length || 1;
    let completedCount = 0;

    checkboxes.forEach(el => {
      const id = el.dataset.topic || el.textContent.trim();
      const input = el.querySelector('input[type="checkbox"]');
      const isCompleted = !!state.completed[id];
      if (isCompleted) completedCount++;

      if (input) input.checked = isCompleted;
      el.classList.toggle('completed', isCompleted);
    });

    const percent = Math.round((completedCount / totalItems) * 100);

    // Render progress rings
    document.querySelectorAll('.progress-ring').forEach(container => {
      container.innerHTML = '';
      const wrapper = document.createElement('div');
      wrapper.style.position = 'relative';
      wrapper.style.display = 'inline-flex';
      wrapper.style.alignItems = 'center';
      wrapper.style.justifyContent = 'center';

      const svg = createRingSVG(percent);
      wrapper.appendChild(svg);

      const label = document.createElement('span');
      label.textContent = percent + '%';
      label.style.position = 'absolute';
      label.style.fontSize = '1.4rem';
      label.style.fontWeight = '800';
      wrapper.appendChild(label);

      container.appendChild(wrapper);

      // Session time display
      const timeEl = document.createElement('div');
      timeEl.style.marginTop = '0.5rem';
      timeEl.style.fontSize = '0.8rem';
      timeEl.style.opacity = '0.7';
      timeEl.textContent = `Session: ${getSessionMinutes()} min`;
      container.appendChild(timeEl);
    });

    // Update any readiness displays
    document.querySelectorAll('[data-readiness]').forEach(el => {
      el.textContent = percent + '%';
    });
  }

  // --- Event Handlers ---
  function handleCheckboxClick(e) {
    const el = e.currentTarget;
    const id = el.dataset.topic || el.textContent.trim();
    const state = loadState();
    if (state.completed[id]) {
      delete state.completed[id];
    } else {
      state.completed[id] = Date.now();
    }
    saveState(state);
    render();
  }

  function handleReset() {
    if (confirm('Reset all study progress? This cannot be undone.')) {
      localStorage.removeItem(STORAGE_KEY);
      sessionStorage.removeItem(SESSION_KEY);
      initSession();
      render();
    }
  }

  // --- Init ---
  function init() {
    initSession();

    document.querySelectorAll('.domain-checkbox').forEach(el => {
      el.addEventListener('click', handleCheckboxClick);
      // Prevent double-toggle from native checkbox
      const input = el.querySelector('input[type="checkbox"]');
      if (input) input.addEventListener('click', e => e.stopPropagation());
    });

    document.querySelectorAll('[data-progress-reset]').forEach(btn => {
      btn.addEventListener('click', handleReset);
    });

    render();

    // Refresh session time display every minute
    setInterval(() => {
      document.querySelectorAll('.progress-ring div[style*="opacity"]').forEach(el => {
        el.textContent = `Session: ${getSessionMinutes()} min`;
      });
    }, 60000);

    // Persist time on unload
    window.addEventListener('beforeunload', () => {
      const state = loadState();
      state.totalTime = (state.totalTime || 0) + getSessionMinutes();
      saveState(state);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
