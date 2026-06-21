# Quick Reference

## Flashcards

!!! info "How to Use"
    Click any card to flip it and reveal the answer. Use these for spaced repetition practice.

<div class="study-grid">

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🔌 What are the four MCP components?</div>
<div class="flashcard-back"><strong>Host</strong> (app running the model), <strong>Client</strong> (connection manager), <strong>Server</strong> (exposes tools/resources/prompts), <strong>Transport</strong> (stdio or HTTP/SSE)</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🌐 What transport protocols does MCP use?</div>
<div class="flashcard-back">JSON-RPC 2.0 over <strong>stdio</strong> (local processes) or <strong>HTTP with Server-Sent Events (SSE)</strong> (remote servers)</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🤖 What distinguishes Agent Mode from Chat mode?</div>
<div class="flashcard-back">Agent Mode is <strong>autonomous and multi-step</strong>: creates/edits files, runs terminal commands, iterates on failures, uses entire workspace. Chat gives a single response without tool use.</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🔄 What is the plan-execute-iterate loop?</div>
<div class="flashcard-back">(1) <strong>Plan</strong> steps from user request, (2) <strong>Execute</strong> each step using tools, (3) <strong>Iterate</strong> — adjust plan based on results/errors until complete</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🔒 Name the 5 access control levels (top → bottom)</div>
<div class="flashcard-back"><strong>O</strong>rganization → <strong>R</strong>epository → <strong>U</strong>ser → <strong>S</strong>ession → <strong>T</strong>ool (ORUST)</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🛡️ What is least privilege for agents?</div>
<div class="flashcard-back">Agents should only access the resources and permissions they need for their <strong>current task</strong> — no more. Deny by default.</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🔑 How should secrets be handled in agent workflows?</div>
<div class="flashcard-back">Reference by <strong>name</strong> (env vars), never by value. Use vault services (GitHub Secrets, Azure Key Vault). Enable secret scanning. Never hardcode.</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">⚖️ What are Microsoft's 6 Responsible AI principles?</div>
<div class="flashcard-back"><strong>T</strong>ransparency, <strong>F</strong>airness, <strong>R</strong>eliability & Safety, <strong>I</strong>nclusiveness, <strong>P</strong>rivacy & Security, <strong>A</strong>ccountability (TFRIPA)</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">⚠️ What are the tool risk categories?</div>
<div class="flashcard-back"><strong>R</strong>ead (safe) → <strong>W</strong>rite (review) → <strong>S</strong>hell (highest, explicit consent) → <strong>N</strong>etwork (data exposure)</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🧰 What are the 3 MCP server capability types?</div>
<div class="flashcard-back"><strong>Tools</strong> (actions to execute), <strong>Resources</strong> (data to read), <strong>Prompts</strong> (reusable templates)</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">✋ When should an agent require human approval?</div>
<div class="flashcard-back">File deletion, package installation, config changes, deployment, accessing production, and any terminal commands that modify state</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🧠 What is context window management?</div>
<div class="flashcard-back">Prioritizing what fits in the token limit. Order: user request > explicit references > active file > semantic search > project structure</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">📊 What metrics define good agent performance?</div>
<div class="flashcard-back">Completion >85%, Acceptance >75%, Iterations <5, Errors <5%, Latency p95 <5s</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">⚡ How does streaming reduce perceived latency?</div>
<div class="flashcard-back">Sends output tokens as generated rather than waiting for full response. Users see results immediately even if total time is the same.</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">📁 What data classification levels apply to agents?</div>
<div class="flashcard-back"><strong>Public</strong> (unrestricted) → <strong>Internal</strong> (with auth) → <strong>Confidential</strong> (encrypted) → <strong>Restricted</strong> (never exposed to agents)</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">📝 What makes a good agent prompt?</div>
<div class="flashcard-back">Specific, constrained, provides context. Example: "Create a Python function that validates email using regex, returns bool, handles + aliases"</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">👁️ What is the role of human oversight?</div>
<div class="flashcard-back">Agents suggest → humans approve (production). Agents generate → humans review (code). Agents monitor → humans decide (incidents). Agents flag → humans investigate (security).</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🧩 What are GitHub Copilot Extensions?</div>
<div class="flashcard-back">Custom agents invoked via <strong>@mentions</strong> in Copilot Chat. Extend Copilot with domain-specific knowledge via an HTTP endpoint.</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🔄 How do agents integrate into CI/CD?</div>
<div class="flashcard-back">Pre-commit (auto-fix), Build (optimize), Test (generate tests), Review (auto PR review), Release (changelogs), Deploy (validation). Never auto-deploy to prod.</div>
</div>
</div>

