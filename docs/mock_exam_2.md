# Mock Exam 2 — GH-600 Agentic AI Developer

**Time limit:** 120 minutes | **Questions:** 60 | **Passing score:** 70% (42/60)

Click an answer to submit. You'll see immediate feedback with explanations.

---

<!-- DOMAIN 1: Prepare agent architecture and SDLC processes (Questions 1-10) -->

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">1. A team is designing an AI agent that will operate within their GitHub-based SDLC. Which of the following BEST describes the role of "structured plan output" in this context?</p>
<div class="quiz-options">
<div class="quiz-option">A. A compiled binary that the agent produces as its final deliverable</div>
<div class="quiz-option" data-correct="true">B. A machine-readable and human-reviewable description of the agent's intended actions, produced before execution begins</div>
<div class="quiz-option">C. A Gantt chart showing project timelines for the development team</div>
<div class="quiz-option">D. The agent's internal neural network architecture diagram</div>
</div>
<div class="quiz-explanation">The correct answer is B. Structured plan output is the agent's proposed set of actions, formatted in a way that both machines can validate (schema compliance) and humans can review (readability). It bridges planning and execution by making intentions explicit. A describes a build artifact. C is project management tooling. D is about model internals, not plan output.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">2. Which of the following is the MOST significant risk of not defining clear success criteria for an AI agent before deployment?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent will use too many API tokens</div>
<div class="quiz-option">B. The agent will generate output in the wrong programming language</div>
<div class="quiz-option" data-correct="true">C. There is no objective way to evaluate whether the agent is performing its intended function or causing harm</div>
<div class="quiz-option">D. The agent will refuse to execute any tasks</div>
</div>
<div class="quiz-explanation">The correct answer is C. Without defined success criteria, there's no objective baseline to measure agent behavior against. You can't determine if the agent is helping or harming, performing well or poorly. This makes evaluation, tuning, and accountability impossible. A and B are specific technical issues, not the fundamental risk. D doesn't follow from missing criteria.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<div class="quiz-scenario">A startup deploys an AI coding agent with semi-autonomous permissions. The agent can create PRs and push to feature branches. After three weeks of successful operation, the team decides to give the agent permission to merge its own PRs if CI passes, transitioning toward fully autonomous operation.</div>
<p class="quiz-stem">3. What principle of graduated autonomy does this scenario demonstrate?</p>
<div class="quiz-options">
<div class="quiz-option">A. Agents should always start with maximum permissions to avoid reconfiguration</div>
<div class="quiz-option" data-correct="true">B. Trust is built incrementally—agents earn expanded autonomy through demonstrated reliable behavior over time</div>
<div class="quiz-option">C. All autonomy transitions should happen simultaneously across all agents</div>
<div class="quiz-option">D. Fully autonomous operation eliminates the need for monitoring</div>
</div>
<div class="quiz-explanation">The correct answer is B. Graduated autonomy is a trust-building process where agents earn expanded permissions based on demonstrated track record. The team observed three weeks of reliable behavior before expanding autonomy. A skips the trust-building phase. C ignores that different agents may have different maturity levels. D is dangerous—monitoring remains essential even for autonomous agents.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">4. Select ALL that apply: Which of the following are anti-patterns in agentic AI SDLC integration?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. An agent that can modify its own configuration files to expand its capabilities</div>
<div class="quiz-option" data-correct="true">B. An agent that bypasses code review by pushing directly to protected branches</div>
<div class="quiz-option">C. An agent that creates detailed decision logs for each action it takes</div>
<div class="quiz-option" data-correct="true">D. An agent that operates without any rate limiting or circuit-breaking mechanisms</div>
<div class="quiz-option">E. An agent that requires human approval for destructive operations</div>
</div>
<div class="quiz-explanation">A, B, and D are anti-patterns. Self-modifying configuration (A) allows uncontrolled capability expansion. Bypassing code review (B) removes a critical safety gate. Operating without rate limits or circuit breakers (D) risks runaway behavior. C is a best practice for observability. E is a best practice for safety.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">5. What is the relationship between agent observability and CI/CD integration?</p>
<div class="quiz-options">
<div class="quiz-option">A. They are unrelated concerns that should be managed by different teams</div>
<div class="quiz-option">B. CI/CD replaces the need for observability because pipeline logs are sufficient</div>
<div class="quiz-option" data-correct="true">C. Agent observability artifacts (decision logs, diffs, plans) should be stored as CI/CD workflow artifacts, making them accessible for review and audit within the existing pipeline infrastructure</div>
<div class="quiz-option">D. Observability should be disabled during CI/CD runs to improve performance</div>
</div>
<div class="quiz-explanation">The correct answer is C. Integrating agent observability with CI/CD infrastructure leverages existing artifact storage, access controls, and review workflows. Decision logs and plans become first-class pipeline artifacts alongside test results and coverage reports. A creates silos. B conflates pipeline logs with agent-specific observability. D sacrifices visibility for marginal performance gains.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">6. When defining agent outputs, why is it important to specify output format constraints?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. To enable automated validation of the agent's output and ensure downstream systems can consume it reliably</div>
<div class="quiz-option">B. To make the output look visually appealing in a terminal</div>
<div class="quiz-option">C. To prevent the agent from producing any output that wasn't explicitly predicted</div>
<div class="quiz-option">D. To reduce the agent's inference time by constraining token generation</div>
</div>
<div class="quiz-explanation">The correct answer is A. Output format constraints (schemas, templates) enable automated validation—downstream systems, CI checks, and review tools can programmatically verify that agent output conforms to expected structure. B is about aesthetics, not reliability. C is too restrictive—agents need flexibility within defined schemas. D conflates output format with model performance optimization.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">7. In the planning phase of an agentic workflow, what should happen if the agent's generated plan fails validation?</p>
<div class="quiz-options">
<div class="quiz-option">A. Execute the plan anyway and fix issues afterward</div>
<div class="quiz-option">B. Immediately terminate the agent session permanently</div>
<div class="quiz-option" data-correct="true">C. Return to the planning step with feedback about the validation failure, allowing the agent to revise its plan</div>
<div class="quiz-option">D. Escalate to a different AI model for plan generation</div>
</div>
<div class="quiz-explanation">The correct answer is C. When plan validation fails, the agent should receive feedback about what failed and regenerate the plan—this is an iterative refinement loop within the planning phase. A defeats the purpose of validation. B is disproportionate for a plan revision need. D unnecessarily introduces model switching when the current agent may simply need better guidance.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">8. Which agent architecture pattern BEST supports incremental rollout of agent capabilities to a development team?</p>
<div class="quiz-options">
<div class="quiz-option">A. Deploy all capabilities simultaneously and let users discover them</div>
<div class="quiz-option">B. Build the agent as a monolithic system with no modular capabilities</div>
<div class="quiz-option" data-correct="true">C. Design the agent with modular capabilities that can be individually enabled, monitored, and expanded based on team readiness</div>
<div class="quiz-option">D. Restrict the agent to a single capability and never expand it</div>
</div>
<div class="quiz-explanation">The correct answer is C. Modular capability design enables incremental rollout—teams can enable one capability at a time, monitor its performance, and expand when ready. This aligns with graduated autonomy at the capability level. A risks overwhelming teams. B makes it impossible to selectively enable features. D prevents growth and limits the agent's value over time.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<div class="quiz-scenario">A CI/CD pipeline includes an AI agent step that generates release notes from commit messages. The agent occasionally halluccinates features that don't exist in the codebase, leading to incorrect documentation being published.</div>
<p class="quiz-stem">9. What architectural change would BEST mitigate this issue?</p>
<div class="quiz-options">
<div class="quiz-option">A. Remove the agent from the pipeline entirely</div>
<div class="quiz-option" data-correct="true">B. Add a validation step that cross-references the agent's release notes against actual commits and diffs before publishing</div>
<div class="quiz-option">C. Increase the agent's context window to include more commit history</div>
<div class="quiz-option">D. Publish release notes without review to maintain pipeline speed</div>
</div>
<div class="quiz-explanation">The correct answer is B. A validation step that verifies agent claims against actual code changes is the appropriate architectural safeguard. This catches hallucinations before they reach users. A is too extreme if the agent is otherwise valuable. C may help but doesn't guarantee accuracy. D prioritizes speed over correctness, worsening the problem.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">10. What is the role of a "decision log" in agent observability?</p>
<div class="quiz-options">
<div class="quiz-option">A. It records which team members approved the agent's deployment</div>
<div class="quiz-option">B. It stores the agent's API authentication credentials</div>
<div class="quiz-option" data-correct="true">C. It captures the agent's reasoning process, including what options were considered, what was selected, and why</div>
<div class="quiz-option">D. It tracks the agent's cloud computing resource usage</div>
</div>
<div class="quiz-explanation">The correct answer is C. A decision log records the agent's decision-making process: what alternatives were evaluated, which one was chosen, and the rationale. This enables debugging, accountability, and continuous improvement. A describes deployment approvals (different from runtime decisions). B is a security concern. D is resource monitoring, not decision transparency.</div>
</div>
</div>

