# Mock Exam 4

!!! info "Instructions"
    60 questions • 120 minutes • Score 700/1000 to pass
    This exam follows the official GH-600 domain weightings and question styles.

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">A team wants their coding agent to generate a refactoring plan before making changes. Which configuration separates planning from execution?</div>
<div class="quiz-option" data-correct="false">Allow the agent to plan and execute in a single step for efficiency</div>
<div class="quiz-option" data-correct="true">Configure the agent to output a structured plan as a durable artifact, then require approval before execution begins</div>
<div class="quiz-option" data-correct="false">Disable all agent actions and only use it for suggestions</div>
<div class="quiz-option" data-correct="false">Run the agent in a sandbox where all actions are automatically reversed</div>
<div class="quiz-explanation">The official exam tests your ability to "Configure agent planning to be distinct from agent execution" and "Prevent agent action until the agent checked and approved." A structured plan artifact enables review before irreversible actions occur.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization notices their agent frequently creates overly complex solutions, adding unnecessary abstractions and files that weren't requested.</div>
<div class="quiz-stem">Which anti-pattern is being exhibited, and how should it be mitigated?</div>
<div class="quiz-option" data-correct="false">Tool misuse — restrict the agent's file creation permissions</div>
<div class="quiz-option" data-correct="true">Scope creep — define explicit success criteria and outputs in the agent's instructions, and validate the plan against those criteria before execution</div>
<div class="quiz-option" data-correct="false">Hallucination — switch to a more capable model</div>
<div class="quiz-option" data-correct="false">Context overflow — reduce the agent's memory window</div>
<div class="quiz-explanation">The exam covers "Identify and mitigate common anti-patterns in agents." Scope creep occurs when agents exceed their defined task boundaries. The fix is clear success criteria and pre-execution plan validation.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which approach correctly configures human intervention for an autonomous agent without slowing delivery?</div>
<div class="quiz-option" data-correct="false">Require human approval for every agent action</div>
<div class="quiz-option" data-correct="false">Remove all human oversight to maximize speed</div>
<div class="quiz-option" data-correct="true">Classify actions by risk level — auto-approve low-risk actions (read, lint), require approval only for high-risk actions (deploy, delete), and produce inspectable artifacts for async review</div>
<div class="quiz-option" data-correct="false">Run all agent actions during off-hours when no humans are available</div>
<div class="quiz-explanation">The exam tests "Configure human intervention for autonomous agents without slowing delivery." Risk-based approval gates balance speed and safety — only high-impact actions need synchronous human approval.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What does it mean to configure an agent to produce "inspectable artifacts within standard development tooling"?</div>
<div class="quiz-option" data-correct="false">The agent must generate PDF reports after each task</div>
<div class="quiz-option" data-correct="true">The agent records its plans, decisions, and actions as pull request comments, commit messages, workflow logs, or issue updates — artifacts developers already review in their normal workflow</div>
<div class="quiz-option" data-correct="false">The agent must create a separate dashboard application</div>
<div class="quiz-option" data-correct="false">The agent must email the team lead after each operation</div>
<div class="quiz-explanation">The exam requires "Configure agent to produce inspectable artifacts within standard development tooling." This means using existing GitHub artifacts (PRs, commits, Actions logs) rather than requiring teams to adopt new tools for agent observability.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which are valid inputs, outputs, or success criteria when defining an agent task? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Input: a GitHub issue describing the feature to implement</div>
<div class="quiz-option" data-correct="true">Output: a pull request with passing CI checks</div>
<div class="quiz-option" data-correct="true">Success criteria: all existing tests continue to pass and new tests cover the added code</div>
<div class="quiz-option" data-correct="false">Success criteria: the agent completes the task as fast as possible regardless of quality</div>
<div class="quiz-option" data-correct="true">Input: custom instructions file specifying coding standards</div>
<div class="quiz-explanation">The exam covers "Define inputs, outputs, and success criteria for agents." Speed alone is never a valid success criterion — quality, correctness, and test coverage matter. Issues, instruction files, PRs with CI, and test pass rates are all valid.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team configures an agent to validate its own plan before execution. The validation step checks that the plan doesn't modify files outside the assigned directory scope and doesn't exceed 5 file changes.</div>
<div class="quiz-stem">What is this practice called?</div>
<div class="quiz-option" data-correct="false">Post-execution auditing</div>
<div class="quiz-option" data-correct="true">Pre-execution plan validation with defined constraints</div>
<div class="quiz-option" data-correct="false">Runtime sandboxing</div>
<div class="quiz-option" data-correct="false">Continuous integration testing</div>
<div class="quiz-explanation">The exam covers "Validate agent plans" and "Prevent agent action until the agent checked and approved." Pre-execution validation enforces constraints before any changes happen, reducing risk of overreach.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which is an anti-pattern when integrating agents into the SDLC?</div>
<div class="quiz-option" data-correct="false">Having the agent create branches for its work</div>
<div class="quiz-option" data-correct="false">Requiring code review on agent-generated PRs</div>
<div class="quiz-option" data-correct="true">Allowing the agent to merge its own pull requests to main without any human review</div>
<div class="quiz-option" data-correct="false">Running the agent's output through CI before merging</div>
<div class="quiz-explanation">Allowing agents to merge their own PRs without review bypasses the standard SDLC control. Even high-confidence agent output should pass through human review gates for production branches.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When planning graduated autonomy for an agent, what is the recommended starting point?</div>
<div class="quiz-option" data-correct="true">Start with advisory mode (suggest-only), then progressively grant execution permissions as trust is established through successful outcomes</div>
<div class="quiz-option" data-correct="false">Start with full autonomy and restrict permissions only after failures occur</div>
<div class="quiz-option" data-correct="false">Give full autonomy on development branches and no autonomy on main</div>
<div class="quiz-option" data-correct="false">Autonomy level should be fixed and never change</div>
<div class="quiz-explanation">The exam covers "Plan and implement the degree of agent autonomy, including guardrails." Graduated autonomy starts conservative and expands based on demonstrated reliability — the opposite of granting full access then reacting to failures.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A DevOps team wants to use an agent to automatically triage incoming bug reports. The agent should label issues, assign priority, and suggest an owner — but should NOT close issues or modify code.</div>
<div class="quiz-stem">How should the agent's boundaries be defined?</div>
<div class="quiz-option" data-correct="false">Give the agent full repository admin access and trust it won't close issues</div>
<div class="quiz-option" data-correct="true">Define explicit inputs (issue body, repo metadata), permitted actions (add labels, set priority field, comment with owner suggestion), and forbidden actions (close issue, push code, modify branch protections)</div>
<div class="quiz-option" data-correct="false">Only allow the agent to read issues, not modify them at all</div>
<div class="quiz-option" data-correct="false">Let the agent decide its own scope based on the issue content</div>
<div class="quiz-explanation">Defining explicit permitted and forbidden actions is how you "Identify steps for agents to perform" while maintaining appropriate boundaries. The agent should have exactly the permissions it needs — no more.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the purpose of requiring an agent to output a structured plan before execution?</div>
<div class="quiz-option" data-correct="false">To slow down the agent and reduce compute costs</div>
<div class="quiz-option" data-correct="false">To generate documentation automatically</div>
<div class="quiz-option" data-correct="true">To make the agent's intended actions transparent and reviewable, enabling humans to catch errors or scope violations before irreversible changes occur</div>
<div class="quiz-option" data-correct="false">To train the agent on better planning strategies</div>
<div class="quiz-explanation">Structured plans serve observability and control. They allow humans or automated validators to inspect intent before action, catching problems early when they're cheap to fix.</div>
</div>
</div>



