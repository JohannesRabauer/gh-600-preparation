# Revision Resources

## Table of Contents

- [Executive Summary](#executive-summary)
- [Cheat Sheets](#cheat-sheets)
- [Flashcards](#flashcards)
- [Mnemonics](#mnemonics)

---

## Executive Summary

!!! note "Quick Review"
    This 2000-word summary covers all 6 exam domains. Use it for last-minute revision before your exam.

### Domain 1: Prepare Agent Architecture and SDLC Processes (15-20%)

Agentic AI architecture is about designing systems where LLMs can autonomously plan, execute, and iterate on development tasks. The key patterns are **single-agent** (one LLM with tools), **multi-agent** (specialized agents collaborating), and **orchestrator-worker** (central coordinator delegating tasks). Agents integrate at every SDLC phase: planning (task decomposition), coding (multi-file generation), testing (automated test creation), review (PR analysis), and deployment (CI/CD automation). Agents communicate via tool calls (structured function invocations), and orchestration follows DAG execution patterns. Autonomy levels range from full (formatting, tests) to supervised (deployments, config changes) to advisory (architecture decisions).

### Domain 2: Design and Implement Agentic Solutions (20-25%)

This is the highest-weighted domain. **GitHub Copilot agent mode** is the primary feature — it autonomously creates files, edits code, runs terminal commands, and iterates on failures. Unlike chat (single response) or inline (autocomplete), agent mode executes multi-step plans. **MCP (Model Context Protocol)** is the open standard for connecting AI models to external tools. MCP has four components: Host (IDE), Client (protocol handler), Server (tool provider), and Transport (stdio or HTTP/SSE). MCP exposes tools (actions), resources (data), and prompts (templates). Multi-step workflows follow decomposition principles: break complex tasks into atomic steps, validate at each checkpoint, handle errors with retry/rollback. Copilot extensions enable custom domain-specific agents invoked via @mentions.

### Domain 3: Evaluate and Optimize Agent Performance (10-15%)

Agent quality is measured across dimensions: correctness (builds/tests pass), completeness (requirements covered), code quality (linting, static analysis), and security (vulnerability scanning). Latency optimization uses streaming (perceived speed), caching (repeated patterns), model selection (speed vs. quality trade-off), and context pruning (less input = faster). Key KPIs: task completion rate (target >85%), user acceptance rate (>75%), average iterations per task (<5), error rate (<5%), p95 latency (<5s). Monitoring should alert on degradation and enable continuous improvement.

### Domain 4: Secure and Govern Agentic AI Solutions (15-20%)

Security uses least-privilege: agents access only what they need. Permission levels span organization → repository → user → session → tool. Human-in-the-loop controls require approval for file deletion, package installation, and configuration changes. Read operations are generally safe; write and shell operations require approval. All agent actions must be logged with timestamps, user identity, action type, and risk level. Data governance classifies information (public → internal → confidential → restricted) and restricts agent access accordingly. Secrets must never be hardcoded — use vault services and environment variable injection. MCP server configurations reference secrets by name, never by value.

### Domain 5: Collaborate with AI Agents in Development (15-20%)

Effective code generation requires specific prompts with constraints and context. AI-assisted code review automates security scanning, style checking, and performance analysis on PRs. Test generation covers unit tests, integration tests, edge cases, and regression tests from function signatures and documentation. CI/CD integration includes pre-commit auto-fixing, build optimization, test generation for coverage gaps, automated PR review, release note generation, and deployment validation. Human-agent interaction patterns: direct instruction (well-defined tasks), iterative refinement (complex tasks), constraint setting (specific requirements), and example-driven (pattern replication).

### Domain 6: Implement Responsible AI Practices (10-15%)

Microsoft's 6 principles: **Fairness** (equitable treatment), **Reliability & Safety** (consistent performance), **Privacy & Security** (data protection), **Inclusiveness** (accessible to all), **Transparency** (explain behavior), **Accountability** (human responsibility). Transparency requires disclosing AI-generated content, explaining reasoning, acknowledging limitations, and indicating confidence. Bias types include training data bias, cultural bias, gender bias, accessibility bias, and language bias. Mitigation includes inclusive language (main not master, allowlist not whitelist), accessibility checks, and diverse testing. Compliance requires audit logs, consent mechanisms, incident response plans, and regular assessments.

---

## Cheat Sheets

### Domain 1: Prepare Agent Architecture and SDLC Processes

| Concept | Key Points |
|---------|-----------|
| Agent Architecture Patterns | Single, Multi, Orchestrator-Worker, Hierarchical |
| SDLC Integration | Plan→Code→Test→Review→Deploy→Monitor |
| Autonomy Levels | Full (formatting) → Supervised (deploy) → Advisory (design) |
| Communication | Tool calls, event-driven, pub-sub, shared context |
| Agent Roles | Code gen, reviewer, test writer, docs, DevOps, security |
| Framework Selection | Complexity, integration needs, security, team size, customization |

### Domain 2: Design and Implement Agentic Solutions

| Concept | Key Points |
|---------|-----------|
| Agent Mode vs Chat | Agent: multi-step, autonomous. Chat: single response |
| Agent Mode Tools | read_file, write_file, edit_file, run_command, search, web |
| MCP Components | Host (IDE), Client (handler), Server (tools), Transport (stdio/HTTP) |
| MCP Capabilities | Tools (actions), Resources (data), Prompts (templates), Sampling |
| MCP Transport | stdio (local), HTTP/SSE (remote) — uses JSON-RPC 2.0 |
| MCP Config | `mcpServers` in JSON config, env vars for secrets |
| Workflow Principles | Decomposition, error handling, checkpoints, validation, rollback |
| Extensions | Custom agents via @mentions, streaming responses |
| Context Priority | Request → References → Active file → Relevant files → Structure |

### Domain 3: Evaluate and Optimize Agent Performance

| Concept | Key Points |
|---------|-----------|
| Quality Dimensions | Correctness, completeness, code quality, security |
| Latency Targets | Inline: <200ms, Chat: <2s, Agent step: <10s, Full task: <5min |
| Optimization | Streaming, caching, model selection, context pruning, parallel calls |
| KPIs | Completion >85%, Acceptance >75%, Iterations <5, Errors <5% |
| Monitoring | Log all actions, alert on degradation, track trends |

### Domain 4: Secure and Govern Agentic AI Solutions

| Concept | Key Points |
|---------|-----------|
| Permission Levels | Organization → Repository → User → Session → Tool |
| Tool Risk | Read (safe) → Write (review) → Shell (approval) → Network (careful) |
| Least Privilege | Only access needed resources, deny by default |
| Audit Requirements | Timestamp, user, action, target, approval status, risk level |
| Data Classification | Public → Internal → Confidential → Restricted |
| Secrets | Never hardcode, use vaults, reference by name not value |
| Human-in-Loop | File deletes, pkg install, config changes, deployments |

### Domain 5: Collaborate with AI Agents in Development

| Concept | Key Points |
|---------|-----------|
| Code Gen Patterns | Prompt-driven, test-first, refactor, pattern extension, docs-first |
| Code Review | Automated on PR, scope to changed files, security+performance+style |
| Test Generation | Unit, integration, edge cases, regression, property-based |
| CI/CD Integration | Pre-commit→Build→Test→Review→Release→Deploy |
| Interaction Patterns | Direct instruction, iterative refinement, constraints, examples |
| Never Auto-Deploy | Always require human approval for production deployments |

### Domain 6: Implement Responsible AI Practices

| Concept | Key Points |
|---------|-----------|
| 6 Principles | Fairness, Reliability, Privacy, Inclusiveness, Transparency, Accountability |
| Transparency | Disclose AI content, explain reasoning, show confidence, cite sources |
| Bias Types | Training data, cultural, gender, accessibility, language |
| Inclusive Language | main (not master), allowlist (not whitelist), replica (not slave) |
| Compliance | Audit logs, consent, incident response, regular assessment |
| Monitoring | Content safety, fairness metrics, compliance checks, incidents |

---

## Flashcards

!!! info "Study Method"
    Cover the answer and try to recall it from memory. Review cards you miss more frequently.

### Domain 1 Flashcards

??? question "Q: What are the 4 main agent architecture patterns?"
    **A:** Single Agent, Multi-Agent, Orchestrator-Worker, Hierarchical

??? question "Q: What is the plan-execute-iterate loop?"
    **A:** The agent's core workflow: 1) Analyze request and create a plan, 2) Execute each step using tools, 3) Check results and adjust plan if needed, 4) Repeat until task is complete or user intervenes.

??? question "Q: Name the 3 autonomy levels for agents."
    **A:** Full Autonomy (acts without approval — e.g., formatting), Supervised (proposes, human approves — e.g., deployments), Advisory (suggests, human decides — e.g., architecture).

??? question "Q: At which SDLC phases can agents operate?"
    **A:** Planning (task decomposition), Design (architecture), Coding (generation), Testing (test creation), Review (PR analysis), Deployment (CI/CD), Monitoring (log analysis).

??? question "Q: What are the 4 agent communication patterns?"
    **A:** Request-Response, Event-Driven, Publish-Subscribe, Shared Context.

??? question "Q: How do you select between Copilot Chat vs. Agent Mode?"
    **A:** Chat = simple questions, single responses. Agent Mode = complex multi-step tasks requiring file edits, terminal commands, and iteration.

### Domain 2 Flashcards

??? question "Q: What are the 3 Copilot modes and their key difference?"
    **A:** Inline (autocomplete, single line/block), Chat (conversation, single response), Agent Mode (autonomous multi-step, creates/edits files, runs commands, iterates).

??? question "Q: What does MCP stand for and what is it?"
    **A:** Model Context Protocol — an open standard defining how AI models connect to external tools and data sources using a unified protocol.

??? question "Q: What are the 4 MCP components?"
    **A:** Host (application running the AI model, e.g., IDE), Client (maintains server connections), Server (exposes tools/resources/prompts), Transport (communication layer — stdio or HTTP/SSE).

??? question "Q: What are the 3 MCP capability types?"
    **A:** Tools (functions the agent can call), Resources (data the agent can access), Prompts (pre-built prompt templates).

??? question "Q: What transport protocols does MCP use?"
    **A:** stdio (local communication via standard input/output) and HTTP/SSE (remote communication via Server-Sent Events). Both use JSON-RPC 2.0.

??? question "Q: What are the 5 workflow design principles?"
    **A:** Decomposition (break into atomic steps), Error Handling (plan for failures), Checkpoints (save progress), Validation (verify outputs), Rollback (undo failed steps).

??? question "Q: What are Copilot agent mode's built-in tools?"
    **A:** read_file, write_file/edit_file, list_directory, search_files, run_command (terminal), web_search, fetch_url.

??? question "Q: How are Copilot Extensions invoked?"
    **A:** Via @mentions in Copilot Chat (e.g., @db query users). They connect to custom backend endpoints that process requests and stream responses.

### Domain 3 Flashcards

??? question "Q: What are the 4 quality dimensions for agent output?"
    **A:** Correctness (builds/tests pass), Completeness (all requirements met), Code Quality (linting/standards), Security (no vulnerabilities).

??? question "Q: What are the target latencies for Copilot?"
    **A:** Inline suggestions: <200ms, Chat first token: <2s, Agent mode step: <10s, Full agent task: <5 min.

??? question "Q: Name 4 latency optimization strategies."
    **A:** Streaming responses (perceived speed), Caching patterns (repeated requests), Model selection (smaller = faster), Context pruning (less input data).

??? question "Q: What are the 5 key agent KPIs?"
    **A:** Task completion rate (>85%), User acceptance rate (>75%), Average iterations (<5), Error rate (<5%), p95 latency (<5s).

### Domain 4 Flashcards

??? question "Q: What are the 5 permission levels from broadest to narrowest?"
    **A:** Organization → Repository → User → Session → Tool.

??? question "Q: How are tools categorized by risk?"
    **A:** Read (always safe, no approval) → Write (requires review) → Shell (highest risk, explicit consent) → Network (data exposure risk).

??? question "Q: What must an agent audit log contain?"
    **A:** Timestamp, user identity, agent session ID, action performed, target resource, tool used, approval status, content hash, risk level.

??? question "Q: How should secrets be handled in agent workflows?"
    **A:** Never hardcoded. Use vault services (GitHub Secrets, Azure Key Vault). Reference by name via environment variables. Enable secret scanning. Rotate regularly.

??? question "Q: What operations always require human approval?"
    **A:** File deletion, package installation, configuration changes, production deployments, access control modifications.

??? question "Q: What are the 4 data classification levels?"
    **A:** Public (open source, docs), Internal (private repos), Confidential (customer data, secrets), Restricted (PII, financial — never exposed to agents).

### Domain 5 Flashcards

??? question "Q: What are the 5 code generation patterns?"
    **A:** Prompt-driven (describe needs), Test-first (write test then implement), Refactor (select and improve), Pattern extension (show example, ask for more), Documentation-first (write docs, generate code).

??? question "Q: What can AI automate in CI/CD?"
    **A:** Pre-commit (auto-fix lint), Build (optimize config), Test (generate missing tests), Review (automated PR review), Release (changelogs, version bumps), Deploy (validation, rollback decisions).

??? question "Q: What should NEVER be automated without human approval?"
    **A:** Production deployments. Always require explicit human approval for any change affecting live systems.

??? question "Q: What are the 4 human-agent interaction patterns?"
    **A:** Direct Instruction (well-defined tasks), Iterative Refinement (complex tasks needing tuning), Constraint Setting (specific requirements), Example-Driven (pattern replication).

### Domain 6 Flashcards

??? question "Q: What are Microsoft's 6 Responsible AI principles?"
    **A:** Fairness, Reliability & Safety, Privacy & Security, Inclusiveness, Transparency, Accountability.

??? question "Q: What does transparency require in AI agents?"
    **A:** Disclosing AI-generated content, explaining reasoning, acknowledging limitations, citing sources, indicating confidence levels.

??? question "Q: What are the inclusive language replacements?"
    **A:** master → main, slave → replica, whitelist → allowlist, blacklist → denylist.

??? question "Q: What 5 types of bias can AI agents introduce?"
    **A:** Training data bias, Cultural bias, Gender bias, Accessibility bias, Language/programming language bias.

??? question "Q: What's needed for responsible AI compliance?"
    **A:** Audit logs, user consent mechanisms, AI content attribution, incident response plan, regular bias assessments, opt-out mechanisms.

---

## Mnemonics

### TFRIPA — The 6 Responsible AI Principles
**T**ransparency, **F**airness, **R**eliability, **I**nclusiveness, **P**rivacy, **A**ccountability

> *"The Friendly Robot Is Pretty Awesome"*

### DVRCE — Agent Workflow Design Principles
**D**ecomposition, **V**alidation, **R**ollback, **C**heckpoints, **E**rror handling

> *"Developers Very Rarely Create Errors"*

### HORSTN — Permission Levels (Broad to Narrow)
**O**rganization, **R**epository, **U**ser, **S**ession, **T**ool

> *"Our Repos Use Secure Tools"*

### RWSN — Tool Risk Levels (Low to High)
**R**ead, **W**rite, **S**hell, **N**etwork

> *"Reading Won't Scare Nobody"*

### HCRST — MCP Components
**H**ost, **C**lient, **S**erver, **T**ransport

> *"How Clients Send Things"*

### PEI — Agent Mode Core Loop
**P**lan, **E**xecute, **I**terate

> *"Plan Every Iteration"*
