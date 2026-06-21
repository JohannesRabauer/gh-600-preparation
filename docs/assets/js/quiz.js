/**
 * Interactive Quiz Engine for MkDocs Material
 * Self-contained quiz system that parses quiz HTML, manages state, and renders results.
 */
(function () {
  "use strict";

  /* ==========================================================================
     Constants
     ========================================================================== */
  const STORAGE_KEY = "quiz_state_" + window.location.pathname;
  const PASS_THRESHOLD = 0.7;

  /* ==========================================================================
     State
     ========================================================================== */
  let state = {
    questions: [],
    currentIndex: 0,
    answers: {}, // { questionIndex: { selected: [...], correct: bool } }
    startTime: null,
    endTime: null,
    retryMode: false,
    retryIndices: [],
  };

  let containerEl = null;

  /* ==========================================================================
     Initialization
     ========================================================================== */
  function init() {
    const quizDivs = document.querySelectorAll(".quiz");
    if (!quizDivs.length) return;

    // Parse questions from HTML
    const questions = parseQuestions(quizDivs);
    if (!questions.length) return;

    // Build container
    containerEl = document.createElement("div");
    containerEl.className = "quiz-container";
    containerEl.setAttribute("role", "region");
    containerEl.setAttribute("aria-label", "Interactive Quiz");

    // Insert container before the first quiz div
    quizDivs[0].parentNode.insertBefore(containerEl, quizDivs[0]);

    // Try to restore state from localStorage
    const saved = loadState();
    if (saved && saved.questionCount === questions.length) {
      state = saved;
      // Re-attach parsed question data (HTML refs not serializable)
      state.questions = questions;
    } else {
      state.questions = questions;
      state.currentIndex = 0;
      state.answers = {};
      state.startTime = Date.now();
      state.endTime = null;
      state.retryMode = false;
      state.retryIndices = [];
    }

    render();
  }

  /* ==========================================================================
     Parsing
     ========================================================================== */
  function parseQuestions(quizDivs) {
    const questions = [];

    quizDivs.forEach(function (quizEl) {
      const domain = quizEl.getAttribute("data-domain") || "General";
      const type = quizEl.getAttribute("data-type") || "single";

      const questionEls = quizEl.querySelectorAll(".quiz-question");
      questionEls.forEach(function (qEl) {
        const stemEl = qEl.querySelector(".quiz-stem");
        const scenarioEl = qEl.querySelector(".quiz-scenario");
        const optionEls = qEl.querySelectorAll(".quiz-option");
        const explanationEl = qEl.querySelector(".quiz-explanation");

        const options = [];
        optionEls.forEach(function (optEl) {
          options.push({
            text: optEl.textContent.trim(),
            correct: optEl.getAttribute("data-correct") === "true",
          });
        });

        questions.push({
          domain: domain,
          type: type,
          stem: stemEl ? stemEl.innerHTML.trim() : "",
          scenario: scenarioEl ? scenarioEl.innerHTML.trim() : null,
          options: options,
          explanation: explanationEl ? explanationEl.innerHTML.trim() : "",
        });
      });
    });

    return questions;
  }

  /* ==========================================================================
     Rendering
     ========================================================================== */
  function render() {
    if (state.endTime) {
      renderResults();
    } else {
      renderQuestion();
    }
    saveState();
  }

  function renderQuestion() {
    const indices = state.retryMode ? state.retryIndices : state.questions.map(function (_, i) { return i; });
    const totalQuestions = indices.length;
    const displayIndex = state.currentIndex + 1;

    const actualIndex = indices[state.currentIndex];
    const q = state.questions[actualIndex];
    if (!q) return;

    const answered = state.answers[actualIndex] !== undefined;
    const elapsed = formatTime(Date.now() - state.startTime);
    const isMulti = q.type === "multiple-select";

    let html = "";

    // Header
    html += '<div class="quiz-header">';
    html += '<span class="quiz-progress-info">Question ' + displayIndex + " of " + totalQuestions + "</span>";
    html += '<span class="quiz-timer" aria-label="Time elapsed">\u23F1 ' + elapsed + "</span>";
    html += "</div>";

    // Progress bar
    const progress = (displayIndex / totalQuestions) * 100;
    html += '<div class="quiz-progress-bar" role="progressbar" aria-valuenow="' + displayIndex + '" aria-valuemin="1" aria-valuemax="' + totalQuestions + '">';
    html += '<div class="quiz-progress-fill" style="width:' + progress + '%"></div>';
    html += "</div>";

    // Card
    html += '<div class="quiz-card">';
    html += '<span class="quiz-domain-badge">' + escapeHtml(q.domain) + "</span>";

    if (q.scenario) {
      html += '<div class="quiz-scenario">' + q.scenario + "</div>";
    }

    html += '<div class="quiz-stem-text">' + q.stem + "</div>";

    // Options
    html += '<div class="quiz-options-list" role="' + (isMulti ? "group" : "radiogroup") + '" aria-label="Answer options">';

    q.options.forEach(function (opt, i) {
      let classes = "quiz-option-btn";
      const answer = state.answers[actualIndex];
      const selected = answer && answer.selected.indexOf(i) !== -1;
      const disabled = answered;

      if (answered) {
        classes += " quiz-option--disabled";
        if (opt.correct && selected) {
          classes += " quiz-option--correct";
        } else if (!opt.correct && selected) {
          classes += " quiz-option--incorrect";
        } else if (opt.correct && !selected) {
          classes += " quiz-option--missed";
        }
      } else if (isMulti && state._tempSelection && state._tempSelection.indexOf(i) !== -1) {
        classes += " quiz-option--selected";
      }

      const multiAttr = isMulti ? ' data-multi="true"' : "";
      const ariaChecked = selected ? ' aria-checked="true"' : ' aria-checked="false"';
      const role = isMulti ? "checkbox" : "radio";

      html += '<button class="' + classes + '"' + multiAttr + ' role="' + role + '"' + ariaChecked;
      html += ' data-index="' + i + '" tabindex="0"';
      if (disabled) html += " disabled";
      html += ">";
      html += '<span class="quiz-option-indicator">' + String.fromCharCode(65 + i) + "</span>";
      html += '<span class="quiz-option-text">' + escapeHtml(opt.text) + "</span>";
      html += "</button>";
    });

    html += "</div>"; // options-list

    // Submit button for multi-select
    if (isMulti && !answered) {
      const hasSelection = state._tempSelection && state._tempSelection.length > 0;
      html += '<button class="quiz-submit-btn"' + (hasSelection ? "" : " disabled") + ">Submit Answer</button>";
    }

    // Explanation
    if (answered) {
      html += '<div class="quiz-explanation-panel quiz-explanation--visible">';
      html += '<div class="quiz-explanation-label">Explanation</div>';
      html += '<div class="quiz-explanation-text">' + q.explanation + "</div>";
      html += "</div>";
    }

    html += "</div>"; // card

    // Navigation
    html += '<div class="quiz-nav">';
    html += '<button class="quiz-nav-btn quiz-nav-btn--prev"' + (state.currentIndex === 0 ? " disabled" : "") + ">";
    html += "\u2190 Previous</button>";

    const isLast = state.currentIndex === totalQuestions - 1;
    const allAnswered = indices.every(function (idx) { return state.answers[idx] !== undefined; });

    if (isLast && allAnswered) {
      html += '<button class="quiz-nav-btn quiz-nav-btn--finish">Finish Quiz \u2192</button>';
    } else {
      html += '<button class="quiz-nav-btn quiz-nav-btn--next"' + (state.currentIndex >= totalQuestions - 1 ? " disabled" : "") + ">";
      html += "Next \u2192</button>";
    }

    html += "</div>"; // nav

    containerEl.innerHTML = html;
    bindQuestionEvents(actualIndex, isMulti);
  }

  function bindQuestionEvents(actualIndex, isMulti) {
    const answered = state.answers[actualIndex] !== undefined;

    // Option clicks
    if (!answered) {
      const optBtns = containerEl.querySelectorAll(".quiz-option-btn");
      optBtns.forEach(function (btn) {
        btn.addEventListener("click", function () {
          const idx = parseInt(btn.getAttribute("data-index"), 10);
          if (isMulti) {
            handleMultiSelect(idx);
          } else {
            handleSingleSelect(actualIndex, idx);
          }
        });

        // Keyboard support
        btn.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            btn.click();
          }
        });
      });

      // Submit button for multi-select
      if (isMulti) {
        const submitBtn = containerEl.querySelector(".quiz-submit-btn");
        if (submitBtn) {
          submitBtn.addEventListener("click", function () {
            handleMultiSubmit(actualIndex);
          });
        }
      }
    }

    // Navigation
    const prevBtn = containerEl.querySelector(".quiz-nav-btn--prev");
    var nextBtn = containerEl.querySelector(".quiz-nav-btn--next");
    var finishBtn = containerEl.querySelector(".quiz-nav-btn--finish");

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        if (state.currentIndex > 0) {
          state.currentIndex--;
          state._tempSelection = null;
          render();
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        const indices = state.retryMode ? state.retryIndices : state.questions.map(function (_, i) { return i; });
        if (state.currentIndex < indices.length - 1) {
          state.currentIndex++;
          state._tempSelection = null;
          render();
        }
      });
    }

    if (finishBtn) {
      finishBtn.addEventListener("click", function () {
        state.endTime = Date.now();
        render();
      });
    }
  }

  function handleSingleSelect(questionIndex, optionIndex) {
    const q = state.questions[questionIndex];
    const correct = q.options[optionIndex].correct;

    state.answers[questionIndex] = {
      selected: [optionIndex],
      correct: correct,
    };

    render();
  }

  function handleMultiSelect(optionIndex) {
    if (!state._tempSelection) {
      state._tempSelection = [];
    }

    var idx = state._tempSelection.indexOf(optionIndex);
    if (idx !== -1) {
      state._tempSelection.splice(idx, 1);
    } else {
      state._tempSelection.push(optionIndex);
    }

    render();
  }

  function handleMultiSubmit(questionIndex) {
    const q = state.questions[questionIndex];
    const selected = state._tempSelection || [];

    // Check correctness: all correct must be selected, no incorrect selected
    const correctIndices = [];
    q.options.forEach(function (opt, i) {
      if (opt.correct) correctIndices.push(i);
    });

    const isCorrect =
      correctIndices.length === selected.length &&
      correctIndices.every(function (ci) { return selected.indexOf(ci) !== -1; });

    state.answers[questionIndex] = {
      selected: selected.slice(),
      correct: isCorrect,
    };

    state._tempSelection = null;
    render();
  }

  /* ==========================================================================
     Results
     ========================================================================== */
  function renderResults() {
    const indices = state.retryMode ? state.retryIndices : state.questions.map(function (_, i) { return i; });
    const totalQuestions = indices.length;
    let correctCount = 0;

    // Calculate per-domain scores
    const domainScores = {};

    indices.forEach(function (idx) {
      const q = state.questions[idx];
      const answer = state.answers[idx];
      if (!domainScores[q.domain]) {
        domainScores[q.domain] = { correct: 0, total: 0 };
      }
      domainScores[q.domain].total++;
      if (answer && answer.correct) {
        domainScores[q.domain].correct++;
        correctCount++;
      }
    });

    const percentage = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0;
    const passed = percentage >= PASS_THRESHOLD * 100;
    const elapsed = formatTime(state.endTime - state.startTime);

    // SVG circle calculations
    const radius = 65;
    const circumference = 2 * Math.PI * radius;
    const dashOffset = circumference - (percentage / 100) * circumference;

    let html = '<div class="quiz-results">';

    // Header with score circle
    html += '<div class="quiz-results-header">';
    html += '<div class="quiz-score-circle">';
    html += '<svg viewBox="0 0 160 160">';
    html += '<circle class="quiz-score-circle-bg" cx="80" cy="80" r="' + radius + '"/>';
    html += '<circle class="quiz-score-circle-fill ' + (passed ? "quiz-score-circle-fill--pass" : "quiz-score-circle-fill--fail") + '"';
    html += ' cx="80" cy="80" r="' + radius + '"';
    html += ' stroke-dasharray="' + circumference + '"';
    html += ' stroke-dashoffset="' + dashOffset + '"/>';
    html += "</svg>";
    html += '<div class="quiz-score-label">';
    html += '<div class="quiz-score-percent">' + percentage + "%</div>";
    html += '<div class="quiz-score-fraction">' + correctCount + "/" + totalQuestions + "</div>";
    html += "</div></div>";

    // Pass/Fail badge
    html += '<div class="quiz-pass-badge ' + (passed ? "quiz-pass-badge--pass" : "quiz-pass-badge--fail") + '">';
    html += passed ? "\u2705 PASS" : "\u274C BELOW PASSING";
    html += "</div>";

    html += '<div class="quiz-results-time">\u23F1 Time: ' + elapsed + "</div>";
    html += "</div>"; // results-header

    // Domain breakdown
    html += '<div class="quiz-domain-results">';
    html += "<h3>Score by Domain</h3>";

    const weakDomains = [];
    const domainNames = Object.keys(domainScores).sort();

    domainNames.forEach(function (domain) {
      const ds = domainScores[domain];
      const pct = Math.round((ds.correct / ds.total) * 100);
      const domainPass = pct >= PASS_THRESHOLD * 100;

      if (!domainPass) {
        weakDomains.push({ name: domain, score: pct });
      }

      html += '<div class="quiz-domain-row">';
      html += '<span class="quiz-domain-name" title="' + escapeHtml(domain) + '">' + escapeHtml(domain) + "</span>";
      html += '<div class="quiz-domain-bar-wrapper">';
      html += '<div class="quiz-domain-bar-fill ' + (domainPass ? "quiz-domain-bar-fill--pass" : "quiz-domain-bar-fill--fail") + '" style="width:' + pct + '%"></div>';
      html += "</div>";
      html += '<span class="quiz-domain-score">' + pct + "% (" + ds.correct + "/" + ds.total + ")</span>";
      html += "</div>";
    });

    html += "</div>"; // domain-results

    // Weak domains section
    if (weakDomains.length > 0) {
      html += '<div class="quiz-weak-domains">';
      html += "<h4>Areas to Improve</h4>";
      html += "<ul>";
      weakDomains.forEach(function (wd) {
        html += "<li>" + escapeHtml(wd.name) + " (" + wd.score + "%) \u2014 Study more in this area</li>";
      });
      html += "</ul></div>";
    }

    // Missed question indices for retry
    const missedIndices = [];
    indices.forEach(function (idx) {
      const answer = state.answers[idx];
      if (!answer || !answer.correct) {
        missedIndices.push(idx);
      }
    });

    // Action buttons
    html += '<div class="quiz-results-actions">';
    if (missedIndices.length > 0) {
      html += '<button class="quiz-results-btn quiz-results-btn--retry">Retry Missed Questions (' + missedIndices.length + ")</button>";
    }
    html += '<button class="quiz-results-btn quiz-results-btn--reset">Restart Full Quiz</button>';
    html += "</div>";

    html += "</div>"; // quiz-results

    containerEl.innerHTML = html;

    // Bind result actions
    var retryBtn = containerEl.querySelector(".quiz-results-btn--retry");
    var resetBtn = containerEl.querySelector(".quiz-results-btn--reset");

    if (retryBtn) {
      retryBtn.addEventListener("click", function () {
        state.retryMode = true;
        state.retryIndices = missedIndices.slice();
        state.currentIndex = 0;
        state.endTime = null;
        state.startTime = Date.now();
        // Clear answers for retry questions only
        missedIndices.forEach(function (idx) {
          delete state.answers[idx];
        });
        render();
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        state.retryMode = false;
        state.retryIndices = [];
        state.currentIndex = 0;
        state.answers = {};
        state.endTime = null;
        state.startTime = Date.now();
        try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
        render();
      });
    }
  }

  /* ==========================================================================
     State Persistence (sessionStorage)
     ========================================================================== */
  function saveState() {
    try {
      const toSave = {
        currentIndex: state.currentIndex,
        answers: state.answers,
        startTime: state.startTime,
        endTime: state.endTime,
        retryMode: state.retryMode,
        retryIndices: state.retryIndices,
        questionCount: state.questions.length,
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
    } catch (e) {
      // sessionStorage may be unavailable
    }
  }

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const saved = JSON.parse(raw);
      return {
        questions: [],
        questionCount: saved.questionCount || 0,
        currentIndex: saved.currentIndex || 0,
        answers: saved.answers || {},
        startTime: saved.startTime || Date.now(),
        endTime: saved.endTime || null,
        retryMode: saved.retryMode || false,
        retryIndices: saved.retryIndices || [],
      };
    } catch (e) {
      return null;
    }
  }

  /* ==========================================================================
     Utilities
     ========================================================================== */
  function escapeHtml(str) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  function formatTime(ms) {
    var totalSeconds = Math.floor(ms / 1000);
    var hours = Math.floor(totalSeconds / 3600);
    var minutes = Math.floor((totalSeconds % 3600) / 60);
    var seconds = totalSeconds % 60;

    if (hours > 0) {
      return hours + "h " + pad(minutes) + "m " + pad(seconds) + "s";
    }
    return minutes + "m " + pad(seconds) + "s";
  }

  function pad(n) {
    return n < 10 ? "0" + n : "" + n;
  }

  /* ==========================================================================
     Timer Update (updates elapsed time display every second)
     ========================================================================== */
  var timerInterval = null;

  function startTimer() {
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(function () {
      if (state.endTime) {
        clearInterval(timerInterval);
        return;
      }
      var timerEl = containerEl && containerEl.querySelector(".quiz-timer");
      if (timerEl) {
        timerEl.textContent = "\u23F1 " + formatTime(Date.now() - state.startTime);
      }
    }, 1000);
  }

  /* ==========================================================================
     Boot
     ========================================================================== */
  function boot() {
    init();
    if (containerEl) startTimer();
  }

  // Run on DOMContentLoaded or immediately if already loaded
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
