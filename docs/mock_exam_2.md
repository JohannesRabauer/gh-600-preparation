# Mock Exam 2

!!! info "Instructions"
    50 questions • 120 minutes • 70% to pass (35/50)
    Emphasis on Domains 2 (Implementation) & 4 (Security).

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which MCP capability type allows servers to expose pre-built prompt templates for common tasks?</div>
<div class="quiz-option" data-correct="false">Tools</div>
<div class="quiz-option" data-correct="false">Resources</div>
<div class="quiz-option" data-correct="true">Prompts</div>
<div class="quiz-option" data-correct="false">Sampling</div>
<div class="quiz-explanation">MCP Prompts are pre-built prompt templates that servers can expose. Tools are actions to invoke, Resources are data to read, and Sampling allows servers to request LLM completions from the host.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the principle of least privilege in the context of AI agents?</div>
<div class="quiz-option" data-correct="false">Give agents maximum access so they can complete tasks faster</div>
<div class="quiz-option" data-correct="true">Grant agents only the minimum permissions required to complete their specific task</div>
<div class="quiz-option" data-correct="false">Remove all agent permissions by default</div>
<div class="quiz-option" data-correct="false">Only allow agents to read files</div>
<div class="quiz-explanation">Least privilege means agents get exactly the access they need — no more, no less. This minimizes risk while maintaining utility. Full access is too permissive; no access is too restrictive.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team is building an MCP server that connects to their CI/CD system. The server needs to let agents check build status (read) and trigger builds (write).</div>
<div class="quiz-stem">What security measures should the server implement?</div>
<div class="quiz-option" data-correct="false">No restrictions — the agent knows what's appropriate</div>
<div class="quiz-option" data-correct="true">Separate tools for read (auto-approved) and write (requires user confirmation), rate limiting on build triggers, and audit logging</div>
<div class="quiz-option" data-correct="false">Only allow build status checks, never triggers</div>
<div class="quiz-option" data-correct="false">Hardcode the CI/CD token in the server code</div>
<div class="quiz-explanation">Best practice: separate read and write tools with different approval levels. Read (build status) is safe for auto-approval. Write (trigger build) requires human confirmation. Add rate limiting and audit logging for governance.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which of the following are valid entries in an agent audit log? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Timestamp of the action</div>
<div class="quiz-option" data-correct="true">User identity who triggered the agent</div>
<div class="quiz-option" data-correct="true">Tool that was used</div>
<div class="quiz-option" data-correct="false">The AI model's internal weights</div>
<div class="quiz-option" data-correct="true">Risk level of the operation</div>
<div class="quiz-option" data-correct="true">Approval status (auto-approved, user-approved, denied)</div>
<div class="quiz-explanation">Audit logs should contain: timestamp, user identity, session ID, action, target resource, tool used, approval status, content hash, and risk level. Model weights are internal implementation details, not audit data.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the role of the "Host" in MCP architecture?</div>
<div class="quiz-option" data-correct="true">The application running the AI model (e.g., VS Code IDE)</div>
<div class="quiz-option" data-correct="false">The external tool being connected to</div>
<div class="quiz-option" data-correct="false">The communication protocol</div>
<div class="quiz-option" data-correct="false">The user's web browser</div>
<div class="quiz-explanation">The Host is the application that runs the AI model and coordinates with MCP clients. In GitHub Copilot's case, the IDE (VS Code) is the host application.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent workflow needs to deploy code to staging. The deployment requires a cloud provider API key.</div>
<div class="quiz-stem">How should this secret be managed?</div>
<div class="quiz-option" data-correct="false">Store it in the repository's README</div>
<div class="quiz-option" data-correct="false">Pass it as a command line argument</div>
<div class="quiz-option" data-correct="true">Store in GitHub Secrets and inject via environment variable in the workflow</div>
<div class="quiz-option" data-correct="false">Email it to the agent service account</div>
<div class="quiz-explanation">Secrets should be stored in a vault (GitHub Secrets) and injected at runtime via environment variables. They should never appear in code, logs, command lines, or any plaintext location.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which Copilot agent mode tool would you use to find all usages of a function across a large codebase?</div>
<div class="quiz-option" data-correct="false">write_file</div>
<div class="quiz-option" data-correct="true">search_files</div>
<div class="quiz-option" data-correct="false">run_command</div>
<div class="quiz-option" data-correct="false">web_search</div>
<div class="quiz-explanation">search_files is the tool for finding code patterns, symbols, and references across the workspace. It's a read operation that doesn't modify anything.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the security implication of using HTTP/SSE transport for MCP instead of stdio?</div>
<div class="quiz-option" data-correct="false">No security difference</div>
<div class="quiz-option" data-correct="true">HTTP/SSE enables remote communication, introducing network attack surface requiring TLS and authentication</div>
<div class="quiz-option" data-correct="false">HTTP/SSE is always more secure</div>
<div class="quiz-option" data-correct="false">stdio has more security risks</div>
<div class="quiz-explanation">HTTP/SSE communicates over the network (vs. stdio's local process communication). This introduces: man-in-the-middle risks (need TLS), unauthorized access risks (need auth), and data exposure risks (need encryption).</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What does "idempotent" mean in the context of agent workflow steps?</div>
<div class="quiz-option" data-correct="false">The step runs only once</div>
<div class="quiz-option" data-correct="true">Running the step multiple times produces the same result as running it once</div>
<div class="quiz-option" data-correct="false">The step cannot fail</div>
<div class="quiz-option" data-correct="false">The step requires no input</div>
<div class="quiz-explanation">Idempotent steps are safe to retry because repeating them doesn't change the outcome. This is crucial for agent workflows: if a step fails mid-way, the agent can safely re-run it without causing duplicate effects.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which operations should be in an agent's "deny" list regardless of other permissions?</div>
<div class="quiz-option" data-correct="false">Reading source code files</div>
<div class="quiz-option" data-correct="true">Commands like rm -rf, sudo, and curl piped to bash</div>
<div class="quiz-option" data-correct="false">Running unit tests</div>
<div class="quiz-option" data-correct="false">Creating new files</div>
<div class="quiz-explanation">Destructive commands (rm -rf), privilege escalation (sudo), and arbitrary code execution (curl | bash) should always be denied. These can cause irreversible damage or compromise system security.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is MCP "Sampling" capability?</div>
<div class="quiz-option" data-correct="false">The server randomly selects which tools to expose</div>
<div class="quiz-option" data-correct="true">The server can request LLM completions from the host application</div>
<div class="quiz-option" data-correct="false">The client samples random data from the server</div>
<div class="quiz-option" data-correct="false">Performance sampling for monitoring</div>
<div class="quiz-explanation">MCP Sampling allows servers to request that the host (which has the LLM) generate completions on behalf of the server. This enables servers to use AI capabilities without having their own model.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer's agent accidentally committed a file containing an API key to a public repository.</div>
<div class="quiz-stem">What is the correct incident response sequence?</div>
<div class="quiz-option" data-correct="false">Delete the file and push again</div>
<div class="quiz-option" data-correct="true">Immediately rotate the exposed key, remove the file from git history, enable secret scanning to prevent recurrence, and document the incident</div>
<div class="quiz-option" data-correct="false">Make the repository private</div>
<div class="quiz-option" data-correct="false">Ignore it since it's just a development key</div>
<div class="quiz-explanation">Secret exposure requires: immediate rotation (the key is compromised), history cleanup (the key exists in git history even if the file is deleted), prevention (enable scanning), and documentation (learn from the incident).</div>
</div>
</div>
</div>