<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How do you configure an MCP allow list for a GitHub Copilot agent?</div>
<div class="quiz-option" data-correct="false">Add allowed servers to the repository's README</div>
<div class="quiz-option" data-correct="true">Define the allowed MCP servers in the agent's configuration, specifying which servers the agent is permitted to connect to — blocking connections to any unlisted servers</div>
<div class="quiz-option" data-correct="false">MCP servers are always allowed by default and cannot be restricted</div>
<div class="quiz-option" data-correct="false">Configure the allow list in the GitHub organization's billing settings</div>
<div class="quiz-explanation">MCP allow lists restrict which servers an agent can connect to. Only explicitly listed servers are permitted, following the principle of least privilege for external tool access.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What distinguishes a GitHub remote MCP server from a local (stdio) MCP server?</div>
<div class="quiz-option" data-correct="false">Remote servers are faster than local servers</div>
<div class="quiz-option" data-correct="true">Remote MCP servers run as hosted services accessible over HTTP/SSE, enabling shared access across team members without local installation, while stdio servers run as local processes on the developer's machine</div>
<div class="quiz-option" data-correct="false">Local servers support more tools than remote servers</div>
<div class="quiz-option" data-correct="false">Remote servers don't require authentication</div>
<div class="quiz-explanation">GitHub remote MCP servers are hosted services that the team shares. They communicate over HTTP/SSE (requiring TLS and auth), unlike local stdio servers that run per-developer as child processes communicating via stdin/stdout.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team configures their agent to work within a CI workflow. The agent should only modify files in the `src/` directory and only on feature branches, never on `main`.</div>
<div class="quiz-stem">Which configurations enforce these constraints?</div>
<div class="quiz-option" data-correct="false">Add a comment in the agent's prompt asking it to stay in src/</div>
<div class="quiz-option" data-correct="true">Configure the agent's scope to the specific repository with branch-based filtering (exclude main), and restrict file system permissions to the src/ directory path</div>
<div class="quiz-option" data-correct="false">Only run the agent on a fork of the repository</div>
<div class="quiz-option" data-correct="false">Use a post-commit hook to revert changes outside src/</div>
<div class="quiz-explanation">The exam covers "Configure an agent's scope to a specific repository" and "Configure an agent to use branch-based scope." Proper scoping uses configuration-level constraints, not prompt-level suggestions that can be ignored.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When implementing error handling for an agent tool call that fails, what is the correct escalation order?</div>
<div class="quiz-option" data-correct="false">Immediately alert the user on any failure</div>
<div class="quiz-option" data-correct="true">Retry with backoff → attempt alternative tool/approach → rollback changes → escalate to human with context</div>
<div class="quiz-option" data-correct="false">Retry indefinitely until the operation succeeds</div>
<div class="quiz-option" data-correct="false">Skip the failed step and continue with the next task</div>
<div class="quiz-explanation">The exam covers "Implement error handling, retries, rollbacks, escalation paths." The correct order is: retry (transient failures), alternative approach (systematic failures), rollback (prevent partial states), then human escalation with full context.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What does "traceability and accountability for agent actions" require?</div>
<div class="quiz-option" data-correct="false">Recording only whether the agent succeeded or failed</div>
<div class="quiz-option" data-correct="true">Recording each tool call with its parameters, results, timestamps, the decision reasoning, and the identity of who triggered the agent — enabling full reconstruction of what happened and why</div>
<div class="quiz-option" data-correct="false">Storing the complete model weights used for each decision</div>
<div class="quiz-option" data-correct="false">Only logging actions that resulted in errors</div>
<div class="quiz-explanation">Traceability means you can reconstruct the full chain: who initiated it, what the agent planned, which tools it called with what parameters, what results it got, and what decisions it made. This is essential for debugging and compliance.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which are valid ways to configure an agent to be invoked in a CI workflow? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">As a GitHub Actions step that triggers on pull_request events</div>
<div class="quiz-option" data-correct="true">As a workflow_dispatch triggered step for on-demand agent execution</div>
<div class="quiz-option" data-correct="true">As a scheduled workflow step for periodic maintenance tasks</div>
<div class="quiz-option" data-correct="false">By committing the agent's API key directly in the workflow YAML</div>
<div class="quiz-option" data-correct="true">Triggered by issue_comment events for conversational invocation</div>
<div class="quiz-explanation">Agents can be invoked via pull_request, workflow_dispatch, schedule, or issue_comment triggers. API keys should never be committed directly — use GitHub Secrets instead.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should an agent handle environment-specific constraints when operating across development, staging, and production?</div>
<div class="quiz-option" data-correct="false">Use the same configuration for all environments</div>
<div class="quiz-option" data-correct="true">Configure environment-aware permissions — broader autonomy in dev, restricted write access in staging, read-only or no access in production — with environment variables controlling behavior</div>
<div class="quiz-option" data-correct="false">Only allow agents to operate in development environments</div>
<div class="quiz-option" data-correct="false">Use different agents for each environment with no shared configuration</div>
<div class="quiz-explanation">The exam covers "Configure an agent to handle environment-specific constraints." Agents should have progressively restricted permissions as environments approach production, controlled via environment configuration.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the correct way to add an MCP server as a tool to a GitHub Copilot agent?</div>
<div class="quiz-option" data-correct="false">Install the MCP server globally on the machine and it's automatically detected</div>
<div class="quiz-option" data-correct="true">Declare the MCP server in the agent's configuration file (e.g., `.github/copilot-agents.yml` or VS Code settings), specifying the server command/URL and any required environment variables</div>
<div class="quiz-option" data-correct="false">Ask Copilot in chat to connect to the MCP server</div>
<div class="quiz-option" data-correct="false">MCP servers are built into Copilot and don't need configuration</div>
<div class="quiz-explanation">Adding MCP servers requires explicit configuration declaring the server endpoint (command for stdio, URL for remote), required credentials (via environment variables), and scope. It's not automatic discovery.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent attempts to push code to a protected branch. The push is rejected by branch protection rules.</div>
<div class="quiz-stem">What is the correct agent behavior?</div>
<div class="quiz-option" data-correct="false">Retry the push with elevated permissions</div>
<div class="quiz-option" data-correct="false">Disable branch protection temporarily</div>
<div class="quiz-option" data-correct="true">Create a new feature branch, push the changes there, and open a pull request targeting the protected branch — following the standard PR workflow</div>
<div class="quiz-option" data-correct="false">Report failure and stop without attempting alternatives</div>
<div class="quiz-explanation">Agents should work within existing repository controls, not circumvent them. Creating a branch and PR is the standard workflow that respects branch protections while still enabling autonomous work. The exam tests "Enable an agent to perform autonomous actions, including creating branches and pull requests."</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When configuring tool permissions for an agent, what does the principle of minimum required permissions mean?</div>
<div class="quiz-option" data-correct="false">Give the agent access to all tools and let it decide which to use</div>
<div class="quiz-option" data-correct="true">Only enable the specific tools the agent needs for its defined task — a code review agent gets read access to files and PR comment ability, but not write access to code or merge permissions</div>
<div class="quiz-option" data-correct="false">Remove all tool access and only allow text generation</div>
<div class="quiz-option" data-correct="false">Grant permissions based on the model's capability level</div>
<div class="quiz-explanation">The exam covers "Configure agent tool permissions." Minimum required permissions means each agent gets exactly the tools it needs — no more. A review agent needs to read and comment, not write or merge.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the purpose of MCP registries?</div>
<div class="quiz-option" data-correct="false">To store agent conversation history</div>
<div class="quiz-option" data-correct="true">To provide a catalog of available MCP servers that agents can discover and connect to, enabling centralized management of approved tool integrations</div>
<div class="quiz-option" data-correct="false">To register domain names for MCP endpoints</div>
<div class="quiz-option" data-correct="false">To track billing for MCP server usage</div>
<div class="quiz-explanation">MCP registries serve as catalogs of approved MCP servers. They enable teams to manage which integrations are available, control versioning, and provide discoverability for agents configured with the registry.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent is configured to perform automated dependency updates. During execution, a package installation fails due to a network timeout.</div>
<div class="quiz-stem">What is the correct retry implementation?</div>
<div class="quiz-option" data-correct="true">Retry with exponential backoff (e.g., 1s, 2s, 4s), set a maximum retry count (e.g., 3 attempts), and if all retries fail, rollback any partial changes and report the failure with context</div>
<div class="quiz-option" data-correct="false">Retry immediately 100 times until it succeeds</div>
<div class="quiz-option" data-correct="false">Skip the dependency and continue with the rest of the update</div>
<div class="quiz-option" data-correct="false">Switch to a different package manager automatically</div>
<div class="quiz-explanation">Proper retry implementation uses exponential backoff to avoid overwhelming the service, caps retries to prevent infinite loops, and rolls back partial state on final failure. The exam explicitly tests "Implement retries" and "Implement rollbacks."</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should an agent implement rollback when a multi-step operation partially fails?</div>
<div class="quiz-option" data-correct="false">Delete the entire repository and restore from backup</div>
<div class="quiz-option" data-correct="true">Track each completed step with its inverse operation, then execute inverse operations in reverse order to restore the system to its pre-execution state</div>
<div class="quiz-option" data-correct="false">Leave the system in the partial state and notify the user</div>
<div class="quiz-option" data-correct="false">Rollback is not possible for agent operations</div>
<div class="quiz-explanation">The exam covers "Implement rollbacks." Proper rollback tracks each action's inverse (e.g., file created → delete file, branch created → delete branch) and applies them in reverse order. This is the compensating transaction pattern.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the execution context for an agent, and why does evaluating it matter?</div>
<div class="quiz-option" data-correct="false">The execution context is the LLM model version being used</div>
<div class="quiz-option" data-correct="true">The execution context includes the repository state, branch, available tools, permissions, environment variables, and runtime constraints — evaluating it ensures the agent operates with correct assumptions about its environment</div>
<div class="quiz-option" data-correct="false">The execution context is the user's IDE theme and settings</div>
<div class="quiz-option" data-correct="false">The execution context only matters for debugging, not during normal operation</div>
<div class="quiz-explanation">The exam covers "Evaluate the execution context for an agent." Context includes everything the agent can access and interact with. Mismatched context (wrong branch, missing permissions, stale state) leads to failures or incorrect actions.</div>
</div>
</div>



