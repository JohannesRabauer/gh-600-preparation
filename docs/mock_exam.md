# Mock Exams

## Overview

| Property | Value |
|----------|-------|
| **Real Exam Questions** | 60 |
| **Time Limit** | 120 minutes |
| **Passing Score** | 700/1000 |
| **Format** | Multiple choice, multiple select, scenario-based |
| **Domains** | 6 official domains |

!!! important "Exam Simulation"
    Take these under realistic conditions: set a 120-minute timer, no reference materials, no breaks. This simulates the actual exam experience.

!!! note "About Scoring"
    The real GH-600 exam requires a score of **700/1000** to pass (not a simple percentage). Mock Exams 4 & 5 use 60 questions matching the real exam format. Exams 1-3 have 50 questions each and are still excellent practice.

---

## Available Mock Exams

### Interactive Exams (Recommended)

| Exam | Questions | Focus | Domain Alignment |
|------|-----------|-------|-----------------|
| [**Mock Exam 1**](mock_exam_1.md) | 50 | Balanced across all domains | Original domains |
| [**Mock Exam 2**](mock_exam_2.md) | 50 | Implementation & Security emphasis | Original domains |
| [**Mock Exam 3**](mock_exam_3.md) | 50 | Advanced cross-domain scenarios | Original domains |
| [**Mock Exam 4**](mock_exam_4.md) | 60 | Full exam simulation — official domain weightings | ✅ Official GH-600 domains |
| [**Mock Exam 5**](mock_exam_5.md) | 60 | Advanced scenarios — official domain weightings | ✅ Official GH-600 domains |
| [**Mock Exam 6**](mock_exam_6.md) | 60 | 🔥 **Expert level** — hardest exam, 2026-current features | ✅ Official GH-600 domains |

!!! tip "Recommended Study Order"
    Start with Exams 1-3 for foundational practice, then use Exams 4-5 for realistic exam simulation with official domain alignment. Attempt Exam 6 only when you're consistently scoring 80%+ on Exams 4-5 — it's designed as the final confidence check before your real exam.

### How It Works

1. Start the exam — timer begins automatically
2. Select your answer for each question
3. For multiple-select: choose all correct options then submit
4. Navigate with Previous/Next buttons
5. Finish when all questions are answered
6. Review your score breakdown by domain
7. Study explanations for missed questions

---

## Official GH-600 Domain Distribution

The real exam uses these domain weightings (Mock Exams 4 & 5 follow these exactly):

| Domain | Weight | Questions (60-Q exam) |
|--------|--------|----------------------|
| 1. Prepare Agent Architecture & SDLC Processes | 15–20% | 10 |
| 2. Implement Tool Use & Environment Interaction | 20–25% | 14 |
| 3. Manage Memory, State, and Execution | 10–15% | 8 |
| 4. Perform Evaluation, Error Analysis, and Tuning | 15–20% | 10 |
| 5. Orchestrate Multi-Agent Coordination | 15–20% | 10 |
| 6. Implement Guardrails and Accountability | 10–15% | 8 |

---

## Key Topics by Domain

### Domain 1: Agent Architecture & SDLC
- Separating planning from execution
- Agent anti-patterns and mitigation
- Inputs, outputs, and success criteria
- Graduated autonomy levels
- Observability via standard dev tooling

### Domain 2: Tool Use & Environment
- MCP server configuration (local stdio + remote HTTP/SSE)
- MCP registries and allow lists
- GitHub remote MCP servers
- Branch-based and repo-scoped agents
- Error handling: retry → rollback → escalate
- Traceability and accountability for tool calls

### Domain 3: Memory, State & Execution
- Short-term vs. long-term vs. external memory
- Context drift detection and correction
- State persistence across sessions
- Memory scoping, pruning, and expiration
- Preventing stale/conflicting context

### Domain 4: Evaluation & Tuning
- Qualitative vs. quantitative evaluation signals
- Root cause categories: reasoning, tool misuse, context, environment
- Automated scanning tools for evaluation
- Tuning instructions, memory, and tools
- Aligning evaluation with development intent

### Domain 5: Multi-Agent Coordination
- Patterns: pipeline, fan-out/fan-in, orchestrator-worker, consensus
- Agent isolation for parallel execution
- Conflict detection (overlapping changes, duplicated effort, contradictions)
- Recovery: rollback and human-in-the-loop
- Agent lifecycle: add, update, retire

### Domain 6: Guardrails & Accountability
- Risk classification (operational, security, compliance)
- Autonomy level assignment
- Least-privilege permissions with temporal scoping
- Blocking policy-violating actions
- Prompt injection defense via system-level restrictions

---

## After the Exam

### If You Scored Well (≥ 80%)

- Review any questions you got wrong
- Identify if there's a pattern (specific domain weakness)
- Try another mock exam to confirm consistency
- Consider scheduling the real exam

### If You Scored Below Target (< 70%)

- Note which domains scored lowest
- Return to [Study Notes](study_notes.md) for those domains
- Review [Flashcards](revision.md#flashcards) for quick reinforcement
- Pay special attention to Domains 3 & 4 if those are weak — they're commonly underestimated
- Retake in 2-3 days after focused study

---

## Grading Rubric

| Score | Result | Recommendation |
|-------|--------|----------------|
| 90-100% | Strong Pass | Ready for the exam |
| 80-89% | Pass | Ready, minor review recommended |
| 70-79% | Borderline | Study weak domains before scheduling |
| 60-69% | Below Target | Need 3-5 more days of focused study |
| Below 60% | Needs Work | Follow a structured study plan focusing on gaps |
