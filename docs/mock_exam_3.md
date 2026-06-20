# Mock Exam 3 — GH-600 Agentic AI Developer

**Time limit:** 120 minutes | **Questions:** 60 | **Passing score:** 70% (42/60)

Click an answer to submit. You'll see immediate feedback with explanations.

---

<!-- DOMAIN 1: Prepare agent architecture and SDLC processes (Questions 1-10) -->

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">1. When integrating an AI agent into an existing CI/CD pipeline, what should be determined FIRST?</p>
<div class="quiz-options">
<div class="quiz-option">A. Which cloud provider will host the agent</div>
<div class="quiz-option">B. What programming language the agent will generate code in</div>
<div class="quiz-option" data-correct="true">C. The specific tasks the agent will perform, its inputs, outputs, and measurable success criteria</div>
<div class="quiz-option">D. How many API tokens the agent will consume per day</div>
</div>
<div class="quiz-explanation">The correct answer is C. Before any implementation, you must define the agent's scope: what it does, what it receives as input, what it produces as output, and how success is measured. Without these definitions, you cannot evaluate whether the integration is working correctly. A, B, and D are implementation details that follow from the scope definition.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<div class="quiz-scenario">A development team has deployed an AI agent that reviews PRs and suggests improvements. Initially, the agent operated in supervised mode where every suggestion required human confirmation before posting. After two months with a 95% acceptance rate, the team wants to move to semi-autonomous operation.</div>
<p class="quiz-stem">2. Which semi-autonomous configuration is MOST appropriate?</p>
<div class="quiz-options">
<div class="quiz-option">A. Allow the agent to post all comments without any review</div>
<div class="quiz-option" data-correct="true">B. Allow the agent to post low-severity suggestions automatically while requiring human review for suggestions that request significant code changes</div>
<div class="quiz-option">C. Disable the agent and have humans do all reviews again</div>
<div class="quiz-option">D. Let the agent approve and merge PRs directly based on its review</div>
</div>
<div class="quiz-explanation">The correct answer is B. Semi-autonomous means the agent handles low-risk actions independently (posting minor suggestions) while humans retain oversight of high-risk actions (significant change requests). This matches the graduated autonomy principle. A is fully autonomous, skipping the semi-autonomous step. C regresses to supervised. D escalates directly to fully autonomous with dangerous merge capability.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">3. What is the PRIMARY risk of not separating planning from execution in an agent workflow?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent will generate plans that are too detailed</div>
<div class="quiz-option" data-correct="true">B. The agent may execute harmful or incorrect actions before anyone has the opportunity to review and intervene</div>
<div class="quiz-option">C. The agent will require more API tokens per task</div>
<div class="quiz-option">D. The agent will be unable to use any tools</div>
</div>
<div class="quiz-explanation">The correct answer is B. Without separation, the agent moves directly from reasoning to action without a review checkpoint. If its plan is flawed—wrong files, wrong logic, wrong scope—the damage is done before anyone notices. A is not a risk (detailed plans are usually good). C is a cost concern, not a safety risk. D is incorrect; tools work regardless of planning architecture.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">4. Select ALL that apply: Which factors should influence the level of autonomy granted to an AI agent in SDLC?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. The agent's demonstrated track record of reliable performance</div>
<div class="quiz-option" data-correct="true">B. The reversibility of the actions the agent performs</div>
<div class="quiz-option" data-correct="true">C. The criticality of the environment (development vs. production)</div>
<div class="quiz-option">D. The agent's self-reported confidence score alone</div>
<div class="quiz-option">E. Whether the agent's name sounds trustworthy</div>
</div>
<div class="quiz-explanation">A, B, and C are correct. Autonomy decisions should consider proven track record (A), action reversibility (B), and environment criticality (C). D is unreliable—an agent's self-reported confidence is not a sufficient basis for autonomy decisions. E is obviously irrelevant—trust is earned through behavior, not naming.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">5. How should an agent's plan be validated before execution is permitted?</p>
<div class="quiz-options">
<div class="quiz-option">A. Only by checking that the plan is syntactically valid JSON</div>
<div class="quiz-option" data-correct="true">B. By verifying the plan's actions are within the agent's authorized scope, the target resources exist, and the plan aligns with the stated task objective</div>
<div class="quiz-option">C. By executing the plan in production and checking if errors occur</div>
<div class="quiz-option">D. By asking another AI agent if the plan looks correct</div>
</div>
<div class="quiz-explanation">The correct answer is B. Plan validation should be multi-dimensional: scope check (is the agent allowed to do this?), feasibility check (do targets exist?), and alignment check (does this match the task goal?). A only checks format, missing semantic validation. C is "test in production" which defeats the purpose of pre-execution validation. D delegates validation to another potentially unreliable agent.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">6. Which of the following BEST describes an appropriate agent output specification?</p>
<div class="quiz-options">
<div class="quiz-option">A. "The agent should produce good code"</div>
<div class="quiz-option">B. "The agent should output something useful"</div>
<div class="quiz-option" data-correct="true">C. "The agent must produce a pull request containing modified files with passing tests, a descriptive title under 72 characters, and a body referencing the originating issue"</div>
<div class="quiz-option">D. "The agent will generate output when it is ready"</div>
</div>
<div class="quiz-explanation">The correct answer is C. A well-defined output specification is specific, measurable, and verifiable: it names the artifact type (PR), quality criteria (passing tests), and format constraints (title length, issue reference). A and B are vague and unmeasurable. D specifies no format, quality, or content requirements whatsoever.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<div class="quiz-scenario">An organization has three environments: dev, staging, and production. They want to deploy an AI agent that automatically applies security patches. The agent has been running successfully in dev for one month.</div>
<p class="quiz-stem">7. What is the recommended NEXT step in graduated deployment?</p>
<div class="quiz-options">
<div class="quiz-option">A. Deploy directly to production since it worked in dev</div>
<div class="quiz-option" data-correct="true">B. Deploy to staging with the same monitoring as dev, validate behavior with production-like data, then plan production rollout</div>
<div class="quiz-option">C. Skip staging and deploy to production with a rollback plan</div>
<div class="quiz-option">D. Keep the agent in dev permanently and never promote it</div>
</div>
<div class="quiz-explanation">The correct answer is B. Graduated deployment means progressing through environments in order: dev → staging → production. Each stage validates the agent with increasingly realistic conditions. A and C skip the staging validation, which is designed to catch issues with production-like data. D prevents the agent from delivering value in production.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">8. What is the PRIMARY purpose of agent observability within an SDLC?</p>
<div class="quiz-options">
<div class="quiz-option">A. To provide entertainment by watching the agent work</div>
<div class="quiz-option">B. To generate billing reports for agent usage</div>
<div class="quiz-option" data-correct="true">C. To enable teams to understand, debug, audit, and continuously improve the agent's behavior through transparent records of its decisions and actions</div>
<div class="quiz-option">D. To compare the agent's speed against human developers</div>
</div>
<div class="quiz-explanation">The correct answer is C. Observability serves multiple engineering purposes: understanding (what is the agent doing?), debugging (why did it fail?), auditing (who did what and when?), and improvement (how can we make it better?). A, B, and D are not primary purposes—billing and performance comparison are secondary concerns at best.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">9. An anti-pattern called "scope creep" in agent architecture refers to:</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent working too slowly on its defined tasks</div>
<div class="quiz-option" data-correct="true">B. The agent gradually expanding its actions beyond its originally defined scope without explicit authorization</div>
<div class="quiz-option">C. The agent refusing to work on tasks it was designed for</div>
<div class="quiz-option">D. The agent's code growing in file size over time</div>
</div>
<div class="quiz-explanation">The correct answer is B. Scope creep in agent architecture occurs when the agent gradually takes on additional responsibilities or modifies additional resources beyond its defined boundaries—typically through reasoning that "this related file also needs updating." Without scope enforcement, agents drift from their intended purpose. A, C, and D describe unrelated concepts.</div>
</div>
</div>