<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the difference between short-term, long-term, and external memory for an agent?</div>
<div class="quiz-option" data-correct="false">They differ only in storage capacity</div>
<div class="quiz-option" data-correct="true">Short-term memory is the current conversation/task context window; long-term memory persists across sessions (e.g., learned preferences); external memory uses outside systems like databases or files to store and retrieve information</div>
<div class="quiz-option" data-correct="false">Short-term is RAM, long-term is disk, external is cloud</div>
<div class="quiz-option" data-correct="false">All three types are identical but stored in different locations</div>
<div class="quiz-explanation">The exam tests "Choose between short-term, long-term, and external memory." Short-term = within-session context; long-term = cross-session persistence (preferences, patterns); external = systems of record (databases, files, APIs) the agent queries.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent working on a large refactoring task has been running for 45 minutes. You notice it's now making changes that contradict decisions it made 30 minutes ago — renaming variables back to their original names.</div>
<div class="quiz-stem">What is happening and how should it be addressed?</div>
<div class="quiz-option" data-correct="false">The model is producing random outputs — restart it</div>
<div class="quiz-option" data-correct="true">Context drift — the agent's earlier decisions have fallen out of its context window. Fix: capture key decisions as durable artifacts (e.g., a decision log file) that the agent references, and implement drift detection that flags contradictory actions</div>
<div class="quiz-option" data-correct="false">The agent is testing different approaches — let it continue</div>
<div class="quiz-option" data-correct="false">Increase the model's temperature setting</div>
<div class="quiz-explanation">The exam covers "Detect and correct drift during extended agent execution." Context drift occurs when earlier context is lost. The fix is persisting decisions externally and checking new actions against prior decisions.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should agent memory be scoped to task-relevant information?</div>
<div class="quiz-option" data-correct="false">Include the entire repository history in the agent's context</div>
<div class="quiz-option" data-correct="true">Filter memory to include only information relevant to the current task — the specific files being modified, related test files, relevant documentation, and prior decisions for this task — excluding unrelated project context</div>
<div class="quiz-option" data-correct="false">Clear all memory at the start of each task</div>
<div class="quiz-option" data-correct="false">Let the agent decide what to remember without constraints</div>
<div class="quiz-explanation">The exam covers "Scope agent memory to task-relevant information." Effective scoping maximizes signal-to-noise — the agent sees what it needs without being overwhelmed by irrelevant context that could confuse it.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When should agent memory be pruned or reset?</div>
<div class="quiz-option" data-correct="true">When the task is complete (prune task-specific details), when memory becomes stale (outdated file references), or when accumulated context causes confusion or contradictions</div>
<div class="quiz-option" data-correct="false">Never — all memory should be preserved indefinitely</div>
<div class="quiz-option" data-correct="false">After every single agent action</div>
<div class="quiz-option" data-correct="false">Only when the user manually requests it</div>
<div class="quiz-explanation">The exam covers "Define memory expiration, pruning, and reset rules." Memory should be pruned when task-complete (retain learnings, discard working details), when stale (references to deleted files), or when contradictory (conflicting context causing errors).</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent is interrupted mid-task after completing 3 of 5 steps. When resumed the next day, it needs to continue from step 4 without repeating steps 1-3 or making decisions that conflict with its earlier work.</div>
<div class="quiz-stem">What mechanism enables this?</div>
<div class="quiz-option" data-correct="false">Replay the entire conversation from the beginning</div>
<div class="quiz-option" data-correct="true">Capture task progress and decisions as durable artifacts (e.g., a state file recording completed steps, their outcomes, and key decisions), allowing the agent to resume by reading this checkpoint</div>
<div class="quiz-option" data-correct="false">Store the complete model state and restore it</div>
<div class="quiz-option" data-correct="false">Ask the user to summarize what happened before</div>
<div class="quiz-explanation">The exam covers "Capture task progress and decisions as durable artifacts" and "Resume agent work without repeating steps or diverging from prior decisions." Checkpointing to durable artifacts (files, issues, PR descriptions) enables reliable resumption.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How do you prevent conflicting context when multiple agents or tools share state?</div>
<div class="quiz-option" data-correct="false">Give each agent its own copy of all state and never synchronize</div>
<div class="quiz-option" data-correct="true">Use a single source of truth (e.g., a shared state file or database), implement read/write coordination (locking or turn-based access), and validate state consistency before each agent acts</div>
<div class="quiz-option" data-correct="false">Only allow one agent to run at a time across the entire organization</div>
<div class="quiz-option" data-correct="false">Conflicting context is acceptable and doesn't need prevention</div>
<div class="quiz-explanation">The exam covers "Prevent conflicting context." Shared state requires coordination — a single source of truth prevents divergence, and consistency checks before action catch conflicts early.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What causes stale context in an agent, and how is it prevented?</div>
<div class="quiz-option" data-correct="false">Stale context is caused by slow network connections</div>
<div class="quiz-option" data-correct="true">Stale context occurs when the agent's memory references information that has changed (files modified by others, merged PRs, updated configs). Prevention: refresh state from source before acting, use timestamps/hashes to detect staleness, and invalidate cached context on relevant events</div>
<div class="quiz-option" data-correct="false">Stale context only happens with long-term memory, never short-term</div>
<div class="quiz-option" data-correct="false">Stale context is prevented by using a larger context window</div>
<div class="quiz-explanation">The exam covers "Prevent stale context." Context becomes stale when the real world changes but the agent's memory doesn't update. Prevention uses freshness checks (timestamps, git hashes) and event-driven invalidation.</div>
</div>
</div>

