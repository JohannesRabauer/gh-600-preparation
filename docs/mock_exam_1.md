# Mock Exam 1 — GH-600 Agentic AI Developer

**Time limit:** 120 minutes | **Questions:** 60 | **Passing score:** 70% (42/60)

Click an answer to submit. You'll see immediate feedback with explanations.

---

<!-- DOMAIN 1: Prepare agent architecture and SDLC processes (Questions 1-10) -->

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">1. When defining an AI agent's architecture within a software development lifecycle, what is the PRIMARY reason for separating the planning phase from the execution phase?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. It enables human review of proposed actions before irreversible changes are made</div>
<div class="quiz-option">B. It reduces the computational cost of running the agent</div>
<div class="quiz-option">C. It eliminates the need for rollback mechanisms</div>
<div class="quiz-option">D. It allows the agent to bypass CI/CD pipelines for faster deployment</div>
</div>
<div class="quiz-explanation">The correct answer is A. Separating planning from execution creates an approval checkpoint where humans can review the agent's proposed plan before any changes are applied. This is a core principle of graduated autonomy. B is incorrect because separation doesn't inherently reduce compute costs. C is wrong because rollback mechanisms are still needed even with separation. D is incorrect because agents should integrate with, not bypass, CI/CD pipelines.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<div class="quiz-scenario">A team is deploying a GitHub Copilot agent that autonomously fixes linting errors across multiple repositories. During the first week, the agent made 47 commits directly to main branches without review, introducing subtle formatting changes that broke three downstream integrations.</div>
<p class="quiz-stem">2. Which anti-pattern does this scenario BEST illustrate?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Direct-to-main commits without human approval gates</div>
<div class="quiz-option">B. Insufficient tool permissions configuration</div>
<div class="quiz-option">C. Lack of memory state management</div>
<div class="quiz-option">D. Missing evaluation metrics for agent output</div>
</div>
<div class="quiz-explanation">The correct answer is A. The core anti-pattern here is the agent committing directly to main without any human review gate. This violates the principle of graduated autonomy—the agent should create pull requests on feature branches and require review before merging. B is partially relevant but the primary issue is the workflow design, not tool permissions. C and D are unrelated to the described failure mode.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">3. Select ALL that apply: Which of the following are essential components of agent observability in an SDLC context?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Decision logs that record why the agent chose a particular action</div>
<div class="quiz-option" data-correct="true">B. Structured plan outputs showing proposed changes before execution</div>
<div class="quiz-option" data-correct="true">C. Diff artifacts that capture the exact modifications made</div>
<div class="quiz-option">D. Real-time streaming of the agent's internal token probabilities</div>
<div class="quiz-option">E. Automatic social media notifications for each agent action</div>
</div>
<div class="quiz-explanation">A, B, and C are correct. Agent observability requires decision logs (why), plan outputs (what is proposed), and diff artifacts (what was done). These enable audit, debugging, and accountability. D is incorrect because internal token probabilities are model internals not relevant to SDLC observability. E is incorrect because social media notifications are not an observability mechanism.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">4. In the graduated autonomy model for AI agents, which sequence correctly represents the progression from least to most autonomous?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Supervised → Semi-autonomous → Fully autonomous</div>
<div class="quiz-option">B. Fully autonomous → Semi-autonomous → Supervised</div>
<div class="quiz-option">C. Semi-autonomous → Supervised → Fully autonomous</div>
<div class="quiz-option">D. Supervised → Fully autonomous → Semi-autonomous</div>
</div>
<div class="quiz-explanation">The correct answer is A. Graduated autonomy follows a trust-building progression: supervised (human approves every action), semi-autonomous (human reviews high-risk actions, agent handles low-risk independently), and fully autonomous (agent operates independently with post-hoc audit). B, C, and D represent incorrect orderings that don't follow the trust-building principle.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">5. What is the PRIMARY purpose of structured plan output validation in an agentic workflow?</p>
<div class="quiz-options">
<div class="quiz-option">A. To ensure the agent's code compiles without errors</div>
<div class="quiz-option">B. To generate documentation for end users</div>
<div class="quiz-option" data-correct="true">C. To verify that the agent's proposed actions align with defined success criteria before execution begins</div>
<div class="quiz-option">D. To optimize the agent's token usage and reduce API costs</div>
</div>
<div class="quiz-explanation">The correct answer is C. Structured plan validation serves as a checkpoint to ensure the agent's proposed actions match the intended outcomes and success criteria. This happens before execution, preventing wasted effort on misaligned plans. A describes compilation which is a different concern. B is about documentation, not plan validation. D is about cost optimization, unrelated to plan validation's purpose.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<div class="quiz-scenario">A software team wants to integrate an AI agent into their CI/CD pipeline. The agent should automatically create fix PRs when CI tests fail, but the team has had issues with agents creating cascading failures in the past.</div>
<p class="quiz-stem">6. What is the BEST approach to safely integrate this agent into the CI/CD pipeline?</p>
<div class="quiz-options">
<div class="quiz-option">A. Give the agent full repository admin access so it can quickly resolve any issues</div>
<div class="quiz-option">B. Run the agent only on the main branch to keep things simple</div>
<div class="quiz-option" data-correct="true">C. Configure the agent to create fix PRs on separate branches with mandatory review before merge, and set a maximum retry limit</div>
<div class="quiz-option">D. Disable CI tests when the agent is active to prevent cascading triggers</div>
</div>
<div class="quiz-explanation">The correct answer is C. This approach follows safe SDLC practices: branch isolation prevents cascading failures, mandatory review provides a human gate, and retry limits prevent infinite loops. A violates least-privilege. B is dangerous because direct-to-main work risks breaking production. D disables the safety net (tests) entirely, which is counterproductive.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">7. Which of the following is an anti-pattern when defining agent inputs and outputs?</p>
<div class="quiz-options">
<div class="quiz-option">A. Specifying clear success criteria for each agent task</div>
<div class="quiz-option">B. Defining expected output format with schema validation</div>
<div class="quiz-option" data-correct="true">C. Allowing the agent to self-modify its own permission scope based on task complexity</div>
<div class="quiz-option">D. Constraining agent inputs to repository-scoped context</div>
</div>
<div class="quiz-explanation">The correct answer is C. Self-modifying permissions is a critical anti-pattern because it violates the principle of least privilege and removes human oversight of access control. An agent should never be able to escalate its own permissions. A, B, and D are all best practices: clear success criteria, validated outputs, and scoped inputs respectively.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">8. Select ALL that apply: Which artifacts should a well-designed AI agent produce for audit purposes during SDLC operations?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. A timestamped log of all decisions and the reasoning behind them</div>
<div class="quiz-option" data-correct="true">B. Before/after diffs of all file modifications</div>
<div class="quiz-option">C. A copy of the entire language model's weights used during the session</div>
<div class="quiz-option" data-correct="true">D. The complete execution plan that was approved before changes were applied</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. Audit artifacts must include decision logs with reasoning (A), diffs showing what changed (B), and the approved plan for traceability (D). C is incorrect because model weights are infrastructure concerns, not audit artifacts—they are static and enormous, providing no useful audit information about specific actions taken.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">9. When defining success criteria for an AI agent tasked with code review, which metric BEST captures the agent's effectiveness?</p>
<div class="quiz-options">
<div class="quiz-option">A. Number of comments generated per pull request</div>
<div class="quiz-option">B. Speed of review completion in seconds</div>
<div class="quiz-option" data-correct="true">C. Percentage of agent suggestions that developers accept and implement</div>
<div class="quiz-option">D. Total lines of code analyzed per hour</div>
</div>
<div class="quiz-explanation">The correct answer is C. Acceptance rate of suggestions directly measures whether the agent provides value that developers find actionable and correct. A is a vanity metric—more comments don't mean better reviews. B measures speed but not quality. D measures throughput but not effectiveness. Success criteria should measure outcomes aligned with development intent, not raw activity.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">10. In the context of agent architecture, what does "human approval gate" refer to?</p>
<div class="quiz-options">
<div class="quiz-option">A. A firewall rule that blocks agent network access</div>
<div class="quiz-option">B. A code review tool that automatically approves all agent PRs</div>
<div class="quiz-option" data-correct="true">C. A checkpoint in the agent workflow where a human must explicitly approve before the agent proceeds with high-risk actions</div>
<div class="quiz-option">D. A login screen that authenticates the agent before it can access repositories</div>
</div>
<div class="quiz-explanation">The correct answer is C. A human approval gate is a deliberate checkpoint in the agent's workflow where execution pauses until a human reviews and explicitly approves the proposed action. This is critical for high-risk operations like merging to main or modifying infrastructure. A describes network security. B defeats the purpose of review. D describes authentication, not workflow approval.</div>
</div>
</div>