<div class="quiz" data-domain="Prepare agent architecture and SDLC processes">
<div class="quiz-question">
<p class="quiz-stem">10. When defining agent inputs, what is the MOST important constraint to specify?</p>
<div class="quiz-options">
<div class="quiz-option">A. The maximum file size the agent can process</div>
<div class="quiz-option">B. The color scheme of the IDE the agent runs in</div>
<div class="quiz-option" data-correct="true">C. The scope boundary that defines which repositories, branches, and file paths the agent is allowed to read from and operate on</div>
<div class="quiz-option">D. The time zone the agent should use for timestamps</div>
</div>
<div class="quiz-explanation">The correct answer is C. Input scope boundaries define the agent's operational perimeter—what it can see and touch. This is the foundational security and correctness constraint. Without it, the agent might read sensitive files from other repositories or branches. A is a technical limitation. B and D are configuration details, not security-critical constraints.</div>
</div>
</div>

<!-- DOMAIN 2: Implement tool use and environment interaction (Questions 11-24) -->

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">11. In the MCP architecture, what is the relationship between an MCP server and the tools it exposes?</p>
<div class="quiz-options">
<div class="quiz-option">A. Each MCP server can only expose exactly one tool</div>
<div class="quiz-option" data-correct="true">B. An MCP server can expose multiple tools, each with defined input schemas, descriptions, and capabilities that the agent can discover and invoke</div>
<div class="quiz-option">C. MCP servers and tools are the same thing with different names</div>
<div class="quiz-option">D. Tools must be installed separately from MCP servers and connected via manual configuration</div>
</div>
<div class="quiz-explanation">The correct answer is B. An MCP server acts as a container for one or more tools. It exposes tool definitions (name, description, input schema) that clients can discover through the protocol, then invoke individually. A is too restrictive. C conflates the server with its tools. D mischaracterizes the integrated nature of MCP servers and their tools.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<div class="quiz-scenario">A team configures their AI agent to use a GitHub MCP server. The agent needs to: (1) list issues, (2) read file contents, (3) create commits, and (4) open pull requests. The team wants to follow security best practices.</div>
<p class="quiz-stem">12. How should the tool allow list be configured?</p>
<div class="quiz-options">
<div class="quiz-option">A. Allow all GitHub API operations to avoid limiting the agent</div>
<div class="quiz-option" data-correct="true">B. Explicitly allow only list_issues, get_file_contents, create_commit, and create_pull_request—the minimum set needed for the defined tasks</div>
<div class="quiz-option">C. Block only the delete_repository operation and allow everything else</div>
<div class="quiz-option">D. Use a deny list instead of an allow list for flexibility</div>
</div>
<div class="quiz-explanation">The correct answer is B. The allow list should contain exactly the operations needed—nothing more. This follows least-privilege precisely. A grants excessive access. C is a deny-list approach that leaves many dangerous operations (force push, admin settings) accessible. D (deny lists) is less secure because you must anticipate every dangerous operation; allow lists are safer because they deny by default.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">13. What is the PRIMARY security benefit of running an AI agent in an isolated container or codespace?</p>
<div class="quiz-options">
<div class="quiz-option">A. It makes the agent run faster due to dedicated resources</div>
<div class="quiz-option">B. It prevents the agent from accessing any network resources</div>
<div class="quiz-option" data-correct="true">C. It limits the blast radius of any unintended agent actions to the container, protecting the host system and other services</div>
<div class="quiz-option">D. It allows the agent to bypass security policies within the container</div>
</div>
<div class="quiz-explanation">The correct answer is C. Container isolation confines the agent's actions—even if it malfunctions or is exploited, the damage is limited to the container's boundaries. The host system and other services remain protected. A is about performance, not security. B is too absolute (containers can have controlled network access). D is incorrect; security policies still apply within containers.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">14. Select ALL that apply: Which are valid approaches for an agent to handle a tool timeout error?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Retry the operation with a longer timeout if the tool supports it</div>
<div class="quiz-option" data-correct="true">B. Try an alternative tool that provides similar functionality</div>
<div class="quiz-option" data-correct="true">C. Report the timeout to the user with context about what was being attempted</div>
<div class="quiz-option">D. Assume the operation succeeded despite the timeout</div>
<div class="quiz-option">E. Delete the tool from the configuration permanently</div>
</div>
<div class="quiz-explanation">A, B, and C are correct. Retrying with adjusted parameters (A), using alternative tools (B), and transparent reporting (C) are all valid responses to timeouts. D is dangerous—a timeout means the result is unknown, not successful. E is an overreaction to what may be a transient issue.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">15. In GitHub Copilot agent mode, what is the agent's workflow when it encounters a task requiring a tool it doesn't currently have access to?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent automatically installs any tool it needs from the internet</div>
<div class="quiz-option">B. The agent modifies its own configuration to add the tool</div>
<div class="quiz-option" data-correct="true">C. The agent acknowledges the limitation and either uses available tools to approximate the task or informs the user that the required capability is not available</div>
<div class="quiz-option">D. The agent crashes with an unhandled exception</div>
</div>
<div class="quiz-explanation">The correct answer is C. When a needed tool isn't available, the agent should work within its constraints—using available tools creatively or transparently communicating the limitation to the user. A and B would be self-modification anti-patterns (agents shouldn't install tools or modify their own config). D describes a bug, not expected behavior.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">16. What is the recommended practice for an agent that needs to invoke a GitHub Actions workflow as part of its task?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Use the workflow_dispatch API with appropriate parameters, monitor the workflow run status, and handle success/failure outcomes</div>
<div class="quiz-option">B. Directly modify the .github/workflows YAML to add inline code execution</div>
<div class="quiz-option">C. SSH into the Actions runner and execute commands directly</div>
<div class="quiz-option">D. Bypass GitHub Actions entirely and run CI commands locally</div>
</div>
<div class="quiz-explanation">The correct answer is A. The proper way to invoke workflows programmatically is through the workflow_dispatch API—it's secure, auditable, and uses the intended interface. B modifies pipeline configuration as a side effect. C is a security violation. D bypasses the CI/CD system entirely, losing its benefits (consistent environment, audit trail, parallelism).</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent running in VS Code with Copilot agent mode attempts to run a terminal command that would install a new npm package globally on the developer's machine. The developer has configured their workspace to restrict agent terminal commands to the project directory only.</div>
<p class="quiz-stem">17. What should happen when the agent attempts the global install?</p>
<div class="quiz-options">
<div class="quiz-option">A. The command executes successfully because the agent has terminal access</div>
<div class="quiz-option" data-correct="true">B. The workspace restriction blocks the global install and the agent is informed the operation is outside its permitted scope</div>
<div class="quiz-option">C. The agent's entire session terminates</div>
<div class="quiz-option">D. The agent retries with sudo privileges</div>
</div>
<div class="quiz-explanation">The correct answer is B. Workspace-level restrictions enforce boundaries on the agent's tool usage. When the agent attempts an operation outside its scope (global install vs. project-scoped), the restriction prevents execution and returns an appropriate error. A ignores the configured restrictions. C is disproportionate. D would be a privilege escalation attempt.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">18. What distinguishes a GitHub remote MCP server from a third-party MCP server in terms of trust model?</p>
<div class="quiz-options">
<div class="quiz-option">A. There is no difference in trust model—all MCP servers are equally trusted</div>
<div class="quiz-option" data-correct="true">B. GitHub remote MCP servers are managed within GitHub's infrastructure with GitHub's security guarantees, while third-party servers require additional vetting of the provider's security practices</div>
<div class="quiz-option">C. Third-party MCP servers are always more trustworthy because they're specialized</div>
<div class="quiz-option">D. GitHub remote MCP servers require no authentication while third-party ones always do</div>
</div>
<div class="quiz-explanation">The correct answer is B. Trust model differs based on who operates the server. GitHub-managed servers inherit GitHub's security posture, SLAs, and compliance certifications. Third-party servers require independent security assessment because you're trusting an external party with your data and operations. A ignores trust differences. C is backwards. D mischaracterizes authentication requirements.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">19. Select ALL that apply: When an agent creates a pull request, which elements support accountability and traceability?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Linking the PR to the originating issue or task</div>
<div class="quiz-option" data-correct="true">B. Including a summary of the agent's reasoning in the PR description</div>
<div class="quiz-option">C. Using a generic "bot" account shared across all organization agents</div>
<div class="quiz-option" data-correct="true">D. Adding labels that identify the PR as agent-generated</div>
<div class="quiz-option" data-correct="true">E. Attaching the execution plan as a PR comment or linked artifact</div>
</div>
<div class="quiz-explanation">A, B, D, and E are correct. Issue links (A) connect changes to requirements. Reasoning summaries (B) explain why changes were made. Labels (D) make agent PRs identifiable. Execution plans (E) provide full audit trail. C reduces accountability because shared accounts make it impossible to distinguish between different agents' actions.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">20. What is the correct order of operations when an agent needs to make a code change in a protected repository?</p>
<div class="quiz-options">
<div class="quiz-option">A. Edit file on main → push → create PR retroactively</div>
<div class="quiz-option">B. Force push to main → notify team → request approval</div>
<div class="quiz-option" data-correct="true">C. Create feature branch → make changes → push to branch → open PR → await review and approval → merge</div>
<div class="quiz-option">D. Request admin access → disable branch protection → push to main → re-enable protection</div>
</div>
<div class="quiz-explanation">The correct answer is C. The standard safe workflow for protected repositories is: branch → change → push → PR → review → merge. This respects branch protection, enables review, and maintains audit trail. A and B push directly to main, violating protections. D disables security controls, creating a window of vulnerability.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">21. What is the purpose of tool descriptions in an MCP server configuration?</p>
<div class="quiz-options">
<div class="quiz-option">A. They are optional decorative text with no functional purpose</div>
<div class="quiz-option">B. They are displayed in the user interface for marketing purposes</div>
<div class="quiz-option" data-correct="true">C. They help the AI agent understand when and how to use each tool, influencing tool selection decisions during task execution</div>
<div class="quiz-option">D. They are only used for generating API documentation</div>
</div>
<div class="quiz-explanation">The correct answer is C. Tool descriptions are semantically meaningful to the AI agent—they inform the agent about each tool's purpose, capabilities, and appropriate use cases. Well-written descriptions lead to better tool selection. A underestimates their importance. B and D describe secondary uses at best; the primary consumer of descriptions is the agent itself.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">22. When configuring an agent to work across multiple repositories, what is the MOST secure approach?</p>
<div class="quiz-options">
<div class="quiz-option">A. Use a single personal access token with organization-wide access</div>
<div class="quiz-option" data-correct="true">B. Use fine-grained personal access tokens or GitHub App installations with per-repository permissions</div>
<div class="quiz-option">C. Share SSH keys across all repositories for simplicity</div>
<div class="quiz-option">D. Give the agent access to the organization owner account</div>
</div>
<div class="quiz-explanation">The correct answer is B. Fine-grained tokens or GitHub App installations allow per-repository permission scoping—the agent gets exactly the access it needs for each repo, nothing more. A creates a single credential with excessive scope. C uses shared credentials without granular control. D provides maximum possible access, violating least-privilege entirely.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<p class="quiz-stem">23. What role does the agent's execution context play in determining tool behavior?</p>
<div class="quiz-options">
<div class="quiz-option">A. Execution context has no effect on tool behavior</div>
<div class="quiz-option" data-correct="true">B. The execution context (environment, permissions, available resources) determines what tools can do, what restrictions apply, and what results are possible</div>
<div class="quiz-option">C. Execution context only affects the agent's response format</div>
<div class="quiz-option">D. Execution context is only relevant for debugging, not runtime behavior</div>
</div>
<div class="quiz-explanation">The correct answer is B. Execution context is the runtime environment that shapes everything: which tools are available, what permissions they have, which resources they can access, and what constraints apply. A tool behaves differently in a production context vs. a development context. A, C, and D all underestimate the foundational role of execution context.</div>
</div>
</div>