<div class="quiz" data-domain="Memory, State & Execution" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which are valid strategies for sharing agent state across tools and environments? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Writing state to a shared file in the repository (e.g., `.agent-state.json`)</div>
<div class="quiz-option" data-correct="true">Using GitHub Actions artifacts to pass state between workflow jobs</div>
<div class="quiz-option" data-correct="true">Storing state in PR descriptions or issue comments as structured data</div>
<div class="quiz-option" data-correct="false">Embedding state in the model's system prompt permanently</div>
<div class="quiz-option" data-correct="true">Using an external database or key-value store accessible to all agents</div>
<div class="quiz-explanation">The exam covers "Share agent state." Valid approaches use durable, accessible storage: repo files, workflow artifacts, PR/issue metadata, or external stores. Embedding in the system prompt is not durable and has size limits.</div>
</div>
</div>



<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the difference between qualitative and quantitative evaluation signals for agent tasks?</div>
<div class="quiz-option" data-correct="false">Qualitative signals are more important than quantitative ones</div>
<div class="quiz-option" data-correct="true">Quantitative signals are measurable metrics (test pass rate, code coverage, build success, latency); qualitative signals require human judgment (code readability, architectural appropriateness, adherence to team conventions)</div>
<div class="quiz-option" data-correct="false">Quantitative signals only apply to performance, qualitative only to security</div>
<div class="quiz-option" data-correct="false">They are the same thing measured differently</div>
<div class="quiz-explanation">The exam covers "Identify qualitative and quantitative evaluation signals to evaluate agents." Both types are needed — quantitative for automated assessment, qualitative for aspects that require human expertise.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent consistently generates code that passes all tests but reviewers reject 40% of its PRs for poor variable naming and inconsistent patterns with the existing codebase.</div>
<div class="quiz-stem">How should this be classified and addressed?</div>
<div class="quiz-option" data-correct="false">This is a tool misuse issue — restrict write access</div>
<div class="quiz-option" data-correct="true">The evaluation criteria are misaligned with development intent. Fix: add team coding conventions and style examples to the agent's instructions, include naming pattern references, and add a qualitative "style consistency" evaluation signal</div>
<div class="quiz-option" data-correct="false">This is acceptable — tests passing means the code is correct</div>
<div class="quiz-option" data-correct="false">Replace the model with a newer version</div>
<div class="quiz-explanation">The exam covers "Align evaluation criteria with development intent." Tests measure correctness, but development intent also includes style, conventions, and maintainability. The fix is tuning instructions and adding qualitative evaluation signals.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which automated scanning tools can generate evaluation signals for agent outputs?</div>
<div class="quiz-option" data-correct="false">Only manual code review can evaluate agent outputs</div>
<div class="quiz-option" data-correct="true">Linters (style compliance), SAST/DAST (security), test runners (correctness), coverage tools (completeness), dependency scanners (supply chain safety), and GitHub code scanning (vulnerability detection)</div>
<div class="quiz-option" data-correct="false">Only the same LLM that generated the code can evaluate it</div>
<div class="quiz-option" data-correct="false">Scanning tools cannot be used to evaluate AI-generated code</div>
<div class="quiz-explanation">The exam covers "Generate evaluation signals by using automated scanning tools." Existing CI/CD scanning tools provide objective, automated evaluation signals that complement human review.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">When analyzing agent failures, which root cause categories should be considered? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Reasoning errors — the agent misunderstood the task or made incorrect logical deductions</div>
<div class="quiz-option" data-correct="true">Tool misuse — the agent called the wrong tool or used incorrect parameters</div>
<div class="quiz-option" data-correct="true">Context issues — the agent had stale, missing, or incorrect context information</div>
<div class="quiz-option" data-correct="true">Environment issues — external systems were unavailable, permissions were wrong, or resources were exhausted</div>
<div class="quiz-option" data-correct="false">Model laziness — the agent intentionally chose not to work</div>
<div class="quiz-explanation">The exam explicitly lists root cause categories: "reasoning errors, tool misuse, and context or environment issues." These cover the full spectrum from agent logic problems to external system failures.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent's log shows: 1) Read file `config.yaml` 2) Parsed database URL 3) Called `deploy_to_production` tool 4) Error: "Permission denied." The agent then retried 5 times before failing.</div>
<div class="quiz-stem">What is the root cause category and what should be tuned?</div>
<div class="quiz-option" data-correct="false">Reasoning error — the agent shouldn't have tried to deploy</div>
<div class="quiz-option" data-correct="true">Environment issue (missing permissions). Tuning: add pre-flight permission checks before attempting restricted operations, and implement an escalation path instead of blind retries for permission errors</div>
<div class="quiz-option" data-correct="false">Tool misuse — the agent used the wrong tool</div>
<div class="quiz-option" data-correct="false">Context issue — the config file was wrong</div>
<div class="quiz-explanation">Permission denied is an environment issue — the agent's reasoning and tool selection were correct, but the environment lacked required permissions. Tuning should add pre-checks and differentiate retriable errors (network timeout) from non-retriable ones (permission denied).</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How do you identify agent failures using workflow artifacts?</div>
<div class="quiz-option" data-correct="false">Only check the final success/failure status of the workflow</div>
<div class="quiz-option" data-correct="true">Examine logs (step-by-step execution), plans (intended vs. actual actions), traces (tool call sequences with parameters and results), outputs (generated code/artifacts), and compare against expected outcomes at each step</div>
<div class="quiz-option" data-correct="false">Ask the agent to explain why it failed</div>
<div class="quiz-option" data-correct="false">Re-run the workflow — if it passes on retry, ignore the failure</div>
<div class="quiz-explanation">The exam covers "Identify failures by using logs, plans, traces, outputs, and workflow artifacts." Multi-signal analysis is needed: logs show execution, plans show intent, traces show tool interactions, outputs show results. Comparing at each step localizes the failure point.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">After evaluation reveals an agent frequently calls the wrong tool for database queries, which tuning approach is most appropriate?</div>
<div class="quiz-option" data-correct="false">Remove all database tools from the agent</div>
<div class="quiz-option" data-correct="true">Refine tool access — clarify tool descriptions so the agent can distinguish between them, add usage examples in tool documentation, and potentially consolidate similar tools to reduce confusion</div>
<div class="quiz-option" data-correct="false">Increase the agent's context window size</div>
<div class="quiz-option" data-correct="false">Add more tools to give the agent more options</div>
<div class="quiz-explanation">The exam covers "Refine tool usage and tool access" as a tuning strategy. When tool misuse is the root cause, the fix is better tool descriptions, clearer differentiation, and potentially simplifying the tool set.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What does "revise instructions, workflows, or constraints" mean as a tuning strategy?</div>
<div class="quiz-option" data-correct="true">Update the agent's system instructions to be clearer, modify workflow steps to add validation checkpoints, or adjust constraints to be more specific — based on patterns observed in evaluation failures</div>
<div class="quiz-option" data-correct="false">Completely rewrite the agent from scratch after each failure</div>
<div class="quiz-option" data-correct="false">Add more constraints until the agent can barely do anything</div>
<div class="quiz-option" data-correct="false">Remove all instructions and let the agent figure things out</div>
<div class="quiz-explanation">The exam covers "Revise instructions, workflows, or constraints." This is iterative tuning — observe failure patterns, then make targeted adjustments to instructions (clearer guidance), workflows (add checkpoints), or constraints (tighter scope) to prevent recurrence.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team evaluates their agent and finds it performs perfectly on their test cases but poorly on real-world tasks from the team.</div>
<div class="quiz-stem">What is the likely issue?</div>
<div class="quiz-option" data-correct="false">The model needs more training data</div>
<div class="quiz-option" data-correct="true">The evaluation set is not representative of real usage — the agent may be effectively "overfitting" to the test scenarios. The evaluation criteria need to be diversified to match actual development patterns</div>
<div class="quiz-option" data-correct="false">Real-world tasks are simply too hard for any agent</div>
<div class="quiz-option" data-correct="false">The team is using the agent incorrectly</div>
<div class="quiz-explanation">This is evaluation set overfitting — the test scenarios don't represent real usage diversity. Evaluation signals must be aligned with actual development intent and cover the range of real-world scenarios.</div>
</div>
</div>

