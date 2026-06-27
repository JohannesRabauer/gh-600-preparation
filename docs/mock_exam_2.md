# Mock Exam 2

!!! info "Instructions"
    60 questions • 120 minutes • Score 700/1000 to pass
    Emphasis on Domains 2 (Implementation) & 4 (Security). Heavy focus on CLI commands, GitHub Actions configuration, and MCP setup.

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which MCP capability type allows servers to expose pre-built prompt templates for common tasks?</div>
<div class="quiz-option" data-correct="false">Tools</div>
<div class="quiz-option" data-correct="false">Resources</div>
<div class="quiz-option" data-correct="true">Prompts</div>
<div class="quiz-option" data-correct="false">Sampling</div>
<div class="quiz-explanation">MCP Prompts are pre-built prompt templates that servers can expose. Tools are actions to invoke, Resources are data to read, and Sampling allows servers to request LLM completions from the host. <a href="../study_notes/#22-model-context-protocol-mcp">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the principle of least privilege in the context of AI agents?</div>
<div class="quiz-option" data-correct="false">Give agents maximum access so they can complete tasks faster</div>
<div class="quiz-option" data-correct="true">Grant agents only the minimum permissions required to complete their specific task</div>
<div class="quiz-option" data-correct="false">Remove all agent permissions by default with token budget allocated from the organization pool</div>
<div class="quiz-option" data-correct="false">Only allow agents to read files, inheriting the parent agent configuration by default</div>
<div class="quiz-explanation">Least privilege means agents get exactly the access they need — no more, no less. This minimizes risk while maintaining utility. Full access is too permissive; no access is too restrictive. <a href="../study_notes/#41-access-controls-for-ai-agents">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team is building an MCP server that connects to their CI/CD system. The server needs to let agents check build status (read) and trigger builds (write).</div>
<div class="quiz-stem">What security measures should the server implement?</div>
<div class="quiz-option" data-correct="false">No restrictions — the agent knows what's appropriate</div>
<div class="quiz-option" data-correct="true">Separate tools for read (auto-approved) and write (requires user confirmation), rate limiting on build triggers, and audit logging</div>
<div class="quiz-option" data-correct="false">Only allow build status checks, never triggers, scoped to the repository context by default</div>
<div class="quiz-option" data-correct="false">Hardcode the CI/CD token in the server code</div>
<div class="quiz-explanation">Best practice: separate read and write tools with different approval levels. Read (build status) is safe for auto-approval. Write (trigger build) requires human confirmation. Add rate limiting and audit logging for governance. <a href="../study_notes/#42-agent-permissions-and-boundaries">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which of the following are valid entries in an agent audit log? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Timestamp of the action</div>
<div class="quiz-option" data-correct="true">User identity who triggered the agent</div>
<div class="quiz-option" data-correct="true">Tool that was used</div>
<div class="quiz-option" data-correct="false">The AI model's internal weights, checked against the configured boundaries</div>
<div class="quiz-option" data-correct="true">Risk level of the operation</div>
<div class="quiz-option" data-correct="true">Approval status (auto-approved, user-approved, denied)</div>
<div class="quiz-explanation">Audit logs should contain: timestamp, user identity, session ID, action, target resource, tool used, approval status, content hash, and risk level. Model weights are internal implementation details, not audit data. <a href="../study_notes/#43-security-compliance-monitoring">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the role of the "Host" in MCP architecture?</div>
<div class="quiz-option" data-correct="true">The application running the AI model (e.g., VS Code IDE)</div>
<div class="quiz-option" data-correct="false">The external tool being connected to</div>
<div class="quiz-option" data-correct="false">The communication protocol using the stdio transport with JSON-RPC framing</div>
<div class="quiz-option" data-correct="false">The user's web browser with connection pooling enabled for concurrent requests</div>
<div class="quiz-explanation">The Host is the application that runs the AI model and coordinates with MCP clients. In GitHub Copilot's case, the IDE (VS Code) is the host application. <a href="../study_notes/#22-model-context-protocol-mcp">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An agent workflow needs to deploy code to staging. The deployment requires a cloud provider API key.</div>
<div class="quiz-stem">How should this secret be managed?</div>
<div class="quiz-option" data-correct="false">Store it in the repository's README with concurrency groups preventing parallel execution</div>
<div class="quiz-option" data-correct="false">Pass it as a command line argument, cached between workflow runs for faster startup</div>
<div class="quiz-option" data-correct="true">Store in GitHub Secrets and inject via environment variable in the workflow</div>
<div class="quiz-option" data-correct="false">Email it to the agent service account</div>
<div class="quiz-explanation">Secrets should be stored in a vault (GitHub Secrets) and injected at runtime via environment variables. They should never appear in code, logs, command lines, or any plaintext location. <a href="../study_notes/#45-managing-secrets-in-agent-workflows">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which Copilot agent mode tool would you use to find all usages of a function across a large codebase?</div>
<div class="quiz-option" data-correct="false">write_file</div>
<div class="quiz-option" data-correct="true">search_files</div>
<div class="quiz-option" data-correct="false">run_command</div>
<div class="quiz-option" data-correct="false">web_search</div>
<div class="quiz-explanation">search_files is the tool for finding code patterns, symbols, and references across the workspace. It's a read operation that doesn't modify anything. <a href="../study_notes/#24-agent-tools-and-capabilities">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the security implication of using HTTP/SSE transport for MCP instead of stdio?</div>
<div class="quiz-option" data-correct="false">No security difference, validated against the server capability schema on startup</div>
<div class="quiz-option" data-correct="true">HTTP/SSE enables remote communication, introducing network attack surface requiring TLS and authentication</div>
<div class="quiz-option" data-correct="false">HTTP/SSE is always more secure</div>
<div class="quiz-option" data-correct="false">stdio has more security risks, configured via the server manifest in the workspace root</div>
<div class="quiz-explanation">HTTP/SSE communicates over the network (vs. stdio's local process communication). This introduces: man-in-the-middle risks (need TLS), unauthorized access risks (need auth), and data exposure risks (need encryption). <a href="../study_notes/#22-model-context-protocol-mcp">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What does "idempotent" mean in the context of agent workflow steps?</div>
<div class="quiz-option" data-correct="false">The step runs only once, pinned to a specific runner image version</div>
<div class="quiz-option" data-correct="true">Running the step multiple times produces the same result as running it once</div>
<div class="quiz-option" data-correct="false">The step cannot fail with the workflow_dispatch trigger for manual override</div>
<div class="quiz-option" data-correct="false">The step requires no input</div>
<div class="quiz-explanation">Idempotent steps are safe to retry because repeating them doesn't change the outcome. This is crucial for agent workflows: if a step fails mid-way, the agent can safely re-run it without causing duplicate effects. <a href="../study_notes/#23-multi-step-agent-workflows">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which operations should be in an agent's "deny" list regardless of other permissions?</div>
<div class="quiz-option" data-correct="false">Reading source code files</div>
<div class="quiz-option" data-correct="true">Commands like rm -rf, sudo, and curl piped to bash</div>
<div class="quiz-option" data-correct="false">Running unit tests, validated by the policy enforcement layer</div>
<div class="quiz-option" data-correct="false">Creating new files with token budget allocated from the organization pool</div>
<div class="quiz-explanation">Destructive commands (rm -rf), privilege escalation (sudo), and arbitrary code execution (curl | bash) should always be denied. These can cause irreversible damage or compromise system security. <a href="../study_notes/#42-agent-permissions-and-boundaries">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is MCP "Sampling" capability?</div>
<div class="quiz-option" data-correct="false">The server randomly selects which tools to expose</div>
<div class="quiz-option" data-correct="true">The server can request LLM completions from the host application</div>
<div class="quiz-option" data-correct="false">The client samples random data from the server</div>
<div class="quiz-option" data-correct="false">Performance sampling for monitoring</div>
<div class="quiz-explanation">MCP Sampling allows servers to request that the host (which has the LLM) generate completions on behalf of the server. This enables servers to use AI capabilities without having their own model. <a href="../study_notes/#22-model-context-protocol-mcp">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer's agent accidentally committed a file containing an API key to a public repository.</div>
<div class="quiz-stem">What is the correct incident response sequence?</div>
<div class="quiz-option" data-correct="false">Delete the file and push again and snapshots captured between each step</div>
<div class="quiz-option" data-correct="true">Immediately rotate the exposed key, remove the file from git history, enable secret scanning to prevent recurrence, and document the incident</div>
<div class="quiz-option" data-correct="false">Make the repository private, compared to the defined guardrail criteria</div>
<div class="quiz-option" data-correct="false">Ignore it since it's just a development key</div>
<div class="quiz-explanation">Secret exposure requires: immediate rotation (the key is compromised), history cleanup (the key exists in git history even if the file is deleted), prevention (enable scanning), and documentation (learn from the incident). <a href="../study_notes/#45-managing-secrets-in-agent-workflows">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team wants their Copilot cloud agent to have access to a custom internal API through MCP. They create a configuration file.</div>
<div class="quiz-stem">Which file path and top-level JSON key is correct for configuring MCP servers for the Copilot cloud agent?</div>
<div class="quiz-option" data-correct="false">.vscode/mcp.json with "servers" key with connection pooling enabled for concurrent requests</div>
<div class="quiz-option" data-correct="true">Repository Settings UI (MCP configuration) or .github/copilot/mcp.json with "mcpServers" key</div>
<div class="quiz-option" data-correct="false">.github/mcp-config.json with "mcpServers" key</div>
<div class="quiz-option" data-correct="false">.github/copilot/mcp.json with "servers" key</div>
<div class="quiz-explanation">The Copilot cloud agent reads MCP configuration from the repository Settings UI (Code &amp; automation → Copilot → MCP servers). The JSON format uses "mcpServers" as the top-level key. This differs from VS Code's .vscode/mcp.json which uses "servers". The two formats are NOT interchangeable.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A repository's MCP configuration for the cloud agent references a secret API key. The secret is stored in the repository's "Agents" secrets section.</div>
<div class="quiz-stem">What naming convention MUST the secret follow to be accessible in MCP configuration?</div>
<div class="quiz-option" data-correct="false">Any name works — secrets are referenced by exact name</div>
<div class="quiz-option" data-correct="true">The secret name MUST be prefixed with COPILOT_MCP_ (e.g., COPILOT_MCP_API_KEY)</div>
<div class="quiz-option" data-correct="false">Secrets must start with MCP_ prefix</div>
<div class="quiz-option" data-correct="false">Secrets must be stored in GitHub Actions secrets, not Agents secrets</div>
<div class="quiz-explanation">MCP secrets for the Copilot cloud agent MUST be prefixed with "COPILOT_MCP_" and are stored under Settings → Security → Secrets and variables → Agents. Only secrets with this prefix are available to MCP configurations. They're referenced as $COPILOT_MCP_VARNAME in the JSON config.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer is setting up copilot-setup-steps.yml for a Python project. They want it to install dependencies and set up the environment.</div>
<div class="quiz-stem">What is the CRITICAL naming requirement for the job in copilot-setup-steps.yml?</div>
<div class="quiz-option" data-correct="false">The job can have any name — Copilot detects setup steps automatically</div>
<div class="quiz-option" data-correct="true">The job MUST be named exactly "copilot-setup-steps"</div>
<div class="quiz-option" data-correct="false">The job must be named "setup" to match GitHub Actions conventions</div>
<div class="quiz-option" data-correct="false">The job name must match the filename without extension</div>
<div class="quiz-explanation">The cloud agent specifically looks for a job named "copilot-setup-steps" in the workflow file. If the job has any other name, it will be completely ignored and the agent will start without any environment setup. This is a common misconfiguration that causes agent failures.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team is configuring the copilot-setup-steps.yml. They want it to validate automatically when modified in a PR.</div>
<div class="quiz-stem">Which trigger configuration allows both cloud agent invocation AND automatic validation on changes?</div>
<div class="quiz-option" data-correct="true">```yaml
on:
  workflow_dispatch:
  push:
    paths:
      - .github/workflows/copilot-setup-steps.yml
  pull_request:
    paths:
      - .github/workflows/copilot-setup-steps.yml
```</div>
<div class="quiz-option" data-correct="false">```yaml
on:
  workflow_dispatch:
```</div>
<div class="quiz-option" data-correct="false">```yaml
on:
  push:
  pull_request:
```</div>
<div class="quiz-option" data-correct="false">```yaml
on:
  copilot_invoke:
  pull_request:
```</div>
<div class="quiz-explanation">The recommended trigger includes: workflow_dispatch (for cloud agent invocation and manual runs), plus push/pull_request filtered to the file's own path (auto-validates when modified). The workflow auto-runs as a PR check when the file itself changes, catching configuration errors before merging to default branch.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the maximum execution time for a single Copilot cloud agent session?</div>
<div class="quiz-option" data-correct="false">30 minutes</div>
<div class="quiz-option" data-correct="true">59 minutes (hard limit)</div>
<div class="quiz-option" data-correct="false">120 minutes</div>
<div class="quiz-option" data-correct="false">No time limit — it runs until completion</div>
<div class="quiz-explanation">The Copilot cloud agent has a hard maximum execution time of 59 minutes per session. This matches the GitHub Actions job timeout maximum. The agent must complete its work (including creating the PR) within this window, making efficient task decomposition critical for complex tasks.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">Which are valid ways to trigger the Copilot cloud agent to start working on a task? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Assign an issue to "Copilot" from the Assignees menu</div>
<div class="quiz-option" data-correct="true">Use the /task slash command in Copilot Chat on GitHub.com</div>
<div class="quiz-option" data-correct="true">Comment @copilot on an existing pull request</div>
<div class="quiz-option" data-correct="true">Use the GitHub CLI: copilot -p "task description"</div>
<div class="quiz-option" data-correct="false">Push a commit with "[copilot]" in the message</div>
<div class="quiz-option" data-correct="true">Click the "Task" button on the GitHub dashboard</div>
<div class="quiz-explanation">The cloud agent can be triggered via: issue assignment, /task slash command in Chat, @copilot in PR comments, the CLI, the dashboard Task button, VS Code/JetBrains IDEs, the Agents tab, and third-party integrations (Slack, Jira, Linear). Commit messages do NOT trigger the agent.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A copilot-setup-steps.yml includes `actions/checkout@v4` with `fetch-depth: 1` specified.</div>
<div class="quiz-stem">What happens with the fetch-depth setting?</div>
<div class="quiz-option" data-correct="false">Only the latest commit is checked out, limiting the agent's git history access</div>
<div class="quiz-option" data-correct="true">The fetch-depth value is automatically overridden by the cloud agent</div>
<div class="quiz-option" data-correct="false">The agent fails because it requires full history (fetch-depth: 0)</div>
<div class="quiz-option" data-correct="false">The setting is respected exactly as configured</div>
<div class="quiz-explanation">Per GitHub documentation, any fetch-depth specified in actions/checkout within copilot-setup-steps is automatically overridden by the cloud agent. The agent manages its own checkout depth requirements. This means you should include actions/checkout but not worry about optimizing fetch-depth for the agent.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer configures a custom agent at `.github/agents/test-expert.agent.md`. They want it to only write tests and never modify production code.</div>
<div class="quiz-stem">Which frontmatter configuration correctly restricts the agent's capabilities?</div>
<div class="quiz-option" data-correct="true">```yaml
---
name: test-expert
description: Writes and maintains tests. Never modifies production source code.
tools: ['read', 'search', 'edit', 'execute']
---
Focus exclusively on test files in tests/ and __tests__/ directories.
Never modify files in src/ unless they are test utilities.
```</div>
<div class="quiz-option" data-correct="false">```yaml
---
name: test-expert
permissions:
  write: ['tests/**']
  deny: ['src/**']
---
```</div>
<div class="quiz-option" data-correct="false">```yaml
---
name: test-expert
scope: tests-only
restricted: true
---
```</div>
<div class="quiz-option" data-correct="false">```yaml
---
agent: test-expert
type: restricted
allowed-paths: ['tests/']
---
```</div>
<div class="quiz-explanation">Custom agents use `.agent.md` files with YAML frontmatter containing: name, description (required), tools (list of allowed tools), and optional properties. The body is natural language instructions. There are no "permissions", "scope", or "restricted" fields — behavioral constraints are expressed in the prompt body and description.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A Copilot cloud agent cannot comply with a ruleset that requires specific commit authors (since the agent commits under its own identity).</div>
<div class="quiz-stem">How should the team resolve this?</div>
<div class="quiz-option" data-correct="false">Disable the ruleset entirely with verbose output logged to ~/.copilot/debug.log</div>
<div class="quiz-option" data-correct="true">Add Copilot as a bypass actor in the ruleset configuration (Settings → Rules → Rulesets → Add bypass → select Copilot)</div>
<div class="quiz-option" data-correct="false">Configure the agent to impersonate a human user's identity</div>
<div class="quiz-option" data-correct="false">Move to branch protection rules instead of rulesets</div>
<div class="quiz-explanation">Rulesets support bypass actors — you can add Copilot to the bypass list so it can operate even when rules like "require specific commit authors" would otherwise block it. Bypass modes include "Always allow" (direct push) or "For pull requests only" (must use PR workflow). This maintains rules for humans while enabling the agent.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which two MCP servers are enabled by DEFAULT for the Copilot cloud agent without any configuration?</div>
<div class="quiz-option" data-correct="false">Fetch and Filesystem, configured via the server manifest in the workspace root</div>
<div class="quiz-option" data-correct="true">GitHub MCP server (read-only, scoped to current repo) and Playwright MCP server (restricted to localhost)</div>
<div class="quiz-option" data-correct="false">GitHub and Docker, validated against the server capability schema on startup</div>
<div class="quiz-option" data-correct="false">No MCP servers are enabled by default</div>
<div class="quiz-explanation">The Copilot cloud agent ships with two out-of-box MCP servers: the GitHub MCP server (providing read-only tools scoped to the current repository) and the Playwright MCP server (browser automation restricted to localhost only). These are available without any MCP configuration.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team has path-specific custom instructions for TypeScript files. They want these instructions to apply to the cloud agent but NOT to Copilot code review.</div>
<div class="quiz-stem">Which frontmatter property in the instructions file achieves this?</div>
<div class="quiz-option" data-correct="false">```yaml
---
applyTo: "**/*.ts"
agent-only: true
---
```</div>
<div class="quiz-option" data-correct="true">```yaml
---
applyTo: "**/*.ts"
excludeAgent: "code-review"
---
```</div>
<div class="quiz-option" data-correct="false">```yaml
---
applyTo: "**/*.ts"
target: "cloud-agent"
---
```</div>
<div class="quiz-option" data-correct="false">```yaml
---
applyTo: "**/*.ts"
scope: ["cloud-agent", "ide"]
---
```</div>
<div class="quiz-explanation">Path-specific instructions (in .github/instructions/*.instructions.md) support the excludeAgent property. Setting excludeAgent: "code-review" means the instructions apply to the cloud agent and IDE but NOT to Copilot code review. If omitted, both agents use the file. Valid values are "code-review" and "cloud-agent".</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team has custom instructions at three levels: personal, repository (.github/copilot-instructions.md), and organization.</div>
<div class="quiz-stem">What is the priority order when instructions conflict?</div>
<div class="quiz-option" data-correct="false">Organization (highest) → Repository → Personal (lowest)</div>
<div class="quiz-option" data-correct="true">Personal (highest) → Repository → Organization (lowest)</div>
<div class="quiz-option" data-correct="false">Repository (highest) → Personal → Organization (lowest)</div>
<div class="quiz-option" data-correct="false">All levels have equal priority and are merged without precedence</div>
<div class="quiz-explanation">Custom instructions follow: Personal (highest priority) → Repository → Organization (lowest). This means a developer's personal instructions override repository defaults, which override org-wide guidelines. This enables individual customization while maintaining organizational baselines.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to reference an MCP secret named "SENTRY_TOKEN" in the cloud agent's MCP configuration JSON.</div>
<div class="quiz-stem">What is the correct way to store and reference this secret?</div>
<div class="quiz-option" data-correct="false">Store as "SENTRY_TOKEN" in Actions secrets, reference as ${{ secrets.SENTRY_TOKEN }}</div>
<div class="quiz-option" data-correct="true">Store as "COPILOT_MCP_SENTRY_TOKEN" in Agents secrets (Settings → Security → Secrets and variables → Agents), reference as $COPILOT_MCP_SENTRY_TOKEN in the JSON</div>
<div class="quiz-option" data-correct="false">Store as "SENTRY_TOKEN" in environment variables, reference as ${env.SENTRY_TOKEN}, configured via the server manifest in the workspace root</div>
<div class="quiz-option" data-correct="false">Store as "MCP_SENTRY_TOKEN" in repository variables, reference as $MCP_SENTRY_TOKEN</div>
<div class="quiz-explanation">MCP secrets for the cloud agent require: (1) COPILOT_MCP_ prefix in the name, (2) stored under "Agents" secrets (not Actions secrets), (3) referenced with $ prefix in JSON: $COPILOT_MCP_SENTRY_TOKEN. Alternative syntax includes ${COPILOT_MCP_SENTRY_TOKEN} and ${COPILOT_MCP_SENTRY_TOKEN:-fallback}.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A repository has this MCP configuration for the cloud agent:
```json
{
  "mcpServers": {
    "sentry": {
      "type": "local",
      "command": "npx",
      "args": ["@sentry/mcp-server@latest"],
      "tools": ["tool-a", "tool-b"],
      "env": {
        "SENTRY_TOKEN": "$COPILOT_MCP_SENTRY_TOKEN"
      }
    }
  }
}
```</div>
<div class="quiz-stem">What does the "tools" field control?</div>
<div class="quiz-option" data-correct="false">It lists tools the agent must use in order</div>
<div class="quiz-option" data-correct="true">It acts as an allowlist</div>
<div class="quiz-option" data-correct="false">It defines new tools that don't exist on the server</div>
<div class="quiz-option" data-correct="false">It's a documentation field with no functional effect</div>
<div class="quiz-explanation">The "tools" field in MCP configuration is a required allowlist. It restricts which tools from the server the agent can use. Specifying ["*"] enables all tools. This is a security control — even if a server exposes dangerous tools, the config can restrict which ones the agent accesses.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer sets up the GitHub MCP server locally for use in VS Code using Docker.</div>
<div class="quiz-stem">Which .vscode/mcp.json configuration is correct for the local GitHub MCP server?</div>
<div class="quiz-option" data-correct="true">```json
{
  "servers": {
    "github": {
      "type": "stdio",
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<your-pat>"
      }
    }
  }
}
```</div>
<div class="quiz-option" data-correct="false">```json
{
  "servers": {
    "github": {
      "url": "https://github.com/mcp/api",
      "type": "http"
    }
  }
}
```</div>
<div class="quiz-option" data-correct="false">```json
{
  "mcpServers": {
    "github": {
      "command": "gh mcp start",
      "type": "local"
    }
  }
}
```</div>
<div class="quiz-option" data-correct="false">```json
{
  "servers": {
    "github": {
      "command": "npm start @github/mcp-server",
      "type": "stdio"
    }
  }
}
```</div>
<div class="quiz-explanation">The local GitHub MCP server runs via Docker with the ghcr.io/github/github-mcp-server image. It uses stdio transport (type: "stdio"), requires GITHUB_PERSONAL_ACCESS_TOKEN, and uses docker run with -i (interactive) and --rm (cleanup) flags. Note: .vscode/mcp.json uses "servers" not "mcpServers".</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization uses GitHub rulesets. Two rulesets target the main branch: one requires 1 reviewer, another requires 2 reviewers.</div>
<div class="quiz-stem">How are conflicting ruleset rules resolved?</div>
<div class="quiz-option" data-correct="false">The first ruleset created takes priority</div>
<div class="quiz-option" data-correct="true">Rules are aggregated and the most restrictive version wins</div>
<div class="quiz-option" data-correct="false">The rulesets are marked as conflicting and an admin must resolve</div>
<div class="quiz-option" data-correct="false">The average is taken — 1.5 rounds up to 2</div>
<div class="quiz-explanation">When multiple rulesets target the same branch, GitHub aggregates all rules and applies the MOST restrictive version of each. This means an agent operating on a branch subject to multiple rulesets must comply with the strictest combination. Understanding this is critical for configuring agent bypass rules.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team wants secret scanning to detect their organization's internal API key format (a 32-character hex string prefixed with "ACME-").</div>
<div class="quiz-stem">Which secret scanning feature enables this?</div>
<div class="quiz-option" data-correct="false">Partner integration — register with GitHub's partner program, subject to the organization retention policy</div>
<div class="quiz-option" data-correct="true">Custom patterns — define a regex pattern (e.g., ACME-[0-9a-f]{32}) that secret scanning uses to detect organization-specific secrets</div>
<div class="quiz-option" data-correct="false">Non-provider patterns — already included in default scanning and rotated automatically on a 90-day schedule</div>
<div class="quiz-option" data-correct="false">This requires a third-party scanning tool — GitHub can't detect custom formats</div>
<div class="quiz-explanation">GitHub secret scanning supports custom patterns — user-defined regex for organization-specific secret formats. This extends detection beyond the default partner patterns and non-provider patterns. Custom patterns can be defined at the repository or organization level.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A Copilot CLI user wants to authenticate to a GitHub Enterprise Cloud instance with data residency.</div>
<div class="quiz-stem">Which command authenticates to a custom GitHub Enterprise host?</div>
<div class="quiz-option" data-correct="false">copilot login --enterprise "company-name"</div>
<div class="quiz-option" data-correct="true">copilot login --host https://example.ghe.com</div>
<div class="quiz-option" data-correct="false">gh auth login -h example.ghe.com && copilot</div>
<div class="quiz-option" data-correct="false">copilot --github-url https://example.ghe.com</div>
<div class="quiz-explanation">Copilot CLI authenticates to GitHub Enterprise Cloud with data residency using copilot login --host URL. This performs OAuth authentication against the specified host. The old gh auth pattern doesn't apply to the new Copilot CLI which has its own authentication flow.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which authentication token types does Copilot CLI accept? (Environment variable priority order)</div>
<div class="quiz-option" data-correct="false">GITHUB_TOKEN → GH_TOKEN → Personal Access Token (ghp_)</div>
<div class="quiz-option" data-correct="true">COPILOT_GITHUB_TOKEN (highest) → GH_TOKEN → GITHUB_TOKEN</div>
<div class="quiz-option" data-correct="false">GH_TOKEN → GITHUB_TOKEN → COPILOT_TOKEN</div>
<div class="quiz-option" data-correct="false">Any GitHub token format is accepted with equal priority</div>
<div class="quiz-explanation">Copilot CLI checks tokens in priority order: COPILOT_GITHUB_TOKEN first, then GH_TOKEN, then GITHUB_TOKEN. Critically, classic Personal Access Tokens (ghp_) are NOT supported — only fine-grained tokens or OAuth tokens work. This is a common authentication failure cause.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team wants to run multiple Copilot CLI tasks in parallel without them interfering with each other.</div>
<div class="quiz-stem">Which approach provides isolation for parallel task execution?</div>
<div class="quiz-option" data-correct="false">Run multiple copilot commands in different terminal tabs</div>
<div class="quiz-option" data-correct="true">Use copilot --cloud to start cloud-backed sessions</div>
<div class="quiz-option" data-correct="false">Use copilot --parallel flag</div>
<div class="quiz-option" data-correct="false">Clone the repository multiple times and run copilot in each clone</div>
<div class="quiz-explanation">Cloud sandboxes (copilot --cloud) provide isolated environments for parallel work. The /fleet command enables parallel task execution within Copilot CLI. Multiple local sessions in the same directory risk file conflicts, while cloud sessions are fully isolated from each other and the local machine.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A custom agent file is located at .github/agents/security-reviewer.agent.md. A developer wants to invoke it from Copilot Chat on GitHub.com.</div>
<div class="quiz-stem">How is a custom agent invoked?</div>
<div class="quiz-option" data-correct="false">@security-reviewer in the chat and piped through the system shell for expansion</div>
<div class="quiz-option" data-correct="true">Use the /agent slash command or select the agent from the agent picker</div>
<div class="quiz-option" data-correct="false">gh copilot --agent security-reviewer</div>
<div class="quiz-option" data-correct="false">Assign the issue to "security-reviewer"</div>
<div class="quiz-explanation">Custom agents defined in .github/agents/ are invokable via the /agent slash command in Copilot CLI or through the agent picker UI. They can also be auto-delegated by Copilot when the task matches their description. The @mention syntax is for Copilot Extensions (deprecated), not custom agents.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">GitHub secret scanning detects a leaked AWS key in a public repository. The key was committed by a Copilot cloud agent.</div>
<div class="quiz-stem">What happens automatically through GitHub's partner integration?</div>
<div class="quiz-option" data-correct="false">GitHub displays an alert and waits for manual action</div>
<div class="quiz-option" data-correct="true">GitHub automatically notifies AWS (the service provider) to revoke the detected key. Partner integration handles this silently</div>
<div class="quiz-option" data-correct="false">GitHub blocks all subsequent pushes from the agent</div>
<div class="quiz-option" data-correct="false">GitHub reverts the commit containing the secret</div>
<div class="quiz-explanation">Secret scanning's partner integration automatically notifies service providers (AWS, Azure, GitHub tokens, etc.) to revoke detected secrets in public repositories. This happens regardless of who committed the secret (human or agent). Partner-handled alerts may not appear in the security tab — they're resolved directly between GitHub and the provider.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A copilot-setup-steps.yml has a step that fails (returns non-zero exit code). The remaining steps haven't run yet.</div>
<div class="quiz-stem">What happens to the cloud agent's session?</div>
<div class="quiz-option" data-correct="false">The entire agent session is aborted with verbose output logged to ~/.copilot/debug.log</div>
<div class="quiz-option" data-correct="true">The remaining setup steps are skipped, but the Copilot cloud agent still continues with its task</div>
<div class="quiz-option" data-correct="false">The workflow retries the failed step 3 times before giving up</div>
<div class="quiz-option" data-correct="false">The agent waits for a human to fix the setup step</div>
<div class="quiz-explanation">Per GitHub documentation: "If any step returns a non-zero exit code, remaining steps are skipped but Copilot continues." The agent proceeds with whatever environment was set up before the failure. This means a failing npm install won't prevent the agent from starting, but it may fail later when trying to use those dependencies.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer has the deprecated `gh copilot` extension installed and wants to use the new Copilot CLI.</div>
<div class="quiz-stem">What is the relationship between the old `gh copilot` extension and the new Copilot CLI?</div>
<div class="quiz-option" data-correct="false">They can be used side by side — the new CLI supplements the old extension</div>
<div class="quiz-option" data-correct="true">The gh copilot extension (github/gh-copilot) was deprecated on October 25, 2025 and replaced by the standalone `copilot` CLI command</div>
<div class="quiz-option" data-correct="false">The new CLI is just a rename — same commands, same functionality</div>
<div class="quiz-option" data-correct="false">The gh copilot extension was upgraded in-place to become the new CLI, honoring any local project overrides</div>
<div class="quiz-explanation">The gh copilot extension (with commands: suggest, explain, alias, config) was deprecated October 2025. The replacement — the standalone `copilot` command — is a full AI agent that can edit files, run commands, create PRs, and work autonomously. It's fundamentally more capable than the old suggest/explain tool.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team is configuring a remote MCP server (Cloudflare) for their cloud agent.</div>
<div class="quiz-stem">Which MCP configuration correctly defines a remote SSE server?</div>
<div class="quiz-option" data-correct="true">```json
{
  "mcpServers": {
    "cloudflare": {
      "type": "sse",
      "url": "https://docs.mcp.cloudflare.com/sse",
      "tools": ["*"]
    }
  }
}
```</div>
<div class="quiz-option" data-correct="false">```json
{
  "mcpServers": {
    "cloudflare": {
      "command": "curl",
      "args": ["https://docs.mcp.cloudflare.com/sse"],
      "type": "remote"
    }
  }
}
```</div>
<div class="quiz-option" data-correct="false">```json
{
  "mcpServers": {
    "cloudflare": {
      "url": "https://docs.mcp.cloudflare.com/sse",
      "transport": "sse"
    }
  }
}
```</div>
<div class="quiz-option" data-correct="false">```json
{
  "mcpServers": {
    "cloudflare": {
      "type": "http",
      "endpoint": "https://docs.mcp.cloudflare.com/sse"
    }
  }
}
```</div>
<div class="quiz-explanation">Remote MCP servers use type: "sse" (or "http") with a "url" field pointing to the server endpoint. The "tools" field is required as an allowlist. Remote servers don't use "command" or "args" (those are for local/stdio servers). The field is "url" not "endpoint", and "type" not "transport".</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">Code scanning finds a SQL injection vulnerability in an agent-generated PR. Copilot Autofix suggests a fix.</div>
<div class="quiz-stem">How does the Autofix suggestion appear and what happens when accepted?</div>
<div class="quiz-option" data-correct="false">Autofix automatically commits the fix without human involvement</div>
<div class="quiz-option" data-correct="true">Autofix posts a suggestion as a PR comment with a one-click "Accept fix" button. When a developer clicks accept, the fix is committed to the PR branch</div>
<div class="quiz-option" data-correct="false">Autofix creates a separate PR with the security fix, reading preferences from the project root</div>
<div class="quiz-option" data-correct="false">Autofix adds an inline code suggestion that the agent auto-applies on next iteration</div>
<div class="quiz-explanation">Copilot Autofix maintains human-in-the-loop: it suggests fixes via PR comments with a one-click accept button. The fix is ONLY committed when a human explicitly accepts it. This ensures security fixes are reviewed before application, even when the original code was agent-generated.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team notices that code scanning results appear differently for alerts from public vs. private repositories.</div>
<div class="quiz-stem">What is the licensing requirement for code scanning on private repositories?</div>
<div class="quiz-option" data-correct="false">Code scanning is free for all repository types</div>
<div class="quiz-option" data-correct="true">Private repositories require GitHub Code Security (part of GitHub Advanced Security) license</div>
<div class="quiz-option" data-correct="false">Only Enterprise plans can use code scanning</div>
<div class="quiz-option" data-correct="false">Code scanning requires a separate third-party license regardless of repo type</div>
<div class="quiz-explanation">Code scanning availability differs by repository visibility: public repos get it included, private repos require GitHub Code Security (formerly part of GitHub Advanced Security). This is important for organizations planning agent governance — code scanning as a guardrail requires proper licensing for private repos.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team wants to upload third-party static analysis results (from a non-CodeQL tool) to GitHub's code scanning.</div>
<div class="quiz-stem">What format must the results be in?</div>
<div class="quiz-option" data-correct="false">JSON with GitHub's proprietary schema</div>
<div class="quiz-option" data-correct="true">SARIF (Static Analysis Results Interchange Format)</div>
<div class="quiz-option" data-correct="false">JUnit XML format</div>
<div class="quiz-option" data-correct="false">CSV with columns: file, line, severity, message</div>
<div class="quiz-explanation">GitHub code scanning accepts results in SARIF format — an OASIS open standard for static analysis tool output. Third-party tools generate SARIF files which are uploaded via the upload-sarif action or API. This enables organizations to combine CodeQL with other SAST tools in their agent evaluation pipeline.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to configure Copilot memory (persistent understanding) for their repository so the agent remembers coding conventions across sessions.</div>
<div class="quiz-stem">What is Copilot Memory and how does it differ from custom instructions?</div>
<div class="quiz-option" data-correct="false">They are the same thing — Memory is just a new name for custom instructions</div>
<div class="quiz-option" data-correct="true">Copilot Memory stores "memories"</div>
<div class="quiz-option" data-correct="false">Memory stores conversation history across all sessions</div>
<div class="quiz-option" data-correct="false">Memory is only available in the IDE, not the cloud agent</div>
<div class="quiz-explanation">Copilot Memory is a persistent understanding system where Copilot automatically deduces and stores patterns, conventions, and preferences from your repository as it works. This differs from custom instructions (manually authored) by being automatically generated. It reduces repetitive context-setting across sessions.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">In the copilot-setup-steps.yml, what is the maximum value allowed for the timeout-minutes setting?</div>
<div class="quiz-option" data-correct="false">30</div>
<div class="quiz-option" data-correct="true">59</div>
<div class="quiz-option" data-correct="false">120</div>
<div class="quiz-option" data-correct="false">360</div>
<div class="quiz-explanation">The maximum timeout-minutes for copilot-setup-steps is 59 minutes, matching the cloud agent's maximum session duration. This prevents setup steps from consuming the entire session time. If setup takes longer than this, you should optimize (caching, smaller images) or pre-build custom runner images.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team uses Copilot Hooks to run a security scan after every agent file modification.</div>
<div class="quiz-stem">What are Copilot Hooks?</div>
<div class="quiz-option" data-correct="false">Git hooks that trigger when Copilot commits</div>
<div class="quiz-option" data-correct="true">Custom shell commands that execute at key points during agent execution</div>
<div class="quiz-option" data-correct="false">Webhook endpoints that Copilot calls</div>
<div class="quiz-option" data-correct="false">Pre-commit hooks specific to AI-generated code</div>
<div class="quiz-explanation">Copilot Hooks execute custom shell commands at key points during agent execution. They can be used for: validation (check code quality after each edit), logging (audit trail), security scanning (detect vulnerabilities in real-time), and workflow automation. They're distinct from git hooks — they're integrated into the agent's execution lifecycle.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to configure the copilot-setup-steps.yml to use a larger GitHub-hosted runner with 4 cores for faster dependency installation.</div>
<div class="quiz-stem">Which runs-on value configures a 4-core Ubuntu runner?</div>
<div class="quiz-option" data-correct="false">runs-on: ubuntu-latest-4x</div>
<div class="quiz-option" data-correct="true">runs-on: ubuntu-4-core</div>
<div class="quiz-option" data-correct="false">runs-on: ubuntu-latest with cores: 4</div>
<div class="quiz-option" data-correct="false">runs-on: ubuntu-22.04-large</div>
<div class="quiz-explanation">Larger GitHub-hosted runners use the format: ubuntu-N-core (e.g., ubuntu-4-core, ubuntu-8-core). The copilot-setup-steps.yml supports customizing runs-on to use larger runners for faster builds. Self-hosted ARC runners are also supported via their scale set name.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A company has both public and private repositories. They want secret scanning protection on all repositories.</div>
<div class="quiz-stem">What is the availability of secret scanning for public vs. private repositories?</div>
<div class="quiz-option" data-correct="false">Secret scanning is only available for Enterprise plans</div>
<div class="quiz-option" data-correct="true">Public repositories get secret scanning free and automatic</div>
<div class="quiz-option" data-correct="false">All repositories get free secret scanning regardless of plan</div>
<div class="quiz-option" data-correct="false">Secret scanning is a third-party service that requires separate licensing</div>
<div class="quiz-explanation">Secret scanning is free and automatic for public repositories (part of GitHub's security commitment). For private and internal repositories, it requires GitHub Secret Protection (Team or Enterprise Cloud plans). This means agent-generated code in public repos always gets scanned, but private repos need proper licensing.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team wants the copilot-setup-steps to only take effect from the default branch.</div>
<div class="quiz-stem">On which branch must the copilot-setup-steps.yml be present to be used by the cloud agent?</div>
<div class="quiz-option" data-correct="false">Any branch — the agent uses the version on its working branch</div>
<div class="quiz-option" data-correct="true">The default branch (typically main)</div>
<div class="quiz-option" data-correct="false">A branch named "copilot-config"</div>
<div class="quiz-option" data-correct="false">The branch specified in the workflow trigger</div>
<div class="quiz-explanation">This is a critical detail: copilot-setup-steps.yml only takes effect when present on the DEFAULT branch. Even if you create it on a feature branch, the cloud agent won't use it until it's merged to main (or whatever the default branch is). This prevents untested setup configurations from affecting agent work.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team is configuring an MCP server for the cloud agent and wants to allow ALL tools the server provides.</div>
<div class="quiz-stem">What value should the "tools" field have?</div>
<div class="quiz-option" data-correct="false">"tools": "all"</div>
<div class="quiz-option" data-correct="true">"tools": ["*"]</div>
<div class="quiz-option" data-correct="false">"tools": [] (empty array means all)</div>
<div class="quiz-option" data-correct="false">Omit the "tools" field entirely</div>
<div class="quiz-explanation">Setting "tools": ["*"] enables all tools from the MCP server. The tools field is required in MCP configuration for the cloud agent — it acts as a security allowlist. An empty array would mean NO tools are allowed. You cannot omit it, and "all" is not valid syntax.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer configures Git LFS in their copilot-setup-steps.yml because the repository uses large binary files.</div>
<div class="quiz-stem">Which checkout configuration enables LFS file download?</div>
<div class="quiz-option" data-correct="true">```yaml
- uses: actions/checkout@v4
  with:
    lfs: true
```</div>
<div class="quiz-option" data-correct="false">```yaml
- uses: actions/checkout@v4
- run: git lfs install && git lfs pull
```</div>
<div class="quiz-option" data-correct="false">```yaml
- uses: actions/checkout@v4
  with:
    include-lfs: true
```</div>
<div class="quiz-option" data-correct="false">```yaml
- uses: actions/lfs-checkout@v1
```</div>
<div class="quiz-explanation">The actions/checkout action supports LFS directly via the `lfs: true` parameter. This fetches LFS objects during checkout. While manual git lfs pull would also work, the built-in option is simpler and handles authentication automatically. There's no "include-lfs" parameter or separate lfs-checkout action.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What scope limitation does the Copilot cloud agent have regarding repositories?</div>
<div class="quiz-option" data-correct="false">It can work across up to 3 repositories simultaneously</div>
<div class="quiz-option" data-correct="true">Single repository per session</div>
<div class="quiz-option" data-correct="false">It can access any repository in the organization</div>
<div class="quiz-option" data-correct="false">It's limited to repositories under 1GB in size</div>
<div class="quiz-explanation">A key constraint of the Copilot cloud agent: single repository per session, one PR per task. Cross-repository work requires multiple agent sessions. This constraint drives the architectural pattern of decomposing cross-repo tasks into separate, coordinated agent invocations.</div>
</div>
</div>


<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which Copilot CLI slash command forces the context window to be compressed to reduce token usage mid-conversation?</div>
<div class="quiz-option" data-correct="false">/context clear</div>
<div class="quiz-option" data-correct="true">/compact</div>
<div class="quiz-option" data-correct="false">/reset</div>
<div class="quiz-option" data-correct="false">/trim</div>
<div class="quiz-explanation">/compact triggers manual context compaction, summarizing the conversation to free token capacity. Automatic compaction also occurs at 95% token limit. /context manages context sources, not compaction.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer sets up environment variables and sees this order in the Copilot CLI docs: "COPILOT_GITHUB_TOKEN → GH_TOKEN → GITHUB_TOKEN"</div>
<div class="quiz-stem">What does this order represent?</div>
<div class="quiz-option" data-correct="true">Token resolution priority</div>
<div class="quiz-option" data-correct="false">Token scoping — each applies to different API endpoints</div>
<div class="quiz-option" data-correct="false">Required tokens — all three must be set</div>
<div class="quiz-option" data-correct="false">Version preference — newer variable names take precedence</div>
<div class="quiz-explanation">The Copilot CLI checks for authentication tokens in priority order: COPILOT_GITHUB_TOKEN first, then GH_TOKEN, then GITHUB_TOKEN. The first one found is used. Note: classic PATs (ghp_ prefix) are NOT supported — only fine-grained PATs and OAuth tokens work.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What keyboard shortcut in the Copilot CLI cycles between ask/execute mode and plan mode?</div>
<div class="quiz-option" data-correct="false">Ctrl+P</div>
<div class="quiz-option" data-correct="false">Tab</div>
<div class="quiz-option" data-correct="true">Shift+Tab</div>
<div class="quiz-option" data-correct="false">Ctrl+Tab</div>
<div class="quiz-explanation">Shift+Tab toggles between ask/execute mode and plan mode in the Copilot CLI. Plan mode creates a multi-step plan before executing, while ask/execute mode handles requests directly.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization wants to restrict which MCP servers can be used with the cloud agent.</div>
<div class="quiz-stem">Where are MCP server restrictions configured at the organization level?</div>
<div class="quiz-option" data-correct="false">In the organization's .github repo under mcp-policy.json</div>
<div class="quiz-option" data-correct="true">Organization settings → Copilot → Policies (or via the Copilot API)</div>
<div class="quiz-option" data-correct="false">In each repository's CODEOWNERS file</div>
<div class="quiz-option" data-correct="false">Via a GitHub Action that validates mcp.json on push</div>
<div class="quiz-explanation">Org-level MCP policies are managed through organization Copilot settings or the Copilot API. Organization admins can restrict which MCP servers repositories are allowed to configure, providing centralized governance over tool access for the cloud agent.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team has the following `.github/agents/deploy.agent.md`:
```yaml
---
description: Handles production deployments
tools: []
model: gpt-4o
---
```</div>
<div class="quiz-stem">What effect does `tools: []` have on this custom agent?</div>
<div class="quiz-option" data-correct="false">It gives the agent all available tools (empty means no restrictions)</div>
<div class="quiz-option" data-correct="true">The agent has NO tools</div>
<div class="quiz-option" data-correct="false">It's an error — tools must be omitted or contain at least one entry</div>
<div class="quiz-option" data-correct="false">It disables MCP tools but keeps built-in tools</div>
<div class="quiz-explanation">In custom agent configuration: tools: [] (empty array) = NO tools at all, making the agent advisory-only. This is different from OMITTING the tools field entirely, which gives the agent ALL available tools. This distinction is critical for creating read-only advisory agents.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">When a copilot-setup-steps.yml step exits with a non-zero code, what happens?</div>
<div class="quiz-option" data-correct="false">The entire agent session fails and is marked as errored</div>
<div class="quiz-option" data-correct="false">The step is retried up to 3 times before failing</div>
<div class="quiz-option" data-correct="true">Remaining setup steps are skipped, but the agent still continues with whatever environment was prepared up to that point</div>
<div class="quiz-option" data-correct="false">The step failure is silently ignored and the next step runs</div>
<div class="quiz-explanation">If a copilot-setup-steps step fails: remaining steps are skipped (they don't run), BUT the agent session itself continues. The agent proceeds with whatever partial environment was set up. This means critical dependencies should be in early steps.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">How do you authenticate the Copilot CLI to a GitHub Enterprise Server instance?</div>
<div class="quiz-option" data-correct="true">copilot login --host https://github.example.com</div>
<div class="quiz-option" data-correct="false">copilot auth --enterprise github.example.com</div>
<div class="quiz-option" data-correct="false">gh auth login --hostname github.example.com (shared with gh)</div>
<div class="quiz-option" data-correct="false">Set COPILOT_ENTERPRISE_URL=https://github.example.com</div>
<div class="quiz-explanation">The standalone Copilot CLI uses `copilot login --host URL` to authenticate to a GitHub Enterprise Server. It does NOT share credentials with the gh CLI — they have separate authentication stores. The --host flag specifies the Enterprise Server URL.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer creates a custom agent file at `.github/agents/my agent!.agent.md`.</div>
<div class="quiz-stem">What happens when this file is pushed to the repository?</div>
<div class="quiz-option" data-correct="false">The agent is registered with the display name "my agent!"</div>
<div class="quiz-option" data-correct="true">The file is ignored — agent filenames may only contain letters (a-z, A-Z), digits (0-9), dots, hyphens, and underscores. Spaces and special characters are not allowed</div>
<div class="quiz-option" data-correct="false">The file causes a validation error in the repository, subject to the model routing rules set by the admin</div>
<div class="quiz-option" data-correct="false">The space is converted to a hyphen automatically with progress saved after each operation</div>
<div class="quiz-explanation">Custom agent filenames have strict naming rules: only a-z, A-Z, 0-9, dots (.), hyphens (-), and underscores (_) are allowed. Files with spaces, exclamation marks, or other characters are silently ignored. Valid examples: deploy-helper.agent.md, code_reviewer.agent.md</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An MCP server in a custom agent needs to reference a specific tool using dotted notation.</div>
<div class="quiz-stem">What is the correct format to reference a tool from an MCP server named "db-admin" in a custom agent's tools list?</div>
<div class="quiz-option" data-correct="false">tools: ["mcp:db-admin:query-users"]</div>
<div class="quiz-option" data-correct="true">tools: ["db-admin/query-users"]</div>
<div class="quiz-option" data-correct="false">tools: ["db-admin.query-users"]</div>
<div class="quiz-option" data-correct="false">tools: ["db-admin::query-users"]</div>
<div class="quiz-explanation">MCP server tools are referenced in custom agent tools lists using forward-slash notation: "server-name/tool-name". The built-in tool aliases (read→view, edit→str_replace, execute→bash, search→grep/glob) use simple names, but MCP tools always use the server-name/tool-name pattern.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization has three levels of custom instructions configured:
1. Organization-level: `.github/copilot-instructions.md` in the .github repo
2. Repository-level: `.github/copilot-instructions.md`
3. Personal settings in the IDE</div>
<div class="quiz-stem">How do these instruction sources combine?</div>
<div class="quiz-option" data-correct="false">Higher priority instructions override lower ones entirely</div>
<div class="quiz-option" data-correct="true">All instruction sources COMBINE (are concatenated)</div>
<div class="quiz-option" data-correct="false">Only the most specific level applies — others are ignored</div>
<div class="quiz-option" data-correct="false">Organization-level instructions always override repository settings</div>
<div class="quiz-explanation">Custom instructions from all sources are combined together and sent to the model. They don't replace each other — they accumulate. When instructions conflict, priority determines which is followed: Personal instructions override repo-level, which overrides org-level. But non-conflicting instructions from all levels apply simultaneously.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the maximum runtime for a single cloud agent session?</div>
<div class="quiz-option" data-correct="false">30 minutes, subject to the model routing rules set by the admin</div>
<div class="quiz-option" data-correct="true">59 minutes (matching the copilot-setup-steps timeout-minutes maximum)</div>
<div class="quiz-option" data-correct="false">120 minutes with temperature and top-p tuned for the task type</div>
<div class="quiz-option" data-correct="false">No limit — it runs until the task is complete</div>
<div class="quiz-explanation">Cloud agent sessions have a maximum runtime of 59 minutes. This same 59-minute limit applies as the maximum value for timeout-minutes in copilot-setup-steps.yml. If the agent hasn't completed its work within this window, the session ends.</div>
</div>
</div>

