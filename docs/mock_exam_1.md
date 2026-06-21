# Mock Exam 1

!!! info "Instructions"
    50 questions • 120 minutes • 70% to pass (35/50)
    Answer all questions. Timer starts automatically.

<div class="quiz" data-domain="Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which agent architecture pattern uses a central coordinator that delegates tasks to specialized sub-agents?</div>
<div class="quiz-option" data-correct="false">Single Agent</div>
<div class="quiz-option" data-correct="false">Multi-Agent (peer)</div>
<div class="quiz-option" data-correct="true">Orchestrator-Worker</div>
<div class="quiz-option" data-correct="false">Advisory</div>
<div class="quiz-explanation">The Orchestrator-Worker pattern has a central coordinator that decomposes complex tasks and delegates them to specialized worker agents. Single Agent has no coordination, Multi-Agent peers collaborate without a central coordinator. <a href="study_notes/#11-agent-architecture-patterns">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the primary difference between GitHub Copilot's agent mode and chat mode?</div>
<div class="quiz-option" data-correct="false">Agent mode is faster at generating code</div>
<div class="quiz-option" data-correct="true">Agent mode can autonomously execute multi-step tasks, create files, and run terminal commands</div>
<div class="quiz-option" data-correct="false">Agent mode works offline</div>
<div class="quiz-option" data-correct="false">Chat mode cannot generate code</div>
<div class="quiz-explanation">Agent mode's defining feature is autonomous multi-step execution — it plans, executes using tools (file creation, terminal, search), checks results, and iterates. Chat mode provides single responses without tool execution. <a href="study_notes/#21-github-copilot-agent-mode">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">In the Model Context Protocol (MCP), what are the four main components?</div>
<div class="quiz-option" data-correct="false">Client, Server, Database, Cache</div>
<div class="quiz-option" data-correct="true">Host, Client, Server, Transport</div>
<div class="quiz-option" data-correct="false">Agent, Tool, Resource, User</div>
<div class="quiz-option" data-correct="false">Input, Processing, Output, Storage</div>
<div class="quiz-explanation">MCP has four components: Host (application running the AI model, e.g., IDE), Client (maintains connections to servers), Server (exposes tools/resources/prompts), and Transport (communication layer — stdio or HTTP/SSE). <a href="study_notes/#22-model-context-protocol-mcp">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which tool category requires the highest level of user approval in agent systems?</div>
<div class="quiz-option" data-correct="false">Read operations</div>
<div class="quiz-option" data-correct="false">Write operations</div>
<div class="quiz-option" data-correct="true">Shell/terminal operations</div>
<div class="quiz-option" data-correct="false">Search operations</div>
<div class="quiz-explanation">Shell/terminal commands carry the highest risk because they can execute arbitrary code, install packages, delete files, or make network requests. The risk hierarchy is: Read (safe) → Write (review) → Shell (explicit approval). <a href="study_notes/#42-agent-permissions-and-boundaries">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What transport protocols does MCP support?</div>
<div class="quiz-option" data-correct="false">HTTP only</div>
<div class="quiz-option" data-correct="false">WebSocket and gRPC</div>
<div class="quiz-option" data-correct="true">stdio (local) and HTTP/SSE (remote)</div>
<div class="quiz-option" data-correct="false">TCP and UDP</div>
<div class="quiz-explanation">MCP supports two transport mechanisms: stdio for local process communication and HTTP/SSE (Server-Sent Events) for remote communication. Both use JSON-RPC 2.0 as the message format. <a href="study_notes/#22-model-context-protocol-mcp">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Responsible AI" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which of Microsoft's Responsible AI principles requires that AI systems explain their behavior and decisions?</div>
<div class="quiz-option" data-correct="false">Fairness</div>
<div class="quiz-option" data-correct="false">Accountability</div>
<div class="quiz-option" data-correct="true">Transparency</div>
<div class="quiz-option" data-correct="false">Reliability</div>
<div class="quiz-explanation">Transparency requires AI systems to be understandable — explaining decisions, acknowledging limitations, disclosing AI involvement, and indicating confidence levels. <a href="study_notes/#62-transparency-and-explainability">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Performance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the target task completion rate for a well-performing agent system?</div>
<div class="quiz-option" data-correct="false">Greater than 50%</div>
<div class="quiz-option" data-correct="false">Greater than 70%</div>
<div class="quiz-option" data-correct="true">Greater than 85%</div>
<div class="quiz-option" data-correct="false">Greater than 99%</div>
<div class="quiz-explanation">Target task completion rate is > 85%. A rate of 70-85% is a warning, and below 70% is critical. 99% is unrealistic for complex autonomous tasks. <a href="study_notes/#33-agent-task-completion-and-monitoring">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Collaboration" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What should NEVER be fully automated in a CI/CD pipeline without human approval?</div>
<div class="quiz-option" data-correct="false">Code formatting</div>
<div class="quiz-option" data-correct="false">Running unit tests</div>
<div class="quiz-option" data-correct="true">Production deployment</div>
<div class="quiz-option" data-correct="false">Generating changelogs</div>
<div class="quiz-explanation">Production deployments must always have human approval gates. They affect live users and are hard to reverse. Formatting, testing, and changelog generation are safe to automate. <a href="study_notes/#53-ai-agents-in-cicd-pipelines">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should secrets be provided to MCP servers?</div>
<div class="quiz-option" data-correct="false">Hardcoded in the server source code</div>
<div class="quiz-option" data-correct="true">Via environment variables referencing a secrets vault</div>
<div class="quiz-option" data-correct="false">Passed directly in tool call parameters</div>
<div class="quiz-option" data-correct="false">Stored in a public configuration file</div>
<div class="quiz-explanation">Secrets must be injected via environment variables that reference a vault (GitHub Secrets, Azure Key Vault). Never hardcode, never pass in plaintext parameters, never store in public files. <a href="study_notes/#45-managing-secrets-in-agent-workflows">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which autonomy level is appropriate for an agent performing code formatting?</div>
<div class="quiz-option" data-correct="true">Full autonomy (acts without human approval)</div>
<div class="quiz-option" data-correct="false">Supervised (requires human approval)</div>
<div class="quiz-option" data-correct="false">Advisory only (suggests, doesn't act)</div>
<div class="quiz-option" data-correct="false">No agent involvement allowed</div>
<div class="quiz-explanation">Code formatting is a low-risk, non-semantic change that can safely be done with full autonomy. Higher risk operations like deployments require supervised autonomy. <a href="study_notes/#14-agent-roles-within-development-workflows">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to build a custom tool that gives their AI agent access to their company's internal documentation wiki. They need to choose between building this as a Copilot Extension or an MCP server.</div>
<div class="quiz-stem">When should they choose an MCP server over a Copilot Extension?</div>
<div class="quiz-option" data-correct="false">When they want a custom UI in the IDE</div>
<div class="quiz-option" data-correct="true">When they need to expose structured tool capabilities (functions with defined inputs/outputs) that any MCP-compatible agent can use</div>
<div class="quiz-option" data-correct="false">When they only need text-based chat responses</div>
<div class="quiz-option" data-correct="false">When they want to replace Copilot entirely</div>
<div class="quiz-explanation">MCP servers are best when you need structured tools with defined schemas that can be discovered and invoked by any compatible client. Extensions are better for custom conversational experiences invoked via @mentions. <a href="study_notes/#22-model-context-protocol-mcp">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Responsible AI" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the correct inclusive alternative to "blacklist" in code?</div>
<div class="quiz-option" data-correct="false">Badlist</div>
<div class="quiz-option" data-correct="true">Denylist</div>
<div class="quiz-option" data-correct="false">Blocklist</div>
<div class="quiz-option" data-correct="false">Redlist</div>
<div class="quiz-explanation">The standard inclusive replacements are: whitelist → allowlist, blacklist → denylist, master → main, slave → replica. <a href="study_notes/#63-bias-and-fairness-in-agent-outputs">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Performance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the primary technique for reducing perceived latency in agent responses?</div>
<div class="quiz-option" data-correct="false">Using a larger model</div>
<div class="quiz-option" data-correct="true">Token streaming (sending output incrementally)</div>
<div class="quiz-option" data-correct="false">Disabling all tools</div>
<div class="quiz-option" data-correct="false">Reducing context to zero</div>
<div class="quiz-explanation">Token streaming sends partial output as it's generated, so users see results immediately rather than waiting for the complete response. This dramatically reduces perceived wait time. <a href="study_notes/#32-optimizing-agent-response-latency">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which of the following should trigger a security alert in an agent monitoring system? (Select all that apply)</div>
<div class="quiz-option" data-correct="false">Agent reads a source file in the allowed src/ directory</div>
<div class="quiz-option" data-correct="true">Agent attempts to access a file in the secrets/ directory</div>
<div class="quiz-option" data-correct="true">Agent attempts to run curl to an unknown external URL</div>
<div class="quiz-option" data-correct="false">Agent generates 100 lines of TypeScript code</div>
<div class="quiz-option" data-correct="true">Agent tries to modify .github/workflows/ files</div>
<div class="quiz-explanation">Security alerts should trigger for: accessing sensitive directories (secrets/), network requests to unknown URLs (data exfiltration risk), and modifying security-critical configurations (CI/CD workflows). Normal file reads and code generation are expected behavior. <a href="study_notes/#43-security-compliance-monitoring">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Collaboration" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer prompts Copilot agent mode with "add pagination." The agent's output is incomplete and doesn't match the project's existing patterns.</div>
<div class="quiz-stem">What is the best next step?</div>
<div class="quiz-option" data-correct="false">Accept the output and manually fix it</div>
<div class="quiz-option" data-correct="true">Provide more specific context: reference the existing pattern, specify the pagination approach, and point to example files</div>
<div class="quiz-option" data-correct="false">Switch to a different AI tool</div>
<div class="quiz-option" data-correct="false">Disable agent mode and write it manually</div>
<div class="quiz-explanation">Iterative refinement with specific context improves output. Referencing existing patterns (#file), specifying approach (cursor-based), and pointing to examples gives the agent the information it needs. The issue is prompt quality, not tool capability. <a href="study_notes/#54-agent-human-interaction-patterns">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What algorithm is used to determine valid task execution order when tasks have dependencies?</div>
<div class="quiz-option" data-correct="false">Binary search</div>
<div class="quiz-option" data-correct="true">Topological sort (Kahn's algorithm)</div>
<div class="quiz-option" data-correct="false">Bubble sort</div>
<div class="quiz-option" data-correct="false">Random shuffle</div>
<div class="quiz-explanation">Topological sort (specifically Kahn's algorithm) determines a valid execution order that respects all dependencies — ensuring no task runs before its prerequisites are complete. <a href="study_notes/#13-agent-communication-and-orchestration">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">In MCP, what is the difference between a "tool" and a "resource"?</div>
<div class="quiz-option" data-correct="false">Tools are free, resources cost money</div>
<div class="quiz-option" data-correct="true">Tools are actions the agent invokes; resources are data the agent reads</div>
<div class="quiz-option" data-correct="false">Tools run on the client; resources run on the server</div>
<div class="quiz-option" data-correct="false">They are synonyms</div>
<div class="quiz-explanation">Tools = functions/actions the agent can call (e.g., query_database, create_file). Resources = data sources the agent can read (e.g., file contents, API responses). Tools DO things; resources PROVIDE information. <a href="study_notes/#24-agent-tools-and-capabilities">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What are the 5 permission levels for AI agents from broadest to narrowest?</div>
<div class="quiz-option" data-correct="true">Organization → Repository → User → Session → Tool</div>
<div class="quiz-option" data-correct="false">Tool → Session → User → Repository → Organization</div>
<div class="quiz-option" data-correct="false">Global → Local → File → Line → Character</div>
<div class="quiz-option" data-correct="false">Admin → Developer → Viewer → Guest → Anonymous</div>
<div class="quiz-explanation">The 5 permission levels from broadest to narrowest: Organization (which repos agents can access), Repository (what operations are allowed), User (individual permissions), Session (per-invocation scope), Tool (per-tool approval). <a href="study_notes/#42-agent-permissions-and-boundaries">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Responsible AI" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An AI code review agent consistently provides fewer review comments on code written by senior developers compared to juniors, even when the code quality is objectively similar.</div>
<div class="quiz-stem">Which responsible AI principle is most likely violated?</div>
<div class="quiz-option" data-correct="true">Fairness</div>
<div class="quiz-option" data-correct="false">Transparency</div>
<div class="quiz-option" data-correct="false">Privacy</div>
<div class="quiz-option" data-correct="false">Reliability</div>
<div class="quiz-explanation">This is a fairness/bias issue — the agent treats users differently based on their identity (seniority) rather than objective code quality. Mitigation: implement blind review (remove author info from context). <a href="study_notes/#63-bias-and-fairness-in-agent-outputs">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What message format does MCP use for communication?</div>
<div class="quiz-option" data-correct="false">REST API calls</div>
<div class="quiz-option" data-correct="true">JSON-RPC 2.0</div>
<div class="quiz-option" data-correct="false">Protocol Buffers</div>
<div class="quiz-option" data-correct="false">XML-RPC</div>
<div class="quiz-explanation">MCP uses JSON-RPC 2.0 as its message format. This provides a standard way to make remote procedure calls with structured request/response objects over either stdio or HTTP/SSE transport. <a href="study_notes/#22-model-context-protocol-mcp">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Collaboration" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which code generation pattern involves writing documentation first, then asking the agent to implement?</div>
<div class="quiz-option" data-correct="false">Prompt-driven</div>
<div class="quiz-option" data-correct="false">Test-first</div>
<div class="quiz-option" data-correct="false">Pattern extension</div>
<div class="quiz-option" data-correct="true">Documentation-first</div>
<div class="quiz-explanation">Documentation-first: write the docs/specs first describing desired behavior, then ask the agent to generate code that matches. This produces well-documented, specification-aligned code. <a href="study_notes/#51-github-copilot-for-code-generation-and-review">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Performance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent's task completion rate has dropped from 90% to 65% over the past week. Code quality for completed tasks remains high.</div>
<div class="quiz-stem">What is the most appropriate first diagnostic step?</div>
<div class="quiz-option" data-correct="false">Switch to a different AI model immediately</div>
<div class="quiz-option" data-correct="true">Analyze failure logs to identify common error patterns and affected task types</div>
<div class="quiz-option" data-correct="false">Disable agent mode for all users</div>
<div class="quiz-option" data-correct="false">Increase the token budget by 10x</div>
<div class="quiz-explanation">Performance diagnosis starts with data: analyze logs to find patterns (which tasks fail, which tools error, what changed). Since quality is fine when tasks complete, the issue is likely task complexity or tool availability, not model capability. <a href="study_notes/#33-agent-task-completion-and-monitoring">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which communication pattern is most appropriate for an agent that needs to react when a PR is opened?</div>
<div class="quiz-option" data-correct="false">Request-Response</div>
<div class="quiz-option" data-correct="true">Event-Driven</div>
<div class="quiz-option" data-correct="false">Publish-Subscribe</div>
<div class="quiz-option" data-correct="false">Shared Context</div>
<div class="quiz-explanation">Event-driven communication is ideal when agents need to react to triggers like PRs being opened, tests failing, or files changing. The agent subscribes to events and acts when they occur. <a href="study_notes/#13-agent-communication-and-orchestration">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What data classification level applies to customer PII (personally identifiable information)?</div>
<div class="quiz-option" data-correct="false">Public</div>
<div class="quiz-option" data-correct="false">Internal</div>
<div class="quiz-option" data-correct="false">Confidential</div>
<div class="quiz-option" data-correct="true">Restricted (never exposed to agents)</div>
<div class="quiz-explanation">PII and financial data are classified as Restricted — the highest sensitivity level. They must never be exposed to AI agents. Even Confidential data requires special handling with encryption and access controls. <a href="study_notes/#44-data-governance-for-agent-interactions">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the correct context priority order for Copilot agent mode?</div>
<div class="quiz-option" data-correct="false">Project structure → Files → Request → References</div>
<div class="quiz-option" data-correct="true">Request → Explicit references → Active file → Relevant files → Structure</div>
<div class="quiz-option" data-correct="false">Active file → Request → Everything else</div>
<div class="quiz-option" data-correct="false">Random selection</div>
<div class="quiz-explanation">Context priority (highest to lowest): User's request → Explicit references (#file, #selection) → Active/open file → Semantically relevant files (found via search) → Project structure overview. <a href="study_notes/#26-agent-context-management">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Responsible AI" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which of the following are part of Microsoft's 6 Responsible AI principles? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Fairness</div>
<div class="quiz-option" data-correct="true">Transparency</div>
<div class="quiz-option" data-correct="false">Profitability</div>
<div class="quiz-option" data-correct="true">Inclusiveness</div>
<div class="quiz-option" data-correct="true">Accountability</div>
<div class="quiz-option" data-correct="false">Speed</div>
<div class="quiz-explanation">Microsoft's 6 Responsible AI principles are: Fairness, Reliability & Safety, Privacy & Security, Inclusiveness, Transparency, and Accountability. Profitability and Speed are not principles. <a href="study_notes/#61-ethical-guidelines-for-agent-behavior">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Collaboration" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">At which CI/CD stage is AI-assisted automatic code formatting most appropriate?</div>
<div class="quiz-option" data-correct="false">After production deployment</div>
<div class="quiz-option" data-correct="true">Pre-commit or early build stage</div>
<div class="quiz-option" data-correct="false">During manual code review</div>
<div class="quiz-option" data-correct="false">Only on weekends</div>
<div class="quiz-explanation">Auto-formatting is a safe, deterministic, non-semantic change. It should happen as early as possible (pre-commit or build) to ensure consistency before more complex pipeline steps. <a href="study_notes/#53-ai-agents-in-cicd-pipelines">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team wants to give their agent access to their internal Jira system for reading ticket details when implementing features.</div>
<div class="quiz-stem">What is the recommended implementation approach?</div>
<div class="quiz-option" data-correct="false">Copy-paste Jira content into every agent prompt</div>
<div class="quiz-option" data-correct="true">Build an MCP server that exposes read-only Jira tools with proper authentication</div>
<div class="quiz-option" data-correct="false">Grant the agent direct database access to Jira's backend</div>
<div class="quiz-option" data-correct="false">Take screenshots of tickets and attach as images</div>
<div class="quiz-explanation">An MCP server with read-only tools is the proper approach: it provides structured access, enforces permissions (read-only), uses proper authentication (API tokens via env vars), and follows the MCP standard for discoverability. <a href="study_notes/#22-model-context-protocol-mcp">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What defines the difference between an AI "agent" and an AI "assistant"?</div>
<div class="quiz-option" data-correct="false">Agents are more expensive</div>
<div class="quiz-option" data-correct="true">Agents can autonomously plan, use tools, and iterate — assistants respond to single prompts</div>
<div class="quiz-option" data-correct="false">Agents only work with code, assistants work with text</div>
<div class="quiz-option" data-correct="false">There is no difference</div>
<div class="quiz-explanation">The key distinction is autonomy: agents maintain state, make tool-use decisions, recover from errors, and iterate toward goals. Assistants respond to individual prompts without autonomous multi-step execution. <a href="study_notes/#11-agent-architecture-patterns">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A company discovers that their AI agent's output occasionally contains patterns that look like API keys (40-character Base64 strings).</div>
<div class="quiz-stem">What is the correct immediate response?</div>
<div class="quiz-option" data-correct="false">Ignore it — the completion rate is fine</div>
<div class="quiz-option" data-correct="true">Implement output filtering to detect and redact secret patterns, alert security team, and investigate the source</div>
<div class="quiz-option" data-correct="false">Remove all file read permissions from the agent</div>
<div class="quiz-option" data-correct="false">Add a disclaimer to the README</div>
<div class="quiz-explanation">Secret leakage is always critical regardless of other metrics. Immediate actions: filter outputs (prevent exposure), alert security (governance), investigate how secrets entered context (root cause). Don't remove all access — that kills utility. <a href="study_notes/#45-managing-secrets-in-agent-workflows">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Performance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the recommended p95 latency target for inline code suggestions?</div>
<div class="quiz-option" data-correct="true">Less than 200 milliseconds</div>
<div class="quiz-option" data-correct="false">Less than 2 seconds</div>
<div class="quiz-option" data-correct="false">Less than 10 seconds</div>
<div class="quiz-option" data-correct="false">Less than 30 seconds</div>
<div class="quiz-explanation">Inline suggestions must feel instantaneous: < 200ms. Chat responses target < 2s for first token (streaming). Agent mode steps target < 10s. Full agent tasks target < 5 minutes. <a href="study_notes/#32-optimizing-agent-response-latency">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Collaboration" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What type of test is an AI agent BEST suited to generate automatically?</div>
<div class="quiz-option" data-correct="false">Visual regression tests</div>
<div class="quiz-option" data-correct="true">Unit tests from function signatures and documentation</div>
<div class="quiz-option" data-correct="false">User acceptance tests</div>
<div class="quiz-option" data-correct="false">Physical hardware tests</div>
<div class="quiz-explanation">AI agents excel at generating unit tests from function signatures, docstrings, and type annotations — they can infer expected behavior, edge cases, and boundary conditions from these structured inputs. <a href="study_notes/#52-agent-assisted-debugging-and-testing">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Responsible AI" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What should happen when an AI agent generates output with low confidence?</div>
<div class="quiz-option" data-correct="false">Hide the output entirely</div>
<div class="quiz-option" data-correct="true">Present it with a confidence indicator and suggest human verification</div>
<div class="quiz-option" data-correct="false">Submit it automatically anyway</div>
<div class="quiz-option" data-correct="false">Generate a completely different response</div>
<div class="quiz-explanation">Transparency requires indicating confidence levels. Low-confidence output should be clearly marked and accompanied by a suggestion for human verification — not hidden or auto-submitted. <a href="study_notes/#62-transparency-and-explainability">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer is building a custom MCP server for their database. They need to define a tool that lets the agent query user data.</div>
<div class="quiz-stem">What is the most important security consideration for this tool definition?</div>
<div class="quiz-option" data-correct="false">Making the tool name short</div>
<div class="quiz-option" data-correct="true">Restricting the tool to read-only queries and implementing input validation to prevent SQL injection</div>
<div class="quiz-option" data-correct="false">Making the tool execute as fast as possible</div>
<div class="quiz-option" data-correct="false">Supporting all SQL commands</div>
<div class="quiz-explanation">Security is paramount: restrict to read-only (SELECT only), validate inputs to prevent SQL injection, and consider data classification — if the table contains PII, access should be denied or heavily restricted. <a href="study_notes/#41-access-controls-for-ai-agents">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A development team of 50 engineers needs to standardize AI agent usage across their organization. They need custom code review rules, internal API documentation access, and enforced coding standards.</div>
<div class="quiz-stem">Which approach best fits their needs?</div>
<div class="quiz-option" data-correct="false">Each developer configures independently</div>
<div class="quiz-option" data-correct="true">Build Copilot Extensions for custom rules, MCP servers for internal docs, and shared workspace config for standards</div>
<div class="quiz-option" data-correct="false">Use only default Copilot without customization</div>
<div class="quiz-option" data-correct="false">Build a completely custom AI system from scratch</div>
<div class="quiz-explanation">Enterprise standardization requires: Extensions (custom review behaviors), MCP servers (internal tool/doc access), and shared configuration (consistency). This leverages GitHub's ecosystem without over-engineering. <a href="study_notes/#25-building-custom-agent-extensions">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the primary security benefit of MCP's tool approval system?</div>
<div class="quiz-option" data-correct="false">It makes the agent faster</div>
<div class="quiz-option" data-correct="true">It ensures humans explicitly authorize each potentially risky operation before execution</div>
<div class="quiz-option" data-correct="false">It prevents the agent from reading any files</div>
<div class="quiz-option" data-correct="false">It encrypts all communication</div>
<div class="quiz-explanation">Tool approval implements human-in-the-loop control: the agent proposes an action, the user reviews it, and only then does it execute. This prevents unintended or risky operations from running automatically. <a href="study_notes/#42-agent-permissions-and-boundaries">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Collaboration" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the most effective prompting strategy when an agent's output doesn't match your project's patterns?</div>
<div class="quiz-option" data-correct="false">Repeat the same prompt louder</div>
<div class="quiz-option" data-correct="true">Reference specific example files using #file and describe the pattern you want followed</div>
<div class="quiz-option" data-correct="false">Switch to a different programming language</div>
<div class="quiz-option" data-correct="false">Write all the code manually</div>
<div class="quiz-explanation">Example-driven prompting: reference existing files that demonstrate the desired pattern. The agent can then understand and replicate the style, architecture, and conventions already in use. <a href="study_notes/#54-agent-human-interaction-patterns">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Performance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">An agent consistently takes 12+ iterations to complete tasks (target is less than 5). Quality is fine when complete. What is the most likely cause?</div>
<div class="quiz-option" data-correct="false">The model is too smart</div>
<div class="quiz-option" data-correct="true">Tasks are too complex and should be decomposed into smaller sub-tasks</div>
<div class="quiz-option" data-correct="false">The agent has too many tools available</div>
<div class="quiz-option" data-correct="false">The network is too slow</div>
<div class="quiz-explanation">High iteration count + good quality when complete = task complexity issue. The solution is better decomposition: break complex tasks into smaller, more focused sub-tasks that the agent can complete in fewer iterations. <a href="study_notes/#23-multi-step-agent-workflows">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Responsible AI" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which action best addresses the Accountability principle when deploying AI agents in production?</div>
<div class="quiz-option" data-correct="false">Removing all human involvement</div>
<div class="quiz-option" data-correct="true">Maintaining human oversight with the ability to review, override, and take responsibility for agent decisions</div>
<div class="quiz-option" data-correct="false">Making the agent explain every decision in detail</div>
<div class="quiz-option" data-correct="false">Running the agent in isolated containers</div>
<div class="quiz-explanation">Accountability means humans remain responsible for AI outcomes. This requires: oversight mechanisms, override capabilities, audit trails, and clear ownership of agent-assisted decisions. Transparency (explaining) is a different principle. <a href="study_notes/#65-monitoring-and-auditing-agent-decisions">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What happens when GitHub Copilot agent mode encounters a test failure after implementing code?</div>
<div class="quiz-option" data-correct="false">It stops and reports the error without attempting to fix it</div>
<div class="quiz-option" data-correct="true">It reads the error output, identifies the issue, and automatically attempts to fix the code</div>
<div class="quiz-option" data-correct="false">It reverts all changes and starts from scratch</div>
<div class="quiz-option" data-correct="false">It asks the user which line to change</div>
<div class="quiz-explanation">Agent mode's iterate capability: when tests fail, it reads the error output, analyzes the cause, makes corrections, and re-runs tests — repeating until successful or reaching its iteration limit. <a href="study_notes/#21-github-copilot-agent-mode">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">In which SDLC phase does AI agent task decomposition provide the most value?</div>
<div class="quiz-option" data-correct="true">Planning — breaking complex requirements into implementable tasks</div>
<div class="quiz-option" data-correct="false">Monitoring — analyzing production logs</div>
<div class="quiz-option" data-correct="false">Deployment — pushing to production</div>
<div class="quiz-option" data-correct="false">Testing — running test suites</div>
<div class="quiz-explanation">Task decomposition is most valuable in the Planning phase — breaking epics and complex requirements into well-scoped, implementable sub-tasks that agents can then execute effectively. <a href="study_notes/#12-sdlc-integration-points-for-ai-agents">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A healthcare company wants to use AI agents for development. Their codebase includes mock patient data for testing and real API endpoints for production.</div>
<div class="quiz-stem">What security configuration is most appropriate?</div>
<div class="quiz-option" data-correct="false">Standard agent mode with full workspace access</div>
<div class="quiz-option" data-correct="true">Agent mode with restricted write paths, explicit deny for patient data patterns, MCP tools limited to mock databases only, and audit logging</div>
<div class="quiz-option" data-correct="false">No AI assistance allowed in healthcare</div>
<div class="quiz-option" data-correct="false">Read-only access to everything</div>
<div class="quiz-explanation">Healthcare requires layered controls: restrict write access, deny PHI patterns, limit tools to test/mock data only, and enable full audit logging for compliance. AI can be safely used with proper boundaries. <a href="study_notes/#44-data-governance-for-agent-interactions">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which workflow design principle ensures that agent work isn't lost if a later step fails?</div>
<div class="quiz-option" data-correct="false">Decomposition</div>
<div class="quiz-option" data-correct="true">Checkpoints (saving progress at each step)</div>
<div class="quiz-option" data-correct="false">Validation</div>
<div class="quiz-option" data-correct="false">Error handling</div>
<div class="quiz-explanation">Checkpoints save intermediate progress so that if a step fails, the workflow can resume from the last successful point rather than starting over. Decomposition breaks tasks apart; validation verifies outputs; error handling manages failures. <a href="study_notes/#23-multi-step-agent-workflows">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Collaboration" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which human-agent interaction pattern is best for complex tasks that need iterative refinement?</div>
<div class="quiz-option" data-correct="false">Direct instruction</div>
<div class="quiz-option" data-correct="true">Iterative refinement — accept partial results, then provide targeted feedback</div>
<div class="quiz-option" data-correct="false">Example-driven</div>
<div class="quiz-option" data-correct="false">Constraint setting</div>
<div class="quiz-explanation">Iterative refinement: provide initial instructions, review the output, then give specific feedback like "good, but change X" or "keep this part, redo that part." This is ideal for complex tasks where requirements emerge during development. <a href="study_notes/#54-agent-human-interaction-patterns">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Performance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which combination of metrics best indicates a healthy agent system?</div>
<div class="quiz-option" data-correct="true">Completion rate > 85%, user acceptance > 75%, iterations < 5, error rate < 5%</div>
<div class="quiz-option" data-correct="false">Completion rate > 50%, any acceptance rate, iterations unlimited</div>
<div class="quiz-option" data-correct="false">Zero errors and instant responses</div>
<div class="quiz-option" data-correct="false">Only code quality score matters</div>
<div class="quiz-explanation">A healthy agent system balances multiple KPIs: high completion (>85%), good user acceptance (>75%), efficient iterations (<5), and low errors (<5%). No single metric tells the full story. <a href="study_notes/#33-agent-task-completion-and-monitoring">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Responsible AI" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What are the 5 types of bias that AI agents can introduce in code?</div>
<div class="quiz-option" data-correct="true">Training data, cultural, gender, accessibility, and programming language bias</div>
<div class="quiz-option" data-correct="false">Speed, memory, network, storage, and compute bias</div>
<div class="quiz-option" data-correct="false">Only gender bias applies to code</div>
<div class="quiz-option" data-correct="false">Bias doesn't exist in code generation</div>
<div class="quiz-explanation">AI agents can introduce: training data bias (outdated patterns), cultural bias (English-centric), gender bias (gendered language), accessibility bias (missing a11y), and language bias (preferring one programming language). <a href="study_notes/#63-bias-and-fairness-in-agent-outputs">📖 Study Guide</a></div>
</div>
</div>