<!-- DOMAIN 2: Implement tool use and environment interaction (Questions 11-24) -->

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">11. When adding an MCP server to a GitHub Copilot workspace configuration, which file is typically used to declare the server?</p>
<div class="quiz-options">
<div class="quiz-option">A. package.json</div>
<div class="quiz-option">B. .gitignore</div>
<div class="quiz-option" data-correct="true">C. The MCP configuration file (e.g., .vscode/mcp.json or the workspace settings)</div>
<div class="quiz-option">D. README.md</div>
</div>
<div class="quiz-explanation">The correct answer is C. MCP servers are declared in dedicated configuration files such as .vscode/mcp.json or workspace settings that specify server connection details, available tools, and allow lists. A is for Node.js dependencies. B is for Git ignore rules. D is for documentation. The MCP configuration is purpose-built for declaring tool servers.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">12. What is the PRIMARY advantage of using a tool allow list over granting an agent unrestricted tool access?</p>
<div class="quiz-options">
<div class="quiz-option">A. It improves the agent's response speed</div>
<div class="quiz-option">B. It reduces the agent's memory consumption</div>
<div class="quiz-option" data-correct="true">C. It explicitly defines the boundaries of what the agent can do, preventing unintended or dangerous operations</div>
<div class="quiz-option">D. It allows the agent to discover new tools automatically</div>
</div>
<div class="quiz-explanation">The correct answer is C. An allow list creates an explicit boundary—only operations on the list are permitted. This prevents the agent from executing operations that weren't anticipated or approved, even if the underlying credentials would permit them. A and B are implementation details, not primary benefits. D describes the opposite of what an allow list does (it restricts, not enables discovery).</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<div class="quiz-scenario">A GitHub Copilot agent in agent mode is configured with access to a file system tool, a terminal tool, and a web search tool. A user asks the agent to "fix the bug in auth.ts." The agent reads the file, identifies the issue, edits the file, then runs the test suite to verify the fix.</div>
<p class="quiz-stem">13. Which sequence of tool usage does this scenario demonstrate?</p>
<div class="quiz-options">
<div class="quiz-option">A. Web search → file edit → terminal (incorrect tool selection)</div>
<div class="quiz-option" data-correct="true">B. File read → file edit → terminal command (appropriate multi-tool coordination for the task)</div>
<div class="quiz-option">C. Terminal → terminal → terminal (single tool repeated)</div>
<div class="quiz-option">D. File edit → file read → web search (reversed and irrelevant tool usage)</div>
</div>
<div class="quiz-explanation">The correct answer is B. The agent correctly used file read to understand the problem, file edit to fix it, and terminal to verify with tests—a logical progression for bug fixing. A incorrectly includes web search for a local bug. C only uses one tool type. D has the read/write order reversed and adds an irrelevant web search step.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">14. What is the role of a Copilot Extension in the GitHub ecosystem?</p>
<div class="quiz-options">
<div class="quiz-option">A. A browser plugin that changes the GitHub UI color scheme</div>
<div class="quiz-option" data-correct="true">B. A custom integration that extends GitHub Copilot's capabilities by connecting it to external services, APIs, or specialized tools</div>
<div class="quiz-option">C. A hardware extension that accelerates model inference</div>
<div class="quiz-option">D. A Git hook that runs before every commit</div>
</div>
<div class="quiz-explanation">The correct answer is B. Copilot Extensions are custom integrations that add new capabilities to GitHub Copilot by connecting it to external services, proprietary APIs, or domain-specific tools. They extend what Copilot can do beyond its default capabilities. A, C, and D describe unrelated concepts (UI theming, hardware acceleration, and Git hooks respectively).</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">15. Select ALL that apply: Which considerations are important when selecting tools for an AI agent's toolkit?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Whether the tool's capabilities align with the agent's defined scope and tasks</div>
<div class="quiz-option" data-correct="true">B. Whether the tool provides adequate error messages for the agent to interpret</div>
<div class="quiz-option">C. Whether the tool is the most expensive option available</div>
<div class="quiz-option" data-correct="true">D. Whether the tool supports appropriate access controls and permission scoping</div>
<div class="quiz-option">E. Whether the tool was released in the current calendar year</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. Tool selection should consider alignment with agent scope (A), quality of error feedback for the agent to recover from failures (B), and security controls (D). C is irrelevant—cost doesn't indicate quality. E is arbitrary; tool maturity and maintenance matter more than release date.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">16. When an agent creates a branch autonomously, what naming convention BEST supports traceability?</p>
<div class="quiz-options">
<div class="quiz-option">A. Using random UUIDs as branch names (e.g., a1b2c3d4-e5f6-...)</div>
<div class="quiz-option" data-correct="true">B. Including the agent identifier, task reference, and timestamp (e.g., copilot-agent/fix-issue-123/2024-01-15)</div>
<div class="quiz-option">C. Using the branch name "main" to avoid confusion</div>
<div class="quiz-option">D. Leaving the branch unnamed and relying on commit hashes</div>
</div>
<div class="quiz-explanation">The correct answer is B. A descriptive branch name that includes the agent identity, task context, and timestamp provides immediate traceability—anyone viewing the branch knows who created it, why, and when. A provides uniqueness but no context. C conflicts with the protected main branch. D is technically impossible—Git branches must have names.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">17. What happens when an MCP tool invocation returns an error to the AI agent?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent's session terminates immediately</div>
<div class="quiz-option">B. The error is hidden from the agent to prevent confusion</div>
<div class="quiz-option" data-correct="true">C. The agent receives the error message and can decide whether to retry, try an alternative approach, or escalate</div>
<div class="quiz-option">D. The MCP server automatically retries indefinitely until success</div>
</div>
<div class="quiz-explanation">The correct answer is C. MCP tools return errors to the agent as part of the normal interaction flow, allowing the agent to reason about the failure and decide on next steps (retry, alternative approach, or escalation). A is too drastic. B prevents the agent from recovering. D could create infinite loops without the agent's awareness or control.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<div class="quiz-scenario">An organization uses GitHub Actions to trigger an AI agent for automated dependency updates. The agent should update package versions, run tests, and create a PR. However, the organization requires that no agent-created PR can be merged without at least one human review.</div>
<p class="quiz-stem">18. How should this requirement be implemented?</p>
<div class="quiz-options">
<div class="quiz-option">A. Trust the agent to not merge its own PRs based on instructions alone</div>
<div class="quiz-option" data-correct="true">B. Configure branch protection rules requiring at least one human approval review before merge, regardless of CI status</div>
<div class="quiz-option">C. Remove the agent's ability to create PRs entirely</div>
<div class="quiz-option">D. Add a comment to each PR asking for review but don't enforce it</div>
</div>
<div class="quiz-explanation">The correct answer is B. Branch protection rules are a platform-level enforcement mechanism that cannot be bypassed by the agent—they require human approval regardless of what the agent does. A relies on instruction-following which is not a guarantee. C is too restrictive; the agent can still create PRs, just not merge them. D is advisory only, not enforceable.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">19. What is the significance of "repository-scoped" agents in GitHub?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. The agent's access and operations are confined to a single repository, limiting its blast radius and ensuring it cannot affect other repositories</div>
<div class="quiz-option">B. The agent can only work with repositories that have fewer than 100 files</div>
<div class="quiz-option">C. The agent stores its memory within the repository's Git history</div>
<div class="quiz-option">D. The agent is installed globally but labeled with a repository name</div>
</div>
<div class="quiz-explanation">The correct answer is A. Repository scoping is a security boundary—the agent can only read, write, and interact within one repository. This limits damage if the agent malfunctions and enforces clear ownership boundaries. B is an arbitrary file limit that doesn't exist. C describes a storage mechanism, not scoping. D describes global access with cosmetic labeling, not true scoping.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">20. When configuring rollback mechanisms for agent actions, which approach provides the MOST reliable recovery?</p>
<div class="quiz-options">
<div class="quiz-option">A. Asking the agent to remember what it changed and undo it manually</div>
<div class="quiz-option">B. Creating a full system backup before every agent action</div>
<div class="quiz-option" data-correct="true">C. Using Git's version control capabilities to revert commits, combined with infrastructure-as-code for non-code changes</div>
<div class="quiz-option">D. Disabling all agent write operations to eliminate the need for rollback</div>
</div>
<div class="quiz-explanation">The correct answer is C. Git provides atomic, reliable rollback through revert commits for code changes, and infrastructure-as-code enables state rollback for infrastructure. Together they provide comprehensive recovery. A is unreliable (agent memory can be imperfect). B is expensive and slow for every action. D eliminates the agent's value by preventing all modifications.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">21. Select ALL that apply: Which are valid reasons to configure environment-specific tool restrictions for an AI agent?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. To prevent the agent from executing destructive operations in production that are safe in development</div>
<div class="quiz-option" data-correct="true">B. To comply with regulatory requirements that differ between environments</div>
<div class="quiz-option">C. To make the agent run faster in production by removing safety checks</div>
<div class="quiz-option" data-correct="true">D. To limit data access based on environment sensitivity levels</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. Environment-specific restrictions protect against destructive actions in sensitive environments (A), ensure compliance with environment-specific regulations (B), and control data access based on sensitivity (D). C is incorrect and dangerous—removing safety checks in production to improve speed contradicts the entire purpose of environment-specific restrictions.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">22. What is the recommended way to handle secrets when an AI agent needs to authenticate with external services?</p>
<div class="quiz-options">
<div class="quiz-option">A. Include secrets directly in the agent's prompt for convenience</div>
<div class="quiz-option">B. Store secrets in the repository's README for easy team access</div>
<div class="quiz-option" data-correct="true">C. Use GitHub Secrets or a dedicated secrets manager, injecting credentials at runtime through environment variables without exposing them in logs or prompts</div>
<div class="quiz-option">D. Encode secrets in base64 within configuration files</div>
</div>
<div class="quiz-explanation">The correct answer is C. Secrets should be managed through dedicated secret stores (GitHub Secrets, HashiCorp Vault, etc.) and injected at runtime. They should never appear in prompts, logs, or code. A exposes secrets to the model context. B makes secrets publicly visible. D is not encryption—base64 is trivially reversible and provides no security.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">23. How does an MCP server's transport layer typically communicate with the AI agent?</p>
<div class="quiz-options">
<div class="quiz-option">A. Through direct memory access between processes</div>
<div class="quiz-option" data-correct="true">B. Through standardized JSON-RPC messages over stdio or HTTP/SSE connections</div>
<div class="quiz-option">C. Through shared file system writes only</div>
<div class="quiz-option">D. Through proprietary binary protocols unique to each server</div>
</div>
<div class="quiz-explanation">The correct answer is B. MCP uses standardized JSON-RPC as its message format, with transport options including stdio (for local servers) and HTTP with Server-Sent Events (for remote servers). This standardization is what makes MCP a universal protocol. A describes shared memory IPC which isn't used. C is too limited. D contradicts MCP's purpose of standardization.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">24. What is the PRIMARY purpose of configuring retry policies for agent tool invocations?</p>
<div class="quiz-options">
<div class="quiz-option">A. To ensure the agent always eventually succeeds regardless of the error type</div>
<div class="quiz-option" data-correct="true">B. To handle transient failures (network timeouts, rate limits) gracefully while avoiding infinite loops on permanent errors</div>
<div class="quiz-option">C. To increase the load on external services to test their capacity</div>
<div class="quiz-option">D. To delay agent execution for performance testing purposes</div>
</div>
<div class="quiz-explanation">The correct answer is B. Retry policies handle transient failures (temporary network issues, rate limiting) by automatically retrying with backoff, while distinguishing them from permanent errors that should not be retried. A is unrealistic—permanent failures can't be resolved by retrying. C describes stress testing, not error handling. D is about artificial delays, not recovery.</div>
</div>
</div>

