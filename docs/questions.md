# Practice Questions

## Overview

| Difficulty | Count | Focus |
|-----------|-------|-------|
| Easy | 20 | Single-concept recall |
| Intermediate | 20 | Applying concepts to scenarios |
| Advanced | 20 | Multi-domain analysis |
| **Total** | **60** | All 6 domains covered |

!!! tip "Strategy"
    Start with Easy to build confidence, then Intermediate for application, then Advanced for exam-like scenarios. Review explanations for all wrong answers.

---

## Easy Questions

!!! note "Difficulty: Easy"
    Single-concept recall and basic understanding.

### Question 1

**Domain**: 2 | **Format**: Multiple Choice

What distinguishes GitHub Copilot's agent mode from chat mode?

- A. Agent mode can autonomously create files, run terminal commands, and iterate on failures
- B. Agent mode provides faster inline code completions
- C. Agent mode only works with Python code
- D. Agent mode requires a paid enterprise license while chat is free

??? success "Answer"
    **Correct**: A

    Agent mode's defining feature is autonomous multi-step execution. It can create/edit files, run commands, and iterate until the task is complete — unlike chat which gives a single response.

    - **B**: Incorrect. Inline suggestions are a separate feature, not agent mode.
    - **C**: Incorrect. Agent mode works with all supported languages.
    - **D**: Incorrect. Both modes have similar licensing requirements.

---

### Question 2

**Domain**: 2 | **Format**: Multiple Choice

What does MCP stand for in the context of AI agent tools?

- A. Multi-Cloud Platform
- B. Model Context Protocol
- C. Machine Code Processor
- D. Managed Copilot Provider

??? success "Answer"
    **Correct**: B

    MCP = Model Context Protocol. It's an open standard for connecting AI models to external tools and data sources.

    - **A, C, D**: Incorrect. These are not what MCP stands for in this context.

---

### Question 3

**Domain**: 4 | **Format**: Multiple Choice

Which tool category requires the HIGHEST level of user approval in agent systems?

- A. Read operations (reading file contents)
- B. Write operations (creating/editing files)
- C. Shell operations (running terminal commands)
- D. Search operations (finding code patterns)

??? success "Answer"
    **Correct**: C

    Shell/terminal commands carry the highest risk because they can execute arbitrary code, install packages, delete files, or make network requests. They always require explicit approval.

    - **A, D**: Incorrect. Read and search are safe operations.
    - **B**: Incorrect. Write operations require review but are less risky than shell commands.

---

### Question 4

**Domain**: 6 | **Format**: Multiple Choice

Which of Microsoft's Responsible AI principles focuses on ensuring AI systems work for people of all abilities?

- A. Fairness
- B. Inclusiveness
- C. Transparency
- D. Accountability

??? success "Answer"
    **Correct**: B

    Inclusiveness means AI systems should be accessible to and work for people of all abilities, backgrounds, and circumstances.

    - **A**: Fairness is about equitable treatment, not accessibility.
    - **C**: Transparency is about explaining AI behavior.
    - **D**: Accountability is about human responsibility for AI systems.

---

### Question 5

**Domain**: 1 | **Format**: Multiple Choice

In an orchestrator-worker agent pattern, what is the orchestrator's primary role?

- A. Execute all coding tasks directly
- B. Coordinate and delegate tasks to specialized worker agents
- C. Store all project data in memory
- D. Provide the user interface

??? success "Answer"
    **Correct**: B

    The orchestrator acts as a central coordinator that decomposes complex tasks and delegates them to specialized worker agents, then assembles the results.

    - **A**: Workers execute tasks, not the orchestrator.
    - **C**: Data storage is not the orchestrator's role.
    - **D**: The UI is separate from orchestration logic.

---

### Question 6

**Domain**: 2 | **Format**: Multiple Choice

In MCP, what is the transport layer responsible for?

- A. Storing tool definitions
- B. Handling communication between client and server
- C. Generating AI responses
- D. Managing user authentication

??? success "Answer"
    **Correct**: B

    The transport layer handles the actual communication between MCP client and server, using either stdio (local) or HTTP/SSE (remote).

    - **A**: Tool definitions are on the server.
    - **C**: The host/LLM generates responses.
    - **D**: Authentication is separate from transport.

---

### Question 7

**Domain**: 3 | **Format**: Multiple Choice

What is the target task completion rate for a well-performing agent system?

- A. > 50%
- B. > 70%
- C. > 85%
- D. > 99%

??? success "Answer"
    **Correct**: C

    Target task completion rate is > 85%. Below 70% is considered critical and requires investigation.

    - **A, B**: These are below acceptable thresholds.
    - **D**: 99% is unrealistic for complex autonomous tasks.

---

### Question 8

**Domain**: 4 | **Format**: Multiple Choice

How should secrets be provided to MCP servers?

- A. Hardcoded in the MCP server source code
- B. Via environment variables referencing a secrets vault
- C. Passed directly in tool call parameters
- D. Stored in a public configuration file