<!-- DOMAIN 2: Implement tool use and environment interaction (Questions 11-24) -->

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">11. What is the Model Context Protocol (MCP) primarily designed to provide for AI agents?</p>
<div class="quiz-options">
<div class="quiz-option">A. A proprietary encryption standard for agent communications</div>
<div class="quiz-option" data-correct="true">B. A standardized interface for connecting AI models to external tools, data sources, and services</div>
<div class="quiz-option">C. A database schema for storing agent conversation history</div>
<div class="quiz-option">D. A testing framework specifically for evaluating agent performance</div>
</div>
<div class="quiz-explanation">The correct answer is B. MCP (Model Context Protocol) provides a standardized, open protocol for connecting AI models to external tools and data sources. It acts as a universal adapter layer, allowing agents to interact with various services through a consistent interface. A is incorrect—MCP is not an encryption standard. C describes a database concern. D describes evaluation tooling, not a connectivity protocol.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<div class="quiz-scenario">A development team configures an MCP server that provides their AI agent with access to a PostgreSQL database, a Jira project management tool, and a Slack messaging API. The agent needs to query bug reports from Jira, check related database records, and post status updates to Slack.</div>
<p class="quiz-stem">12. What is the MOST important security consideration when configuring this MCP server?</p>
<div class="quiz-options">
<div class="quiz-option">A. Ensuring the MCP server runs on the fastest available hardware</div>
<div class="quiz-option">B. Configuring the agent to cache all database results locally for performance</div>
<div class="quiz-option" data-correct="true">C. Implementing an allow list that restricts which tools and operations the agent can invoke through the MCP server</div>
<div class="quiz-option">D. Granting the agent superuser database access to avoid permission errors</div>
</div>
<div class="quiz-explanation">The correct answer is C. Allow lists are a critical security control for MCP servers—they explicitly define which tools and operations are permitted, following the principle of least privilege. A is about performance, not security. B introduces data exposure risks by caching sensitive data. D directly violates least-privilege by granting excessive permissions.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">13. When configuring a repository-scoped agent in GitHub, what does "branch-based scope" mean?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent can only read code from branches that start with a specific prefix</div>
<div class="quiz-option">B. The agent is restricted to operating on one branch at a time for performance reasons</div>
<div class="quiz-option" data-correct="true">C. The agent's write permissions are limited to specific branches, preventing direct modifications to protected branches like main</div>
<div class="quiz-option">D. The agent creates a new branch for each token it generates</div>
</div>
<div class="quiz-explanation">The correct answer is C. Branch-based scope restricts an agent's write access to designated branches (typically feature branches), ensuring it cannot directly push to protected branches like main or production. This enforces code review workflows. A incorrectly limits read access by prefix. B is about concurrency, not scope. D is nonsensical—branches aren't created per token.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">14. Select ALL that apply: Which are valid error handling strategies for an AI agent that encounters a tool invocation failure?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Retry with exponential backoff for transient failures</div>
<div class="quiz-option" data-correct="true">B. Escalate to a human operator when retry limits are exceeded</div>
<div class="quiz-option">C. Silently ignore the error and continue with the next task</div>
<div class="quiz-option" data-correct="true">D. Roll back any partial changes made before the failure</div>
<div class="quiz-option">E. Automatically increase the agent's permission level to bypass the error</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. Proper error handling includes retrying transient failures with backoff (A), escalating to humans when automated recovery fails (B), and rolling back partial changes to maintain consistency (D). C is dangerous because silent failures can lead to corrupted state. E is a critical security anti-pattern—agents should never self-escalate permissions.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">15. How does a GitHub remote MCP server differ from a local MCP server in the context of Copilot agent mode?</p>
<div class="quiz-options">
<div class="quiz-option">A. Remote MCP servers are always faster than local ones</div>
<div class="quiz-option">B. Local MCP servers can only access files on disk, never network resources</div>
<div class="quiz-option" data-correct="true">C. Remote MCP servers are hosted and managed by GitHub, requiring no local infrastructure, while local servers run on the developer's machine</div>
<div class="quiz-option">D. Remote MCP servers do not support tool allow lists</div>
</div>
<div class="quiz-explanation">The correct answer is C. GitHub remote MCP servers are hosted infrastructure that GitHub manages, eliminating the need for developers to run and maintain local server processes. Local MCP servers run on the developer's machine and require local setup. A is not necessarily true—latency depends on many factors. B is incorrect; local servers can access network resources. D is wrong; both support allow lists.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">16. When an AI agent autonomously creates a pull request in GitHub, which of the following ensures traceability and accountability?</p>
<div class="quiz-options">
<div class="quiz-option">A. Using a shared team service account with no identifying information</div>
<div class="quiz-option" data-correct="true">B. Using a dedicated bot account with clear labeling that identifies the agent as the author and links to decision logs</div>
<div class="quiz-option">C. Attributing the PR to the repository owner regardless of who triggered it</div>
<div class="quiz-option">D. Creating the PR anonymously to avoid bias in code review</div>
</div>
<div class="quiz-explanation">The correct answer is B. Traceability requires clear attribution—a dedicated bot account identifies the agent, and linking to decision logs provides audit trail. A loses individual accountability with shared accounts. C misattributes authorship, which is dishonest and defeats accountability. D removes attribution entirely, making it impossible to trace actions back to the agent.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<div class="quiz-scenario">An agent running in a CI workflow needs to invoke a GitHub API to create a branch, commit generated test files, and open a pull request. The workflow uses a GITHUB_TOKEN with default permissions.</div>
<p class="quiz-stem">17. What permission adjustment is needed for the agent to successfully complete all three operations?</p>
<div class="quiz-options">
<div class="quiz-option">A. No changes needed; GITHUB_TOKEN has full admin access by default</div>
<div class="quiz-option" data-correct="true">B. The workflow must explicitly grant contents: write and pull-requests: write permissions to the GITHUB_TOKEN</div>
<div class="quiz-option">C. Replace GITHUB_TOKEN with a personal access token stored as a plaintext environment variable</div>
<div class="quiz-option">D. Disable branch protection rules so the token works without additional scopes</div>
</div>
<div class="quiz-explanation">The correct answer is B. GITHUB_TOKEN in Actions has restrictive default permissions. Creating branches and commits requires contents: write, and opening PRs requires pull-requests: write—these must be explicitly declared in the workflow YAML. A is wrong; defaults are read-only for most operations. C is insecure (plaintext secrets) and unnecessary. D removes security controls rather than properly configuring permissions.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">18. What is the purpose of an MCP tool registry in the context of GitHub Copilot?</p>
<div class="quiz-options">
<div class="quiz-option">A. To store the source code of all tools the agent has ever used</div>
<div class="quiz-option">B. To track billing information for tool API calls</div>
<div class="quiz-option" data-correct="true">C. To provide a discoverable catalog of available MCP servers and tools that agents can be configured to use</div>
<div class="quiz-option">D. To enforce rate limiting on tool invocations</div>
</div>
<div class="quiz-explanation">The correct answer is C. An MCP tool registry serves as a discoverable catalog where available MCP servers and their tools are listed, making it easy to find, configure, and connect tools to agents. A describes a code repository, not a registry. B is about billing systems. D describes rate limiting infrastructure, which is a separate concern from discovery.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">19. When evaluating an agent's execution context, which factor is MOST critical to assess before allowing the agent to perform write operations?</p>
<div class="quiz-options">
<div class="quiz-option">A. The time of day the operation is being performed</div>
<div class="quiz-option">B. The number of files in the repository</div>
<div class="quiz-option" data-correct="true">C. Whether the target environment is production, staging, or development</div>
<div class="quiz-option">D. The programming language used in the repository</div>
</div>
<div class="quiz-explanation">The correct answer is C. The target environment (production vs. staging vs. development) directly determines the risk level of write operations. Writing to production carries significantly higher risk than writing to a development environment, and permissions/approvals should be calibrated accordingly. A, B, and D may be tangentially relevant but don't fundamentally change the risk profile of write operations.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">20. Select ALL that apply: Which of the following are environment-specific constraints that should be configured for an AI agent operating in a production environment?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Read-only access to production databases with no direct write capability</div>
<div class="quiz-option" data-correct="true">B. Mandatory human approval for any deployment or infrastructure changes</div>
<div class="quiz-option">C. Unlimited API call rate to ensure maximum agent productivity</div>
<div class="quiz-option" data-correct="true">D. Restricted network egress to prevent data exfiltration</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. Production environments require strict controls: read-only database access prevents accidental data corruption (A), human approval gates prevent unauthorized deployments (B), and network restrictions prevent data leakage (D). C is incorrect because unlimited API rates in production can cause resource exhaustion, cascading failures, and cost overruns.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">21. What is the recommended approach when an agent needs to interact with multiple tools that have different authentication requirements?</p>
<div class="quiz-options">
<div class="quiz-option">A. Use a single shared credential for all tools to simplify configuration</div>
<div class="quiz-option">B. Hardcode credentials directly in the agent's configuration file</div>
<div class="quiz-option" data-correct="true">C. Configure each tool with its own scoped credential, stored securely in a secrets manager, with minimum required permissions</div>
<div class="quiz-option">D. Disable authentication for internal tools to reduce complexity</div>
</div>
<div class="quiz-explanation">The correct answer is C. Each tool should have its own credential with minimum necessary permissions, stored in a secrets manager (like GitHub Secrets or a vault). This follows least-privilege and limits blast radius if one credential is compromised. A creates a single point of failure. B exposes credentials in plaintext. D removes security controls entirely.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">22. In a CI workflow that invokes a GitHub Copilot agent, what is the PRIMARY benefit of using workflow_dispatch events with input parameters?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. It allows humans to provide specific context and constraints to the agent at invocation time</div>
<div class="quiz-option">B. It bypasses all branch protection rules for the agent</div>
<div class="quiz-option">C. It automatically grants the agent elevated permissions</div>
<div class="quiz-option">D. It prevents the agent from accessing repository secrets</div>
</div>
<div class="quiz-explanation">The correct answer is A. workflow_dispatch with input parameters enables human operators to specify context, scope, and constraints when manually triggering an agent workflow. This supports supervised and semi-autonomous patterns where humans guide agent behavior. B and C are incorrect—workflow_dispatch doesn't change permissions. D is wrong; secret access is controlled by workflow permissions, not trigger type.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent configured with MCP tools attempts to delete a production database table. The MCP server's allow list does not include the DROP TABLE operation, but the underlying database credentials have full admin access.</div>
<p class="quiz-stem">23. What happens in this scenario?</p>
<div class="quiz-options">
<div class="quiz-option">A. The operation succeeds because the database credentials allow it</div>
<div class="quiz-option" data-correct="true">B. The MCP server blocks the operation at the tool layer because DROP TABLE is not on the allow list</div>
<div class="quiz-option">C. The agent automatically adds DROP TABLE to the allow list and retries</div>
<div class="quiz-option">D. The database silently ignores the request without any error</div>
</div>
<div class="quiz-explanation">The correct answer is B. MCP allow lists act as a policy enforcement layer between the agent and the underlying tools. Even if the underlying credentials have broader access, the MCP server will block operations not explicitly permitted on the allow list. This is defense-in-depth. A would only happen without the MCP layer. C is a permission self-escalation anti-pattern. D is not how databases work.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">24. What is the escalation path when an agent encounters an error it cannot resolve through retries?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent should attempt increasingly aggressive workarounds until something works</div>
<div class="quiz-option">B. The agent should terminate silently without notifying anyone</div>
<div class="quiz-option">C. The agent should modify its own instructions to avoid the problematic operation</div>
<div class="quiz-option" data-correct="true">D. The agent should log the failure context, preserve its current state, and notify a human operator for manual intervention</div>
</div>
<div class="quiz-explanation">The correct answer is D. Proper escalation involves preserving context (logs, state, error details) and notifying a human operator who can make decisions about how to proceed. This maintains accountability and prevents the agent from causing further damage. A can lead to cascading failures. B loses valuable debugging information. C is self-modification of instructions, an anti-pattern.</div>
</div>
</div>