<div class="quiz" data-domain="Implement tool use and environment interaction">
<div class="quiz-question">
<div class="quiz-scenario">An organization wants to use a third-party MCP server that provides database query tools. Before connecting it to their AI agent, the security team needs to evaluate it.</div>
<p class="quiz-stem">24. What should the security team evaluate FIRST about this third-party MCP server?</p>
<div class="quiz-options">
<div class="quiz-option">A. The visual design of the MCP server's documentation website</div>
<div class="quiz-option" data-correct="true">B. What data the server can access, how it handles credentials, whether it logs or transmits data externally, and what operations it permits</div>
<div class="quiz-option">C. How many stars the server's GitHub repository has</div>
<div class="quiz-option">D. Whether the server was written in a compiled language</div>
</div>
<div class="quiz-explanation">The correct answer is B. Security evaluation of a third-party MCP server must focus on data access, credential handling, data flow (does it send data elsewhere?), and operation scope. These determine the risk of connecting it to your systems. A is irrelevant to security. C is a popularity metric, not a security indicator. D is about implementation choice, not security posture.</div>
</div>
</div>

<!-- DOMAIN 3: Manage memory, state, and execution (Questions 25-31) -->

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">25. An AI agent working on a large codebase needs to maintain awareness of recently changed files without loading the entire repository into context. What memory pattern BEST achieves this?</p>
<div class="quiz-options">
<div class="quiz-option">A. Load every file in the repository into the agent's context at startup</div>
<div class="quiz-option" data-correct="true">B. Use a retrieval-augmented pattern that queries recent Git history and selectively loads only files relevant to the current task</div>
<div class="quiz-option">C. Rely entirely on the agent's pre-trained knowledge of the codebase</div>
<div class="quiz-option">D. Store the entire repository as a single string in the agent's prompt</div>
</div>
<div class="quiz-explanation">The correct answer is B. Retrieval-augmented memory uses Git history and relevance filtering to load only pertinent files, keeping context focused and manageable. A and D would exceed context limits for any non-trivial repository. C doesn't work because pre-trained knowledge doesn't include your specific codebase's current state.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">26. What is an "idempotent" operation in the context of agent task resumption?</p>
<div class="quiz-options">
<div class="quiz-option">A. An operation that can only be performed once and then becomes impossible</div>
<div class="quiz-option" data-correct="true">B. An operation that produces the same result regardless of how many times it is executed, making it safe to retry or re-execute during resumption</div>
<div class="quiz-option">C. An operation that automatically reverses itself after a timeout</div>
<div class="quiz-option">D. An operation that requires no permissions to execute</div>
</div>
<div class="quiz-explanation">The correct answer is B. Idempotent operations are safe to repeat because re-executing them doesn't change the outcome. This is crucial for task resumption—if the agent isn't sure whether a step completed, it can safely re-execute idempotent steps without causing damage. A describes a one-shot operation. C describes auto-rollback. D describes permission-free operations.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<div class="quiz-scenario">Two agents are working on the same repository. Agent A stores its task progress in a branch-specific state file. Agent B reads this file to understand what Agent A has completed. However, Agent B's reads sometimes see stale data because Agent A hasn't pushed its latest state yet.</div>
<p class="quiz-stem">27. What is the BEST solution to this state synchronization problem?</p>
<div class="quiz-options">
<div class="quiz-option">A. Have Agent B constantly poll the file every second</div>
<div class="quiz-option">B. Disable Agent B until Agent A is completely finished</div>
<div class="quiz-option" data-correct="true">C. Implement an event-driven notification system where Agent A signals when state is updated, or use a shared state service with consistent read guarantees</div>
<div class="quiz-option">D. Give both agents direct access to each other's memory</div>
</div>
<div class="quiz-explanation">The correct answer is C. Event-driven notifications or a consistent shared state service solve the synchronization problem properly—Agent B is informed when new state is available, or reads are guaranteed to see the latest write. A wastes resources with aggressive polling. B eliminates parallelism. D violates agent isolation and creates tight coupling.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">28. When should an agent perform a full memory reset versus selective pruning?</p>
<div class="quiz-options">
<div class="quiz-option">A. Always use reset because it's simpler</div>
<div class="quiz-option">B. Never reset—only prune to preserve all information</div>
<div class="quiz-option" data-correct="true">C. Use reset when the accumulated context is fundamentally corrupted or the task has changed entirely; use pruning when context is mostly valid but contains some outdated elements</div>
<div class="quiz-option">D. Use reset for short tasks and pruning for long tasks</div>
</div>
<div class="quiz-explanation">The correct answer is C. The choice depends on the state of the context: if it's fundamentally wrong or irrelevant (e.g., the agent was working on the wrong task), reset is appropriate. If the context is mostly good but contains some stale items, surgical pruning preserves valuable information. A loses good context unnecessarily. B risks context pollution. D uses an irrelevant criterion.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">29. Select ALL that apply: Which are characteristics of a well-designed durable artifact for capturing task progress?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. It records which steps have been completed and which are pending</div>
<div class="quiz-option" data-correct="true">B. It includes intermediate outputs that future steps depend on</div>
<div class="quiz-option">C. It contains the entire conversation history verbatim</div>
<div class="quiz-option" data-correct="true">D. It is stored in a location accessible across session boundaries</div>
<div class="quiz-option">E. It is encrypted so that no other agent can ever read it</div>
</div>
<div class="quiz-explanation">A, B, and D are correct. Good progress artifacts track completed/pending status (A), store intermediate results needed by later steps (B), and are persistently accessible (D). C would be excessive and potentially exceed storage/retrieval limits. E prevents legitimate state sharing between collaborating agents.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">30. What is the PRIMARY risk of not implementing memory scoping for an agent?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. The agent accumulates irrelevant context that dilutes its attention, leading to degraded performance and potential hallucinations about unrelated information</div>
<div class="quiz-option">B. The agent will be unable to access any files</div>
<div class="quiz-option">C. The agent will automatically delete important memories</div>
<div class="quiz-option">D. The agent will stop responding entirely</div>
</div>
<div class="quiz-explanation">The correct answer is A. Without scoping, the agent's context fills with irrelevant information from past tasks, unrelated files, and outdated states. This "context pollution" reduces the model's ability to focus on the current task and can introduce hallucinations from irrelevant context. B, C, and D describe consequences that don't follow from missing memory scoping.</div>
</div>
</div>