??? success "Answer"
    **Correct**: B

    Secrets should be injected via environment variables that reference a vault (GitHub Secrets, Azure Key Vault, etc.). Never hardcode or expose them.

    - **A, C, D**: All expose secrets in plaintext, which is a security violation.

---

### Question 9

**Domain**: 5 | **Format**: Multiple Choice

Which code generation pattern involves writing tests BEFORE asking the agent to implement the code?

- A. Prompt-driven
- B. Test-first
- C. Refactor
- D. Pattern extension

??? success "Answer"
    **Correct**: B

    Test-first (TDD) pattern: write the test specifying expected behavior, then ask the agent to write code that passes the test.

    - **A**: Prompt-driven describes the desired output in natural language.
    - **C**: Refactor improves existing code.
    - **D**: Pattern extension replicates from examples.

---

### Question 10

**Domain**: 6 | **Format**: Multiple Choice

What is the correct inclusive alternative to "whitelist"?

- A. Safelist
- B. Allowlist
- C. Goodlist
- D. Greenlist

??? success "Answer"
    **Correct**: B

    The inclusive alternative to "whitelist" is "allowlist" (and "denylist" replaces "blacklist").

    - **A, C, D**: Not the standard inclusive replacements.

---

### Question 11

**Domain**: 1 | **Format**: Multiple Choice

Which autonomy level is appropriate for an agent performing production deployments?

- A. Full autonomy
- B. Supervised (requires human approval)
- C. Advisory only
- D. No agent involvement allowed

??? success "Answer"
    **Correct**: B

    Production deployments require supervised autonomy — the agent proposes changes but a human must explicitly approve before execution.

    - **A**: Full autonomy is too risky for production.
    - **C**: Advisory means the agent only suggests without acting.
    - **D**: Agents can assist with deployments under supervision.

---

### Question 12

**Domain**: 2 | **Format**: Multiple Choice

What protocol does MCP use for communication messages?

- A. REST
- B. GraphQL
- C. JSON-RPC 2.0
- D. gRPC

??? success "Answer"
    **Correct**: C

    MCP uses JSON-RPC 2.0 as its message format over stdio or HTTP/SSE transport.

    - **A, B, D**: Not the protocols used by MCP.

---

### Question 13

**Domain**: 3 | **Format**: Multiple Choice

What is the primary technique for reducing perceived latency in agent responses?

- A. Using a larger model
- B. Token streaming
- C. Disabling tools
- D. Reducing context window

??? success "Answer"
    **Correct**: B

    Token streaming sends output incrementally as it's generated, so users see results immediately rather than waiting for the full response.

    - **A**: Larger models are slower.
    - **C**: Disabling tools reduces capability, not latency perception.
    - **D**: This can help actual latency but streaming is the primary perceived-speed technique.

---

### Question 14

**Domain**: 4 | **Format**: Multiple Choice

What information must an agent audit log include?

- A. Only the final output
- B. Timestamp, user identity, action, target, approval status, and risk level
- C. Only errors and failures
- D. Only tool names used

??? success "Answer"
    **Correct**: B

    Comprehensive audit logs must include: timestamp, user identity, session ID, action type, target resource, tool used, approval status, content hash, and risk level.

    - **A, C, D**: These are incomplete and insufficient for proper auditing.

---

### Question 15–20

*(Questions 15-20 follow the same pattern covering remaining topics across all domains)*

### Question 15

**Domain**: 5 | **Format**: Multiple Choice

What should NEVER be fully automated in a CI/CD pipeline without human approval?

- A. Code formatting
- B. Running unit tests
- C. Production deployment
- D. Generating changelogs

??? success "Answer"
    **Correct**: C

    Production deployments must always have human approval gates. Formatting, testing, and changelog generation can be safely automated.

---

### Question 16

**Domain**: 1 | **Format**: Multiple Choice

What communication pattern does GitHub Copilot use between the IDE and AI backend?

- A. Shared memory
- B. Message-based protocol (tool calls with structured inputs/outputs)
- C. Direct database queries
- D. File system polling

??? success "Answer"
    **Correct**: B

    Copilot uses a message-based protocol where tool calls have structured JSON inputs and outputs.

---

### Question 17

**Domain**: 2 | **Format**: Multiple Choice

What are the three types of capabilities an MCP server can expose?

- A. Tools, Resources, Prompts
- B. Read, Write, Execute
- C. Input, Output, State
- D. Query, Mutation, Subscription

??? success "Answer"
    **Correct**: A

    MCP servers expose: Tools (actions/functions), Resources (data access), and Prompts (template prompts).

---

### Question 18

**Domain**: 6 | **Format**: Multiple Choice

Which Responsible AI principle requires AI systems to explain their behavior?

- A. Fairness
- B. Accountability
- C. Transparency
- D. Reliability