<!-- DOMAIN 3: Manage memory, state, and execution (Questions 25-31) -->

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">25. What is "external memory" in the context of an AI agent system?</p>
<div class="quiz-options">
<div class="quiz-option">A. The RAM installed on the server running the agent</div>
<div class="quiz-option" data-correct="true">B. Persistent storage systems outside the model's context window (databases, files, vector stores) that the agent can query and update</div>
<div class="quiz-option">C. The agent's knowledge of programming languages</div>
<div class="quiz-option">D. USB drives attached to the development machine</div>
</div>
<div class="quiz-explanation">The correct answer is B. External memory refers to durable storage systems that persist beyond a single session and exist outside the model's context window. The agent actively reads from and writes to these stores (databases, vector stores, files) to maintain knowledge across sessions. A describes hardware. C describes pre-trained knowledge. D describes physical storage media.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">26. Why should memory expiration rules be implemented for AI agent state?</p>
<div class="quiz-options">
<div class="quiz-option">A. To force the agent to forget all previous tasks for privacy</div>
<div class="quiz-option" data-correct="true">B. To prevent the agent from acting on outdated information that no longer reflects the current state of the codebase or environment</div>
<div class="quiz-option">C. To reduce cloud storage costs as the primary concern</div>
<div class="quiz-option">D. To comply with a universal 24-hour data retention law</div>
</div>
<div class="quiz-explanation">The correct answer is B. Memory expiration prevents context drift by ensuring the agent doesn't rely on stale information. Code changes, configuration updates, and environment shifts can invalidate old context—expiration rules force re-fetching of current state. A is too aggressive. C may be a side benefit but isn't the primary driver. D doesn't exist as a universal law.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent is performing a database migration across 50 tables. After successfully migrating 30 tables, the process crashes. The team restarts the agent, but there is no record of which tables have been migrated already.</div>
<p class="quiz-stem">27. What state management practice should have been implemented?</p>
<div class="quiz-options">
<div class="quiz-option">A. Running all 50 migrations in a single atomic transaction</div>
<div class="quiz-option">B. Only migrating one table per session to avoid the issue</div>
<div class="quiz-option" data-correct="true">C. Maintaining a durable progress tracker that records each completed table migration, enabling idempotent resumption</div>
<div class="quiz-option">D. Backing up the entire database before each individual table migration</div>
</div>
<div class="quiz-explanation">The correct answer is C. A durable progress tracker (e.g., a migration state table or checkpoint file) records completed steps, allowing the agent to resume from table 31 without re-migrating the first 30. A may not be feasible for 50 tables due to transaction size limits. B is impractically slow. D is expensive and doesn't solve the resumption problem.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">28. Select ALL that apply: Which techniques help an agent detect and correct context drift during a long-running task?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Periodically checking the repository for new commits that may affect the agent's working files</div>
<div class="quiz-option" data-correct="true">B. Validating assumptions against current file state before applying changes</div>
<div class="quiz-option">C. Ignoring all external changes until the task is complete</div>
<div class="quiz-option" data-correct="true">D. Comparing the expected state (from memory) with actual state (from disk) before each operation</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. Checking for new commits (A) detects external changes. Validating assumptions (B) ensures the agent's understanding matches reality. State comparison (D) catches any divergence before applying changes. C is the opposite of drift detection—ignoring changes guarantees drift will go unnoticed and cause conflicts.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">29. What is the difference between "memory reset" and "memory pruning" for an AI agent?</p>
<div class="quiz-options">
<div class="quiz-option">A. They are the same operation with different names</div>
<div class="quiz-option" data-correct="true">B. Reset clears all accumulated state to start fresh, while pruning selectively removes low-value or outdated information while preserving critical context</div>
<div class="quiz-option">C. Reset is faster than pruning so it should always be preferred</div>
<div class="quiz-option">D. Pruning deletes more data than reset</div>
</div>
<div class="quiz-explanation">The correct answer is B. Reset is a complete state wipe—appropriate when accumulated context has become too corrupted or irrelevant to salvage. Pruning is surgical—it removes specific pieces of outdated or irrelevant information while keeping valuable context intact. A is incorrect; they serve different purposes. C and D mischaracterize the operations' scope and intent.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">30. When an agent needs to resume a partially completed task, what information is MOST critical to have persisted?</p>
<div class="quiz-options">
<div class="quiz-option">A. The complete conversation history including all intermediate reasoning steps</div>
<div class="quiz-option">B. The model's internal attention weights from the previous session</div>
<div class="quiz-option" data-correct="true">C. A structured checkpoint containing completed steps, pending steps, and any intermediate artifacts produced</div>
<div class="quiz-option">D. The list of all files in the repository at the time of interruption</div>
</div>
<div class="quiz-explanation">The correct answer is C. A structured checkpoint provides exactly what's needed for resumption: what's done, what's left, and what intermediate results exist. This enables the agent to pick up where it left off. A may exceed context limits and contain irrelevant detail. B is not accessible or useful. D provides file state but no task progress information.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">31. How should an agent handle state sharing between a local development environment and a CI/CD pipeline?</p>
<div class="quiz-options">
<div class="quiz-option">A. Rely on the developer to manually copy state between environments</div>
<div class="quiz-option">B. Store all state in local-only files that CI cannot access</div>
<div class="quiz-option" data-correct="true">C. Use repository-based artifacts or a shared state service that both environments can access through authenticated APIs</div>
<div class="quiz-option">D. Run the same agent instance simultaneously in both environments</div>
</div>
<div class="quiz-explanation">The correct answer is C. Repository artifacts (committed files, GitHub Actions artifacts) or shared state services provide a bridge between local and CI environments. Both can read and write through standard APIs. A introduces manual error. B prevents CI access entirely. D creates concurrency conflicts and is architecturally unsound.</div>
</div>
</div>