<div class="flashcard" onclick="this.classList.toggle('flipped')">
<div class="flashcard-inner">
<div class="flashcard-front">🎭 What is bias in AI agent outputs?</div>
<div class="flashcard-back">Training data, cultural, gender, accessibility, language bias. Mitigate with inclusive language (main not master, allowlist not whitelist) and diverse testing.</div>
</div>
</div>

</div>

---

## Mnemonics

### TFRIPA — Six Responsible AI Principles

| Letter | Principle | Remember |
|--------|-----------|----------|
| **T** | Transparency | Tell users what you're doing |
| **F** | Fairness | Fair treatment for all |
| **R** | Reliability & Safety | Reliable, safe behavior |
| **I** | Inclusiveness | Include everyone |
| **P** | Privacy & Security | Protect data |
| **A** | Accountability | Always have human oversight |

### ORUST — Permission Levels (top → bottom)

| Letter | Level | Remember |
|--------|-------|----------|
| **O** | Organization Policy | Org sets the rules |
| **R** | Repository Settings | Repo-level controls |
| **U** | User Permissions | User-specific access |
| **S** | Session Scope | Scoped per invocation |
| **T** | Tool-Level Access | Tool approval required |

### RWSN — Tool Risk Categories (lowest → highest)

| Letter | Category | Risk Level |
|--------|----------|-----------|
| **R** | Read | Safe — no approval needed |
| **W** | Write | Medium — requires review |
| **S** | Shell | High — explicit consent |
| **N** | Network | High — data exposure risk |

### HCST — MCP Components

| Letter | Component | Role |
|--------|-----------|------|
| **H** | Host | Application running the AI model |
| **C** | Client | Protocol handler / connection manager |
| **S** | Server | Exposes tools, resources, prompts |
| **T** | Transport | Communication layer (stdio/HTTP+SSE) |

### PEI — Agent Loop

| Letter | Phase | What Happens |
|--------|-------|-------------|
| **P** | Plan | Analyze request, create steps |
| **E** | Execute | Run tools, modify files, run commands |
| **I** | Iterate | Check results, fix errors, repeat |

---

## Cheat Sheet Tables

### Domain 1: Agent Architecture & SDLC

| Concept | Key Facts |
|---------|-----------|
| Single Agent | One LLM + tools, simple tasks |
| Multi-Agent | Specialized agents, complex workflows |
| Orchestrator-Worker | Central coordinator delegates |
| Autonomy Levels | Full (formatting) → Supervised (deploy) → Advisory (architecture) |
| SDLC Phases | Plan → Code → Test → Review → Deploy → Monitor |
| Agent ≠ Assistant | Agents have autonomy, state, tool use, error recovery |

### Domain 2: Design & Implementation

| Concept | Key Facts |
|---------|-----------|
| Agent Mode | Multi-step, autonomous, full tool access, workspace context |
| Chat Mode | Single response, limited tools, conversation context |
| MCP Protocol | JSON-RPC 2.0, stdio or HTTP/SSE transport |
| MCP Tools | Actions agent can execute (functions) |
| MCP Resources | Data agent can read (files, APIs) |
| MCP Prompts | Reusable prompt templates |
| Workflow Design | Decompose → Error handle → Checkpoint → Validate → Rollback |
| Extensions | @mention invocation, HTTP endpoint, domain-specific |

### Domain 3: Performance & Optimization

| Concept | Key Facts |
|---------|-----------|
| Latency Targets | Inline <200ms, Chat <2s, Agent step <10s, Full task <5min |
| Streaming | Primary technique for perceived speed |
| Task Completion | Target >85%, alert <70% |
| User Acceptance | Target >75% |
| Avg Iterations | Target <5, warning >10 |
| Optimization | Cache, smaller models, context pruning, parallel tool calls |

### Domain 4: Security & Governance