<div class="quiz" data-domain="Manage memory, state, and execution">
<div class="quiz-question">
<p class="quiz-stem">31. How should an agent handle the situation where its persisted state conflicts with the current state of the repository?</p>
<div class="quiz-options">
<div class="quiz-option">A. Always trust its persisted state and ignore the repository</div>
<div class="quiz-option">B. Always discard its state and start over from scratch</div>
<div class="quiz-option" data-correct="true">C. Detect the conflict, determine what changed, assess whether its pending actions are still valid, and either adapt its plan or escalate to a human</div>
<div class="quiz-option">D. Merge both states automatically without validation</div>
</div>
<div class="quiz-explanation">The correct answer is C. When persisted state conflicts with current reality, the agent should analyze the discrepancy: what changed externally? Are its planned actions still valid? Can it adapt? If not, it should escalate. A ignores real changes (context drift). B wastes completed work unnecessarily. D risks creating inconsistencies by blindly merging conflicting states.</div>
</div>
</div>

<!-- DOMAIN 4: Perform evaluation, error analysis, and tuning (Questions 32-41) -->

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">32. What is the MOST important principle when defining success criteria for an AI agent?</p>
<div class="quiz-options">
<div class="quiz-option">A. Success criteria should be as broad as possible to give the agent flexibility</div>
<div class="quiz-option">B. Success criteria should only measure speed of task completion</div>
<div class="quiz-option" data-correct="true">C. Success criteria should be specific, measurable, and directly aligned with the business or development outcome the agent is supposed to achieve</div>
<div class="quiz-option">D. Success criteria should be defined after the agent is deployed based on observed behavior</div>
</div>
<div class="quiz-explanation">The correct answer is C. Good success criteria are SMART-like: specific enough to evaluate objectively, measurable to track progress, and aligned with actual goals. A makes criteria unmeasurable. B ignores quality dimensions. D means there's no baseline for evaluation during initial deployment—you can't know if the agent is performing well without predefined criteria.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent is configured to fix failing tests by modifying source code. In 30% of cases, the agent fixes the test by modifying the test assertions to match the (incorrect) actual behavior rather than fixing the source code bug.</div>
<p class="quiz-stem">33. What root cause classification and tuning action is appropriate?</p>
<div class="quiz-options">
<div class="quiz-option">A. Tool misuse—restrict the agent's access to test files</div>
<div class="quiz-option" data-correct="true">B. Reasoning error—refine instructions to explicitly state that tests define expected behavior and source code should be fixed to match tests, not the other way around</div>
<div class="quiz-option">C. Context issue—provide more repository files to the agent</div>
<div class="quiz-option">D. Permission error—revoke the agent's write access to all files</div>
</div>
<div class="quiz-explanation">The correct answer is B. The agent has the right tools and context but is reasoning incorrectly about what to fix. The tuning action is to clarify in instructions that tests are the specification and source code is what should change. A would prevent legitimate test updates. C doesn't address the reasoning flaw. D prevents the agent from doing any work.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">34. Which evaluation signal would BEST detect that an agent is producing syntactically correct but semantically meaningless code?</p>
<div class="quiz-options">
<div class="quiz-option">A. Compilation success rate</div>
<div class="quiz-option">B. Lines of code produced per minute</div>
<div class="quiz-option" data-correct="true">C. Human review scoring the code's functional correctness and meaningfulness against the task requirements</div>
<div class="quiz-option">D. File size of generated output</div>
</div>
<div class="quiz-explanation">The correct answer is C. Semantic meaningfulness requires human judgment—does the code actually do what was asked? Automated checks can't distinguish between correct-looking code and code that genuinely solves the problem. A only checks syntax. B measures productivity, not quality. D is irrelevant to semantic correctness.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">35. Select ALL that apply: Which are valid quantitative evaluation metrics for an AI code generation agent?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Test pass rate of generated code</div>
<div class="quiz-option" data-correct="true">B. Number of linting errors in generated code</div>
<div class="quiz-option" data-correct="true">C. Percentage of PRs accepted without modification</div>
<div class="quiz-option">D. The agent's subjective opinion of its own code quality</div>
<div class="quiz-option" data-correct="true">E. Code coverage percentage of generated tests</div>
</div>
<div class="quiz-explanation">A, B, C, and E are correct quantitative metrics. Test pass rate (A), linting errors (B), PR acceptance rate (C), and code coverage (E) are all objectively measurable numbers. D is not quantitative—an agent's self-assessment is not an objective metric and shouldn't be used for evaluation.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">36. An agent fails because it tries to use a REST API endpoint that was deprecated and removed. What root cause category is this?</p>
<div class="quiz-options">
<div class="quiz-option">A. Reasoning error—the agent's logic was flawed</div>
<div class="quiz-option">B. Tool misuse—the agent should have used a different tool entirely</div>
<div class="quiz-option" data-correct="true">C. Context issue—the agent's information about available APIs was outdated</div>
<div class="quiz-option">D. Permission error—the agent wasn't authorized to use the API</div>
</div>
<div class="quiz-explanation">The correct answer is C. The agent tried to use the correct tool (REST API) for the right purpose, but its knowledge was stale—the endpoint no longer exists. This is a context/information freshness problem. A doesn't apply because the logic of "call this API" was sound if the API existed. B is wrong because the right type of tool was selected. D is wrong because the issue is existence, not authorization.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">37. What is the BEST approach to tuning an agent that frequently makes the same type of error?</p>
<div class="quiz-options">
<div class="quiz-option">A. Add the specific failing examples to the agent's prompt as "things to avoid"</div>
<div class="quiz-option">B. Reduce the agent's temperature to zero for deterministic outputs</div>
<div class="quiz-option" data-correct="true">C. Identify the pattern in the errors, revise instructions to address the root cause, add positive examples showing correct behavior, and validate the fix with the previously failing cases</div>
<div class="quiz-option">D. Accept the error rate as an inherent limitation</div>
</div>
<div class="quiz-explanation">The correct answer is C. Systematic tuning involves pattern recognition, root cause addressing through instruction revision, positive guidance (not just negative), and regression testing with previously failing cases. A only provides negative examples without root cause understanding. B may help consistency but doesn't fix incorrect reasoning. D gives up on improvement prematurely.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<div class="quiz-scenario">A team reviews their agent's performance over the past month. The data shows: Task completion rate: 92%. Developer satisfaction: 78%. Average time to completion: 3 minutes. However, 40% of completed tasks required post-agent manual corrections by developers.</div>
<p class="quiz-stem">38. What evaluation insight does this data reveal?</p>
<div class="quiz-options">
<div class="quiz-option">A. The agent is performing excellently with no improvement needed</div>
<div class="quiz-option" data-correct="true">B. The task completion rate is misleading—the 40% correction rate indicates that many "completed" tasks were not truly complete, and a more meaningful metric would be "tasks completed without human intervention"</div>
<div class="quiz-option">C. The agent is too slow and needs performance optimization</div>
<div class="quiz-option">D. Developer satisfaction should be ignored as it's subjective</div>
</div>
<div class="quiz-explanation">The correct answer is B. The disconnect between "92% completion rate" and "40% needing corrections" reveals that the completion metric is too lenient—it counts partially correct work as complete. A more meaningful metric (full completion without corrections) would be approximately 55%, painting a more accurate picture. A overlooks the correction rate. C misreads the speed data. D dismisses valid signal.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">39. How do workflow artifacts contribute to agent failure analysis?</p>
<div class="quiz-options">
<div class="quiz-option">A. They provide entertaining reading for the operations team</div>
<div class="quiz-option" data-correct="true">B. They preserve concrete evidence of what happened during execution (logs, outputs, exit codes, timing data) enabling reconstruction of the failure sequence after the fact</div>
<div class="quiz-option">C. They automatically fix the agent's errors</div>
<div class="quiz-option">D. They prevent failures from occurring in the first place</div>
</div>
<div class="quiz-explanation">The correct answer is B. Workflow artifacts are the forensic evidence of execution—they capture what happened (logs), what was produced (outputs), whether it succeeded (exit codes), and how long it took (timing). This enables post-mortem analysis. A trivializes their importance. C and D attribute preventive or corrective powers they don't have—artifacts are observational, not active.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">40. When an agent fails on a task it previously succeeded on, what should the investigation focus on FIRST?</p>
<div class="quiz-options">
<div class="quiz-option">A. Whether the model version changed</div>
<div class="quiz-option" data-correct="true">B. What changed between the successful execution and the failed one—comparing inputs, context, environment state, and tool availability</div>
<div class="quiz-option">C. Whether the agent needs retraining on new data</div>
<div class="quiz-option">D. Whether the task is still relevant to the business</div>
</div>
<div class="quiz-explanation">The correct answer is B. When something that worked before stops working, the investigation should focus on the delta—what changed? This could be different input data, modified environment, updated dependencies, changed file state, or altered tool configurations. A is one possibility but not the only one to check first. C conflates tuning with retraining. D questions the task rather than investigating the failure.</div>
</div>
</div>