<!-- DOMAIN 4: Perform evaluation, error analysis, and tuning (Questions 32-41) -->

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">32. An agent consistently produces correct code changes but includes unnecessary modifications to unrelated files. What root cause category does this represent?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Reasoning error—the agent's scope management is flawed, causing it to exceed the boundaries of the task</div>
<div class="quiz-option">B. Tool misuse—the agent is using the wrong file editing tool</div>
<div class="quiz-option">C. Context issue—the agent doesn't have access to enough files</div>
<div class="quiz-option">D. Permission error—the agent shouldn't be able to access those files</div>
</div>
<div class="quiz-explanation">The correct answer is A. This is a reasoning error in scope management—the agent correctly uses tools but applies them too broadly, modifying files beyond what the task requires. The tool usage itself is correct (B is wrong), the agent has adequate context (C is wrong), and the access is technically permitted (D is wrong). The flaw is in the agent's reasoning about what should be changed.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<div class="quiz-scenario">A team uses an AI agent for automated code review. They track two metrics: (1) the percentage of review comments that are actionable, and (2) the average developer satisfaction score from post-review surveys. Metric 1 shows 85% actionable comments, but Metric 2 shows only 40% satisfaction.</div>
<p class="quiz-stem">33. What does this discrepancy MOST likely indicate?</p>
<div class="quiz-options">
<div class="quiz-option">A. The metrics are measured incorrectly</div>
<div class="quiz-option">B. Developers are not reading the review comments</div>
<div class="quiz-option" data-correct="true">C. The quantitative metric (actionable %) doesn't capture important qualitative factors like comment tone, relevance, or whether the suggestions align with the project's architectural intent</div>
<div class="quiz-option">D. The agent should stop providing code reviews entirely</div>
</div>
<div class="quiz-explanation">The correct answer is C. High actionability but low satisfaction suggests the comments are technically correct but miss something qualitative—perhaps they're nitpicky, miss the bigger picture, or are communicated in an unhelpful way. This highlights the gap between quantitative and qualitative evaluation. A is unlikely given specific numbers. B doesn't explain the pattern. D is an overreaction.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">34. What is the FIRST step in performing failure analysis on an agent that produced incorrect output?</p>
<div class="quiz-options">
<div class="quiz-option">A. Immediately change the agent's model to a newer version</div>
<div class="quiz-option">B. Delete the agent's configuration and start over</div>
<div class="quiz-option" data-correct="true">C. Examine the execution trace to understand the sequence of actions the agent took and identify where it diverged from expected behavior</div>
<div class="quiz-option">D. Add more tools to the agent's toolkit</div>
</div>
<div class="quiz-explanation">The correct answer is C. Failure analysis starts with understanding what happened—examining the trace reveals the agent's decision sequence and pinpoints where things went wrong. Without this understanding, any fix is guesswork. A, B, and D are remediation actions that should only follow after the root cause is understood. Jumping to solutions without diagnosis often doesn't fix the actual problem.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">35. Select ALL that apply: Which are valid success criteria for evaluating an AI agent that generates pull request descriptions?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. The description accurately summarizes the changes in the PR diff</div>
<div class="quiz-option" data-correct="true">B. The description includes relevant context about why the change was made</div>
<div class="quiz-option">C. The description is at least 5,000 words long</div>
<div class="quiz-option" data-correct="true">D. Reviewers can understand the PR without reading every line of code</div>
<div class="quiz-option">E. The description contains the agent's full execution trace</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. Good PR descriptions summarize changes accurately (A), provide motivation/context (B), and enable efficient review (D). C sets an arbitrary length that would make descriptions excessively verbose. E would overwhelm reviewers with irrelevant implementation details—execution traces belong in logs, not PR descriptions.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">36. How should evaluation signals be aligned with development intent?</p>
<div class="quiz-options">
<div class="quiz-option">A. Use only automated metrics since they are objective</div>
<div class="quiz-option">B. Rely exclusively on developer opinions since they know the codebase best</div>
<div class="quiz-option" data-correct="true">C. Define evaluation criteria that directly measure whether the agent's output achieves the specific developer goals stated in the task, combining automated checks with human review</div>
<div class="quiz-option">D. Compare agent output against other AI agents' outputs to determine quality</div>
</div>
<div class="quiz-explanation">The correct answer is C. Alignment with intent requires mapping evaluation criteria to the specific goals of each task. This means combining automated checks (compilation, tests, linting) with human assessment of whether the output actually solves the intended problem. A misses nuanced quality. B lacks scalability and objectivity. D measures relative performance, not intent alignment.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">37. An agent's failure is classified as a "context issue." Which of the following BEST describes this root cause?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent used the correct tool but with wrong parameters</div>
<div class="quiz-option">B. The agent's logical reasoning chain was flawed</div>
<div class="quiz-option" data-correct="true">C. The agent lacked necessary information to make a correct decision, or the information it had was stale/incorrect</div>
<div class="quiz-option">D. The agent had correct information but chose to ignore it</div>
</div>
<div class="quiz-explanation">The correct answer is C. A context issue means the agent's failure stemmed from inadequate or incorrect information—either it didn't have the data it needed, or the data it had was outdated. A describes tool misuse. B describes a reasoning error. D would be a reasoning error (ignoring available information is a decision-making flaw, not a context problem).</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">38. When tuning an agent's memory usage to improve performance, which approach is MOST effective?</p>
<div class="quiz-options">
<div class="quiz-option">A. Include the entire repository in the agent's context for every task</div>
<div class="quiz-option">B. Remove all context and let the agent operate from instructions alone</div>
<div class="quiz-option" data-correct="true">C. Analyze which context items correlate with successful task completion and refine the memory retrieval to prioritize high-signal information</div>
<div class="quiz-option">D. Randomly sample files from the repository for each task</div>
</div>
<div class="quiz-explanation">The correct answer is C. Effective memory tuning involves understanding which context items actually help the agent succeed and optimizing retrieval to surface those items. This is data-driven refinement based on correlation with outcomes. A causes context pollution. B removes necessary context. D provides unpredictable, potentially irrelevant information.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">39. What is the relationship between evaluation signals and tuning iterations?</p>
<div class="quiz-options">
<div class="quiz-option">A. Evaluation should only happen once when the agent is first deployed</div>
<div class="quiz-option" data-correct="true">B. Evaluation signals identify areas for improvement, which inform tuning changes, which are then validated by subsequent evaluation—forming a continuous improvement loop</div>
<div class="quiz-option">C. Tuning should happen before any evaluation to save time</div>
<div class="quiz-option">D. Evaluation and tuning are independent processes that don't inform each other</div>
</div>
<div class="quiz-explanation">The correct answer is B. Evaluation and tuning form a feedback loop: evaluate → identify issues → tune → re-evaluate → confirm improvement. This iterative cycle drives continuous improvement. A misses the ongoing nature of the process. C is backwards (you need to know what's wrong before fixing it). D misses the fundamental connection between measuring and improving.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent is tasked with refactoring a Python module. The evaluation shows: tests pass (✓), linter passes (✓), code coverage unchanged (✓), but the refactored code uses an entirely different architectural pattern than the rest of the codebase, making it inconsistent with team conventions.</div>
<p class="quiz-stem">40. What type of evaluation is missing from this assessment?</p>
<div class="quiz-options">
<div class="quiz-option">A. Performance benchmarking</div>
<div class="quiz-option">B. Security scanning</div>
<div class="quiz-option" data-correct="true">C. Qualitative review assessing architectural consistency and adherence to team conventions</div>
<div class="quiz-option">D. Load testing</div>
</div>
<div class="quiz-explanation">The correct answer is C. All automated checks pass, but they can't detect architectural inconsistency or convention violations. This requires qualitative human review that considers the broader codebase context and team standards. A, B, and D are additional automated checks that also wouldn't catch this issue—it's fundamentally a human judgment about code style and architecture.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">41. After identifying that an agent fails due to context issues, what is the BEST tuning response?</p>
<div class="quiz-options">
<div class="quiz-option">A. Rewrite the agent's core reasoning logic</div>
<div class="quiz-option">B. Remove tools that the agent uses incorrectly</div>
<div class="quiz-option" data-correct="true">C. Improve the agent's memory retrieval to ensure relevant context is available, and add instructions about when to fetch fresh information</div>
<div class="quiz-option">D. Switch to a completely different agent framework</div>
</div>
<div class="quiz-explanation">The correct answer is C. Since the root cause is context (missing or stale information), the fix should target context delivery—better retrieval, fresher data, and instructions about when to re-query. A addresses reasoning, not context. B addresses tools, not context. D is a drastic change that doesn't specifically address the context gap.</div>
</div>
</div>

<!-- DOMAIN 5: Orchestrate multi-agent coordination (Questions 42-51) -->

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">42. In a hub-and-spoke multi-agent architecture, what is the orchestrator's PRIMARY responsibility?</p>
<div class="quiz-options">
<div class="quiz-option">A. Executing all tasks itself without delegating to other agents</div>
<div class="quiz-option" data-correct="true">B. Decomposing tasks, delegating to specialized agents, collecting results, and managing the overall workflow coordination</div>
<div class="quiz-option">C. Storing all agent memory in a central database</div>
<div class="quiz-option">D. Providing the user interface for all agents</div>
</div>
<div class="quiz-explanation">The correct answer is B. The orchestrator in a hub-and-spoke pattern acts as the central coordinator: it breaks down work, assigns tasks to specialized agents, collects their outputs, and manages the workflow. A defeats the purpose of multi-agent architecture. C describes a storage concern, not orchestration. D describes a UI layer, not coordination logic.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">43. What is the PRIMARY risk of not implementing agent isolation in parallel multi-agent execution?</p>
<div class="quiz-options">
<div class="quiz-option">A. Agents will consume too much CPU</div>
<div class="quiz-option">B. Agents will use different programming languages</div>
<div class="quiz-option" data-correct="true">C. Agents may create race conditions, overwrite each other's changes, or produce conflicting outputs that corrupt the shared state</div>
<div class="quiz-option">D. Agents will be unable to access the internet</div>
</div>
<div class="quiz-explanation">The correct answer is C. Without isolation, parallel agents operating on shared resources create classic concurrency problems: race conditions, lost updates, and conflicting modifications. This can corrupt the codebase or produce inconsistent results. A is a resource concern, not an isolation issue. B and D are unrelated to isolation.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<div class="quiz-scenario">A multi-agent system uses a pipeline pattern: Agent A generates a feature implementation, Agent B writes tests for it, and Agent C performs a security audit. Agent B discovers that Agent A's implementation has a design flaw that makes it untestable.</div>
<p class="quiz-stem">44. What is the appropriate coordination response?</p>
<div class="quiz-options">
<div class="quiz-option">A. Agent B should modify Agent A's code directly to make it testable</div>
<div class="quiz-option" data-correct="true">B. Agent B should signal the orchestrator about the design flaw, which can then re-invoke Agent A with feedback about testability requirements</div>
<div class="quiz-option">C. Skip testing and proceed to Agent C's security audit</div>
<div class="quiz-option">D. Replace Agent A with a human developer permanently</div>
</div>
<div class="quiz-explanation">The correct answer is B. Proper pipeline coordination uses feedback loops—when a downstream agent identifies issues, it communicates back through the orchestrator, which can re-invoke upstream agents with specific improvement requirements. A violates agent scope boundaries. C skips a critical quality step. D is an overreaction to a solvable coordination issue.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">45. Select ALL that apply: Which observability artifacts should a multi-agent system produce for effective post-hoc review?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. A timeline showing when each agent started and completed its work</div>
<div class="quiz-option" data-correct="true">B. Records of all inter-agent communications and data transfers</div>
<div class="quiz-option" data-correct="true">C. The final merged output with attribution showing which agent produced each part</div>
<div class="quiz-option">D. Screen recordings of each agent's internal model processing</div>
<div class="quiz-option">E. Social media posts announcing each agent's completion</div>
</div>
<div class="quiz-explanation">A, B, and C are correct. Effective observability includes temporal information (A) for understanding sequencing, communication records (B) for tracing data flow, and attributed outputs (C) for accountability. D is impossible—model internals can't be screen-recorded. E is irrelevant to technical observability.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">46. When two agents produce overlapping changes to the same module, what conflict resolution strategy preserves the most value?</p>
<div class="quiz-options">
<div class="quiz-option">A. Accept only the changes from the agent that finished first</div>
<div class="quiz-option">B. Reject both sets of changes and start over</div>
<div class="quiz-option" data-correct="true">C. Use semantic merge analysis to combine non-conflicting portions and flag truly conflicting sections for human or orchestrator resolution</div>
<div class="quiz-option">D. Randomly select one agent's changes</div>
</div>
<div class="quiz-explanation">The correct answer is C. Semantic merge analysis maximizes value by keeping compatible changes from both agents and only escalating genuine conflicts. A arbitrarily discards potentially valuable work. B wastes both agents' outputs. D provides no rational basis for selection and may discard the better solution.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">47. What is the BEST practice for managing agent lifecycle when updating an agent's configuration in a multi-agent system?</p>
<div class="quiz-options">
<div class="quiz-option">A. Update all agents simultaneously to maintain version consistency</div>
<div class="quiz-option" data-correct="true">B. Use canary deployment: update one instance, validate behavior, then roll out to remaining instances</div>
<div class="quiz-option">C. Never update agents once they are deployed</div>
<div class="quiz-option">D. Delete and recreate the entire multi-agent system for each update</div>
</div>
<div class="quiz-explanation">The correct answer is B. Canary deployment for agent updates limits blast radius—if the updated configuration causes issues, only one instance is affected. A risks simultaneous failure across all instances. C prevents improvements and bug fixes. D is wasteful and risks losing accumulated state and configuration history.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">48. How should a multi-agent system handle the detection of duplicate work being performed by two agents?</p>
<div class="quiz-options">
<div class="quiz-option">A. Allow both agents to complete and keep both outputs</div>
<div class="quiz-option" data-correct="true">B. Detect the duplication early through task tracking, halt one agent, and redirect it to a different task</div>
<div class="quiz-option">C. Terminate both agents and reassign the task to a new agent</div>
<div class="quiz-option">D. Merge the duplicate outputs without review</div>
</div>
<div class="quiz-explanation">The correct answer is B. Early duplication detection through task tracking prevents wasted effort. Once detected, one agent can be redirected to productive work while the other completes the original task. A wastes resources on redundant work. C penalizes both agents unnecessarily. D risks creating a confused merged result.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">49. When replacing an agent in a multi-agent system, what must be verified to ensure continuity?</p>
<div class="quiz-options">
<div class="quiz-option">A. The new agent uses the exact same model and version as the old one</div>
<div class="quiz-option">B. The new agent has a similar name to the old one</div>
<div class="quiz-option" data-correct="true">C. The new agent's input/output interfaces are compatible with the existing agents that depend on or provide data to it</div>
<div class="quiz-option">D. The new agent was created by the same team as the old one</div>
</div>
<div class="quiz-explanation">The correct answer is C. Interface compatibility is the critical continuity requirement—downstream agents expect specific output formats and upstream agents provide specific input formats. If the new agent's interfaces don't match, the pipeline breaks. A is unnecessarily restrictive. B is cosmetic. D is an organizational concern unrelated to technical compatibility.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<div class="quiz-scenario">A multi-agent system processes a large refactoring task. Agent A completes its portion and hands off to Agent B. Agent B starts working but encounters an error after 30 minutes of processing. The orchestrator detects the failure and needs to decide on recovery.</div>
<p class="quiz-stem">50. What information does the orchestrator need to make an effective recovery decision?</p>
<div class="quiz-options">
<div class="quiz-option">A. Only the error message from Agent B</div>
<div class="quiz-option">B. The total runtime cost of both agents</div>
<div class="quiz-option" data-correct="true">C. Agent B's error details, what work Agent B completed before failure, Agent A's handoff state, and whether Agent B's partial work is salvageable</div>
<div class="quiz-option">D. The personal preferences of the team lead</div>
</div>
<div class="quiz-explanation">The correct answer is C. Effective recovery requires comprehensive context: the error itself, what was accomplished before failure (to avoid re-doing work), the handoff state (to understand the starting point), and whether partial results can be reused. A is insufficient for informed recovery decisions. B is about cost, not recovery strategy. D is irrelevant to technical recovery.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">51. What is the PRIMARY purpose of documenting agent decisions and outcomes in a multi-agent system?</p>
<div class="quiz-options">
<div class="quiz-option">A. To create training data for future model fine-tuning</div>
<div class="quiz-option">B. To generate weekly status reports for management</div>
<div class="quiz-option" data-correct="true">C. To enable accountability, debugging, and continuous improvement by providing a traceable record of what each agent did and why</div>
<div class="quiz-option">D. To satisfy a regulatory requirement to log all AI activity</div>
</div>
<div class="quiz-explanation">The correct answer is C. Documentation of decisions and outcomes serves multiple core purposes: accountability (who did what), debugging (why did something fail), and improvement (what patterns work or don't). A is a potential side benefit, not the primary purpose. B is a reporting concern. D may be relevant in some contexts but isn't the primary engineering reason.</div>
</div>
</div>

<!-- DOMAIN 6: Implement guardrails and accountability (Questions 52-60) -->

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">52. What is the difference between operational risk and compliance risk when classifying agent actions?</p>
<div class="quiz-options">
<div class="quiz-option">A. They are the same thing measured at different times</div>
<div class="quiz-option" data-correct="true">B. Operational risk concerns potential service disruption or data loss, while compliance risk concerns violation of regulatory, legal, or policy requirements</div>
<div class="quiz-option">C. Operational risk only applies to production environments</div>
<div class="quiz-option">D. Compliance risk is always higher than operational risk</div>
</div>
<div class="quiz-explanation">The correct answer is B. Operational risk is about things breaking—service outages, data corruption, performance degradation. Compliance risk is about violating rules—regulations, industry standards, organizational policies. Both require different mitigation strategies. A conflates distinct risk categories. C is false; operational risk exists in all environments. D is not universally true.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent has been configured with a guardrail that blocks any action attempting to disable branch protection rules. A developer asks the agent to temporarily disable branch protection to push an emergency hotfix directly to main.</div>
<p class="quiz-stem">53. What should the agent do?</p>
<div class="quiz-options">
<div class="quiz-option">A. Disable branch protection since the developer explicitly requested it</div>
<div class="quiz-option">B. Disable branch protection but log the action for later review</div>
<div class="quiz-option" data-correct="true">C. Refuse the action because it violates a security guardrail, and suggest alternative approaches like creating a hotfix branch with expedited review</div>
<div class="quiz-option">D. Ignore the request entirely without explanation</div>
</div>
<div class="quiz-explanation">The correct answer is C. Security guardrails are non-negotiable boundaries—they cannot be overridden by user requests. However, the agent should explain why it's refusing and suggest safe alternatives. A and B both violate the guardrail, regardless of the requestor. D refuses but provides no guidance, which isn't helpful.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">54. Select ALL that apply: Which principles should guide the assignment of execution contexts for AI agents?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Agents should run in isolated environments to limit blast radius</div>
<div class="quiz-option" data-correct="true">B. Execution contexts should be scoped to the minimum resources needed for the task</div>
<div class="quiz-option">C. All agents should share a single execution context for efficiency</div>
<div class="quiz-option" data-correct="true">D. Network access should be restricted to only necessary endpoints</div>
<div class="quiz-option">E. Agents should have root/admin access to handle any situation that arises</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. Isolation limits damage (A), minimum resources follows least-privilege (B), and restricted network access prevents unauthorized data access (D). C creates a shared failure domain and security risk. E violates least-privilege and creates maximum blast radius if the agent malfunctions.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">55. What is the PRIMARY purpose of requiring authorization for irreversible actions?</p>
<div class="quiz-options">
<div class="quiz-option">A. To create a paper trail for legal discovery</div>
<div class="quiz-option">B. To slow down the agent intentionally</div>
<div class="quiz-option" data-correct="true">C. To ensure a human has confirmed the intent and accepted the consequences before an action that cannot be undone is executed</div>
<div class="quiz-option">D. To prevent agents from ever performing irreversible actions</div>
</div>
<div class="quiz-explanation">The correct answer is C. Authorization for irreversible actions ensures informed consent—a human confirms they understand and accept the permanent consequences. This prevents accidental destruction and ensures deliberate decision-making. A is a side benefit. B mischaracterizes the purpose. D is too restrictive; irreversible actions are sometimes necessary, they just need explicit authorization.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">56. Which approach to guardrails BEST balances safety with agent productivity?</p>
<div class="quiz-options">
<div class="quiz-option">A. Block all agent actions by default and whitelist only after incidents</div>
<div class="quiz-option" data-correct="true">B. Classify actions by risk tier and apply proportional controls: low-risk actions proceed freely, medium-risk actions are logged, and high-risk actions require approval</div>
<div class="quiz-option">C. Allow all agent actions and review logs weekly</div>
<div class="quiz-option">D. Randomly approve or reject agent actions to keep them unpredictable</div>
</div>
<div class="quiz-explanation">The correct answer is B. Tiered guardrails provide proportional controls—they don't slow down safe operations while maintaining oversight for risky ones. This balances throughput with safety. A is too restrictive and reactive. C provides no real-time protection. D provides no consistent safety guarantee and would confuse the agent.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">57. What actions require human judgment that CANNOT be replaced by automated guardrails?</p>
<div class="quiz-options">
<div class="quiz-option">A. Checking if a file compiles successfully</div>
<div class="quiz-option">B. Verifying that tests pass before merge</div>
<div class="quiz-option" data-correct="true">C. Deciding whether a proposed architectural change aligns with the long-term vision of the product</div>
<div class="quiz-option">D. Validating that JSON output conforms to a schema</div>
</div>
<div class="quiz-explanation">The correct answer is C. Architectural decisions about long-term product vision require human judgment—understanding business context, team capabilities, technical debt tolerance, and strategic direction that automated rules cannot capture. A, B, and D are all deterministic checks that can be fully automated (compilation, test execution, schema validation).</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">58. An organization identifies that their AI agent has been approving its own code changes by auto-merging PRs it created. What guardrail principle is being violated?</p>
<div class="quiz-options">
<div class="quiz-option">A. Least privilege</div>
<div class="quiz-option" data-correct="true">B. Separation of duties—the entity that creates changes should not be the same entity that approves them</div>
<div class="quiz-option">C. Defense in depth</div>
<div class="quiz-option">D. Fail-safe defaults</div>
</div>
<div class="quiz-explanation">The correct answer is B. Separation of duties (also called separation of concerns in security) requires that the creator and approver be different entities. An agent approving its own PRs provides no independent verification—it's like signing your own expense reports. A is about permission scope. C is about multiple security layers. D is about secure default configurations.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<div class="quiz-scenario">A security audit reveals that an AI agent has access to 15 different GitHub repositories, but its defined tasks only involve 2 repositories. The agent has never accessed the other 13 repositories, but the permissions remain active.</div>
<p class="quiz-stem">59. What guardrail principle should be applied to remediate this finding?</p>
<div class="quiz-options">
<div class="quiz-option">A. Defense in depth—add additional monitoring on all 15 repositories</div>
<div class="quiz-option" data-correct="true">B. Least privilege—revoke access to the 13 repositories that are not needed for the agent's defined tasks</div>
<div class="quiz-option">C. Fail-open—keep the access in case future tasks need it</div>
<div class="quiz-option">D. Security through obscurity—hide the repository list from audit tools</div>
</div>
<div class="quiz-explanation">The correct answer is B. Least privilege dictates that access should be limited to exactly what's needed. Unused permissions represent unnecessary attack surface—if the agent is compromised, those 13 repos would be exposed. A adds monitoring but doesn't remove the risk. C is the opposite of secure defaults. D is never an acceptable security practice.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">60. How should guardrails handle an agent's attempt to perform a compliance-sensitive action (e.g., processing personal data)?</p>
<div class="quiz-options">
<div class="quiz-option">A. Allow the action and log it for monthly compliance review</div>
<div class="quiz-option">B. Block the action permanently with no override mechanism</div>
<div class="quiz-option" data-correct="true">C. Block the action by default, require explicit authorization from a compliance-qualified approver, and log the decision with full context</div>
<div class="quiz-option">D. Allow the action if the agent provides a justification in natural language</div>
</div>
<div class="quiz-explanation">The correct answer is C. Compliance-sensitive actions need pre-authorization from qualified personnel (not post-hoc review), with full audit logging. The block is the default safe state, but legitimate needs can be approved through proper channels. A provides no pre-authorization. B is too rigid for legitimate use cases. D relies on agent self-justification, which isn't a valid compliance control.</div>
</div>
</div>

