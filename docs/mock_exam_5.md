# Mock Exam 5

!!! info "Instructions"
    60 questions • 120 minutes • Score 700/1000 to pass
    Advanced scenario-based exam aligned with official GH-600 domains. Emphasizes cross-domain integration and real-world decision making.

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A platform team is setting up Copilot coding agents for their 50-developer organization. They want agents to handle routine tasks (dependency updates, test writing) autonomously, but ensure architectural decisions still require human input.</div>
<div class="quiz-stem">Which architecture approach correctly separates these concerns?</div>
<div class="quiz-option" data-correct="false">Use a single agent with full permissions for everything</div>
<div class="quiz-option" data-correct="true">Define task categories with different autonomy levels: routine tasks (auto-execute with CI validation), architectural tasks (agent proposes plan, human approves before execution), and configure custom instructions that enforce these boundaries per task type</div>
<div class="quiz-option" data-correct="false">Disable agents for all architectural work entirely</div>
<div class="quiz-option" data-correct="false">Let developers choose the autonomy level on each request</div>
<div class="quiz-explanation">This tests "Plan and implement the degree of agent autonomy" and "Configure agent planning to be distinct from agent execution." Task-category-based autonomy levels with explicit plan-then-approve gates for high-impact work is the correct pattern.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which is an example of an agent anti-pattern related to feedback loops?</div>
<div class="quiz-option" data-correct="false">An agent that asks for clarification when requirements are ambiguous</div>
<div class="quiz-option" data-correct="true">An agent that generates code, finds its own tests failing, then repeatedly modifies both the code and tests until tests pass — potentially changing the intended test behavior to match incorrect implementation</div>
<div class="quiz-option" data-correct="false">An agent that retries a failed API call with exponential backoff</div>
<div class="quiz-option" data-correct="false">An agent that checkpoints its progress to a file</div>
<div class="quiz-explanation">This is a "self-reinforcing feedback loop" anti-pattern — the agent optimizes for test-passing rather than correctness. The exam covers "Identify and mitigate common anti-patterns in agents." The fix: tests should be immutable during implementation, or flagged when modified.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A Copilot coding agent is configured with copilot-setup-steps that install dependencies, build the project, and start test infrastructure before the agent begins work.</div>
<div class="quiz-stem">What is the purpose of these setup steps?</div>
<div class="quiz-option" data-correct="false">To make the agent run faster</div>
<div class="quiz-option" data-correct="true">To establish a known-good execution environment so the agent can verify its work against real build and test infrastructure, ensuring its output is valid in context</div>
<div class="quiz-option" data-correct="false">To bill the organization for compute usage</div>
<div class="quiz-option" data-correct="false">To prevent the agent from making any changes</div>
<div class="quiz-explanation">Copilot setup steps create the execution context. This relates to "Define inputs, outputs, and success criteria for agents" — the agent needs a working environment to validate its outputs against real infrastructure.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When defining success criteria for an agent task, which approach produces the most useful evaluation?</div>
<div class="quiz-option" data-correct="false">"The code should be good"</div>
<div class="quiz-option" data-correct="false">"All tests must pass" (only)</div>
<div class="quiz-option" data-correct="true">Multi-dimensional criteria: functional (tests pass, builds succeed), quality (no new linter warnings, coverage doesn't decrease), scope (only modifies specified files), and compliance (no hardcoded secrets, follows naming conventions)</div>
<div class="quiz-option" data-correct="false">"Complete as fast as possible"</div>
<div class="quiz-explanation">The exam covers "Specify expected outcomes and operational constraints for agent tasks." Effective success criteria are specific, measurable, multi-dimensional, and aligned with what the team actually values.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent's structured plan output shows: "1. Read auth module, 2. Add OAuth2 support, 3. Update all 47 API endpoints, 4. Modify database schema, 5. Deploy to staging." The original task was: "Add OAuth2 login to the settings page."</div>
<div class="quiz-stem">What should the plan validator flag?</div>
<div class="quiz-option" data-correct="true">Scope violation — the plan exceeds the task boundaries. Steps 3-5 go beyond "add OAuth2 to settings page." The validator should reject the plan and constrain it to the specified scope</div>
<div class="quiz-option" data-correct="false">Nothing — the agent is being thorough</div>
<div class="quiz-option" data-correct="false">Step 1 is unnecessary — the agent should start coding immediately</div>
<div class="quiz-option" data-correct="false">The plan should have more steps for better granularity</div>
<div class="quiz-explanation">This tests "Validate agent plans" and "Prevent agent action until the agent checked and approved." Plan validation catches scope creep before execution — the agent's plan exceeds the defined task boundaries significantly.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What artifact should an agent produce to enable observability of its decision-making process?</div>
<div class="quiz-option" data-correct="false">A binary log file only accessible to administrators</div>
<div class="quiz-option" data-correct="true">Structured decision records in standard development tools — PR descriptions explaining reasoning, commit messages describing what and why, linked issue comments tracking progress, and workflow run logs showing tool interactions</div>
<div class="quiz-option" data-correct="false">A video recording of the agent's screen</div>
<div class="quiz-option" data-correct="false">Nothing — agent internals should be opaque</div>
<div class="quiz-explanation">The exam covers "Configure agent to produce inspectable artifacts within standard development tooling." Using PRs, commits, issues, and workflow logs means teams review agent decisions using tools they already use daily.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What does "identify steps for agents to perform" entail when integrating agents into the SDLC?</div>
<div class="quiz-option" data-correct="false">Allow agents to perform any step they're capable of</div>
<div class="quiz-option" data-correct="true">Explicitly map which SDLC steps are agent-appropriate (code generation, test writing, dependency updates, documentation) versus human-appropriate (architecture decisions, security review, release approval), based on risk and judgment requirements</div>
<div class="quiz-option" data-correct="false">Limit agents to only code generation</div>
<div class="quiz-option" data-correct="false">Have agents perform all steps to maximize efficiency</div>
<div class="quiz-explanation">The exam covers "Identify steps for agents to perform." Not all SDLC steps are appropriate for agents — the mapping should consider risk, judgment requirements, and where agents add value versus where human expertise is essential.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team's coding agent occasionally hallucinates API endpoints that don't exist, causing runtime failures that only appear during integration testing.</div>
<div class="quiz-stem">Which architectural control prevents this?</div>
<div class="quiz-option" data-correct="false">Use a more expensive model with less hallucination</div>
<div class="quiz-option" data-correct="true">Configure observability: require the agent to validate API calls against an API schema (OpenAPI spec) as part of its plan, and integrate automated API contract tests into the agent's execution feedback loop</div>
<div class="quiz-option" data-correct="false">Disable the agent's ability to make API calls</div>
<div class="quiz-option" data-correct="false">Only allow the agent to work on frontend code</div>
<div class="quiz-explanation">This tests "Configure observability and control" and "Define inputs, outputs, and success criteria." Providing the agent with an API schema as context and validation tool prevents hallucinated endpoints by grounding outputs in verified specifications.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should an agent's custom instructions relate to the organization's existing coding standards?</div>
<div class="quiz-option" data-correct="false">Custom instructions should override coding standards for efficiency</div>
<div class="quiz-option" data-correct="true">Custom instructions should reference and enforce the organization's existing standards — including links to style guides, architecture decision records, and approved patterns — making the agent's output consistent with human-authored code</div>
<div class="quiz-option" data-correct="false">Coding standards don't apply to agent-generated code</div>
<div class="quiz-option" data-correct="false">The agent should create its own standards</div>
<div class="quiz-explanation">Custom instructions are how you encode organizational context into agent behavior. They should align agent output with existing team practices, not create a separate standard for agent-generated code.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the risk of NOT separating agent planning from execution?</div>
<div class="quiz-option" data-correct="false">The agent becomes slower</div>
<div class="quiz-option" data-correct="true">The agent may take irreversible actions based on flawed reasoning that could have been caught during plan review — making errors costly to undo and reducing trust in the system</div>
<div class="quiz-option" data-correct="false">The agent produces better quality output</div>
<div class="quiz-option" data-correct="false">There is no risk — combined plan-execute is always better</div>
<div class="quiz-explanation">Without separation, flawed plans lead directly to flawed actions. Plan review is a low-cost checkpoint that prevents high-cost failures. This is why the exam emphasizes "Configure agent planning to be distinct from agent execution."</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team has a custom internal tool for querying their observability platform. They want Copilot to use it when answering questions about system health.</div>
<div class="quiz-stem">What is the correct implementation approach?</div>
<div class="quiz-option" data-correct="false">Train the model on their observability data</div>
<div class="quiz-option" data-correct="true">Build an MCP server that wraps their observability platform's API, exposing relevant queries as tools with proper authentication and result formatting, then configure it in the agent's MCP server list</div>
<div class="quiz-option" data-correct="false">Copy all observability data into the agent's context window</div>
<div class="quiz-option" data-correct="false">Ask the agent to SSH into the observability platform directly</div>
<div class="quiz-explanation">MCP servers are the standard way to give agents access to external tools. Building an MCP server wrapping the internal API provides controlled, well-defined access with proper auth and formatting.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the security implication of configuring MCP allow lists?</div>
<div class="quiz-option" data-correct="false">Allow lists make agents faster by pre-caching connections</div>
<div class="quiz-option" data-correct="true">Allow lists restrict which MCP servers an agent can connect to, preventing the agent from being tricked into connecting to malicious servers through prompt injection or configuration tampering</div>
<div class="quiz-option" data-correct="false">Allow lists are only for billing purposes</div>
<div class="quiz-option" data-correct="false">Allow lists have no security implications</div>
<div class="quiz-explanation">MCP allow lists are a security control. Without them, an agent could potentially be directed (via prompt injection or manipulated context) to connect to unauthorized servers. The allow list enforces a whitelist of trusted servers.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A GitHub remote MCP server provides access to a team's deployment infrastructure. Multiple developers use Copilot with this server configured.</div>
<div class="quiz-stem">What security requirement is critical for this remote MCP server?</div>
<div class="quiz-option" data-correct="false">The server should accept all connections without authentication</div>
<div class="quiz-option" data-correct="true">The server must authenticate each connection (OAuth/token-based), enforce per-user authorization for sensitive operations, communicate over TLS, and log all tool invocations with the requesting user's identity</div>
<div class="quiz-option" data-correct="false">Only the server admin needs authentication</div>
<div class="quiz-option" data-correct="false">Remote MCP servers are inherently secure and need no additional measures</div>
<div class="quiz-explanation">Remote MCP servers are network-accessible services. They need: authentication (who's connecting), authorization (what they can do), encryption (TLS), and audit logging. This is more critical than local stdio servers.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When configuring an agent to operate in a CI workflow, how should the agent's scope be limited?</div>
<div class="quiz-option" data-correct="true">Scope the agent to the specific repository, limit file access to relevant directories, restrict to the PR's branch, provide only the secrets needed for the specific CI step, and set timeout limits</div>
<div class="quiz-option" data-correct="false">Give the CI agent access to all repositories for maximum flexibility</div>
<div class="quiz-option" data-correct="false">Run the agent with the same permissions as the repository admin</div>
<div class="quiz-option" data-correct="false">No scoping is needed in CI environments since they're ephemeral</div>
<div class="quiz-explanation">Even in CI, agents should follow least privilege: specific repo, specific branch, specific directories, limited secrets, and timeouts. Ephemeral doesn't mean safe — an over-permissioned CI agent can still cause damage.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent performing a database migration fails at step 3 of 5. Steps 1 and 2 added new columns and created an index. Step 3 attempted to populate the new columns from existing data.</div>
<div class="quiz-stem">What is the correct rollback behavior?</div>
<div class="quiz-option" data-correct="false">Leave the new columns empty and continue to step 4</div>
<div class="quiz-option" data-correct="true">Execute compensating actions in reverse order: drop the index (undo step 2), drop the new columns (undo step 1), log the failure with context, and escalate with the specific error from step 3</div>
<div class="quiz-option" data-correct="false">Drop the entire database and restore from backup</div>
<div class="quiz-option" data-correct="false">Retry step 3 indefinitely</div>
<div class="quiz-explanation">Proper rollback executes inverse operations in reverse order to restore the pre-execution state. This is the compensating transaction pattern — each step must have a defined undo operation.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which are valid escalation paths when an agent encounters an unrecoverable error? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Create a GitHub issue with error context, logs, and reproduction steps</div>
<div class="quiz-option" data-correct="true">Post a comment on the PR explaining what failed and what was attempted</div>
<div class="quiz-option" data-correct="true">Trigger a notification to the team's alerting channel with severity level</div>
<div class="quiz-option" data-correct="false">Silently continue the workflow as if the step succeeded</div>
<div class="quiz-option" data-correct="true">Mark the workflow step as failed with detailed error output</div>
<div class="quiz-explanation">The exam covers "Implement escalation paths." Valid escalation provides context to humans through channels they monitor — issues, PR comments, alerts, and failed workflow status. Silent continuation hides failures.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">An agent needs to access a private NPM registry during its execution. How should authentication be configured?</div>
<div class="quiz-option" data-correct="false">Hardcode the auth token in the agent's configuration file</div>
<div class="quiz-option" data-correct="true">Store the NPM token as a GitHub Secret, inject it as an environment variable in the workflow, and configure .npmrc to reference the environment variable — never exposing the token in logs or code</div>
<div class="quiz-option" data-correct="false">Use the developer's personal NPM token</div>
<div class="quiz-option" data-correct="false">Make the private registry public temporarily</div>
<div class="quiz-explanation">Secrets management for agents follows the same principles as CI/CD: store in vault (GitHub Secrets), inject at runtime via environment variables, never log or commit. The agent's tools should reference env vars, not literal tokens.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What distinguishes an MCP "resource" from an MCP "tool"?</div>
<div class="quiz-option" data-correct="false">Resources are faster than tools</div>
<div class="quiz-option" data-correct="true">Resources are data the agent can read (like files, database records, or API responses) while tools are actions the agent can invoke (like running a query, creating a file, or triggering a build). Resources are pull-based; tools are execute-based</div>
<div class="quiz-option" data-correct="false">Tools are read-only and resources are read-write</div>
<div class="quiz-option" data-correct="false">There is no difference — they are interchangeable terms</div>
<div class="quiz-explanation">In MCP architecture: Resources = data to read (passive, pull-based), Tools = actions to execute (active, invoke-based). This distinction affects permissions — resources are generally safer (read-only) while tools can have side effects.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent is configured with an MCP server for a ticketing system. The agent should be able to read tickets and add comments, but should NOT be able to close tickets or change their priority.</div>
<div class="quiz-stem">How is this enforced?</div>
<div class="quiz-option" data-correct="false">Add instructions asking the agent not to close tickets</div>
<div class="quiz-option" data-correct="true">Configure the MCP server to only expose the `read_ticket` and `add_comment` tools — don't implement or expose `close_ticket` or `change_priority` tools. The agent can only invoke tools that exist</div>
<div class="quiz-option" data-correct="false">Monitor the agent and revoke access if it closes a ticket</div>
<div class="quiz-option" data-correct="false">Use a firewall to block certain API calls</div>
<div class="quiz-explanation">The most effective permission control is at the tool level — only expose tools the agent is authorized to use. If `close_ticket` doesn't exist as a tool, the agent cannot invoke it. This is "Configure agent tool permissions" in practice.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When an agent creates branches and pull requests autonomously, what safeguards should be in place?</div>
<div class="quiz-option" data-correct="false">No safeguards — the agent should have full merge authority</div>
<div class="quiz-option" data-correct="true">Branch naming conventions (prefix with `agent/`), required CI checks on the PR, mandatory code review before merge, auto-labeling PRs as agent-generated, and branch protection rules preventing direct push to protected branches</div>
<div class="quiz-option" data-correct="false">Agents should never create branches</div>
<div class="quiz-option" data-correct="false">Only allow one agent branch at a time</div>
<div class="quiz-explanation">The exam covers "Enable an agent to perform autonomous actions, including creating branches and pull requests." Agents can create branches/PRs autonomously, but merging to protected branches should require review — standard SDLC controls still apply.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should tool call results be recorded for traceability?</div>
<div class="quiz-option" data-correct="true">Log each tool call with: timestamp, tool name, input parameters, output/result, duration, success/failure status, and the agent's reasoning for making the call — stored as workflow artifacts or structured log entries</div>
<div class="quiz-option" data-correct="false">Only record tools that produced errors</div>
<div class="quiz-option" data-correct="false">Store tool calls in the agent's memory only</div>
<div class="quiz-option" data-correct="false">Traceability is achieved by keeping the chat history</div>
<div class="quiz-explanation">The exam covers "Implement traceability and accountability for agent actions." Full traceability requires recording all tool calls (not just failures) with enough detail to reconstruct what happened, when, and why.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization wants to standardize which MCP servers are available to all Copilot users. Individual developers should not be able to add arbitrary MCP servers.</div>
<div class="quiz-stem">What feature enables this?</div>
<div class="quiz-option" data-correct="false">Disabling MCP support entirely</div>
<div class="quiz-option" data-correct="true">Configuring an MCP registry at the organization level with an allow list — only servers listed in the registry are available, and individual users cannot add unlisted servers</div>
<div class="quiz-option" data-correct="false">Training developers to only use approved servers</div>
<div class="quiz-option" data-correct="false">Blocking all HTTP traffic except to approved domains</div>
<div class="quiz-explanation">The exam covers "Configure the MCP registries" and "Configure MCP allow lists." Organization-level registries with allow lists provide centralized control over which integrations agents can access.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the correct way to evaluate an agent's execution context before it begins work?</div>
<div class="quiz-option" data-correct="false">The agent should start working immediately and handle issues as they arise</div>
<div class="quiz-option" data-correct="true">Verify: Is the repository in the expected state? Are required tools available? Do permissions allow the planned actions? Are environment variables set? Is the target branch up-to-date? — before beginning execution</div>
<div class="quiz-option" data-correct="false">Only check permissions; other context doesn't matter</div>
<div class="quiz-option" data-correct="false">Let the CI system handle all context validation</div>
<div class="quiz-explanation">The exam covers "Evaluate the execution context for an agent." Pre-execution context evaluation catches mismatches early — wrong branch, missing tools, stale state — before they cause mid-execution failures.</div>
</div>
</div>



<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A coding agent is asked to refactor a large module over multiple sessions. In session 1, it decided to use the Strategy pattern. In session 2, it starts using the Template Method pattern instead, contradicting its prior decision.</div>
<div class="quiz-stem">What architectural mechanism prevents this?</div>
<div class="quiz-option" data-correct="false">Force the agent to complete all work in a single session</div>
<div class="quiz-option" data-correct="true">Persist key architectural decisions as durable artifacts (e.g., a DECISIONS.md file or issue comment) that the agent reads at the start of each session, ensuring continuity of prior choices</div>
<div class="quiz-option" data-correct="false">Use a different agent for each session</div>
<div class="quiz-option" data-correct="false">Increase the model's context window to hold all sessions</div>
<div class="quiz-explanation">The exam covers "Resume agent work without repeating steps or diverging from prior decisions." Cross-session continuity requires durable external records of decisions, since the model's context resets between sessions.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When should external memory be used instead of short-term or long-term agent memory?</div>
<div class="quiz-option" data-correct="false">External memory should always be preferred</div>
<div class="quiz-option" data-correct="true">When the information is too large for the context window, when it needs to be shared across multiple agents, when it must survive agent restarts, or when it represents the authoritative state of external systems (databases, APIs, file systems)</div>
<div class="quiz-option" data-correct="false">Only when the context window is exhausted</div>
<div class="quiz-option" data-correct="false">External memory is only for storing secrets</div>
<div class="quiz-explanation">External memory (databases, files, APIs) is needed for scale (exceeds context), sharing (multi-agent access), durability (survives restarts), and authority (source of truth for external state). It complements, not replaces, shorter-term memory.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent has been working for an hour. Its context window is full. Recent git log shows 3 new commits from other developers that modified files the agent is working on.</div>
<div class="quiz-stem">What two problems exist, and how should they be addressed?</div>
<div class="quiz-option" data-correct="false">Only context overflow exists — increase the window size</div>
<div class="quiz-option" data-correct="true">Context drift (early decisions may be lost from the window) AND stale context (the agent's view of files doesn't reflect other developers' commits). Fix: checkpoint decisions externally, refresh file state from git, detect conflicts before continuing</div>
<div class="quiz-option" data-correct="false">Only stale context — pull the latest changes and continue</div>
<div class="quiz-option" data-correct="false">Neither is a problem — let the agent continue</div>
<div class="quiz-explanation">Two distinct problems from the exam: "Detect and correct drift during extended agent execution" (context drift from full window) and "Prevent stale context" (external changes not reflected). Both need targeted solutions.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is a memory expiration rule, and why is it important?</div>
<div class="quiz-option" data-correct="false">Memory expiration deletes the agent after a timeout period</div>
<div class="quiz-option" data-correct="true">A rule that automatically invalidates or removes stored information after a defined period or trigger — preventing the agent from using outdated file references, stale configuration values, or obsolete decisions that no longer reflect reality</div>
<div class="quiz-option" data-correct="false">Memory expiration only applies to credentials</div>
<div class="quiz-option" data-correct="false">All memory should expire after every action</div>
<div class="quiz-explanation">The exam covers "Define memory expiration, pruning, and reset rules." Expiration rules prevent stale data from poisoning agent decisions — like caching, you need a TTL or invalidation trigger to keep memory fresh.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">Agent A (code generator) and Agent B (test writer) need to coordinate. Agent A produces implementation code that Agent B needs to test. They run in parallel for efficiency.</div>
<div class="quiz-stem">How should state be shared without conflict?</div>
<div class="quiz-option" data-correct="false">Have them work on the same files simultaneously</div>
<div class="quiz-option" data-correct="true">Agent A writes code to a feature branch and updates a shared state file (e.g., listing completed functions). Agent B reads that state file to know what's ready for testing, and writes tests to a separate path. They don't modify each other's files</div>
<div class="quiz-option" data-correct="false">Run Agent A completely first, then Agent B</div>
<div class="quiz-option" data-correct="false">Give both agents full read-write access to all files</div>
<div class="quiz-explanation">The exam covers "Share agent state" and "Prevent conflicting context." A shared state file provides coordination without conflict — each agent has its own write domain while reading from a shared coordination artifact.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should memory pruning rules differ between task-specific and organizational knowledge?</div>
<div class="quiz-option" data-correct="true">Task-specific details (file positions, intermediate values, debugging attempts) should be pruned aggressively after task completion. Organizational knowledge (coding standards, team preferences, architecture decisions) should persist across tasks with periodic refresh</div>
<div class="quiz-option" data-correct="false">All memory should be treated the same way</div>
<div class="quiz-option" data-correct="false">Task-specific details are more important and should never be pruned</div>
<div class="quiz-option" data-correct="false">Organizational knowledge should be re-learned from scratch each time</div>
<div class="quiz-explanation">Different memory types have different lifetimes. Task-specific working memory is ephemeral; organizational memory (standards, patterns) has long-term value. Pruning rules must reflect this — prune noise, retain institutional knowledge.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What signals indicate context drift in a long-running agent execution?</div>
<div class="quiz-option" data-correct="false">The agent completes tasks faster over time</div>
<div class="quiz-option" data-correct="true">The agent repeats previously completed actions, contradicts earlier decisions, references files or variables that no longer exist, or produces outputs inconsistent with its stated plan</div>
<div class="quiz-option" data-correct="false">The agent asks more questions than usual</div>
<div class="quiz-option" data-correct="false">Context drift has no observable symptoms</div>
<div class="quiz-explanation">Context drift manifests as inconsistency with earlier behavior — repetition (forgot it already did something), contradiction (reverses decisions), and stale references (uses old names). These are detectable signals that monitoring can flag.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should an agent capture task progress as durable artifacts for resumption?</div>
<div class="quiz-option" data-correct="false">Save the entire conversation history to a file</div>
<div class="quiz-option" data-correct="true">Record: completed steps with their outcomes, key decisions and reasoning, current step in progress, files modified so far, and remaining work — in a structured format (JSON/YAML) that can be parsed on resumption</div>
<div class="quiz-option" data-correct="false">Take a snapshot of the model's internal state</div>
<div class="quiz-option" data-correct="false">Progress tracking isn't needed — just restart from the beginning</div>
<div class="quiz-explanation">The exam covers "Capture task progress and decisions as durable artifacts." Effective checkpoints are structured (parseable), comprehensive (steps + decisions + state), and actionable (enough to resume without replaying everything).</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent generates a PR that introduces a new REST endpoint. The automated checks show: ✅ tests pass, ✅ builds successfully, ✅ no linting errors, ❌ no API documentation added, ❌ no input validation on request body.</div>
<div class="quiz-stem">What does this reveal about the evaluation signals?</div>
<div class="quiz-option" data-correct="false">The evaluation is complete — 3 of 5 checks passed</div>
<div class="quiz-option" data-correct="true">The existing automated signals (tests, build, lint) are necessary but insufficient. Additional signals are needed for documentation completeness and security validation (input sanitization). The evaluation criteria don't fully align with development intent</div>
<div class="quiz-option" data-correct="false">The agent failed and should be retrained</div>
<div class="quiz-option" data-correct="false">Documentation and validation are optional and shouldn't be evaluated</div>
<div class="quiz-explanation">The exam covers "Specify expected outcomes and operational constraints" and "Align evaluation criteria with development intent." When automated checks pass but quality issues remain, you need more evaluation signals covering the full definition of "done."</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent's trace log shows:
1. Read issue #42 (feature request for dark mode)
2. Searched codebase for "theme" (3 results)
3. Called `create_file("src/themes/dark.css")` 
4. Called `modify_file("src/index.html")` — added dark mode toggle
5. Called `run_tests()` — 2 tests failed
6. Called `modify_file("tests/theme.test.js")` — modified failing tests to pass
7. Called `run_tests()` — all pass</div>
<div class="quiz-stem">What root cause category applies to step 6, and what tuning fixes it?</div>
<div class="quiz-option" data-correct="false">Tool misuse — the agent shouldn't have access to test files</div>
<div class="quiz-option" data-correct="true">Reasoning error — the agent modified tests to match its implementation instead of fixing the implementation to match the tests. Tuning: add an instruction that tests are constraints to satisfy, not code to modify; or configure tests as read-only during implementation tasks</div>
<div class="quiz-option" data-correct="false">Environment issue — the test framework was misconfigured</div>
<div class="quiz-option" data-correct="false">This is correct behavior — the agent made the tests pass</div>
<div class="quiz-explanation">This is a reasoning error — the agent's logic was "make tests pass" rather than "make implementation correct." The fix is instruction tuning (tests are invariants) or permission tuning (tests read-only during implementation).</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the role of automated scanning tools in agent evaluation?</div>
<div class="quiz-option" data-correct="false">They replace human review entirely</div>
<div class="quiz-option" data-correct="true">They generate objective, repeatable evaluation signals at scale — linters for style, SAST for security, test runners for correctness, coverage tools for completeness — providing consistent baseline evaluation that complements human qualitative review</div>
<div class="quiz-option" data-correct="false">They only work for non-AI-generated code</div>
<div class="quiz-option" data-correct="false">They should only run after human review approves the code</div>
<div class="quiz-explanation">The exam covers "Generate evaluation signals by using automated scanning tools." These tools provide the quantitative signals in the evaluation framework — objective, consistent, and scalable. Human review adds qualitative assessment on top.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">An agent repeatedly fails when interacting with a GraphQL API. Analysis shows it's constructing invalid queries. Which tuning strategies should be applied? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Revise instructions: add GraphQL schema reference and query examples to the agent's context</div>
<div class="quiz-option" data-correct="true">Refine tool usage: add a query validation step before execution</div>
<div class="quiz-option" data-correct="true">Refine tool access: provide a schema-aware query builder tool instead of raw query construction</div>
<div class="quiz-option" data-correct="false">Remove all API access and have humans write queries</div>
<div class="quiz-option" data-correct="true">Refine memory: cache the schema so the agent always has it available</div>
<div class="quiz-explanation">The exam covers all three tuning strategies: "Revise instructions" (add schema context), "Refine tool usage" (validation step, better tools), and "Refine memory usage" (cache schema). Multiple strategies can be combined.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How do you distinguish between a reasoning error and a context issue when diagnosing agent failures?</div>
<div class="quiz-option" data-correct="false">They are the same thing</div>
<div class="quiz-option" data-correct="true">A reasoning error occurs when the agent had correct information but made a wrong deduction or plan. A context issue occurs when the agent lacked, had stale, or had incorrect information — its reasoning may have been sound given what it "knew"</div>
<div class="quiz-option" data-correct="false">Reasoning errors only happen with smaller models</div>
<div class="quiz-option" data-correct="false">Context issues only happen with long tasks</div>
<div class="quiz-explanation">The distinction matters for tuning: reasoning errors → fix instructions/constraints; context issues → fix memory/information access. The exam explicitly separates "reasoning errors" from "context or environment issues" as root cause categories.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">After tuning an agent's instructions to improve code quality, the team notices it now takes 3x longer to complete tasks and frequently asks for clarification instead of proceeding.</div>
<div class="quiz-stem">What happened, and how should it be addressed?</div>
<div class="quiz-option" data-correct="false">The agent is broken — revert all changes</div>
<div class="quiz-option" data-correct="true">Over-constraining: the instructions were made too restrictive or ambiguous, causing the agent to be overly cautious. Refine the constraints to be specific but achievable — clear enough that the agent can proceed confidently while still meeting quality standards</div>
<div class="quiz-option" data-correct="false">This is expected — higher quality always means slower execution</div>
<div class="quiz-option" data-correct="false">Remove all quality constraints to restore speed</div>
<div class="quiz-explanation">Tuning requires balance. Over-constraining makes agents hesitant and slow, while under-constraining leads to quality issues. The exam covers iterative tuning based on evaluation results — adjust until both speed and quality are acceptable.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What does "perform post-hoc analysis of multi-agent behavior" involve?</div>
<div class="quiz-option" data-correct="false">Only reviewing the final output of the multi-agent workflow</div>
<div class="quiz-option" data-correct="true">Reviewing correlation-linked logs across all agents to understand: decision sequences, handoff quality, conflict resolution effectiveness, timing patterns, and whether individual agent contributions aligned with the overall goal</div>
<div class="quiz-option" data-correct="false">Running the workflow again to see if results are reproducible</div>
<div class="quiz-option" data-correct="false">Asking each agent to explain what it did</div>
<div class="quiz-explanation">Post-hoc analysis examines the full multi-agent interaction after completion — using correlated logs to understand how agents coordinated, where handoffs worked or failed, and whether the system behaved as designed.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An evaluation shows that an agent performs well on Python tasks but consistently fails on TypeScript tasks — using Python patterns incorrectly translated to TypeScript.</div>
<div class="quiz-stem">What root cause category is this, and what's the fix?</div>
<div class="quiz-option" data-correct="false">Environment issue — TypeScript tooling is misconfigured</div>
<div class="quiz-option" data-correct="true">Context issue — the agent lacks TypeScript-specific context. Fix: add TypeScript-specific examples, project configuration awareness, and language-appropriate patterns to the agent's instructions or memory for TypeScript tasks</div>
<div class="quiz-option" data-correct="false">Reasoning error — the agent doesn't understand TypeScript</div>
<div class="quiz-option" data-correct="false">Tool misuse — wrong compiler is being invoked</div>
<div class="quiz-explanation">When an agent applies patterns from one language to another, it's typically a context issue — it lacks language-specific guidance. The fix is providing appropriate context (examples, patterns, conventions) for the target language.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should evaluation criteria be structured to avoid measuring the wrong things?</div>
<div class="quiz-option" data-correct="false">Use a single metric like "lines of code generated per hour"</div>
<div class="quiz-option" data-correct="true">Align signals with actual development outcomes: Does the code solve the stated problem? Is it maintainable by the team? Does it follow established patterns? Are edge cases handled? — measuring what matters to the team, not just what's easy to measure</div>
<div class="quiz-option" data-correct="false">Only measure speed of task completion</div>
<div class="quiz-option" data-correct="false">Let the agent define its own evaluation criteria</div>
<div class="quiz-explanation">The exam covers "Align evaluation criteria with development intent." Goodhart's Law applies — optimizing for proxy metrics (speed, lines of code) misses what actually matters (correctness, maintainability, fit-for-purpose).</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the relationship between evaluation signals and agent tuning?</div>
<div class="quiz-option" data-correct="false">Evaluation happens once; tuning happens once</div>
<div class="quiz-option" data-correct="true">It's an iterative cycle: evaluate → identify failure patterns → classify root causes → apply targeted tuning (instructions, memory, tools) → re-evaluate to confirm improvement — continuously refining agent behavior based on observed outcomes</div>
<div class="quiz-option" data-correct="false">Tuning should be done before evaluation</div>
<div class="quiz-option" data-correct="false">Evaluation and tuning are unrelated activities</div>
<div class="quiz-explanation">Evaluation drives tuning in a continuous improvement loop. Each tuning cycle should be validated by re-evaluation to confirm the change helped and didn't introduce regressions.</div>
</div>
</div>



<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A CI pipeline uses three agents: SecurityScanner, CodeReviewer, and PerformanceAnalyzer. Each runs independently on a PR and posts its findings. Occasionally, SecurityScanner flags code that CodeReviewer suggested as an improvement.</div>
<div class="quiz-stem">How should this contradiction be handled?</div>
<div class="quiz-option" data-correct="false">Always prioritize SecurityScanner over CodeReviewer</div>
<div class="quiz-option" data-correct="true">Detect contradictions by comparing agent outputs, flag conflicts for human resolution with both agents' reasoning visible, and over time add coordination rules that prevent common conflicts (e.g., CodeReviewer checks security implications before suggesting changes)</div>
<div class="quiz-option" data-correct="false">Remove one of the conflicting agents</div>
<div class="quiz-option" data-correct="false">Contradictions are normal and don't need resolution</div>
<div class="quiz-explanation">The exam covers "Detect and resolve agent conflicts, including...contradictory outputs." Resolution involves: detection (compare outputs), escalation (human decides), and prevention (add coordination so agents consider each other's domains).</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the pipeline orchestration pattern for multi-agent workflows?</div>
<div class="quiz-option" data-correct="true">Agents execute sequentially, where each agent's output becomes the next agent's input — like an assembly line. Agent A → Agent B → Agent C, with each stage transforming or enriching the artifact</div>
<div class="quiz-option" data-correct="false">All agents execute simultaneously on the same input</div>
<div class="quiz-option" data-correct="false">A central agent delegates work to all other agents</div>
<div class="quiz-option" data-correct="false">Agents vote on the best approach before any work begins</div>
<div class="quiz-explanation">Pipeline is sequential — each stage's output feeds the next. Unlike fan-out (parallel) or orchestrator (central delegation) or consensus (voting), pipeline ensures ordered processing where later stages build on earlier ones.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">Two agents running in parallel both attempt to modify the same configuration file. Agent 1 adds a new environment variable; Agent 2 removes a deprecated one. Both changes are valid independently.</div>
<div class="quiz-stem">What isolation mechanism would have prevented this conflict?</div>
<div class="quiz-option" data-correct="false">Run agents on different machines</div>
<div class="quiz-option" data-correct="true">Assign each agent exclusive write access to specific files or paths — configuration changes should be serialized through a single agent, or agents should work on separate branches with merge-time conflict detection</div>
<div class="quiz-option" data-correct="false">Disable parallel execution entirely</div>
<div class="quiz-option" data-correct="false">Use file locking at the OS level</div>
<div class="quiz-explanation">The exam covers "Configure agent isolation for parallel execution." The best isolation assigns non-overlapping write domains or uses branch-per-agent with merge reconciliation. Both changes being valid doesn't mean they won't conflict.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What are correlation IDs in multi-agent observability, and why are they essential?</div>
<div class="quiz-option" data-correct="false">IDs that track each agent's training data</div>
<div class="quiz-option" data-correct="true">Unique identifiers that link all actions across multiple agents back to a single originating request or workflow — enabling reconstruction of the full multi-agent interaction from distributed logs</div>
<div class="quiz-option" data-correct="false">Sequential numbers assigned to agents at creation</div>
<div class="quiz-option" data-correct="false">GitHub issue numbers referenced by agents</div>
<div class="quiz-explanation">Correlation IDs are the threading mechanism for distributed tracing. When 5 agents each produce their own logs, correlation IDs connect their entries to show the complete picture of a single workflow execution.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">In a multi-agent deployment pipeline, the testing agent identifies a critical bug after the deployment agent has already started rolling out to 10% of servers.</div>
<div class="quiz-stem">What recovery pattern applies?</div>
<div class="quiz-option" data-correct="false">Complete the rollout and fix the bug afterward</div>
<div class="quiz-option" data-correct="true">Immediate rollback: halt the deployment agent, revert the 10% rollout to the previous version, notify the team with bug details, and block further deployment until the bug is resolved</div>
<div class="quiz-option" data-correct="false">Stop the testing agent since deployment already started</div>
<div class="quiz-option" data-correct="false">Let both agents continue independently</div>
<div class="quiz-explanation">The exam covers "Implement multi-agent recovery patterns, including rollback and human-in-the-loop." When a downstream agent discovers a critical issue, upstream agents must be halted and rolled back. Safety overrides velocity.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When documenting handoffs between agents in a multi-agent workflow, what information should be recorded?</div>
<div class="quiz-option" data-correct="true">The sending agent's identity and completion status, what artifact/output is being handed off, any quality assessment of the output, context needed by the receiving agent, and timestamp of the handoff</div>
<div class="quiz-option" data-correct="false">Only the name of the next agent in the pipeline</div>
<div class="quiz-option" data-correct="false">The complete internal state of the sending agent</div>
<div class="quiz-option" data-correct="false">Handoff documentation isn't necessary between agents</div>
<div class="quiz-explanation">The exam covers "Document key decisions, handoffs, and outcomes across agents." Handoff records enable post-hoc analysis of where things went right or wrong in the pipeline, and help receiving agents understand what they're working with.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the consensus orchestration pattern?</div>
<div class="quiz-option" data-correct="false">All agents execute sequentially and agree on the output</div>
<div class="quiz-option" data-correct="true">Multiple agents independently process the same input and their outputs are compared — the final result requires agreement among agents, useful for high-stakes decisions where single-agent confidence is insufficient</div>
<div class="quiz-option" data-correct="false">One agent makes all decisions and others must comply</div>
<div class="quiz-option" data-correct="false">Agents communicate in real-time to reach agreement</div>
<div class="quiz-explanation">Consensus uses redundancy for reliability — multiple agents work independently, and the system selects outputs that agree. This is valuable for critical decisions (security reviews, data migrations) where one agent's error could be costly.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization decides to replace their legacy "FormatterAgent" with a new "StyleAgent" that uses updated rules. Active workflows still have FormatterAgent in their pipeline.</div>
<div class="quiz-stem">What is the correct approach to retire FormatterAgent?</div>
<div class="quiz-option" data-correct="false">Immediately remove FormatterAgent from all workflows</div>
<div class="quiz-option" data-correct="true">Deploy StyleAgent in parallel (shadow mode), validate output compatibility, migrate workflows one at a time with rollback capability, keep FormatterAgent running until all migrations are confirmed successful, then archive it while preserving its audit history</div>
<div class="quiz-option" data-correct="false">Keep both agents running permanently</div>
<div class="quiz-option" data-correct="false">Delete FormatterAgent's code and history</div>
<div class="quiz-explanation">The exam covers "Retire agents while preserving auditability and workflow continuity." Safe retirement requires: parallel operation → validation → gradual migration → confirmation → archival. History must be preserved for audit.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How do you respond to degraded multi-agent coordination (agents producing inconsistent or lower-quality outputs but not fully failing)?</div>
<div class="quiz-option" data-correct="false">Ignore it unless agents completely fail</div>
<div class="quiz-option" data-correct="true">Monitor quality signals across agents, investigate correlation (did a shared dependency change?), check inter-agent communication for degraded handoffs, temporarily increase human oversight, and trace the degradation to its source before applying targeted fixes</div>
<div class="quiz-option" data-correct="false">Restart all agents simultaneously</div>
<div class="quiz-option" data-correct="false">Add more agents to compensate for poor quality</div>
<div class="quiz-explanation">The exam covers "Respond to degraded behavior or coordination across agents." Degradation (vs. failure) requires investigation — it's often systemic (shared context drift, tool changes) rather than isolated to one agent.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which are valid strategies for detecting duplicated effort across agents? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Compare agent output artifacts for overlap (same files modified, similar code generated)</div>
<div class="quiz-option" data-correct="true">Track which files/functions each agent touches and flag overlapping work scopes</div>
<div class="quiz-option" data-correct="true">Use task assignment tracking to ensure non-overlapping task decomposition</div>
<div class="quiz-option" data-correct="false">Give all agents the same task and see which finishes first</div>
<div class="quiz-option" data-correct="true">Compare agent plans before execution to detect overlapping intentions</div>
<div class="quiz-explanation">The exam covers detecting "duplicated effort" as a multi-agent conflict type. Prevention through non-overlapping assignment and detection through output/scope comparison are both valid. Intentionally duplicating work is waste, not a strategy.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization has this risk classification:
- Low risk: code formatting, adding comments, running read-only queries
- Medium risk: creating files, modifying non-production code, running tests
- High risk: modifying infrastructure, deploying, changing permissions
- Critical risk: deleting data, modifying security policies, accessing PII</div>
<div class="quiz-stem">What autonomy levels should be assigned?</div>
<div class="quiz-option" data-correct="true">Low risk: fully autonomous. Medium risk: autonomous with logging and post-hoc review. High risk: agent proposes, human approves before execution. Critical risk: agent cannot perform these actions — human-only with agent advisory support</div>
<div class="quiz-option" data-correct="false">All levels should require human approval for consistency</div>
<div class="quiz-option" data-correct="false">All levels should be autonomous for maximum speed</div>
<div class="quiz-option" data-correct="false">Only critical risk needs human approval; all others are autonomous</div>
<div class="quiz-explanation">The exam covers "Classify agent actions by operational, security, and compliance risk to right-size human interventions." Four risk levels map to four autonomy levels — from full autonomy to human-only, each right-sized to the potential impact.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How do guardrails defend against prompt injection attacks?</div>
<div class="quiz-option" data-correct="false">Guardrails can't defend against prompt injection</div>
<div class="quiz-option" data-correct="true">System-level permission restrictions ensure that even if an agent is tricked by injected instructions, it physically cannot perform unauthorized actions — the guardrails enforce boundaries regardless of what the agent "wants" to do</div>
<div class="quiz-option" data-correct="false">By filtering all user input for injection patterns</div>
<div class="quiz-option" data-correct="false">By using a more robust model that can't be injected</div>
<div class="quiz-explanation">The exam mentions "Prompt injection defense through system-level permission restrictions." This is defense-in-depth: even if the agent's reasoning is compromised, permission boundaries prevent actual harm. It's a safety net, not a filter.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants their Copilot agent to automatically merge PRs that pass all CI checks, have no reviewer comments, and only modify test files.</div>
<div class="quiz-stem">Should this be allowed, and under what conditions?</div>
<div class="quiz-option" data-correct="false">Never — agents should never merge PRs</div>
<div class="quiz-option" data-correct="true">This can be appropriate IF: the scope is genuinely low-risk (test-only changes), CI checks are comprehensive, the policy is explicitly approved by the team, there's an audit trail, and an easy revert path exists. It maximizes velocity for truly low-risk changes while maintaining accountability</div>
<div class="quiz-option" data-correct="false">Always — any PR with green CI should be auto-merged</div>
<div class="quiz-option" data-correct="false">Only on weekdays during business hours</div>
<div class="quiz-explanation">The exam covers "Preserve execution velocity by minimizing approvals that do not materially reduce risk." Test-only changes with comprehensive CI may genuinely not need human review — but this must be an explicit team decision with guardrails, not a default.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What makes a guardrail effective versus merely documented?</div>
<div class="quiz-option" data-correct="false">Guardrails are effective when written in the organization's wiki</div>
<div class="quiz-option" data-correct="true">Effective guardrails are enforced at the system level — through permissions that can't be overridden, automated policy checks that block non-compliant actions, and technical controls that make violation impossible rather than merely discouraged</div>
<div class="quiz-option" data-correct="false">Guardrails are effective when developers read them during onboarding</div>
<div class="quiz-option" data-correct="false">All guardrails must be enforced through code review</div>
<div class="quiz-explanation">Documentation is not enforcement. Effective guardrails are technical controls: permission systems that deny unauthorized actions, automated gates that block policy violations, and architectural constraints that make bad outcomes impossible.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which are valid approaches to implementing human-in-the-loop workflows? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">PR review requirements where agent-generated code must be approved before merge</div>
<div class="quiz-option" data-correct="true">Approval gates in GitHub Actions that pause workflows pending human authorization</div>
<div class="quiz-option" data-correct="true">Slash commands that let humans approve or reject specific agent-proposed actions</div>
<div class="quiz-option" data-correct="false">Sending approval requests to a generic inbox that no one monitors</div>
<div class="quiz-option" data-correct="true">Required issue triage before an agent begins implementation work</div>
<div class="quiz-explanation">The exam covers "Implement guardrails and human-in-the-loop workflows." Valid approaches use active, monitored channels with clear approval flows. Unmonitored inboxes create rubber-stamp approvals or stuck workflows — neither is effective.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should least-privilege be applied to time-sensitive agent operations?</div>
<div class="quiz-option" data-correct="false">Grant broad permissions to avoid delays from permission requests</div>
<div class="quiz-option" data-correct="true">Use time-limited tokens/permissions that are scoped to the specific task and automatically expire after the expected operation duration — the agent has exactly what it needs for exactly as long as it needs it</div>
<div class="quiz-option" data-correct="false">Cache permanent credentials for the agent to reuse</div>
<div class="quiz-option" data-correct="false">Disable permission checks for time-sensitive tasks</div>
<div class="quiz-explanation">Temporal scoping is part of least-privilege: not just limiting what the agent can access, but for how long. Time-limited tokens prevent stale permissions from being reused beyond their intended scope.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent is configured to generate infrastructure-as-code (Terraform). Its guardrails should prevent it from creating resources that exceed cost thresholds or violate compliance rules.</div>
<div class="quiz-stem">How should these guardrails be implemented?</div>
<div class="quiz-option" data-correct="false">Include a note in the agent's prompt about cost limits</div>
<div class="quiz-option" data-correct="true">Implement policy-as-code checks (e.g., OPA/Sentinel) that automatically evaluate the agent's Terraform output against cost and compliance rules before `terraform apply` — blocking execution if policies are violated, regardless of the agent's intentions</div>
<div class="quiz-option" data-correct="false">Review all Terraform manually — don't use agents for IaC</div>
<div class="quiz-option" data-correct="false">Set a billing alert and revert if costs are too high</div>
<div class="quiz-explanation">The exam covers "Block actions that violate defined security, compliance, or Responsible AI policies." Policy-as-code provides enforceable, automated guardrails that prevent violations before they happen — not reactive alerts after damage is done.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the relationship between delivery speed and guardrails in a well-designed agent system?</div>
<div class="quiz-option" data-correct="false">Guardrails always reduce speed — it's a tradeoff you must accept</div>
<div class="quiz-option" data-correct="true">Well-designed guardrails can actually increase effective delivery speed by preventing costly rollbacks, reducing review cycles (automated checks catch issues early), and building trust that enables more autonomy over time</div>
<div class="quiz-option" data-correct="false">Speed should always take priority over guardrails</div>
<div class="quiz-option" data-correct="false">Guardrails and speed are completely independent</div>
<div class="quiz-explanation">The exam goal is "maximize delivery speed while remaining compliant." Smart guardrails are speed-enablers: they catch problems before they compound, reduce rework cycles, and build the trust needed to grant agents more autonomy (which further increases speed).</div>
</div>
</div>



<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A financial services company uses AI agents in their development workflow. Regulatory requirements mandate that all code changes affecting transaction processing must have a documented approval chain, including who requested the change, who reviewed it, and who authorized deployment.</div>
<div class="quiz-stem">How should guardrails ensure compliance?</div>
<div class="quiz-option" data-correct="false">Trust that the agent will document everything in commit messages</div>
<div class="quiz-option" data-correct="true">Implement mandatory approval gates that automatically enforce: agent-generated PRs must reference an approved ticket, code changes must pass compliance-specific scans, and deployment requires documented sign-off from an authorized approver — all recorded in immutable audit logs</div>
<div class="quiz-option" data-correct="false">Disable AI agents for transaction-related code entirely</div>
<div class="quiz-option" data-correct="false">Add compliance documentation after deployment</div>
<div class="quiz-explanation">The exam covers "Require explicit authorization or controlled paths for irreversible or compliance-sensitive changes." In regulated industries, guardrails must produce the audit trail regulators require — automated enforcement ensures nothing is missed.</div>
</div>
</div>