<div class="quiz" data-domain="Perform evaluation, error analysis, and tuning">
<div class="quiz-question">
<p class="quiz-stem">41. What is a "regression test" in the context of agent tuning?</p>
<div class="quiz-options">
<div class="quiz-option">A. A test that measures how quickly the agent responds</div>
<div class="quiz-option">B. A test that compares two different AI models</div>
<div class="quiz-option" data-correct="true">C. Re-running previously passing test cases after a tuning change to verify that the improvement didn't break existing capabilities</div>
<div class="quiz-option">D. A test that measures the agent's memory consumption</div>
</div>
<div class="quiz-explanation">The correct answer is C. Regression testing verifies that improvements don't introduce regressions—after tuning the agent (e.g., revising instructions), you re-run cases that previously worked to confirm they still work. This prevents fixing one issue while breaking another. A measures latency. B is model comparison. D measures resource usage.</div>
</div>
</div>

<!-- DOMAIN 5: Orchestrate multi-agent coordination (Questions 42-51) -->

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">42. What is the key difference between a pipeline orchestration pattern and a hub-and-spoke pattern?</p>
<div class="quiz-options">
<div class="quiz-option">A. Pipeline is faster while hub-and-spoke is more accurate</div>
<div class="quiz-option" data-correct="true">B. Pipeline executes agents sequentially with each output feeding the next, while hub-and-spoke uses a central orchestrator that delegates tasks to agents that may run in parallel</div>
<div class="quiz-option">C. Pipeline requires fewer agents than hub-and-spoke</div>
<div class="quiz-option">D. Hub-and-spoke doesn't require an orchestrator agent</div>
</div>
<div class="quiz-explanation">The correct answer is B. Pipeline is sequential (A→B→C with data flowing forward), while hub-and-spoke is centrally coordinated (orchestrator delegates to A, B, C which may work in parallel). A makes unsupported performance claims. C conflates pattern structure with agent count. D contradicts the definition of hub-and-spoke (the hub IS the orchestrator).</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<div class="quiz-scenario">A company uses a multi-agent system where Agent A generates documentation, Agent B reviews it for accuracy, and Agent C publishes it. One day, Agent C publishes documentation that contains factual errors. Investigation reveals Agent B approved the errors.</div>
<p class="quiz-stem">43. What does this reveal about the multi-agent system's design?</p>
<div class="quiz-options">
<div class="quiz-option">A. Agent C is responsible since it performed the publish action</div>
<div class="quiz-option" data-correct="true">B. The pipeline's quality gate (Agent B) is ineffective—either its evaluation criteria are too lenient or it lacks the context needed to identify factual errors</div>
<div class="quiz-option">C. Agent A should be removed from the system</div>
<div class="quiz-option">D. Multi-agent systems cannot produce accurate documentation</div>
</div>
<div class="quiz-explanation">The correct answer is B. The review agent (Agent B) is the quality gate in this pipeline—its failure to catch errors indicates either inadequate evaluation criteria or insufficient context for verification. The system design placed trust in this gate, and it failed. A misattributes responsibility (C just published what was approved). C removes the source without fixing the filter. D overgeneralizes from one failure.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">44. How should an orchestrator handle the situation where one agent in a parallel group takes significantly longer than expected while others have completed?</p>
<div class="quiz-options">
<div class="quiz-option">A. Cancel the slow agent immediately and proceed without its results</div>
<div class="quiz-option">B. Wait indefinitely for the slow agent regardless of how long it takes</div>
<div class="quiz-option" data-correct="true">C. Apply a timeout policy: if the agent exceeds the threshold, evaluate whether to wait longer, retry with different parameters, or proceed with partial results and flag the gap</div>
<div class="quiz-option">D. Restart all agents in the group from scratch</div>
</div>
<div class="quiz-explanation">The correct answer is C. A timeout policy with multiple response options gives the orchestrator flexibility—it can extend the timeout for important tasks, retry with adjustments, or proceed with what's available while flagging incompleteness. A may discard important work. B risks infinite waits. D wastes already-completed work from other agents.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">45. Select ALL that apply: Which techniques help prevent conflicting changes when multiple agents work on the same codebase?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. Assigning each agent to work on a separate branch</div>
<div class="quiz-option" data-correct="true">B. Using file-level locking to prevent simultaneous modification of the same file</div>
<div class="quiz-option" data-correct="true">C. Defining clear ownership boundaries (e.g., Agent A owns /src/auth, Agent B owns /src/ui)</div>
<div class="quiz-option">D. Giving all agents write access to the same branch simultaneously</div>
<div class="quiz-option">E. Disabling version control to avoid merge conflicts</div>
</div>
<div class="quiz-explanation">A, B, and C are correct. Branch isolation (A), file locking (B), and ownership boundaries (C) all prevent conflicting modifications through different mechanisms. D directly causes the problem—multiple agents writing to the same branch creates race conditions. E removes the safety net that detects and resolves conflicts.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">46. What is the role of an "agent registry" in a multi-agent system?</p>
<div class="quiz-options">
<div class="quiz-option">A. It stores the source code of all agents in a single repository</div>
<div class="quiz-option" data-correct="true">B. It maintains a catalog of available agents, their capabilities, current status, and version information, enabling dynamic task routing and lifecycle management</div>
<div class="quiz-option">C. It provides a user interface for visualizing agent conversations</div>
<div class="quiz-option">D. It handles authentication for all agent API calls</div>
</div>
<div class="quiz-explanation">The correct answer is B. An agent registry is a service discovery and management layer—it knows what agents exist, what they can do, whether they're active, and which version is deployed. This enables orchestrators to route tasks dynamically and manage the agent lifecycle. A describes a code repository. C describes a monitoring UI. D describes an auth service.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">47. When performing post-hoc analysis of a multi-agent execution that produced incorrect results, what should be analyzed FIRST?</p>
<div class="quiz-options">
<div class="quiz-option">A. The cost of running all the agents</div>
<div class="quiz-option" data-correct="true">B. The handoff points between agents to determine if information was lost, corrupted, or misinterpreted during transfers</div>
<div class="quiz-option">C. The number of tokens each agent consumed</div>
<div class="quiz-option">D. The time zone settings of each agent's execution environment</div>
</div>
<div class="quiz-explanation">The correct answer is B. In multi-agent systems, handoffs are the most common failure points—information can be lost, reformatted incorrectly, or misinterpreted when passed between agents. Analyzing handoffs first identifies whether the failure originated in processing or communication. A and C are operational metrics, not failure diagnostics. D is rarely relevant.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">48. What is the recommended approach for rolling back a multi-agent execution that produced partially incorrect results?</p>
<div class="quiz-options">
<div class="quiz-option">A. Roll back all agents' changes regardless of which ones were correct</div>
<div class="quiz-option" data-correct="true">B. Identify which agents produced correct results and which produced incorrect ones, roll back only the incorrect portions while preserving valid work</div>
<div class="quiz-option">C. Leave all changes in place and fix issues in a follow-up task</div>
<div class="quiz-option">D. Delete the entire repository and restore from the last backup</div>
</div>
<div class="quiz-explanation">The correct answer is B. Surgical rollback preserves valuable work while removing only the problematic portions. This requires good observability (knowing which agent did what) and isolation (changes can be independently reverted). A wastes valid work unnecessarily. C leaves known-bad code in the codebase. D is a catastrophic overreaction that destroys unrelated work.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">49. In a multi-agent system, what is a "contradiction" in agent outputs?</p>
<div class="quiz-options">
<div class="quiz-option">A. When two agents produce outputs of different lengths</div>
<div class="quiz-option">B. When agents use different programming languages</div>
<div class="quiz-option" data-correct="true">C. When two or more agents produce outputs that are logically incompatible—applying both would result in broken or inconsistent system state</div>
<div class="quiz-option">D. When agents complete their tasks at different times</div>
</div>
<div class="quiz-explanation">The correct answer is C. A contradiction occurs when agent outputs cannot coexist—for example, one agent renames a function while another adds calls to the old name, or one sets a config value to "true" while another sets it to "false." A, B, and D describe differences that aren't contradictions—they can all coexist without causing logical conflicts.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<div class="quiz-scenario">An organization decides to retire their legacy code review agent and replace it with a newer, more capable version. The transition needs to happen without disrupting the team's development workflow.</div>
<p class="quiz-stem">50. What is the safest approach to this agent replacement?</p>
<div class="quiz-options">
<div class="quiz-option">A. Remove the old agent immediately and deploy the new one</div>
<div class="quiz-option" data-correct="true">B. Run both agents in parallel temporarily (shadow mode), compare outputs to validate the new agent, then gradually shift traffic from old to new before decommissioning the old agent</div>
<div class="quiz-option">C. Keep both agents permanently to ensure redundancy</div>
<div class="quiz-option">D. Deploy the new agent to production without any testing because it's "newer and better"</div>
</div>
<div class="quiz-explanation">The correct answer is B. Parallel running (shadow mode) allows comparison without risk—the old agent continues serving while the new one is validated against the same inputs. Gradual traffic shifting minimizes disruption. A creates a gap or introduces an unvalidated agent. C adds unnecessary complexity and cost long-term. D skips validation entirely.</div>
</div>
</div>