| Concept | Key Facts |
|---------|-----------|
| Least Privilege | Only access what's needed for current task |
| Permission Levels | Org → Repo → User → Session → Tool |
| Sensitive Files | .env, secrets/, *.key — always deny agent access |
| Audit Logs | Timestamp, user, session, action, target, approval status |
| Data Classification | Public → Internal → Confidential → Restricted |
| Secrets | Reference by name, never by value; use vaults |

### Domain 5: Collaboration

| Concept | Key Facts |
|---------|-----------|
| Code Gen Patterns | Prompt-driven, test-first, refactor, pattern-extension, docs-first |
| Effective Prompts | Specific, constrained, provide context |
| CI/CD Integration | Lint-fix, test-gen, PR review, release notes, deploy validation |
| Never Auto-deploy | Production requires human approval always |
| Interaction Patterns | Direct, iterative, constraint-setting, example-driven, exploratory |

### Domain 6: Responsible AI

| Concept | Key Facts |
|---------|-----------|
| 6 Principles | Transparency, Fairness, Reliability, Inclusiveness, Privacy, Accountability |
| Bias Types | Training data, cultural, gender, accessibility, language |
| Inclusive Terms | main (not master), replica (not slave), allowlist/denylist |
| Transparency | Disclose AI content, explain reasoning, show confidence, cite sources |
| Compliance | GDPR/CCPA, audit logs, opt-out mechanisms, incident response |
| Monitoring | Content safety, fairness metrics, compliance logs, alerting |

---

## Cross-Domain Connections

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#6366f1', 'primaryTextColor': '#fff', 'lineColor': '#94a3b8', 'fontSize': '12px'}}}%%
graph LR
  subgraph CC["🔗 Cross-Cutting Concerns"]
    MCP["🔌 MCP Protocol"]:::mcp
    SEC["🛡️ Security"]:::sec
    HO["👁️ Human Oversight"]:::ho
    PERF["📊 Performance"]:::perf
  end

  subgraph Domains["📚 Domains"]
    D1["🏗️ D1: Architecture"]:::d1
    D2["⚙️ D2: Implementation"]:::d2
    D3["📊 D3: Performance"]:::d3
    D4["🛡️ D4: Security"]:::d4
    D5["🤝 D5: Collaboration"]:::d5
    D6["⚖️ D6: Responsible AI"]:::d6
  end

  MCP --> D2
  MCP --> D4
  MCP --> D5
  SEC --> D1
  SEC --> D2
  SEC --> D3
  SEC --> D4
  SEC --> D5
  SEC --> D6
  HO --> D1
  HO --> D4
  HO --> D5
  HO --> D6
  PERF --> D2
  PERF --> D3
  PERF --> D5

  classDef mcp fill:#06b6d4,stroke:#0891b2,color:#fff
  classDef sec fill:#f59e0b,stroke:#d97706,color:#fff
  classDef ho fill:#8b5cf6,stroke:#7c3aed,color:#fff
  classDef perf fill:#10b981,stroke:#059669,color:#fff
  classDef d1 fill:#6366f1,stroke:#4f46e5,color:#fff
  classDef d2 fill:#06b6d4,stroke:#0891b2,color:#fff
  classDef d3 fill:#10b981,stroke:#059669,color:#fff
  classDef d4 fill:#f59e0b,stroke:#d97706,color:#fff
  classDef d5 fill:#ef4444,stroke:#dc2626,color:#fff
  classDef d6 fill:#8b5cf6,stroke:#7c3aed,color:#fff
```

| Cross-Domain Theme | Where It Appears | Key Insight |
|-------------------|------------------|-------------|
| **MCP** | D2 (implement), D4 (secure), D5 (CI/CD) | One protocol, multiple security and implementation concerns |
| **Security** | All 6 domains | Not just Domain 4 — secure architecture, secure tools, secure pipelines, compliance |
| **Human Oversight** | D1 (autonomy levels), D4 (approval gates), D5 (review), D6 (accountability) | Every domain requires human decision points for high-risk actions |
| **Performance** | D2 (streaming), D3 (core metrics), D5 (CI/CD speed) | Balance thoroughness with speed; streaming is universal solution for latency |
| **Context Management** | D2 (context window), D3 (optimization), D4 (data boundaries) | What the agent sees determines quality AND security |
| **Tool Permissions** | D2 (tool categories), D4 (least privilege), D5 (CI/CD safety) | RWSN risk model applies everywhere tools are used |