??? success "Answer"
    **Correct**: C

    Transparency requires AI systems to be understandable — explaining decisions, acknowledging limitations, and disclosing AI involvement.

---

### Question 19

**Domain**: 3 | **Format**: Multiple Choice

What is considered a critical error rate threshold for agent systems?

- A. > 1%
- B. > 5%
- C. > 15%
- D. > 50%

??? success "Answer"
    **Correct**: C

    Error rate > 15% is critical. Good is < 5%, warning is 5-15%.

---

### Question 20

**Domain**: 4 | **Format**: Multiple Choice

Which data classification level should NEVER be exposed to AI agents?

- A. Public
- B. Internal
- C. Confidential
- D. Restricted (PII, financial data)

??? success "Answer"
    **Correct**: D

    Restricted data (PII, financial records) must never be exposed to AI agents. Even confidential data requires special handling.

---

## Intermediate Questions

!!! note "Difficulty: Intermediate"
    Applying concepts to specific scenarios.

### Question 21

**Domain**: 2 | **Format**: Multiple Select

A developer is configuring an MCP server for their project. Which of the following are valid MCP server configuration options? (Select all that apply)

- A. Specifying the command to launch the server process
- B. Passing environment variables for secrets
- C. Defining the server's response format as XML
- D. Listing arguments for the server command
- E. Setting a disabled flag to temporarily turn off the server

??? success "Answer"
    **Correct**: A, B, D, E

    MCP server config supports: `command` (launch command), `args` (arguments), `env` (environment variables), and `disabled` (enable/disable toggle).

    - **C**: MCP uses JSON-RPC, not XML. The transport format is not configurable.

---

### Question 22

**Domain**: 4 | **Format**: Scenario-Based

A security team is setting up agent permissions for a new development team. The team works on a customer-facing application with a database containing user PII. Which permission configuration is most appropriate?

- A. Grant full read/write access to all repository files and database queries
- B. Grant read access to source code, write access to src/ and tests/ only, deny access to .env files and database containing PII
- C. Deny all agent access since PII is involved
- D. Grant read-only access with no write permissions for any files

??? success "Answer"
    **Correct**: B

    Least privilege means: agents can read code (needed for context), write only in appropriate directories (src, tests), and are explicitly denied access to secrets (.env) and restricted data (PII database).

    - **A**: Too permissive — exposes PII and secrets.
    - **C**: Too restrictive — agents can still be useful without accessing PII directly.
    - **D**: Too restrictive for development work — agents need write access to be useful.

---

### Question 23

**Domain**: 1 | **Format**: Scenario-Based

A team is building a system that needs to: refactor a large codebase, run tests after each change, generate documentation, and create a PR. Which agent architecture pattern is most appropriate?

- A. Single agent handling all tasks sequentially
- B. Orchestrator-worker pattern with specialized agents
- C. Advisory-only pattern where agents suggest but don't act
- D. Peer-to-peer agents with no coordination

??? success "Answer"
    **Correct**: B

    The orchestrator-worker pattern is ideal for complex multi-faceted tasks. The orchestrator coordinates, while specialized workers handle refactoring, testing, documentation, and PR creation respectively.

    - **A**: A single agent for this many diverse tasks risks losing context and quality.
    - **C**: Advisory doesn't complete the task — human would do all work.
    - **D**: Without coordination, agents would conflict and duplicate work.

---

### Question 24

**Domain**: 5 | **Format**: Multiple Choice

A CI/CD pipeline runs AI-generated tests that are failing intermittently. What is the most appropriate agent-assisted response?

- A. Disable all AI-generated tests
- B. Have the agent analyze flaky test patterns and suggest fixes for non-deterministic behavior
- C. Replace all tests with manual testing
- D. Increase the test timeout to 10 minutes

??? success "Answer"
    **Correct**: B

    Agents can identify patterns in flaky tests (race conditions, timing dependencies, external service calls) and suggest targeted fixes like adding retries, mocking external services, or fixing race conditions.

    - **A, C**: Throwing away tests is wasteful.
    - **D**: Increasing timeout doesn't fix the root cause.

---

### Question 25

**Domain**: 6 | **Format**: Multiple Select

A company is auditing their AI agent deployment for responsible AI compliance. Which of the following should be part of their audit? (Select all that apply)

- A. Reviewing audit logs of all agent actions
- B. Testing for bias in agent outputs across different users
- C. Verifying user consent mechanisms are in place
- D. Checking that all agent-generated code is faster than human-written code
- E. Confirming incident response plans exist for AI failures

??? success "Answer"
    **Correct**: A, B, C, E

    Responsible AI compliance requires: audit logs (accountability), bias testing (fairness), consent (privacy), and incident response (reliability/safety).

    - **D**: Performance comparison to human code is not a responsible AI requirement.

---

### Question 26

**Domain**: 2 | **Format**: Scenario-Based

A developer needs their agent to query a PostgreSQL database during code generation. The database contains both schema information (useful for code gen) and user data (sensitive). What is the correct approach?