<div class="quiz" data-domain="Evaluation & Tuning" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When tuning agent memory usage based on evaluation results, which approach is correct?</div>
<div class="quiz-option" data-correct="false">Always maximize memory — more context is always better</div>
<div class="quiz-option" data-correct="true">Analyze whether failures correlate with missing context (add relevant memory) or context overload (prune irrelevant memory), and adjust scoping rules to include what's needed while excluding noise</div>
<div class="quiz-option" data-correct="false">Set memory to a fixed size regardless of task type</div>
<div class="quiz-option" data-correct="false">Disable all memory between tasks</div>
<div class="quiz-explanation">The exam covers "Refine memory usage" as a tuning strategy. The right amount of memory depends on the task — too little causes missing-context failures, too much causes confusion. Evaluation results reveal which direction to tune.</div>
</div>
</div>



<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which orchestration pattern has a central agent that decomposes work and delegates subtasks to specialized agents, then assembles their outputs?</div>
<div class="quiz-option" data-correct="false">Pipeline pattern</div>
<div class="quiz-option" data-correct="true">Orchestrator-worker pattern</div>
<div class="quiz-option" data-correct="false">Fan-out/fan-in pattern</div>
<div class="quiz-option" data-correct="false">Consensus pattern</div>
<div class="quiz-explanation">Orchestrator-worker has a central coordinator that plans, delegates, and assembles. Pipeline is sequential handoff. Fan-out/fan-in is parallel but without central planning. Consensus requires agreement among peers.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What does "agent isolation for parallel execution" mean?</div>
<div class="quiz-option" data-correct="false">Agents cannot communicate with each other at all</div>
<div class="quiz-option" data-correct="true">Each parallel agent operates in its own execution context (separate branches, sandboxed workspaces, or isolated file sets) to prevent interference — their outputs are merged or reconciled after completion</div>
<div class="quiz-option" data-correct="false">Only one agent can run at a time across the system</div>
<div class="quiz-option" data-correct="false">Agents are isolated on different physical machines</div>
<div class="quiz-explanation">The exam covers "Configure agent isolation for parallel execution." Isolation means each agent has its own workspace so parallel execution doesn't create conflicts (e.g., two agents editing the same file simultaneously).</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">Two agents working in parallel both modify the same utility function — one adds error handling, the other refactors its signature. When their branches are merged, there's a conflict.</div>
<div class="quiz-stem">How should this conflict be detected and resolved?</div>
<div class="quiz-option" data-correct="false">Always accept the most recent change</div>
<div class="quiz-option" data-correct="true">Detect overlapping changes during merge (file-level or function-level conflict detection), then either: automatically merge if changes are compatible, escalate to a coordinator agent or human if they conflict, or rollback one agent's work and re-run with the other's output as context</div>
<div class="quiz-option" data-correct="false">Delete both agents' work and start over</div>
<div class="quiz-option" data-correct="false">Merge conflicts are impossible with proper agent configuration</div>
<div class="quiz-explanation">The exam covers "Detect and resolve agent conflicts, including overlapping code changes." Multi-level resolution: detect (merge tools), auto-resolve (compatible changes), escalate (conflicting changes), or sequence (re-run with merged context).</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What should multi-agent workflows produce for observability and audit?</div>
<div class="quiz-option" data-correct="false">Only the final merged output</div>
<div class="quiz-option" data-correct="true">Per-agent decision logs with correlation IDs linking related actions across agents, documented handoffs between agents, key decision points, and final outcomes — all suitable for post-hoc review and audit</div>
<div class="quiz-option" data-correct="false">A single combined log file with all agent outputs mixed together</div>
<div class="quiz-option" data-correct="false">Observability is only needed for single-agent workflows</div>
<div class="quiz-explanation">The exam covers "Configure multi-agent workflows to produce artifacts suitable for review and audit" and "Document key decisions, handoffs, and outcomes across agents." Correlation IDs are essential for tracing actions across multiple agents.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">In a multi-agent pipeline, Agent A (code generation) completes successfully, Agent B (testing) finds issues, but Agent C (deployment) has already started because of a race condition.</div>
<div class="quiz-stem">What recovery pattern should be applied?</div>
<div class="quiz-option" data-correct="false">Let Agent C complete the deployment anyway</div>
<div class="quiz-option" data-correct="true">Implement a rollback pattern: halt Agent C immediately, rollback any partial deployment actions, return the system to the state before Agent C started, then fix the race condition by adding proper sequencing gates between agents</div>
<div class="quiz-option" data-correct="false">Restart all three agents from the beginning</div>
<div class="quiz-option" data-correct="false">Only notify the team without taking corrective action</div>
<div class="quiz-explanation">The exam covers "Implement multi-agent recovery patterns, including rollback and human-in-the-loop." The immediate fix is rollback of the incorrectly-started agent. The systemic fix is proper sequencing gates to prevent the race condition.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How do you add a new agent to an existing multi-agent workflow without disrupting active workflows?</div>
<div class="quiz-option" data-correct="true">Deploy the new agent alongside existing ones in a shadow/observation mode first, validate its outputs don't conflict with existing agents, then gradually integrate it into the workflow with feature flags or progressive rollout</div>
<div class="quiz-option" data-correct="false">Stop all existing workflows, add the new agent, and restart everything</div>
<div class="quiz-option" data-correct="false">Immediately add the agent to the production workflow</div>
<div class="quiz-option" data-correct="false">New agents cannot be added to existing workflows</div>
<div class="quiz-explanation">The exam covers "Add agents to existing multi-agent workflows." Safe addition uses progressive deployment: observe first, validate compatibility, then integrate gradually — never disrupting running workflows.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When retiring an agent from a multi-agent workflow, what must be preserved?</div>
<div class="quiz-option" data-correct="false">Nothing — just remove it and let other agents adapt</div>
<div class="quiz-option" data-correct="true">Auditability (logs and artifacts from past executions remain accessible), workflow continuity (other agents aren't broken by the removal), and any state the retired agent managed must be migrated or archived</div>
<div class="quiz-option" data-correct="false">Only the agent's source code needs to be preserved</div>
<div class="quiz-option" data-correct="false">The agent should be kept running indefinitely instead of retiring it</div>
<div class="quiz-explanation">The exam covers "Retire agents while preserving auditability and workflow continuity." Retirement requires: archive historical artifacts, migrate responsibilities, ensure dependent agents have alternatives, and maintain audit trail.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How do you identify a stalled agent execution in a multi-agent workflow?</div>
<div class="quiz-option" data-correct="false">Wait until the user complains about missing results</div>
<div class="quiz-option" data-correct="true">Monitor execution time against expected duration thresholds, check for progress signals (tool calls, artifact updates), and flag agents that exceed time limits or stop producing observable activity</div>
<div class="quiz-option" data-correct="false">Stalled agents will always throw an error</div>
<div class="quiz-option" data-correct="false">Check if the agent's CPU usage is zero</div>
<div class="quiz-explanation">The exam covers "Identify failed, partial, or stalled agent executions." Stall detection requires active monitoring: timeout thresholds, progress heartbeats, and activity signals. Stalls are silent failures that don't produce errors.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the fan-out/fan-in orchestration pattern?</div>
<div class="quiz-option" data-correct="false">A single agent processes tasks sequentially</div>
<div class="quiz-option" data-correct="true">Work is split into independent subtasks (fan-out) executed in parallel by multiple agents, then results are collected and combined (fan-in) — useful when subtasks don't depend on each other</div>
<div class="quiz-option" data-correct="false">Agents vote on the correct output</div>
<div class="quiz-option" data-correct="false">Each agent's output becomes the next agent's input sequentially</div>
<div class="quiz-explanation">Fan-out/fan-in maximizes parallelism for independent work. Fan-out distributes, fan-in aggregates. Unlike pipeline (sequential) or consensus (voting), it's optimized for embarrassingly parallel subtasks.</div>
</div>
</div>

<div class="quiz" data-domain="Multi-Agent Coordination" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization has 3 agents: CodeGen, Reviewer, and Deployer. They need to update CodeGen's system prompt to use a new coding standard, but Reviewer and Deployer depend on CodeGen's output format.</div>
<div class="quiz-stem">How should this update be managed?</div>
<div class="quiz-option" data-correct="false">Update CodeGen immediately — other agents should handle format changes automatically</div>
<div class="quiz-option" data-correct="true">Update CodeGen with the new standard, validate that its output format remains compatible with Reviewer and Deployer expectations, run integration tests across the pipeline, and deploy the update only after confirming end-to-end compatibility</div>
<div class="quiz-option" data-correct="false">Rebuild all three agents from scratch with the new standard</div>
<div class="quiz-option" data-correct="false">Keep using the old standard indefinitely to avoid risk</div>
<div class="quiz-explanation">The exam covers "Update, reconfigure, or replace agents without disrupting active workflows." Changes to one agent require validating downstream compatibility, running integration tests, and progressive rollout.</div>
</div>
</div>



<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should agent actions be classified for determining autonomy levels?</div>
<div class="quiz-option" data-correct="false">By the time they take to execute</div>
<div class="quiz-option" data-correct="true">By operational risk (impact scope), security risk (data sensitivity, system access), and compliance risk (regulatory requirements) — to right-size human interventions for each category</div>
<div class="quiz-option" data-correct="false">By the model's confidence score for each action</div>
<div class="quiz-option" data-correct="false">All actions should have the same autonomy level for consistency</div>
<div class="quiz-explanation">The exam covers "Classify agent actions by operational, security, and compliance risk to right-size human interventions." Three risk dimensions determine how much oversight each action needs.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the goal of assigning autonomy levels in an agent system?</div>
<div class="quiz-option" data-correct="false">To minimize all agent actions for maximum safety</div>
<div class="quiz-option" data-correct="true">To maximize delivery speed while remaining compliant with organizational security and Responsible AI standards — high autonomy for safe actions, restricted autonomy for risky ones</div>
<div class="quiz-option" data-correct="false">To maximize agent autonomy regardless of risk</div>
<div class="quiz-option" data-correct="false">To create the most complex approval workflow possible</div>
<div class="quiz-explanation">The exam states: "Assign autonomy levels to maximize delivery speed while remaining compliant with organizational security and Responsible AI standards." It's explicitly about balancing speed AND compliance.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which actions require human judgment and should NOT be fully autonomous? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Deleting production data or resources</div>
<div class="quiz-option" data-correct="true">Modifying access control or security policies</div>
<div class="quiz-option" data-correct="true">Merging code that affects compliance-sensitive functionality</div>
<div class="quiz-option" data-correct="false">Running unit tests in a development environment</div>
<div class="quiz-option" data-correct="true">Deploying to production environments</div>
<div class="quiz-option" data-correct="false">Formatting code according to team standards</div>
<div class="quiz-explanation">The exam covers "Identify the subset of actions that require human judgment." Irreversible actions (delete production), security changes (access control), compliance-sensitive operations (deploy), and policy modifications all need human oversight.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent is configured with the following guardrail: "If the generated code includes any `eval()` calls, external URL fetches, or file system access outside the project directory, block the action and request human review."</div>
<div class="quiz-stem">What type of guardrail is this?</div>
<div class="quiz-option" data-correct="false">A performance guardrail</div>
<div class="quiz-option" data-correct="true">A security and compliance guardrail that blocks actions violating defined security policies — specifically preventing code injection, unauthorized network access, and path traversal</div>
<div class="quiz-option" data-correct="false">A style guardrail for code quality</div>
<div class="quiz-option" data-correct="false">An authentication guardrail</div>
<div class="quiz-explanation">The exam covers "Block actions that violate defined security, compliance, or Responsible AI policies." This guardrail specifically targets security risks (eval injection, unauthorized network/filesystem access).</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How should permissions and execution contexts be scoped to enforce least-privilege access?</div>
<div class="quiz-option" data-correct="false">Give agents admin access to everything and rely on guardrails to block bad actions</div>
<div class="quiz-option" data-correct="true">Grant only the specific permissions needed for the defined task scope — read-only where reading suffices, write access only to specific paths, no access to secrets unless required, and time-limited tokens that expire after the task</div>
<div class="quiz-option" data-correct="false">Use the same service account for all agents regardless of task</div>
<div class="quiz-option" data-correct="false">Least-privilege only applies to human users, not agents</div>
<div class="quiz-explanation">The exam covers "Scope permissions and execution contexts to enforce least-privilege access." Least privilege for agents means task-specific permissions, path restrictions, credential scoping, and temporal bounds.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What does "preserve execution velocity by minimizing approvals that do not materially reduce risk" mean?</div>
<div class="quiz-option" data-correct="false">Never require approvals for anything</div>
<div class="quiz-option" data-correct="true">Only require human approval for actions where the approval actually prevents meaningful harm — don't gate low-risk actions (formatting, running tests, reading files) behind approval workflows just for the sake of oversight</div>
<div class="quiz-option" data-correct="false">Require approval only from senior engineers</div>
<div class="quiz-option" data-correct="false">Batch all approvals into a daily review meeting</div>
<div class="quiz-explanation">This is directly from the exam objectives. Unnecessary approvals slow delivery without improving safety. Gate only what matters — actions where human judgment actually prevents harm that automated checks cannot catch.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization needs to ensure that irreversible or compliance-sensitive changes always go through a controlled path. Examples include database schema migrations and API breaking changes.</div>
<div class="quiz-stem">What should be implemented?</div>
<div class="quiz-option" data-correct="false">Block agents from making any changes to databases or APIs</div>
<div class="quiz-option" data-correct="true">Require explicit authorization gates for these specific action categories — the agent can propose the change (generate migration script, draft API change), but execution requires human authorization through a defined approval workflow</div>
<div class="quiz-option" data-correct="false">Allow the agent to make the change and alert humans afterward</div>
<div class="quiz-option" data-correct="false">Only allow these changes during maintenance windows</div>
<div class="quiz-explanation">The exam covers "Require explicit authorization or controlled paths for irreversible or compliance-sensitive changes." The agent can still add value (generating proposals), but execution of high-impact actions needs explicit human authorization.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How do guardrails relate to Responsible AI principles in agent systems?</div>
<div class="quiz-option" data-correct="false">Guardrails and Responsible AI are separate, unrelated concerns</div>
<div class="quiz-option" data-correct="true">Guardrails are the implementation mechanism for Responsible AI policies — they translate principles like fairness, transparency, and safety into enforceable rules that prevent agents from taking actions that violate these principles</div>
<div class="quiz-option" data-correct="false">Responsible AI only applies to model training, not agent operations</div>
<div class="quiz-option" data-correct="false">Guardrails replace the need for Responsible AI policies</div>
<div class="quiz-explanation">The exam links guardrails to "Responsible AI standards." Guardrails are how you operationalize Responsible AI — turning abstract principles into concrete, enforceable constraints on agent behavior.</div>
</div>
</div>