<!-- DOMAIN 3: Manage memory, state, and execution (Questions 25-31) -->

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">25. What is the key difference between short-term memory and long-term memory in an AI agent's architecture?</p>
<div class="quiz-options">
<div class="quiz-option">A. Short-term memory is stored in RAM while long-term memory is stored on disk</div>
<div class="quiz-option" data-correct="true">B. Short-term memory holds context for the current task session and is discarded after completion, while long-term memory persists across sessions and informs future behavior</div>
<div class="quiz-option">C. Short-term memory is encrypted while long-term memory is stored in plaintext</div>
<div class="quiz-option">D. Short-term memory is shared across all agents while long-term memory is private</div>
</div>
<div class="quiz-explanation">The correct answer is B. Short-term memory is session-scoped—it holds the working context for the current task (conversation history, intermediate results) and is released when the task completes. Long-term memory persists across sessions, storing learned patterns, preferences, and historical context. A conflates implementation details with the conceptual distinction. C and D describe access control patterns, not memory types.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent is working on a multi-file refactoring task. After modifying 5 of 12 files, the agent's session is interrupted due to a timeout. When the agent resumes, it starts the refactoring from scratch, re-modifying the 5 files it already changed and introducing inconsistencies.</div>
<p class="quiz-stem">26. Which memory management practice would BEST prevent this issue?</p>
<div class="quiz-options">
<div class="quiz-option">A. Increasing the session timeout to avoid interruptions</div>
<div class="quiz-option" data-correct="true">B. Capturing task progress as durable artifacts (e.g., a checkpoint file listing completed steps) so the agent can resume without repeating work</div>
<div class="quiz-option">C. Running the agent with unlimited memory allocation</div>
<div class="quiz-option">D. Disabling all timeout mechanisms for agent processes</div>
</div>
<div class="quiz-explanation">The correct answer is B. Durable progress artifacts (checkpoints) allow an agent to resume from where it left off after an interruption. The checkpoint records which files were already modified, enabling idempotent resumption. A and D try to prevent interruptions rather than handling them gracefully—interruptions will always be possible. C conflates system memory with agent state management.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">27. What is "context drift" in the context of AI agent execution?</p>
<div class="quiz-options">
<div class="quiz-option">A. When the agent's model weights change during a session</div>
<div class="quiz-option">B. When the agent's API key expires mid-execution</div>
<div class="quiz-option" data-correct="true">C. When the agent's accumulated context becomes stale or misaligned with the actual current state of the environment</div>
<div class="quiz-option">D. When the agent moves between different programming languages</div>
</div>
<div class="quiz-explanation">The correct answer is C. Context drift occurs when the agent's internal understanding (its memory/context) diverges from the actual state of the environment. For example, another developer may have pushed changes that invalidate the agent's assumptions. A describes model mutation (doesn't happen mid-session). B is an authentication issue. D describes language switching, not drift.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">28. Select ALL that apply: Which strategies help prevent conflicting or stale context in an AI agent?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Periodically refreshing state from the source of truth (e.g., pulling latest from the repository)</div>
<div class="quiz-option" data-correct="true">B. Implementing memory expiration rules that invalidate cached context after a defined period</div>
<div class="quiz-option">C. Never reading from external sources to avoid contamination</div>
<div class="quiz-option" data-correct="true">D. Using optimistic locking or conflict detection when writing shared state</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. Refreshing from source of truth (A) ensures the agent works with current data. Expiration rules (B) prevent indefinitely stale cache. Optimistic locking (D) detects conflicts when multiple actors modify shared state. C is incorrect—isolation from external sources means the agent works with increasingly outdated information, worsening context drift.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">29. When scoping memory to task-relevant information, what is the PRIMARY risk of including too much context?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent will take longer to authenticate</div>
<div class="quiz-option" data-correct="true">B. The agent may become confused by irrelevant information, leading to degraded reasoning and incorrect actions</div>
<div class="quiz-option">C. The agent's API costs will always exceed budget</div>
<div class="quiz-option">D. The agent will automatically delete files to make room for new context</div>
</div>
<div class="quiz-explanation">The correct answer is B. Overloading an agent's context with irrelevant information degrades its ability to reason effectively—a problem often called "lost in the middle" or context pollution. The agent may fixate on irrelevant details or miss critical information buried in noise. A is unrelated. C may happen but isn't guaranteed. D describes behavior that doesn't occur automatically.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">30. How should an agent share state across tools operating in different environments (e.g., local IDE and CI runner)?</p>
<div class="quiz-options">
<div class="quiz-option">A. By passing state through environment variables only</div>
<div class="quiz-option">B. By relying on the language model's internal memory across sessions</div>
<div class="quiz-option" data-correct="true">C. By using external durable storage (e.g., artifacts, shared state files in the repository, or a state API) accessible from both environments</div>
<div class="quiz-option">D. By duplicating the agent instance in each environment with identical configurations</div>
</div>
<div class="quiz-explanation">The correct answer is C. External durable storage provides a shared, persistent medium that multiple environments can read from and write to. Repository artifacts, shared state files, or dedicated state APIs work well for this purpose. A is limited and environment-specific. B doesn't work—LLMs don't maintain memory across separate sessions. D duplicates the agent but doesn't solve state sharing.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">31. What is the recommended approach for memory pruning in a long-running agent session?</p>
<div class="quiz-options">
<div class="quiz-option">A. Delete all memory at fixed time intervals regardless of content</div>
<div class="quiz-option">B. Never prune memory to ensure no information is lost</div>
<div class="quiz-option" data-correct="true">C. Apply relevance-based pruning that removes information no longer pertinent to the current task while preserving critical context and decision history</div>
<div class="quiz-option">D. Replace all existing memory with the most recent tool output</div>
</div>
<div class="quiz-explanation">The correct answer is C. Effective memory pruning balances context window utilization with information retention. Relevance-based pruning keeps task-critical context and decision history while removing superseded or irrelevant details. A is too aggressive and may remove critical context. B leads to context overflow. D destroys all historical context, preventing the agent from understanding how it arrived at its current state.</div>
</div>
</div>

<!-- DOMAIN 4: Perform evaluation, error analysis, and tuning (Questions 32-41) -->

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">32. When classifying root causes of agent failures, which category does "the agent had correct instructions but selected an inappropriate tool for the task" belong to?</p>
<div class="quiz-options">
<div class="quiz-option">A. Reasoning error</div>
<div class="quiz-option" data-correct="true">B. Tool misuse</div>
<div class="quiz-option">C. Context issue</div>
<div class="quiz-option">D. Permission error</div>
</div>
<div class="quiz-explanation">The correct answer is B. Tool misuse occurs when the agent selects the wrong tool or uses a tool incorrectly despite having adequate instructions and context. A (reasoning error) would mean flawed logic in planning. C (context issue) would mean the agent lacked necessary information. D (permission error) would mean the tool was correct but access was denied.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">33. Which evaluation approach BEST measures whether an AI agent's code changes align with the developer's original intent?</p>
<div class="quiz-options">
<div class="quiz-option">A. Counting the number of lines of code modified</div>
<div class="quiz-option">B. Checking if the code compiles without syntax errors</div>
<div class="quiz-option" data-correct="true">C. Comparing the agent's output against defined acceptance criteria and having developers rate alignment with their intent</div>
<div class="quiz-option">D. Measuring the agent's response latency</div>
</div>
<div class="quiz-explanation">The correct answer is C. Alignment with developer intent requires checking against predefined acceptance criteria and getting human feedback on whether the changes match what was actually wanted. A is a volume metric, not quality. B only checks syntax validity, not intent alignment. D measures performance, not correctness. Qualitative evaluation from developers is essential for measuring intent alignment.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">34. Select ALL that apply: Which artifacts are useful for failure analysis when an AI agent produces incorrect output?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. The agent's execution plan showing the sequence of steps it intended to take</div>
<div class="quiz-option" data-correct="true">B. Trace logs showing each tool invocation and its response</div>
<div class="quiz-option" data-correct="true">C. The input context provided to the agent at the start of the task</div>
<div class="quiz-option">D. The agent's CSS stylesheet preferences</div>
<div class="quiz-option" data-correct="true">E. Workflow run artifacts including exit codes and error messages</div>
</div>
<div class="quiz-explanation">A, B, C, and E are correct. Failure analysis requires the plan (A) to understand intent, traces (B) to see what happened at each step, input context (C) to verify the agent had correct information, and workflow artifacts (E) for concrete error signals. D is irrelevant—CSS preferences have no bearing on failure analysis of agent behavior.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent is tasked with writing unit tests for a JavaScript module. It generates tests that all pass, but upon human review, the tests are found to be trivial—they only test obvious happy paths and miss edge cases entirely. The agent's evaluation metrics show 100% test pass rate.</div>
<p class="quiz-stem">35. What does this scenario reveal about the evaluation approach?</p>
<div class="quiz-options">
<div class="quiz-option">A. The evaluation metrics are correctly capturing agent quality</div>
<div class="quiz-option">B. The agent needs more computational resources to generate better tests</div>
<div class="quiz-option" data-correct="true">C. The quantitative metric (pass rate) is insufficient—qualitative evaluation of test coverage and meaningfulness is needed to align with development intent</div>
<div class="quiz-option">D. The agent should be switched to a different programming language</div>
</div>
<div class="quiz-explanation">The correct answer is C. This is a classic example of Goodhart's Law—the metric (pass rate) became the target and lost its value as a measure of quality. A purely quantitative metric missed that the tests were trivially easy. Qualitative evaluation (are the tests meaningful? do they cover edge cases?) is needed alongside quantitative signals. A is clearly wrong. B and D don't address the evaluation gap.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">36. After identifying that an agent consistently misuses a particular tool, what is the MOST effective tuning approach?</p>
<div class="quiz-options">
<div class="quiz-option">A. Remove the tool entirely from the agent's toolkit</div>
<div class="quiz-option">B. Increase the agent's temperature parameter to generate more diverse responses</div>
<div class="quiz-option" data-correct="true">C. Refine the tool's description and usage instructions in the agent's system prompt, adding examples of correct and incorrect usage</div>
<div class="quiz-option">D. Add more unrelated tools to give the agent more options</div>
</div>
<div class="quiz-explanation">The correct answer is C. Tuning tool usage involves revising the instructions that guide tool selection—adding clearer descriptions, usage examples, and explicit guidance about when to use (and not use) the tool. A is too drastic if the tool is needed. B affects randomness, not tool understanding. D adds noise without addressing the root cause of misuse.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">37. What role do automated scanning tools play in agent evaluation?</p>
<div class="quiz-options">
<div class="quiz-option">A. They replace the need for human evaluation entirely</div>
<div class="quiz-option">B. They are only useful for checking spelling errors in agent output</div>
<div class="quiz-option" data-correct="true">C. They provide automated evaluation signals such as linting results, security scan findings, and test coverage metrics that complement human review</div>
<div class="quiz-option">D. They are used exclusively for measuring agent response time</div>
</div>
<div class="quiz-explanation">The correct answer is C. Automated scanners (linters, SAST tools, test runners) provide objective, repeatable evaluation signals that can be collected without human effort. These complement but don't replace human judgment. A overstates their capability—nuanced quality requires human review. B drastically underestimates their scope. D describes performance monitoring, not scanning tools.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">38. An agent's trace log shows: Plan → Read file → Edit file → Run tests → Tests fail → Edit file again → Run tests → Tests pass. Upon review, the second edit introduced a bug that happens to make the specific test pass but breaks other functionality. How should this be classified?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Reasoning error—the agent optimized for passing the specific test rather than correctly solving the underlying problem</div>
<div class="quiz-option">B. Tool misuse—the agent used the wrong testing tool</div>
<div class="quiz-option">C. Context issue—the agent lacked information about other tests</div>
<div class="quiz-option">D. Permission error—the agent shouldn't have been able to edit files</div>
</div>
<div class="quiz-explanation">The correct answer is A. This is a reasoning error where the agent's goal collapsed from "fix the bug correctly" to "make this test pass." The tools were used correctly (editing, testing), so it's not tool misuse. It's not a context issue if other tests were available but ignored in reasoning. Permission error doesn't apply since file editing was intentional.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">39. What is the difference between qualitative and quantitative evaluation of an AI agent?</p>
<div class="quiz-options">
<div class="quiz-option">A. Qualitative evaluation uses numbers; quantitative evaluation uses descriptions</div>
<div class="quiz-option">B. Qualitative evaluation is automated; quantitative evaluation requires humans</div>
<div class="quiz-option" data-correct="true">C. Quantitative evaluation measures objective metrics (pass rates, latency, coverage); qualitative evaluation assesses subjective quality (code readability, alignment with intent, appropriateness of approach)</div>
<div class="quiz-option">D. They are the same thing with different names</div>
</div>
<div class="quiz-explanation">The correct answer is C. Quantitative evaluation produces measurable numbers (test pass rate, code coverage percentage, response time). Qualitative evaluation involves human judgment about quality aspects that are difficult to quantify—is the code readable? Does the approach make sense architecturally? A reverses the definitions. B reverses the typical automation patterns. D is factually incorrect.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">40. When tuning an agent that frequently provides responses that are technically correct but overly complex, what is the BEST adjustment?</p>
<div class="quiz-options">
<div class="quiz-option">A. Reduce the model's context window size</div>
<div class="quiz-option" data-correct="true">B. Revise the agent's instructions to emphasize simplicity, add examples of preferred simple solutions, and include constraints like maximum lines of code</div>
<div class="quiz-option">C. Switch to a smaller, less capable model</div>
<div class="quiz-option">D. Remove all tools to force simpler outputs</div>
</div>
<div class="quiz-explanation">The correct answer is B. Tuning agent behavior is primarily done through instruction refinement—updating prompts, adding positive/negative examples, and setting explicit constraints. This directly addresses the complexity issue without sacrificing capability. A may worsen quality. C sacrifices overall capability. D removes functionality rather than guiding behavior.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">41. Which evaluation signal is MOST useful for detecting when an agent is stuck in a retry loop?</p>
<div class="quiz-options">
<div class="quiz-option">A. High code quality scores on the generated output</div>
<div class="quiz-option">B. Low token usage per request</div>
<div class="quiz-option" data-correct="true">C. Repeated identical or near-identical tool invocations in the execution trace with the same error responses</div>
<div class="quiz-option">D. Fast response times from the agent</div>
</div>
<div class="quiz-explanation">The correct answer is C. A retry loop manifests as repeated identical tool calls receiving the same errors—the agent keeps trying the same approach without adapting. This pattern is visible in execution traces and should trigger escalation or circuit-breaking. A, B, and D don't indicate loops; they may even look positive while the agent is stuck.</div>
</div>
</div>

<!-- DOMAIN 5: Orchestrate multi-agent coordination (Questions 42-51) -->

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">42. In a multi-agent system, what is the PRIMARY purpose of agent isolation during parallel execution?</p>
<div class="quiz-options">
<div class="quiz-option">A. To ensure each agent uses a different programming language</div>
<div class="quiz-option">B. To reduce API costs by limiting concurrent calls</div>
<div class="quiz-option" data-correct="true">C. To prevent agents from interfering with each other's work, such as overwriting files or creating conflicting changes</div>
<div class="quiz-option">D. To ensure agents cannot communicate with each other under any circumstances</div>
</div>
<div class="quiz-explanation">The correct answer is C. Agent isolation ensures that parallel agents operate in separate workspaces (e.g., separate branches or containers) so they don't overwrite each other's changes or create merge conflicts. A is irrelevant to isolation. B is about cost control, not isolation. D is too extreme—agents may need to share results, but their active workspaces should be isolated.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<div class="quiz-scenario">Three AI agents are working in parallel: Agent A refactors the authentication module, Agent B updates the user interface components, and Agent C modifies the API endpoints. All three agents modify the shared types/user.ts file with different, incompatible changes.</div>
<p class="quiz-stem">43. What is the BEST strategy to resolve this conflict?</p>
<div class="quiz-options">
<div class="quiz-option">A. Let the last agent to commit win and overwrite the others' changes</div>
<div class="quiz-option">B. Automatically merge all changes regardless of compatibility</div>
<div class="quiz-option" data-correct="true">C. Detect the conflict through automated merge checks, halt the affected agents, and escalate to a human or orchestrator for resolution</div>
<div class="quiz-option">D. Delete the shared file and have each agent recreate its own version</div>
</div>
<div class="quiz-explanation">The correct answer is C. When multiple agents create conflicting changes to the same file, automated conflict detection should identify the issue, pause further modifications, and escalate for resolution—either to a human reviewer or an orchestrating agent that understands the overall intent. A loses work. B risks broken code. D creates fragmentation rather than resolving the conflict.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">44. Select ALL that apply: Which orchestration patterns are commonly used for coordinating multiple AI agents?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Hub-and-spoke: a central orchestrator delegates tasks to specialized agents</div>
<div class="quiz-option" data-correct="true">B. Pipeline: agents execute sequentially, each passing output to the next</div>
<div class="quiz-option" data-correct="true">C. Peer-to-peer: agents communicate directly and negotiate task ownership</div>
<div class="quiz-option">D. Chaos mode: agents compete randomly and the fastest result wins</div>
</div>
<div class="quiz-explanation">A, B, and C are correct orchestration patterns. Hub-and-spoke (A) uses central coordination for task distribution. Pipeline (B) creates sequential processing chains. Peer-to-peer (C) enables decentralized collaboration. D is not a recognized pattern—random competition without coordination leads to wasted resources, conflicts, and unpredictable outcomes.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">45. What is the PRIMARY purpose of documenting handoffs between agents in a multi-agent workflow?</p>
<div class="quiz-options">
<div class="quiz-option">A. To increase the file count in the repository</div>
<div class="quiz-option">B. To slow down the workflow for safety reasons</div>
<div class="quiz-option" data-correct="true">C. To maintain traceability so that any failure can be attributed to the correct agent and the context of the handoff can be reviewed</div>
<div class="quiz-option">D. To generate marketing materials about the AI system</div>
</div>
<div class="quiz-explanation">The correct answer is C. Documented handoffs create an audit trail showing what information was passed between agents, enabling root cause analysis when failures occur. Without handoff documentation, it's impossible to determine whether a downstream failure was caused by the receiving agent or by incomplete/incorrect information from the upstream agent. A, B, and D are not legitimate purposes of handoff documentation.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">46. How should a multi-agent system detect that one agent has stalled during execution?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Implement heartbeat monitoring with timeout thresholds—if an agent doesn't report progress within the expected interval, flag it as potentially stalled</div>
<div class="quiz-option">B. Wait indefinitely until the agent eventually produces output</div>
<div class="quiz-option">C. Assume any agent taking more than 1 second is stalled</div>
<div class="quiz-option">D. Only check agent status when a human manually requests it</div>
</div>
<div class="quiz-explanation">The correct answer is A. Heartbeat monitoring with configurable timeouts is the standard approach for detecting stalled agents. The orchestrator expects periodic progress signals and flags agents that miss their reporting window. B risks infinite waits. C is unrealistically short for most agent tasks. D is reactive rather than proactive and could leave stalled agents undetected for long periods.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">47. When retiring an agent from a multi-agent system, what is the MOST important consideration for preserving auditability?</p>
<div class="quiz-options">
<div class="quiz-option">A. Immediately deleting all the agent's historical logs to free storage</div>
<div class="quiz-option">B. Transferring the agent's permissions to another agent</div>
<div class="quiz-option" data-correct="true">C. Archiving the agent's decision logs, configuration, and execution history before decommissioning</div>
<div class="quiz-option">D. Replacing the agent with a human performing the same tasks</div>
</div>
<div class="quiz-explanation">The correct answer is C. Preserving auditability during agent lifecycle changes requires archiving all historical artifacts before decommissioning. This ensures that past decisions can still be traced and audited even after the agent is gone. A destroys the audit trail. B is about access management, not auditability. D is about replacement strategy, not preserving history.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<div class="quiz-scenario">A multi-agent pipeline processes code changes: Agent 1 generates code, Agent 2 writes tests, Agent 3 performs security review. Agent 2 produces tests, but Agent 3's security review reveals a vulnerability in Agent 1's generated code. The fix requires changes that would invalidate Agent 2's tests.</div>
<p class="quiz-stem">48. What is the appropriate recovery pattern for this situation?</p>
<div class="quiz-options">
<div class="quiz-option">A. Skip the security fix and accept the vulnerability to preserve Agent 2's work</div>
<div class="quiz-option">B. Only apply Agent 3's fix and ignore the test failures</div>
<div class="quiz-option" data-correct="true">C. Apply Agent 3's security fix, then re-trigger Agent 2 to regenerate tests for the fixed code, creating a feedback loop</div>
<div class="quiz-option">D. Discard all agent outputs and start the entire pipeline from scratch with new agents</div>
</div>
<div class="quiz-explanation">The correct answer is C. The appropriate recovery is a feedback loop: apply the security fix (higher priority), then re-run the test generation step on the corrected code. This preserves security while maintaining test validity. A accepts known vulnerabilities. B leaves broken tests. D is wasteful—only the affected downstream steps need re-execution, not the entire pipeline.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">49. What is the PRIMARY benefit of post-hoc analysis of multi-agent behavior?</p>
<div class="quiz-options">
<div class="quiz-option">A. It allows agents to modify their own past outputs retroactively</div>
<div class="quiz-option" data-correct="true">B. It enables identification of coordination inefficiencies, repeated work, and interaction patterns that can inform system improvements</div>
<div class="quiz-option">C. It automatically fixes bugs in the agents' code</div>
<div class="quiz-option">D. It replaces the need for real-time monitoring</div>
</div>
<div class="quiz-explanation">The correct answer is B. Post-hoc analysis reviews completed multi-agent executions to find patterns: where did agents duplicate work? Where were handoffs slow? What coordination patterns led to failures? These insights inform systemic improvements. A is impossible—past outputs are immutable. C conflates analysis with automated repair. D is incorrect—post-hoc complements but doesn't replace real-time monitoring.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">50. When adding a new agent to an existing multi-agent system, what should be validated BEFORE the agent begins processing production tasks?</p>
<div class="quiz-options">
<div class="quiz-option">A. That the agent can process tasks faster than all existing agents</div>
<div class="quiz-option" data-correct="true">B. That the new agent's outputs are compatible with downstream agents' expected inputs and that it doesn't create conflicts with existing agents' scopes</div>
<div class="quiz-option">C. That the agent uses the same model version as all other agents</div>
<div class="quiz-option">D. That the agent can access all secrets in the organization</div>
</div>
<div class="quiz-explanation">The correct answer is B. Integration validation ensures the new agent's outputs conform to the format/schema expected by downstream consumers and that its scope doesn't overlap with or conflict with existing agents. A prioritizes speed over correctness. C is unnecessarily restrictive—different agents may use different models. D violates least-privilege principles.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">51. Select ALL that apply: Which are valid recovery patterns when a multi-agent execution partially fails?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Rollback: reverting all changes made by the failed agent and its dependents</div>
<div class="quiz-option" data-correct="true">B. Human-in-the-loop: pausing execution and presenting the failure context to a human for decision</div>
<div class="quiz-option" data-correct="true">C. Retry with modified parameters: re-executing the failed step with adjusted inputs or constraints</div>
<div class="quiz-option">D. Ignore and continue: proceeding with subsequent agents as if the failure didn't occur</div>
</div>
<div class="quiz-explanation">A, B, and C are correct recovery patterns. Rollback (A) ensures consistency by reverting partial changes. Human-in-the-loop (B) leverages human judgment for complex failures. Retry with modifications (C) gives the agent another chance with better inputs. D is dangerous because subsequent agents may depend on the failed step's output, leading to cascading errors.</div>
</div>
</div>

<!-- DOMAIN 6: Implement guardrails and accountability (Questions 52-60) -->

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">52. When classifying agent actions by risk level, which action would be classified as HIGH risk?</p>
<div class="quiz-options">
<div class="quiz-option">A. Reading a public README file from a repository</div>
<div class="quiz-option">B. Creating a new branch from the default branch</div>
<div class="quiz-option" data-correct="true">C. Deleting a production database table</div>
<div class="quiz-option">D. Running a linter on staged files</div>
</div>
<div class="quiz-explanation">The correct answer is C. Deleting a production database table is an irreversible, high-impact action that could cause data loss and service disruption—it's clearly high risk. A is read-only and low risk. B is reversible and low-to-medium risk. D is a non-destructive analysis action and low risk. Risk classification considers irreversibility, blast radius, and environment sensitivity.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">53. What does "least-privilege" mean in the context of AI agent permissions?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent should have no permissions and request them one at a time during execution</div>
<div class="quiz-option" data-correct="true">B. The agent should be granted only the minimum permissions necessary to complete its defined tasks, and no more</div>
<div class="quiz-option">C. The agent should have the same privileges as the least-privileged human user</div>
<div class="quiz-option">D. The agent should have admin privileges but only use them sparingly</div>
</div>
<div class="quiz-explanation">The correct answer is B. Least-privilege means granting exactly the permissions needed for the agent's defined scope of work—nothing more. This limits the blast radius if the agent malfunctions or is compromised. A is impractical and would require dynamic permission escalation. C doesn't consider the agent's specific needs. D is not least-privilege at all—having admin privileges "just in case" violates the principle entirely.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent is configured to automatically merge pull requests that pass all CI checks. A developer accidentally pushes a commit that disables a critical security test. The agent merges the PR because all remaining tests pass.</div>
<p class="quiz-stem">54. Which guardrail would have prevented this issue?</p>
<div class="quiz-options">
<div class="quiz-option">A. Requiring the agent to run tests twice before merging</div>
<div class="quiz-option" data-correct="true">B. Implementing a policy that blocks merges when required security checks are missing or disabled, not just when they fail</div>
<div class="quiz-option">C. Giving the agent access to more repositories for context</div>
<div class="quiz-option">D. Increasing the agent's token limit for longer analysis</div>
</div>
<div class="quiz-explanation">The correct answer is B. The guardrail should verify not just that all checks pass, but that all required checks are present and running. A policy that detects missing/disabled security checks would catch this scenario. A wouldn't help if the test is disabled. C is irrelevant to the merge policy. D doesn't address the missing check detection problem.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">55. Select ALL that apply: Which actions should ALWAYS require human authorization before an AI agent executes them?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Deleting or dropping production data</div>
<div class="quiz-option" data-correct="true">B. Modifying authentication or access control configurations</div>
<div class="quiz-option">C. Creating a new feature branch from the development branch</div>
<div class="quiz-option" data-correct="true">D. Deploying changes to a production environment</div>
<div class="quiz-option">E. Running read-only queries against a staging database</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. These are all irreversible or high-impact actions: production data deletion (A) causes permanent data loss, auth modifications (B) can create security vulnerabilities, and production deployments (D) affect live users. C is a low-risk, reversible operation. E is read-only and non-destructive—both can be safely automated.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">56. What is the concept of "right-sizing human interventions" in agent guardrails?</p>
<div class="quiz-options">
<div class="quiz-option">A. Requiring human approval for every single action the agent takes</div>
<div class="quiz-option">B. Never requiring human approval to maximize agent speed</div>
<div class="quiz-option" data-correct="true">C. Calibrating approval requirements so humans review high-risk actions while low-risk, reversible actions proceed without interruption</div>
<div class="quiz-option">D. Randomly selecting which actions need human approval</div>
</div>
<div class="quiz-explanation">The correct answer is C. Right-sizing means finding the optimal balance—too many approvals create bottlenecks and approval fatigue, too few create risk. The goal is to require human judgment only where it genuinely reduces risk. A causes approval fatigue and slows everything. B is reckless for high-risk actions. D provides no rational basis for intervention decisions.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">57. An agent's guardrails should block actions that violate Responsible AI policies. Which of the following is an example of such a violation?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent creating a pull request with a descriptive title</div>
<div class="quiz-option">B. The agent adding comprehensive code comments</div>
<div class="quiz-option" data-correct="true">C. The agent generating code that collects user data without consent mechanisms or privacy disclosures</div>
<div class="quiz-option">D. The agent suggesting a performance optimization</div>
</div>
<div class="quiz-explanation">The correct answer is C. Generating code that collects user data without consent mechanisms violates Responsible AI principles around privacy and user autonomy. Guardrails should detect and block such outputs. A, B, and D are all legitimate, beneficial agent actions that don't violate any Responsible AI policies.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">58. How should autonomy levels be assigned to different agent operations?</p>
<div class="quiz-options">
<div class="quiz-option">A. All operations should have the same autonomy level for consistency</div>
<div class="quiz-option" data-correct="true">B. Based on a risk assessment that considers the operation's reversibility, blast radius, and compliance implications</div>
<div class="quiz-option">C. Based solely on how fast the operation needs to complete</div>
<div class="quiz-option">D. Based on the day of the week the operation is performed</div>
</div>
<div class="quiz-explanation">The correct answer is B. Autonomy levels should be calibrated by risk: irreversible operations with large blast radius need more human oversight, while reversible, low-impact operations can be fully automated. This is a risk-based approach. A ignores the varying risk profiles of different operations. C and D use irrelevant criteria for determining appropriate oversight levels.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">59. What is the purpose of minimizing approvals that don't reduce risk?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. To prevent approval fatigue, where reviewers rubber-stamp approvals due to excessive volume, actually reducing overall safety</div>
<div class="quiz-option">B. To eliminate human involvement entirely from the SDLC</div>
<div class="quiz-option">C. To reduce the number of humans needed on the team</div>
<div class="quiz-option">D. To allow agents to bypass security policies more easily</div>
</div>
<div class="quiz-explanation">The correct answer is A. When reviewers face too many low-value approval requests, they develop approval fatigue and start rubber-stamping without careful review—paradoxically reducing safety. Eliminating unnecessary approvals keeps reviewers focused on decisions that genuinely matter. B, C, and D mischaracterize the goal—it's about effective human oversight, not removing it.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<div class="quiz-scenario">A company deploys an AI agent that manages infrastructure as code. The agent needs to modify Terraform files and apply changes. The security team wants to ensure the agent cannot accidentally destroy critical infrastructure while still being useful for routine changes.</div>
<p class="quiz-stem">60. What is the BEST guardrail configuration for this agent?</p>
<div class="quiz-options">
<div class="quiz-option">A. Give the agent full Terraform apply permissions and rely on state locking</div>
<div class="quiz-option">B. Restrict the agent to only reading Terraform files with no modify capability</div>
<div class="quiz-option" data-correct="true">C. Allow the agent to modify Terraform files and run plan, but require human approval before apply, with an additional block on any plan that includes resource destruction</div>
<div class="quiz-option">D. Disable all infrastructure automation and require manual changes only</div>
</div>
<div class="quiz-explanation">The correct answer is C. This configuration provides graduated guardrails: the agent can propose changes (modify files, run plan) but cannot execute destructive changes without human approval. Specifically blocking destruction plans adds an extra safety layer for the most dangerous operations. A lacks safeguards for destructive actions. B makes the agent too restricted to be useful. D eliminates automation benefits entirely.</div>
</div>
</div>