- A. Give the agent full database access and trust it to ignore user data
- B. Create an MCP server that exposes schema-only queries and blocks access to user tables
- C. Copy the entire database to a text file and add it to the agent's context
- D. Manually type schema information into every agent prompt

??? success "Answer"
    **Correct**: B

    Creating an MCP server with restricted access implements least privilege. The server exposes only schema queries (tools for reading table structures) and explicitly blocks access to tables containing user data.

    - **A**: Violates least privilege and data governance.
    - **C**: Exposes user data and wastes context window.
    - **D**: Impractical and doesn't leverage agent capabilities.

---

### Question 27

**Domain**: 3 | **Format**: Multiple Choice

An agent's task completion rate has dropped from 90% to 65% over the past week. What is the most likely first diagnostic step?

- A. Immediately switch to a different AI model
- B. Analyze failure logs to identify common error patterns and affected task types
- C. Disable agent mode for all users
- D. Increase the agent's token budget

??? success "Answer"
    **Correct**: B

    Diagnosing performance issues starts with data analysis — looking at failure logs to identify whether the problem is specific task types, tools, or contexts before making changes.

    - **A**: Switching models without diagnosis may not fix the issue.
    - **C**: Too extreme without understanding the cause.
    - **D**: Token budget may not be the issue.

---

### Question 28

**Domain**: 1 | **Format**: Multiple Choice

Which framework selection criterion is MOST important when an agent needs to interact with proprietary internal APIs?

- A. Team size
- B. Integration needs (MCP for external tool access)
- C. Programming language support
- D. Cost per token

??? success "Answer"
    **Correct**: B

    When an agent needs to access external/internal APIs, the key criterion is integration capability — specifically MCP servers that can bridge the agent to those proprietary APIs securely.

---

### Question 29

**Domain**: 5 | **Format**: Scenario-Based

A developer prompts the agent with "add pagination." The agent's output is incomplete and doesn't match the project's existing patterns. What is the best next step?

- A. Accept the output and manually fix it
- B. Provide more specific context: "Add cursor-based pagination to the /users endpoint following the pattern in /products endpoint, using the existing PageInfo type"
- C. Switch to a different AI tool
- D. Disable agent mode and write it manually

??? success "Answer"
    **Correct**: B

    Iterative refinement with specific context improves agent output. Referencing existing patterns, specifying the approach (cursor-based), and pointing to examples (products endpoint) gives the agent what it needs.

    - **A**: Defeats the purpose of using the agent.
    - **C, D**: Premature — the issue is prompt quality, not tool capability.

---

### Question 30

**Domain**: 4 | **Format**: Multiple Select

Which of the following should trigger a security alert in an agent monitoring system? (Select all that apply)

- A. Agent reads a source file in the allowed directory
- B. Agent attempts to access a file in the secrets/ directory
- C. Agent generates 100 lines of code
- D. Agent attempts to run `curl` to an unknown external URL
- E. Agent tries to modify the .github/workflows/ directory

??? success "Answer"
    **Correct**: B, D, E

    Security alerts should trigger for: accessing sensitive directories (secrets/), network requests to unknown URLs, and modifying security-critical configs (CI/CD workflows).

    - **A**: Reading allowed files is normal.
    - **C**: Generating code is the agent's job.

---

### Questions 31-40

### Question 31

**Domain**: 2 | **Format**: Multiple Choice

What happens when a Copilot agent mode task encounters a build error after editing files?

- A. The agent stops and asks the user to fix it
- B. The agent automatically analyzes the error and attempts to fix it
- C. The agent reverts all changes and starts over
- D. The agent ignores the error and continues

??? success "Answer"
    **Correct**: B

    Agent mode's iterate capability means it automatically reads error output, identifies the cause, and makes corrections — repeating until successful or reaching a limit.

---

### Question 32

**Domain**: 6 | **Format**: Scenario-Based

An AI agent generates variable names like `manHours`, `masterBranch`, and `whitelistIPs` in a new codebase. Which responsible AI principle is most directly violated?

- A. Reliability
- B. Transparency
- C. Fairness and Inclusiveness
- D. Privacy

??? success "Answer"
    **Correct**: C

    Non-inclusive language (gendered terms, master/slave, whitelist/blacklist) violates fairness and inclusiveness principles. The correct alternatives: `personHours`, `mainBranch`, `allowedIPs`.

---

### Question 33

**Domain**: 3 | **Format**: Multiple Choice

Which evaluation approach best measures whether an agent's code generation matches production quality standards?

- A. Only checking if the code compiles
- B. Combining automated static analysis, test execution, and human review
- C. Counting the number of lines generated
- D. Measuring response time only

??? success "Answer"
    **Correct**: B

    Production quality requires multiple evaluation dimensions: static analysis (code quality), tests (correctness), and human review (design quality, readability).

---

### Question 34