<div class="quiz" data-domain="Orchestrate multi-agent coordination">
<div class="quiz-question">
<p class="quiz-stem">51. How should multi-agent observability differ from single-agent observability?</p>
<div class="quiz-options">
<div class="quiz-option">A. Multi-agent systems don't need observability since the orchestrator handles everything</div>
<div class="quiz-option">B. Multi-agent observability should only track the final output, not individual agent contributions</div>
<div class="quiz-option" data-correct="true">C. Multi-agent observability must additionally track inter-agent communication, coordination timing, dependency relationships, and the contribution of each agent to the final outcome</div>
<div class="quiz-option">D. Multi-agent observability is identical to single-agent observability with no additional requirements</div>
</div>
<div class="quiz-explanation">The correct answer is C. Multi-agent systems have additional observability needs beyond individual agent tracking: how agents communicate, how coordination affects timing, what dependencies exist between agents, and which agent contributed what to the final result. These are emergent properties of the multi-agent system. A, B, and D all underestimate the additional complexity of coordinated systems.</div>
</div>
</div>

<!-- DOMAIN 6: Implement guardrails and accountability (Questions 52-60) -->

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">52. What is the key principle behind "defense in depth" for AI agent guardrails?</p>
<div class="quiz-options">
<div class="quiz-option">A. Using a single, very strong security control to protect against all threats</div>
<div class="quiz-option" data-correct="true">B. Implementing multiple layers of controls so that if one layer fails, others still provide protection</div>
<div class="quiz-option">C. Making the agent's code extremely complex so attackers can't understand it</div>
<div class="quiz-option">D. Relying on the AI model's built-in safety training as the only safeguard</div>
</div>
<div class="quiz-explanation">The correct answer is B. Defense in depth means layered security—multiple independent controls (allow lists, permissions, approval gates, monitoring, scope restrictions) that provide overlapping protection. If one fails, others catch the issue. A creates a single point of failure. C is security through obscurity. D relies on a single layer that isn't designed as a security control.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent is configured to manage Kubernetes deployments. The team defines three risk tiers: Tier 1 (low) - reading pod status, viewing logs; Tier 2 (medium) - scaling replicas, restarting pods; Tier 3 (high) - deleting namespaces, modifying network policies.</div>
<p class="quiz-stem">53. What autonomy levels should be assigned to each tier?</p>
<div class="quiz-options">
<div class="quiz-option">A. All tiers should require the same level of human approval</div>
<div class="quiz-option" data-correct="true">B. Tier 1: fully autonomous (no approval needed); Tier 2: semi-autonomous (logged and alerting, approval for production); Tier 3: supervised (always requires explicit human authorization)</div>
<div class="quiz-option">C. Tier 1: supervised; Tier 2: fully autonomous; Tier 3: semi-autonomous</div>
<div class="quiz-option">D. All tiers: fully autonomous to maximize agent efficiency</div>
</div>
<div class="quiz-explanation">The correct answer is B. Autonomy levels should correspond to risk: low-risk read operations need no approval, medium-risk operational changes get monitoring with conditional approval, and high-risk destructive/security operations always need human authorization. A over-controls low-risk actions. C inverts the appropriate relationship. D ignores risk entirely.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability" data-type="multiple-select">
<div class="quiz-question">
<p class="quiz-stem">54. Select ALL that apply: Which are valid criteria for classifying an agent action as "high security risk"?</p>
<div class="quiz-options">
<div class="quiz-option" data-correct="true">A. The action modifies authentication or authorization mechanisms</div>
<div class="quiz-option" data-correct="true">B. The action could expose sensitive data to unauthorized parties</div>
<div class="quiz-option" data-correct="true">C. The action changes network firewall rules or security groups</div>
<div class="quiz-option">D. The action reads a public documentation page</div>
<div class="quiz-option">E. The action creates a comment on a pull request</div>
</div>
<div class="quiz-explanation">A, B, and C are correct. High security risk involves actions that could compromise system security: modifying auth (A), exposing data (B), or changing network controls (C). D is a non-destructive read of public data (no risk). E is a low-impact, reversible communication action (low risk).</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">55. What is the difference between "blocking" and "alerting" guardrails?</p>
<div class="quiz-options">
<div class="quiz-option">A. They are the same mechanism with different names</div>
<div class="quiz-option" data-correct="true">B. Blocking guardrails prevent the action from executing entirely, while alerting guardrails allow the action but notify relevant parties for review</div>
<div class="quiz-option">C. Blocking guardrails are for production only, alerting guardrails are for development only</div>
<div class="quiz-option">D. Alerting guardrails are stronger than blocking guardrails</div>
</div>
<div class="quiz-explanation">The correct answer is B. Blocking guardrails are hard stops—the action cannot proceed under any circumstances. Alerting guardrails allow the action but create visibility through notifications, enabling post-hoc review. Both have their place: blocking for truly dangerous actions, alerting for suspicious but potentially legitimate ones. A, C, and D all mischaracterize the relationship.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">56. An agent attempts to commit code that includes a hardcoded API key. What type of guardrail should catch this?</p>
<div class="quiz-options">
<div class="quiz-option">A. A rate-limiting guardrail</div>
<div class="quiz-option">B. A code formatting guardrail</div>
<div class="quiz-option" data-correct="true">C. A secret-detection guardrail that scans commits for sensitive patterns (API keys, passwords, tokens) and blocks the commit</div>
<div class="quiz-option">D. A file-size guardrail</div>
</div>
<div class="quiz-explanation">The correct answer is C. Secret detection guardrails scan for patterns matching credentials, tokens, and keys in code before it's committed. This prevents accidental exposure of sensitive information. GitHub's secret scanning and pre-commit hooks serve this purpose. A limits frequency, not content. B checks formatting. D checks file size—none address secret exposure.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">57. What is "approval fatigue" and why is it dangerous in the context of AI agent guardrails?</p>
<div class="quiz-options">
<div class="quiz-option">A. When the approval system runs out of computing resources</div>
<div class="quiz-option" data-correct="true">B. When reviewers are overwhelmed with too many approval requests, leading them to approve without careful review, effectively negating the safety benefit of the guardrail</div>
<div class="quiz-option">C. When the agent becomes tired of waiting for approvals</div>
<div class="quiz-option">D. When the approval system's SSL certificates expire</div>
</div>
<div class="quiz-explanation">The correct answer is B. Approval fatigue is a human behavioral pattern where excessive approval requests lead to rubber-stamping—reviewers approve automatically without genuine evaluation. This makes the guardrail a formality rather than an effective safety control. A and D describe system issues. C anthropomorphizes the agent incorrectly.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<div class="quiz-scenario">A healthcare company uses an AI agent to process code changes in their patient data management system. The system is subject to HIPAA compliance requirements. The agent proposes a change that would log patient names in plain text to a debugging console.</div>
<p class="quiz-stem">58. What should the compliance guardrail do?</p>
<div class="quiz-options">
<div class="quiz-option">A. Allow the change since it's for debugging purposes</div>
<div class="quiz-option" data-correct="true">B. Block the change because logging patient names in plain text violates HIPAA's data protection requirements, and suggest using anonymized identifiers instead</div>
<div class="quiz-option">C. Allow the change but add a comment saying "HIPAA notice"</div>
<div class="quiz-option">D. Escalate to the legal department for a three-week review</div>
</div>
<div class="quiz-explanation">The correct answer is B. A compliance guardrail for HIPAA should detect and block PII/PHI exposure in logs, regardless of the stated purpose. It should also suggest a compliant alternative (anonymized IDs). A ignores compliance requirements. C adds cosmetic notice without preventing the violation. D is disproportionate for a clear-cut violation that can be blocked automatically.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">59. How should accountability be maintained when an agent operates fully autonomously?</p>
<div class="quiz-options">
<div class="quiz-option">A. Accountability is not possible with fully autonomous agents</div>
<div class="quiz-option">B. The agent's developers are always personally liable for every action</div>
<div class="quiz-option" data-correct="true">C. Through comprehensive audit logging, clear ownership assignment, immutable records of decisions, and periodic human review of agent behavior patterns</div>
<div class="quiz-option">D. By limiting the agent to only one action per day</div>
</div>
<div class="quiz-explanation">The correct answer is C. Even fully autonomous agents maintain accountability through observability mechanisms: immutable audit logs capture what happened, ownership records establish who is responsible for the agent, and periodic reviews ensure the agent's behavior remains aligned with expectations. A gives up on accountability. B oversimplifies liability. D arbitrarily limits utility.</div>
</div>
</div>

<div class="quiz" data-domain="Implement guardrails and accountability">
<div class="quiz-question">
<p class="quiz-stem">60. What is the correct approach when an organization discovers that a guardrail is producing too many false positives (blocking legitimate agent actions)?</p>
<div class="quiz-options">
<div class="quiz-option">A. Remove the guardrail entirely since it's causing problems</div>
<div class="quiz-option">B. Keep the guardrail unchanged and tell developers to work around it</div>
<div class="quiz-option" data-correct="true">C. Refine the guardrail's detection rules to reduce false positives while maintaining its protection against genuine threats, and monitor the impact of changes</div>
<div class="quiz-option">D. Convert the blocking guardrail to a logging-only mode permanently</div>
</div>
<div class="quiz-explanation">The correct answer is C. Guardrails should be tuned iteratively—reducing false positives while maintaining true positive detection. This involves refining rules, adding exceptions for known-safe patterns, and monitoring effectiveness after changes. A removes protection entirely. B creates developer frustration and workarounds. D removes the blocking capability that provides actual protection.</div>
</div>
</div>