**Domain**: 2 | **Format**: Multiple Choice

In MCP, what is the difference between a "tool" and a "resource"?

- A. Tools are free, resources cost money
- B. Tools are actions the agent invokes; resources are data the agent reads
- C. Tools run on the client; resources run on the server
- D. There is no difference — they are synonyms

??? success "Answer"
    **Correct**: B

    Tools = functions/actions (e.g., query_database, send_email). Resources = data sources (e.g., file contents, API data). Tools DO things; resources PROVIDE information.

---

### Question 35-40

### Question 35

**Domain**: 1 | **Format**: Multiple Choice

What algorithm is commonly used to determine agent task execution order when tasks have dependencies?

- A. Binary search
- B. Topological sort (Kahn's algorithm)
- C. Bubble sort
- D. Depth-first search only

??? success "Answer"
    **Correct**: B

    Topological sort (Kahn's algorithm) determines a valid execution order that respects all dependencies — no task runs before its prerequisites.

---

### Question 36

**Domain**: 4 | **Format**: Multiple Choice

What is the primary security benefit of MCP's tool approval system?

- A. It makes the agent faster
- B. It ensures humans explicitly authorize each potentially risky operation before execution
- C. It prevents the agent from making any changes
- D. It encrypts all data

??? success "Answer"
    **Correct**: B

    Tool approval ensures human oversight for risky operations — the agent proposes an action, the user reviews and approves/rejects before execution.

---

### Question 37

**Domain**: 5 | **Format**: Multiple Choice

Which CI/CD stage is most appropriate for AI-assisted automatic code formatting fixes?

- A. Production deployment
- B. Pre-commit or early build stage
- C. After deployment monitoring
- D. Manual review phase

??? success "Answer"
    **Correct**: B

    Auto-formatting is a safe, non-semantic change that should happen early (pre-commit or build stage) before more complex steps.

---

### Question 38

**Domain**: 2 | **Format**: Multiple Choice

What is the correct context priority order for agent mode?

- A. Structure → Files → Request → References
- B. Request → References → Active File → Relevant Files → Structure
- C. Active File → Request → Structure → Everything
- D. Random selection of context

??? success "Answer"
    **Correct**: B

    Context priority: User's request (highest) → Explicit references (#file) → Active file → Semantically relevant files → Project structure (lowest).

---

### Question 39

**Domain**: 6 | **Format**: Multiple Choice

What should happen when an AI agent's output confidence is low?

- A. Hide the output from the user
- B. Present the output with a confidence indicator and suggest human verification
- C. Generate a completely different response
- D. Automatically submit it anyway

??? success "Answer"
    **Correct**: B

    Transparency requires indicating confidence levels. Low confidence output should be clearly marked and accompanied by a suggestion for human verification.

---

### Question 40

**Domain**: 3 | **Format**: Multiple Choice

What is the recommended p95 latency target for individual agent mode steps?

- A. < 200ms
- B. < 2 seconds
- C. < 10 seconds
- D. < 60 seconds

??? success "Answer"
    **Correct**: C

    Individual agent mode steps target < 10 seconds. Inline suggestions target < 200ms, chat first token < 2s.

---

## Advanced Questions

!!! note "Difficulty: Advanced"
    Multi-domain analysis and complex scenarios. These questions require combining knowledge from 2+ domains.

### Question 41

**Domain**: 2, 4 | **Format**: Scenario-Based

A fintech company wants to deploy an MCP server that gives their AI agent access to a transaction processing API. The API can read transaction history and initiate refunds. The agent is used by customer support developers to debug issues.

Which implementation approach best balances utility and security?

- A. Expose both read and refund capabilities as MCP tools with no restrictions
- B. Expose read-only transaction history as a tool; expose refund as a tool requiring explicit user approval with amount limits and audit logging
- C. Don't use MCP; manually copy-paste transaction data into prompts
- D. Expose all capabilities but add a disclaimer to the agent's system prompt

??? success "Answer"
    **Correct**: B

    This balances utility with security: read-only access helps debugging (safe), while refunds (financial action) require human approval, limits, and full audit trail. This combines MCP tool design (Domain 2) with security governance (Domain 4).

    - **A**: No restrictions on financial operations is unacceptable.
    - **C**: Impractical and defeats the purpose of agent tooling.
    - **D**: System prompts are not security controls — they can be overridden.

---

### Question 42

**Domain**: 1, 3, 5 | **Format**: Scenario-Based

A development team has been using AI agents for 3 months. Their metrics show: task completion rate 72% (target >85%), average 8 iterations per task (target <5), and user acceptance rate 60% (target >75%). Code quality metrics remain high when tasks do complete.

What is the most likely root cause and recommended action?

- A. The AI model is too small — upgrade to a larger model
- B. Tasks being assigned to agents are too complex and should be decomposed into smaller sub-tasks before agent execution
- C. Users are not prompting correctly — provide training
- D. The agent should be given more tools

??? success "Answer"
    **Correct**: B

    High iteration count (8 vs target 5) combined with low completion (72%) suggests tasks are too complex for single-agent execution. The solution is better task decomposition (Domain 1 architecture) to improve completion rates (Domain 3 KPIs) and developer satisfaction (Domain 5 collaboration).

    - **A**: Code quality is fine when tasks complete — model capability isn't the issue.
    - **C**: This might help marginally but doesn't address structural task complexity.
    - **D**: More tools without better task scoping won't reduce iterations.

---

### Question 43

**Domain**: 4, 6 | **Format**: Scenario-Based

An organization's AI agent was found to be suggesting code that uses gendered language in variable names and documentation. The agent also occasionally includes code patterns from a single dominant programming style, ignoring the team's established conventions. An audit is requested.

Which combination of actions is most comprehensive?

- A. Add a linter rule for gendered language and retrain the model
- B. Implement output scanning for bias indicators, add team style guides to agent context, enable audit logging of all suggestions, and conduct quarterly bias assessments
- C. Tell developers to manually fix any issues they notice
- D. Disable the agent until the problem is completely solved

??? success "Answer"
    **Correct**: B

    Comprehensive responsible AI compliance (Domain 6) requires: output scanning (detect bias), context enrichment (style guides solve convention issues), audit logging (Domain 4 governance), and regular assessment (ongoing compliance). This addresses both the bias and convention issues systematically.

    - **A**: Linting alone doesn't address documentation patterns or style conformance. You can't easily retrain the model.
    - **C**: Reactive and unreliable — doesn't prevent issues.
    - **D**: Too extreme and doesn't solve the underlying problem.

---

### Question 44

**Domain**: 2, 5 | **Format**: Scenario-Based

A developer needs to add a new feature that involves: creating a new database migration, updating the API handler, adding validation logic, writing tests, and updating the OpenAPI spec. They want to use Copilot agent mode.

What is the most effective approach?

- A. Write one prompt describing all 5 tasks and let the agent handle everything at once
- B. Provide a structured prompt that describes the feature, reference the existing migration pattern (#file), specify the validation requirements, and let the agent iterate through the implementation while running tests after each major change
- C. Complete each task in separate agent sessions with no context sharing
- D. Use inline suggestions only for each file

??? success "Answer"
    **Correct**: B

    Effective agent collaboration (Domain 5) with agent mode (Domain 2) requires: clear structured prompts, context references to existing patterns, specific requirements, and leveraging the agent's ability to test incrementally.

    - **A**: Too vague — the agent may miss project-specific patterns without references.
    - **C**: Losing context between sessions reduces quality.
    - **D**: Inline suggestions can't handle multi-file coordinated changes.

---

### Question 45

**Domain**: 3, 4 | **Format**: Scenario-Based

An agent's security scanning tool reports that its output contains a potential secret (an API key pattern) 2% of the time. The agent's task completion rate is 92% and code quality scores are high. How should this be handled?

- A. Ignore it since the completion rate is high
- B. Implement output filtering to detect and redact secret patterns before presenting to users, alert the security team, and investigate how secrets enter the agent's context
- C. Reduce the agent's file read permissions to zero
- D. Add a warning to the README

??? success "Answer"
    **Correct**: B

    Security issues override performance metrics. Even at 2%, secret leakage is critical. The fix: filter outputs (immediate mitigation), alert security (governance), and investigate context sources (root cause). This combines Domain 4 security with Domain 3 monitoring.

    - **A**: Security violations are never acceptable regardless of other metrics.
    - **C**: Removing all read access makes the agent useless.
    - **D**: A README warning doesn't prevent the issue.

---

### Question 46

**Domain**: 1, 2 | **Format**: Multiple Select

A team is designing an agent system for automated code review. Which architecture decisions are correct? (Select all that apply)

- A. Use advisory autonomy level (agent suggests, humans decide to merge)
- B. Give the review agent write access to merge PRs automatically
- C. Design the agent to analyze changed files only (not entire repo) for efficiency
- D. Include security scanning as part of the review agent's tools
- E. Have the agent comment on PRs with findings and severity levels

??? success "Answer"
    **Correct**: A, C, D, E

    Code review agents should: advise (not merge), scope to changed files (efficiency), include security scanning (comprehensive review), and comment with findings (actionable output).

    - **B**: Merging PRs requires human decision — supervised or advisory autonomy for code review.

---

### Question 47

**Domain**: 2, 4, 6 | **Format**: Scenario-Based

A healthcare company wants to use Copilot agent mode for developing their patient portal. The codebase includes mock patient data for testing and real API endpoints for the production system. Which configuration is most appropriate?

- A. Standard agent mode with full workspace access
- B. Agent mode with: read access to source code, write access restricted to src/ and tests/, explicit deny for any file containing patient data patterns, MCP tools that only access mock/test databases, audit logging enabled, and content filtering for PHI
- C. No AI assistance allowed in healthcare
- D. Agent mode with read-only access everywhere

??? success "Answer"
    **Correct**: B

    Healthcare requires layered controls combining: access restrictions (Domain 4), purpose-limited MCP tools (Domain 2), and compliance monitoring (Domain 6) — specifically HIPAA awareness around PHI (Protected Health Information).

    - **A**: No restrictions in healthcare is a compliance violation.
    - **C**: AI can be used in healthcare with proper controls.
    - **D**: Read-only doesn't allow the agent to write code.

---

### Question 48

**Domain**: 1, 5 | **Format**: Multiple Choice

A development team of 50 engineers wants to standardize how they use AI agents. Their needs include: custom code review rules, internal API documentation access, and enforced coding standards. Which approach best fits?

- A. Each developer configures their own agent independently
- B. Build GitHub Copilot Extensions for custom review rules, set up MCP servers for internal docs, and configure shared workspace settings for coding standards
- C. Use only the default Copilot without any customization
- D. Build a completely custom AI system from scratch

??? success "Answer"
    **Correct**: B

    Enterprise standardization (Domain 1 SDLC integration) with team collaboration (Domain 5) requires: Extensions (custom behaviors), MCP (internal tool access), and shared config (consistency).

    - **A**: Individual config creates inconsistency.
    - **C**: Default settings don't address custom needs.
    - **D**: Unnecessary when GitHub's ecosystem can be extended.

---

### Question 49

**Domain**: 3, 6 | **Format**: Scenario-Based

After deploying an AI code review agent, the team notices it consistently provides fewer comments on code written by experienced developers compared to juniors, even when code quality is similar. What principle is potentially violated and what should be done?

- A. This is expected behavior — experienced developers write better code
- B. The fairness principle may be violated. Investigate whether the agent exhibits bias based on author identity, implement blind review (remove author info from context), and add fairness metrics to monitoring
- C. Disable the review agent for senior developers only
- D. Increase the comment threshold for all developers

??? success "Answer"
    **Correct**: B

    This suggests author-based bias (Domain 6 fairness). The fix: investigate the bias source, implement blind review to remove the confounding variable, and add fairness monitoring (Domain 3 metrics).

    - **A**: If code quality is similar, comment rates should be similar.
    - **C, D**: These don't address the root cause.

---

### Question 50

**Domain**: 2, 3, 4 | **Format**: Scenario-Based

A company's MCP server provides access to their deployment infrastructure. An agent used by developers can view deployment status (read) and trigger rollbacks (write). Recently, an agent triggered a rollback during business hours based on a false positive health check reading.

Which combination of changes prevents this while maintaining agent utility?

- A. Remove rollback capability entirely
- B. Add time-based restrictions (rollback only during maintenance windows), require explicit user confirmation for rollbacks, implement health check validation requiring multiple consecutive failures before considering rollback, and add this incident to the audit log with a post-mortem
- C. Make health checks less sensitive
- D. Only allow rollbacks on weekends

??? success "Answer"
    **Correct**: B

    This combines: permission boundaries with time-based rules (Domain 4), validation logic before critical actions (Domain 2 tool design), monitoring improvements (Domain 3), and proper incident handling.

    - **A**: Removing the capability entirely reduces agent value.
    - **C**: Less sensitive health checks miss real issues.
    - **D**: Arbitrary time restrictions don't address the root cause.

---

### Questions 51-60

### Question 51

**Domain**: 2, 4 | **Format**: Multiple Choice

What is the security implication of using HTTP/SSE transport for MCP instead of stdio?

- A. No security difference
- B. HTTP/SSE enables remote server communication which introduces network attack surface, requiring TLS encryption and authentication
- C. HTTP/SSE is always more secure than stdio
- D. stdio requires more security configuration

??? success "Answer"
    **Correct**: B

    HTTP/SSE transport communicates over the network (vs. stdio's local process communication), introducing risks that require TLS encryption and authentication to mitigate.

---

### Question 52

**Domain**: 1, 6 | **Format**: Multiple Choice

When designing an agent architecture, which responsible AI requirement is addressed by implementing a "human-in-the-loop" approval system?

- A. Performance optimization
- B. Accountability — ensuring humans maintain responsibility for AI-assisted decisions
- C. Cost reduction
- D. Faster development cycles

??? success "Answer"
    **Correct**: B

    Human-in-the-loop directly addresses the Accountability principle: humans remain responsible for AI system outcomes by reviewing and approving critical actions.

---

### Question 53-60

*(Questions 53-60 continue with similar cross-domain advanced scenarios covering all remaining topic combinations)*

### Question 53

**Domain**: 5, 6 | **Format**: Multiple Choice

A PR reviewer notices that an AI agent's auto-generated documentation uses only male pronouns. What is the correct response?

- A. Accept it since it's technically correct
- B. Flag it as a bias issue, fix the documentation to use gender-neutral language, and add inclusive language checks to the CI pipeline
- C. Ignore it for now and address in a future sprint
- D. Disable documentation generation

??? success "Answer"
    **Correct**: B

    This is a fairness/inclusiveness issue. Fix immediately, then implement automated checks to prevent recurrence.

---

### Question 54

**Domain**: 2, 3 | **Format**: Multiple Choice

An agent mode task is taking 15 minutes to complete a feature that should take 3 minutes. The agent is on iteration 12. What does this indicate?

- A. The model is too slow — use a faster model
- B. The agent is likely stuck in a fix-break cycle and should be interrupted for human guidance
- C. This is normal for complex tasks
- D. The agent needs more token budget

??? success "Answer"
    **Correct**: B

    12 iterations (well above the target of <5) and 15 minutes (above the <5 min target) indicates the agent is stuck. Human intervention to guide or restructure the approach is needed.

---

### Question 55

**Domain**: 4, 5 | **Format**: Multiple Choice

When should a CI/CD pipeline block a deployment based on AI agent analysis?

- A. When the agent suggests a deployment might fail
- B. When the agent detects confirmed security vulnerabilities at critical severity or policy violations in the code changes
- C. When the agent's confidence is below 50%
- D. Always — no deployment should proceed without agent approval

??? success "Answer"
    **Correct**: B

    AI should block deployments only for confirmed, objective findings (security vulnerabilities, policy violations) — not for subjective assessments or low confidence guesses.

---

### Question 56

**Domain**: 1, 2 | **Format**: Multiple Choice

Which is the correct execution flow for GitHub Copilot agent mode?

- A. Generate code → Present to user → Done
- B. Plan steps → Execute step with tools → Check result → Iterate if needed → Complete when all steps pass
- C. Ask user for each line of code → Write it → Ask again
- D. Generate all files simultaneously → Present result

??? success "Answer"
    **Correct**: B

    Agent mode follows the Plan-Execute-Iterate loop: plan multi-step approach, execute using tools, check results, iterate on failures, complete when successful.

---

### Question 57

**Domain**: 3, 5 | **Format**: Multiple Choice

A team measures that their AI-assisted code review catches 40% more bugs than manual review alone. However, developer satisfaction with the tool is only 55%. What is the likely issue and fix?

- A. The tool is working fine — metrics prove it
- B. The AI review is likely producing too many false positives or nitpicky comments, reducing signal-to-noise ratio. Tune severity thresholds and focus on high-impact findings
- C. Developers don't understand the tool — more training needed
- D. Remove the tool since satisfaction is low

??? success "Answer"
    **Correct**: B

    High bug detection + low satisfaction typically means noise — too many low-value comments drowning out important ones. Tuning severity and focusing on actionable, high-impact findings improves the ratio.

---

### Question 58

**Domain**: 2, 6 | **Format**: Multiple Choice

An MCP server provides access to a code search tool that indexes open source repositories. When should the agent's output from this tool be treated with extra caution?

- A. Never — open source code is always safe to use
- B. When the results may include code with restrictive licenses that could conflict with the project's licensing, or when code patterns might introduce security vulnerabilities
- C. Only when the code is in a language the developer doesn't know
- D. Only during production deployments

??? success "Answer"
    **Correct**: B

    Open source code carries licensing and security risks. Responsible AI (Domain 6) requires awareness of IP/licensing, and security (Domain 4) requires scanning external code for vulnerabilities.

---

### Question 59

**Domain**: 4, 6 | **Format**: Multiple Choice

What is the key difference between transparency and accountability in the context of AI agents?

- A. They are the same principle
- B. Transparency = explain how the AI works and what it does; Accountability = humans are responsible for the AI's outcomes and have authority to override
- C. Transparency = fast performance; Accountability = low cost
- D. Transparency = user interface; Accountability = backend code

??? success "Answer"
    **Correct**: B

    Transparency is about making AI behavior understandable (explainability). Accountability is about maintaining human responsibility and authority over AI systems.

---

### Question 60

**Domain**: 1, 2, 4 | **Format**: Scenario-Based

A startup is deploying its first AI agent system. They want the agent to help with: code generation, PR reviews, and basic DevOps tasks. They have one repository, 5 developers, and limited security infrastructure. What is the best starting architecture?

- A. Full multi-agent system with 10 specialized agents
- B. Single agent with GitHub Copilot agent mode, basic MCP servers for internal tools, supervised autonomy for all operations, and GitHub's built-in secret scanning enabled
- C. No agent — too risky for a startup
- D. Fully autonomous agent with no human oversight

??? success "Answer"
    **Correct**: B

    A startup's first deployment should be simple: single agent mode (matches their single repo, small team), supervised autonomy (safe while learning), basic MCP (internal tool access), and GitHub's built-in security features (low overhead).

    - **A**: Over-engineered for 5 developers and one repo.
    - **C**: Agents are safe with proper basic controls.
    - **D**: Full autonomy without experience is dangerous.
