# Mock Exam 3

!!! info "Instructions"
    60 questions • 120 minutes • Score 700/1000 to pass
    Advanced scenarios requiring cross-domain knowledge. Heavy emphasis on practical CLI, configuration, and GitHub Actions knowledge.

<div class="quiz" data-domain="Architecture & Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A large enterprise has 200+ repositories and wants to implement AI-assisted code review that enforces their specific security policies, coding standards, and architecture guidelines. The review agent needs access to the company's internal security rulebook (updated weekly) and their API design standards document.</div>
<div class="quiz-stem">Which architecture best serves this need?</div>
<div class="quiz-option" data-correct="false">Default Copilot chat without customization, which addresses a common misconception about this feature</div>
<div class="quiz-option" data-correct="true">A Copilot Extension for review logic combined with MCP servers that expose the security rulebook and design standards as resources</div>
<div class="quiz-option" data-correct="false">A single large prompt containing all rules, encrypted at rest with the repository public key</div>
<div class="quiz-option" data-correct="false">Manual code review by the security team for all PRs, as described in the original design specification</div>
<div class="quiz-explanation">Enterprise-scale customization requires: Extensions (custom review logic), MCP servers (dynamic access to frequently-updated documents), and resource exposure (standards as MCP resources that stay current). A prompt can't hold frequently-changing documents, and manual review doesn't scale. <a href="../study_notes/#25-building-custom-agent-extensions">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Responsible AI" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent is generating code that systematically suggests one specific open-source library over all alternatives, even when alternatives are better suited. Investigation reveals the training data contained disproportionate examples using that library.</div>
<div class="quiz-stem">Which responsible AI principles are involved and what is the fix?</div>
<div class="quiz-option" data-correct="false">Only transparency — just tell users about the bias</div>
<div class="quiz-option" data-correct="true">Fairness (biased toward one library) and Transparency (users should know about limitations)</div>
<div class="quiz-option" data-correct="false">Reliability — the agent isn't reliable enough, checked against the configured boundaries</div>
<div class="quiz-option" data-correct="false">This isn't a problem — consistency is good with token budget allocated from the organization pool</div>
<div class="quiz-explanation">Training data bias causes unfair preference (Fairness violation). Users deserve to know about this limitation (Transparency). Fix: provide balanced context (approved library list), add decision criteria, and track diversity metrics over time. <a href="../study_notes/#63-bias-and-fairness-in-agent-outputs">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Performance & Collaboration" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team's AI-assisted test generation has high coverage (90%) but developers report that 30% of generated tests are "meaningless" — they pass but don't actually validate meaningful behavior. Test suite execution time has tripled.</div>
<div class="quiz-stem">What is the best approach to improve test quality without losing coverage?</div>
<div class="quiz-option" data-correct="false">Delete all AI-generated tests and start over, blocking the merge queue until all required checks report success</div>
<div class="quiz-option" data-correct="true">Add test quality review criteria (mutation testing</div>
<div class="quiz-option" data-correct="false">Reduce coverage target to 50% and gated by the CODEOWNERS approval requirement, as described in the original design specification</div>
<div class="quiz-option" data-correct="false">Keep all tests — more is always better, scoped to protected branches matching the pattern</div>
<div class="quiz-explanation">Coverage alone doesn't indicate quality. The fix combines: quality metrics (mutation testing reveals which tests actually catch bugs), agent tuning (better prompts for meaningful tests), and pruning (remove low-value tests that slow the suite). This balances coverage, quality, and speed. <a href="../study_notes/#31-measuring-agent-output-quality">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation & Security" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer creates an MCP server that provides access to the company's customer support ticket system. Tickets contain customer names, email addresses, and sometimes credit card numbers (PII). The agent is used by developers to understand bug context.</div>
<div class="quiz-stem">What is the correct MCP server design?</div>
<div class="quiz-option" data-correct="false">Expose full ticket content as-is with connection pooling enabled for concurrent requests</div>
<div class="quiz-option" data-correct="true">Implement a data filtering layer that: redacts PII (names</div>
<div class="quiz-option" data-correct="false">Don't build the integration — too risky, which addresses a common misconception about this feature</div>
<div class="quiz-option" data-correct="false">Only expose ticket IDs without any content, reducing coordination overhead but limiting scalability</div>
<div class="quiz-explanation">The correct approach filters sensitive data at the server level: redact PII before the agent sees it, expose only the technical context developers need (errors, traces), and maintain audit logs. This balances utility (developers get bug context) with privacy (PII is protected). <a href="../study_notes/#44-data-governance-for-agent-interactions">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="All Domains" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A startup is choosing between three approaches for their AI agent deployment:
A) Full autonomy with minimal oversight
B) Supervised autonomy with approval gates for sensitive operations
C) Advisory only — agents suggest but never act</div>
<div class="quiz-stem">For a team doing rapid iteration on a non-critical internal tool, which approach balances speed and safety?</div>
<div class="quiz-option" data-correct="false">Option A — full autonomy maximizes speed with temperature and top-p tuned for the task type, as described in the original design specification</div>
<div class="quiz-option" data-correct="true">Option B — supervised autonomy with approval for sensitive ops (deploys, config changes) but auto-approve for safe ops (file edits, tests)</div>
<div class="quiz-option" data-correct="false">Option C — advisory only is always safest, simplifying the architecture at the cost of flexibility</div>
<div class="quiz-option" data-correct="false">No AI agents until the product is mature, subject to the model routing rules set by the admin</div>
<div class="quiz-explanation">Supervised autonomy balances speed and safety: auto-approve low-risk operations (reading, writing code, running tests) for speed, while requiring approval for higher-risk operations (deployments, config changes). Even for internal tools, full autonomy risks unintended changes, while advisory-only loses the speed benefit. <a href="../study_notes/#14-agent-roles-within-development-workflows">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Architecture & Performance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A company monitors their agent system and sees these metrics:
- Task completion: 88% (target >85%) ✓
- User acceptance: 62% (target >75%) ✗
- Avg iterations: 3.2 (target <5) ✓
- Error rate: 2% (target <5%) ✓
- p95 latency: 4.1s (target <5s) ✓</div>
<div class="quiz-stem">Only user acceptance is below target despite other metrics being healthy. What is the most likely cause?</div>
<div class="quiz-option" data-correct="false">The model is too slow, inheriting the parent agent configuration by default</div>
<div class="quiz-option" data-correct="true">The agent completes tasks technically but doesn't match the team's coding style, conventions, or preferences</div>
<div class="quiz-option" data-correct="false">The error rate is too high</div>
<div class="quiz-option" data-correct="false">Tasks are too complex with temperature and top-p tuned for the task type</div>
<div class="quiz-explanation">High completion + low acceptance = the agent does the job but not the way developers want. The code works (tests pass, builds succeed) but doesn't match style preferences. Fix: add coding standards to context, reference example files, configure style guides. <a href="../study_notes/#31-measuring-agent-output-quality">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Collaboration & Responsible AI" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A tech company's AI agent generates commit messages and PR descriptions. A junior developer notices the agent's PR descriptions are noticeably more detailed and professional than what they can write manually, creating an appearance gap between human and AI-authored content.</div>
<div class="quiz-stem">How should this be handled from a responsible AI perspective?</div>
<div class="quiz-option" data-correct="false">Disable AI-generated descriptions, inheriting the parent agent configuration by default, with an admin override available for emergency situations only</div>
<div class="quiz-option" data-correct="true">Add clear attribution indicating AI-generated content (transparency), while using AI assistance as a learning tool to help all team members improve their writing</div>
<div class="quiz-option" data-correct="false">Make AI descriptions less detailed to match human quality with token budget allocated from the organization pool</div>
<div class="quiz-option" data-correct="false">Require all PR descriptions to be AI-generated for consistency, which addresses a common misconception about this feature</div>
<div class="quiz-explanation">Transparency principle: AI-generated content should be clearly attributed. Additionally, framing AI as a learning tool (not a replacement) supports inclusiveness and helps the team grow. Don't reduce quality or force uniformity. <a href="../study_notes/#62-transparency-and-explainability">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Implementation" data-type="multiple-select">
<div class="quiz-question">
<div class="quiz-stem">When implementing a custom MCP server for production use, which security measures are essential? (Select all that apply)</div>
<div class="quiz-option" data-correct="true">Input validation on all tool parameters</div>
<div class="quiz-option" data-correct="true">Rate limiting to prevent abuse</div>
<div class="quiz-option" data-correct="true">Authentication for remote connections</div>
<div class="quiz-option" data-correct="false">Storing credentials in the tool response</div>
<div class="quiz-option" data-correct="true">Audit logging of all tool invocations</div>
<div class="quiz-option" data-correct="false">Making all tools auto-approved</div>
<div class="quiz-explanation">Production MCP servers need: input validation (prevent injection), rate limiting (prevent abuse), authentication (for HTTP/SSE transport), and audit logging (compliance). Never store credentials in responses or auto-approve all tools. <a href="../study_notes/#22-model-context-protocol-mcp">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="All Domains" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization is deploying their first AI agent system. The CISO wants a complete security review. The development team wants to ship fast. The compliance team needs documentation. The HR team has concerns about AI replacing jobs.</div>
<div class="quiz-stem">What is the correct order of actions to address all stakeholders?</div>
<div class="quiz-option" data-correct="false">Ship first, address concerns later and scoped to the target branch filter, as described in the original design specification</div>
<div class="quiz-option" data-correct="true">1) Define agent boundaries and permissions (CISO)</div>
<div class="quiz-option" data-correct="false">Wait until all concerns are fully resolved before any deployment, which addresses a common misconception about this feature</div>
<div class="quiz-option" data-correct="false">Ignore non-technical stakeholders, pinned to a specific runner image version</div>
<div class="quiz-explanation">Successful deployment addresses all stakeholders: security first (boundaries), compliance second (documentation), controlled rollout third (pilot with supervision), and clear communication fourth (agents augment humans). This balances safety, governance, speed, and organizational change. <a href="../study_notes/#64-compliance-with-responsible-ai-policies">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Performance & Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">An agent is making parallel tool calls to speed up a multi-file refactoring task. What risk does this introduce?</div>
<div class="quiz-option" data-correct="false">Higher cost per token, validated by the policy enforcement layer</div>
<div class="quiz-option" data-correct="true">Race conditions where parallel edits to related files may conflict or create inconsistencies</div>
<div class="quiz-option" data-correct="false">Slower overall completion and checkpointed at each tool-use boundary</div>
<div class="quiz-option" data-correct="false">No risks — parallel is always better</div>
<div class="quiz-explanation">Parallel tool calls can cause conflicts when editing related files — one edit might depend on the state created by another. The fix: identify dependencies between edits and only parallelize truly independent operations. <a href="../study_notes/#23-multi-step-agent-workflows">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer's copilot-setup-steps.yml enables a snapshot feature to speed up subsequent agent sessions.</div>
<div class="quiz-stem">What is the "snapshot" capability in copilot-setup-steps?</div>
<div class="quiz-option" data-correct="false">A git snapshot (stash) of the current working tree</div>
<div class="quiz-option" data-correct="true">A feature that saves the state of the configured environment after setup steps complete</div>
<div class="quiz-option" data-correct="false">A backup of the agent's conversation history, which addresses a common misconception about this feature</div>
<div class="quiz-option" data-correct="false">A Docker container image exported after setup, as described in the original design specification</div>
<div class="quiz-explanation">The snapshot capability in copilot-setup-steps caches the environment state after setup completes. This means subsequent agent sessions can start almost instantly without re-running npm ci, pip install, etc. It's a significant performance optimization for repositories with slow dependency installation.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team has both `.github/copilot-instructions.md` (repository-wide) and `.github/instructions/api-routes.instructions.md` (path-specific) files.</div>
<div class="quiz-stem">What is the correct format for the path-specific instructions file?</div>
<div class="quiz-option" data-correct="true">```markdown
---
applyTo: "src/api/**/*.ts"
---

Use Express.js error middleware pattern.
Always validate request body with Zod schemas.
Return standardized error responses with status codes.
```</div>
<div class="quiz-option" data-correct="false">```markdown
# API Routes Instructions
scope: src/api/**/*.ts

Use Express.js error middleware pattern.
```</div>
<div class="quiz-option" data-correct="false">```yaml
target: "src/api/**/*.ts"
instructions: |
  Use Express.js error middleware pattern.
```</div>
<div class="quiz-option" data-correct="false">```markdown
---
files: ["src/api/**/*.ts"]
type: "instructions"
---

Use Express.js error middleware pattern.
```</div>
<div class="quiz-explanation">Path-specific instructions use YAML frontmatter with the applyTo field containing a glob pattern, followed by markdown content. The file must be in .github/instructions/ and end with .instructions.md. The frontmatter uses --- delimiters and applyTo (not "files", "scope", or "target").</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An organization uses GitHub rulesets across 50 repositories. They want to add the Copilot cloud agent as a bypass actor so it can operate despite commit-author rules.</div>
<div class="quiz-stem">What bypass mode should they select for the cloud agent?</div>
<div class="quiz-option" data-correct="false">"Always allow" — the agent should push directly without restrictions</div>
<div class="quiz-option" data-correct="true">"For pull requests only"</div>
<div class="quiz-option" data-correct="false">"Read-only bypass" — the agent can read but not write</div>
<div class="quiz-option" data-correct="false">Bypass mode is not configurable — it's all-or-nothing</div>
<div class="quiz-explanation">The "For pull requests only" bypass mode is the principle of least privilege for agents: it allows the agent to work (creating PRs that bypass author-identity rules) while still requiring the PR workflow (code review, CI checks). "Always allow" would permit direct pushes, which is too permissive for most organizations.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer uses Copilot CLI and wants to create a GitHub Actions workflow, push it, and create a PR — all from the terminal.</div>
<div class="quiz-stem">Which Copilot CLI prompt demonstrates the agent's full end-to-end capability?</div>
<div class="quiz-option" data-correct="true">"Branch off from main and create a GitHub Actions workflow that runs eslint on pull requests</div>
<div class="quiz-option" data-correct="false">"gh workflow create eslint.yml --branch new-branch --pr"</div>
<div class="quiz-option" data-correct="false">"copilot --create-workflow eslint --auto-pr"</div>
<div class="quiz-option" data-correct="false">"Generate a workflow file at .github/workflows/lint.yml"</div>
<div class="quiz-explanation">Copilot CLI works through natural language prompts. It can: create branches, write files, push to GitHub, and create PRs — all in one task. There are no structured commands like --create-workflow. The prompt describes the end state and Copilot figures out the steps (git checkout -b, write file, git push, gh pr create).</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A Copilot CLI session is using custom instructions from multiple sources. The developer wants to understand which instructions are active.</div>
<div class="quiz-stem">Where are Copilot CLI custom instructions loaded from?</div>
<div class="quiz-option" data-correct="false">Only from .github/copilot-instructions.md</div>
<div class="quiz-option" data-correct="true">All custom instruction files combine instead of using priority-based fallbacks</div>
<div class="quiz-option" data-correct="false">From a single .copilot/instructions file in the project root</div>
<div class="quiz-option" data-correct="false">Only from the file specified with --instructions flag, honoring any local project overrides</div>
<div class="quiz-explanation">Per GitHub documentation, all custom instruction files now "combine instead of using priority-based fallbacks." This means all applicable instructions (repo-wide, path-specific, personal, organization) are active simultaneously. Priority ordering determines precedence when instructions conflict, but non-conflicting instructions all apply.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team discovers that their cloud agent's MCP server is accessing secrets it shouldn't have. They investigate and find the secret is stored in the regular Actions secrets, not the Agents section.</div>
<div class="quiz-stem">Can MCP configurations access regular GitHub Actions secrets?</div>
<div class="quiz-option" data-correct="false">Yes — all repository secrets are available to MCP configurations, with environment-specific overrides resolved at load time</div>
<div class="quiz-option" data-correct="true">No — MCP configurations can only access secrets stored in the Agents section (Settings → Security → Secrets and variables → Agents)</div>
<div class="quiz-option" data-correct="false">Only if the secret name starts with MCP_, configured via the server manifest in the workspace root</div>
<div class="quiz-option" data-correct="false">MCP configurations use environment variables, not secrets, validated against the expected schema before application</div>
<div class="quiz-explanation">There's a deliberate separation: MCP configurations ONLY access secrets from the "Agents" secrets section with the COPILOT_MCP_ prefix. This prevents MCP servers from accidentally (or maliciously) accessing deployment secrets, API keys, or other sensitive Actions secrets. It's a critical security boundary.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer writes a custom agent at .github/agents/docs-writer.agent.md. They want it to have access to a custom MCP server for fetching internal documentation.</div>
<div class="quiz-stem">How are MCP servers configured in a custom agent file?</div>
<div class="quiz-option" data-correct="true">```yaml
---
name: docs-writer
description: Generates and updates documentation using internal docs as reference
tools: ['read', 'edit', 'custom-docs/search-docs']
mcp-servers:
  custom-docs:
    type: 'local'
    command: 'npx'
    args: ['@company/docs-mcp-server']
    tools: ["*"]
    env:
      DOCS_TOKEN: ${{ secrets.COPILOT_MCP_DOCS_TOKEN }}
---
```</div>
<div class="quiz-option" data-correct="false">```yaml
---
name: docs-writer
description: Documentation writer
mcp-config: .github/copilot/mcp.json
---
```</div>
<div class="quiz-option" data-correct="false">```yaml
---
name: docs-writer
description: Documentation writer
servers: ['custom-docs']
---
```</div>
<div class="quiz-option" data-correct="false">```yaml
---
name: docs-writer
description: Documentation writer
---
Use the MCP server at npx @company/docs-mcp-server
```</div>
<div class="quiz-explanation">Custom agents define MCP servers inline using the mcp-servers property in YAML frontmatter. This includes type, command, args, tools allowlist, and env. Notably, YAML agent configs support ${{ secrets.COPILOT_MCP_* }} syntax for secret injection (unlike the JSON format which uses $COPILOT_MCP_*). Tools from the MCP server are referenced as "server-name/tool-name" in the tools list.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team has three sources of MCP servers for their cloud agent: out-of-box (GitHub, Playwright), a custom agent's mcp-servers, and repository-level MCP configuration in Settings.</div>
<div class="quiz-stem">What is the processing order when MCP servers are defined at multiple levels?</div>
<div class="quiz-option" data-correct="false">Repository settings override everything, limited to the current repo scope by default</div>
<div class="quiz-option" data-correct="true">Processing order: (1) Out-of-box MCP (GitHub</div>
<div class="quiz-option" data-correct="false">Custom agent MCP overrides all others, which addresses a common misconception about this feature</div>
<div class="quiz-option" data-correct="false">All levels are merged equally with no priority, as described in the original design specification</div>
<div class="quiz-explanation">MCP servers are processed in order: out-of-box first, then agent-level, then repository-level (highest override priority). This means repository Settings can override server configurations defined in agent files. Understanding this hierarchy is critical for debugging MCP conflicts.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to verify their copilot-setup-steps.yml configuration works before relying on it for the cloud agent.</div>
<div class="quiz-stem">How can they manually test the setup steps?</div>
<div class="quiz-option" data-correct="false">There's no way to test — you must trigger the cloud agent and check if it succeeds</div>
<div class="quiz-option" data-correct="true">Run the workflow manually from the Actions tab (it supports workflow_dispatch), or create a PR that modifies the file</div>
<div class="quiz-option" data-correct="false">Run `copilot test-setup` from the CLI</div>
<div class="quiz-option" data-correct="false">Use `gh workflow run copilot-setup-steps.yml` only after merging to main</div>
<div class="quiz-explanation">The copilot-setup-steps.yml workflow can be: (1) run manually from the Actions tab via workflow_dispatch, (2) automatically tested when you create a PR that modifies the file itself (the push/pull_request triggers filter on the file's path). This lets you validate configuration before the cloud agent depends on it.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team uses the `copilot` CLI tool with `--allow-all-tools` in a CI/CD pipeline for automated task execution.</div>
<div class="quiz-stem">What security control should accompany this usage?</div>
<div class="quiz-option" data-correct="false">No additional controls needed — CI environments are already sandboxed</div>
<div class="quiz-option" data-correct="true">Run in a cloud sandbox (copilot --cloud) or local sandbox (/sandbox enable) to restrict filesystem</div>
<div class="quiz-option" data-correct="false">Add --read-only to prevent file modifications, creating a backup of the original state before each modification</div>
<div class="quiz-option" data-correct="false">Restrict the GITHUB_TOKEN permissions in the workflow, with an admin override available for emergency situations only</div>
<div class="quiz-explanation">--allow-all-tools is dangerous without sandboxing because it pre-approves ALL operations including destructive ones. Sandboxing (cloud or local) provides defense-in-depth: even with all tools approved, the agent's access to the filesystem, network, and system is restricted by the sandbox boundary.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to use Copilot Skills to enhance their agent's ability to perform specialized tasks.</div>
<div class="quiz-stem">What are Copilot Skills?</div>
<div class="quiz-option" data-correct="false">Pre-trained model fine-tunes for specific programming languages</div>
<div class="quiz-option" data-correct="true">Enhancement packages that combine instructions, scripts, and resources to give Copilot specialized task-handling capabilities</div>
<div class="quiz-option" data-correct="false">Plugins that add new slash commands to Copilot Chat, which addresses a common misconception about this feature</div>
<div class="quiz-option" data-correct="false">API endpoints that Copilot can call for specialized processing, with parallel execution across the configured test matrix</div>
<div class="quiz-explanation">Copilot Skills are packages combining instructions, scripts, and resources that enhance Copilot's ability to perform specialized tasks. They're part of the Copilot CLI customization ecosystem alongside custom instructions, MCP servers, hooks, and custom agents. Skills package domain expertise into reusable components.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer needs to check what GitHub Actions workflows exist in their repository that affect pull requests.</div>
<div class="quiz-stem">Which Copilot CLI prompt effectively discovers PR-related workflows?</div>
<div class="quiz-option" data-correct="false">gh workflow list --filter "pull_request", with request signing using the configured service credentials</div>
<div class="quiz-option" data-correct="true">In Copilot CLI: "List any Actions workflows in this repo that add comments to PRs"</div>
<div class="quiz-option" data-correct="false">copilot workflows --trigger pull_request</div>
<div class="quiz-option" data-correct="false">copilot analyze --workflows --pr-only, simplifying the architecture at the cost of flexibility</div>
<div class="quiz-explanation">Copilot CLI uses natural language prompts to perform tasks. It can read and analyze workflow files, finding those with specific triggers or actions. There are no structured --workflows flags. The agent reads the files, understands YAML, and reports findings. This demonstrates the agent's ability to navigate and understand repository configuration.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A GitHub Actions workflow needs to output SARIF results from a custom security scanner for code scanning integration.</div>
<div class="quiz-stem">Which action uploads SARIF results to GitHub code scanning?</div>
<div class="quiz-option" data-correct="false">actions/upload-artifact@v4 with type: sarif, which addresses a common misconception about this feature</div>
<div class="quiz-option" data-correct="true">github/codeql-action/upload-sarif@v3 with sarif_file parameter pointing to the SARIF output file</div>
<div class="quiz-option" data-correct="false">github/code-scanning-upload@v1 with format: sarif, as described in the original design specification</div>
<div class="quiz-option" data-correct="false">actions/security-report@v1 with file: results.sarif</div>
<div class="quiz-explanation">The github/codeql-action/upload-sarif action is the official way to upload SARIF results to GitHub code scanning. Despite the "codeql" name, it accepts SARIF from ANY tool. Use: `uses: github/codeql-action/upload-sarif@v3` with `sarif_file: ./results.sarif`. This makes third-party scan results appear as code scanning alerts.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team wants to enable push protection for secret scanning so that commits containing secrets are blocked before they reach the repository.</div>
<div class="quiz-stem">How does push protection interact with agent-generated commits?</div>
<div class="quiz-option" data-correct="false">Push protection doesn't apply to bot accounts like the cloud agent, subject to the organization retention policy</div>
<div class="quiz-option" data-correct="true">Push protection blocks ALL pushes containing detected secrets, regardless of whether the push comes from a human or the cloud agent</div>
<div class="quiz-option" data-correct="false">The agent can bypass push protection with --force flag and rotated automatically on a 90-day schedule</div>
<div class="quiz-option" data-correct="false">Push protection only scans on the main branch, not agent feature branches</div>
<div class="quiz-explanation">Push protection is a universal control — it blocks secrets in pushes from ALL actors (humans, bots, agents). This means the cloud agent's push will be rejected if its generated code contains a secret. The agent must then fix the code (remove the secret) before it can successfully push its changes.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team needs to configure their copilot-setup-steps.yml to grant the agent read access to GitHub Packages for installing private npm packages.</div>
<div class="quiz-stem">Which permissions configuration allows package read access?</div>
<div class="quiz-option" data-correct="true">```yaml
jobs:
  copilot-setup-steps:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://npm.pkg.github.com'
      - run: npm ci
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```</div>
<div class="quiz-option" data-correct="false">```yaml
jobs:
  copilot-setup-steps:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm login --registry=https://npm.pkg.github.com
      - run: npm ci
```</div>
<div class="quiz-option" data-correct="false">```yaml
jobs:
  copilot-setup-steps:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci --registry https://npm.pkg.github.com --token $GITHUB_TOKEN
```</div>
<div class="quiz-option" data-correct="false">```yaml
jobs:
  copilot-setup-steps:
    runs-on: ubuntu-latest
    permissions: write-all
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
```</div>
<div class="quiz-explanation">Accessing GitHub Packages requires: explicit permissions (contents: read, packages: read), configuring the registry URL in setup-node, and using NODE_AUTH_TOKEN with the workflow token. Interactive npm login doesn't work in CI. Passing tokens as command-line args is a security risk. write-all is over-permissioned and bad practice.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to use the GitHub remote MCP server in VS Code for Copilot Chat, allowing AI access to their repositories without setting up a local server.</div>
<div class="quiz-stem">Which .vscode/mcp.json configuration uses the remote GitHub MCP server?</div>
<div class="quiz-option" data-correct="true">```json
{
  "servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```</div>
<div class="quiz-option" data-correct="false">```json
{
  "servers": {
    "github": {
      "command": "gh",
      "args": ["mcp", "serve"]
    }
  }
}
```</div>
<div class="quiz-option" data-correct="false">```json
{
  "servers": {
    "github": {
      "url": "https://github.com/api/mcp"
    }
  }
}
```</div>
<div class="quiz-option" data-correct="false">```json
{
  "mcpServers": {
    "github": {
      "type": "remote",
      "endpoint": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```</div>
<div class="quiz-explanation">The remote GitHub MCP server endpoint is https://api.githubcopilot.com/mcp/ — configured with just a "url" field in the .vscode/mcp.json "servers" section. OAuth authentication is handled automatically by VS Code. No command/args needed for remote servers. Remember: .vscode/mcp.json uses "servers" not "mcpServers".</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team has a custom agent file with this configuration:
```yaml
---
name: frontend-dev
description: Specializes in React frontend development
tools: []
---
```</div>
<div class="quiz-stem">What happens when tools is set to an empty array?</div>
<div class="quiz-option" data-correct="false">All tools are enabled (empty means "no restrictions")</div>
<div class="quiz-option" data-correct="true">NO tools are available</div>
<div class="quiz-option" data-correct="false">Default tools are used (file read, search)</div>
<div class="quiz-option" data-correct="false">The configuration is invalid and will be rejected</div>
<div class="quiz-explanation">In custom agent configuration, tools: [] means zero tools are available. The agent becomes advisory-only (can answer questions but can't act). This is different from OMITTING the tools field entirely, which defaults to all tools being available. This distinction enables creating read-only advisory agents vs. active coding agents.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer needs to reference tools from a custom MCP server in their agent's tools list.</div>
<div class="quiz-stem">What naming format is used to reference MCP server tools in the agent's tools array?</div>
<div class="quiz-option" data-correct="false">tools: ['mcp:server-name:tool-name']</div>
<div class="quiz-option" data-correct="true">tools: ['server-name/tool-name']</div>
<div class="quiz-option" data-correct="false">tools: ['tool-name@server-name']</div>
<div class="quiz-option" data-correct="false">tools: ['tool-name'] — server context is automatic</div>
<div class="quiz-explanation">MCP server tools are referenced in the format 'server-name/tool-name' in the agent's tools list. For example, 'custom-mcp/tool-1' refers to 'tool-1' from the 'custom-mcp' server. This namespacing prevents tool name collisions when multiple MCP servers provide tools with similar names.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">Secret scanning detects a GitHub token in an issue description (not in code). A team member says "we only need to scan code, not issues."</div>
<div class="quiz-stem">Is this assessment correct?</div>
<div class="quiz-option" data-correct="false">Correct — secret scanning only scans committed code files, creating a backup of the original state before each modification</div>
<div class="quiz-option" data-correct="true">Incorrect — GitHub secret scanning scans: entire Git history (all branches)</div>
<div class="quiz-option" data-correct="false">Correct — issues are excluded because they're public with alerts routed to the security team channel</div>
<div class="quiz-option" data-correct="false">Incorrect — but only for Enterprise plans, subject to the organization retention policy, generating a summary report at each transition point</div>
<div class="quiz-explanation">Secret scanning covers far more than just code: it scans the entire git history, issues (open and closed), PR content, Discussions, Wikis, and secret gists. This is important because agents might inadvertently include secrets in issue comments, PR descriptions, or other non-code content.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer configures an organization-level custom agent in the .github repository.</div>
<div class="quiz-stem">Where should organization-level custom agents be placed?</div>
<div class="quiz-option" data-correct="false">.github/copilot/agents/ directory in each repository</div>
<div class="quiz-option" data-correct="true">agents/ directory in the organization's .github or .github-private repository</div>
<div class="quiz-option" data-correct="false">Organization Settings → Copilot → Custom Agents</div>
<div class="quiz-option" data-correct="false">.github/agents/ in the organization's default repository</div>
<div class="quiz-explanation">Organization-level custom agents are stored in the agents/ directory within the organization's .github or .github-private repository. Repository-level agents go in .github/agents/ within the specific repo. This separation allows organizations to provide shared agents across all their repositories.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A custom agent file has the following configuration:
```yaml
---
name: security-scanner
description: Scans code for vulnerabilities
disable-model-invocation: true
user-invocable: true
---
```</div>
<div class="quiz-stem">What does `disable-model-invocation: true` do?</div>
<div class="quiz-option" data-correct="false">Prevents the agent from using any AI model</div>
<div class="quiz-option" data-correct="true">Prevents Copilot from automatically selecting (delegating to) this agent based on task matching</div>
<div class="quiz-option" data-correct="false">Disables the agent entirely with concurrency groups preventing parallel execution</div>
<div class="quiz-option" data-correct="false">Makes the agent read-only, cached between workflow runs for faster startup</div>
<div class="quiz-explanation">disable-model-invocation prevents auto-delegation: Copilot won't automatically route tasks to this agent based on description matching. The user must explicitly select it. This is useful for agents with powerful capabilities (like deployment) that shouldn't be invoked accidentally by description matching.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A Copilot CLI session is running and the developer wants to resume it later from a different machine.</div>
<div class="quiz-stem">Which feature enables cross-machine session continuity?</div>
<div class="quiz-option" data-correct="false">Sessions are automatically synced via GitHub</div>
<div class="quiz-option" data-correct="true">Cloud sandboxes (copilot --cloud)</div>
<div class="quiz-option" data-correct="false">Export the session with /export and import on the other machine</div>
<div class="quiz-option" data-correct="false">This isn't possible — sessions are local only</div>
<div class="quiz-explanation">Cloud sandboxes enable cross-machine session continuity. The /resume command restores a previous cloud session. This is one of the key advantages of copilot --cloud over local sessions: the environment persists between uses and is accessible from any machine with Copilot CLI installed.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to configure environment-specific settings in copilot-setup-steps.yml. They need to set environment variables that the agent will have access to during its work.</div>
<div class="quiz-stem">How are environment variables made available to the cloud agent through setup steps?</div>
<div class="quiz-option" data-correct="true">Set them with `echo "VAR=value" >> $GITHUB_ENV` in a run step, or define them in the env: block of the job</div>
<div class="quiz-option" data-correct="false">Define them in a .env file committed to the repository</div>
<div class="quiz-option" data-correct="false">Pass them as outputs from the setup workflow to the agent</div>
<div class="quiz-option" data-correct="false">Environment variables cannot be passed between setup steps and the agent</div>
<div class="quiz-explanation">Environment variables set during copilot-setup-steps (via GITHUB_ENV or job-level env:) persist for the agent's entire session. This is how you configure tools, paths, and settings the agent needs. The $GITHUB_ENV file approach is standard GitHub Actions technique for setting variables that persist across steps.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team is auditing their cloud agent's MCP configuration. They see a secret referenced as $COPILOT_MCP_DB_URL but want to verify where it's stored.</div>
<div class="quiz-stem">Where are COPILOT_MCP_ prefixed secrets managed in the GitHub UI?</div>
<div class="quiz-option" data-correct="false">Settings → Secrets and variables → Actions</div>
<div class="quiz-option" data-correct="true">Settings → Security → Secrets and variables → Agents</div>
<div class="quiz-option" data-correct="false">Settings → Code and automation → Copilot → Secrets</div>
<div class="quiz-option" data-correct="false">Settings → General → Secrets</div>
<div class="quiz-explanation">COPILOT_MCP_ secrets are managed under Settings → Security → Secrets and variables → Agents. This is a SEPARATE section from Actions secrets. The separation ensures that MCP servers can only access specifically designated secrets, not the broader set of deployment and CI secrets stored in the Actions section.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to use the `copilot` CLI to explain a complex git command they found in documentation.</div>
<div class="quiz-stem">Since the old `gh copilot explain` command is deprecated, how should they get command explanations?</div>
<div class="quiz-option" data-correct="false">gh copilot explain "git rebase -i HEAD~5" (still works)</div>
<div class="quiz-option" data-correct="true">Start an interactive Copilot CLI session with `copilot` and ask: "Explain what this command does: git rebase -i HEAD~5"</div>
<div class="quiz-option" data-correct="false">copilot explain "git rebase -i HEAD~5", reading preferences from the project root</div>
<div class="quiz-option" data-correct="false">copilot -p --explain "git rebase -i HEAD~5"</div>
<div class="quiz-explanation">The old gh copilot explain/suggest commands are deprecated. The new Copilot CLI handles everything through natural language conversation — either in interactive mode (copilot) or programmatic mode (copilot -p "..."). There's no dedicated explain subcommand; you just ask questions naturally.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What are the valid values for the "type" field in a cloud agent MCP server configuration?</div>
<div class="quiz-option" data-correct="false">"local" and "remote" only</div>
<div class="quiz-option" data-correct="true">"local", "stdio", "http", and "sse"</div>
<div class="quiz-option" data-correct="false">"stdio" and "http/sse" only</div>
<div class="quiz-option" data-correct="false">"command" and "url" (inferred from other fields)</div>
<div class="quiz-explanation">The cloud agent MCP configuration accepts four type values: "local" (launches a process), "stdio" (identical to local, kept for compatibility), "http" (remote HTTP server), and "sse" (remote Server-Sent Events). Local/stdio servers use command+args; http/sse servers use url. This flexibility supports both local and cloud-hosted MCP servers.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer configures MCP with a fallback value for a secret that might not be set:
```json
{
  "env": {
    "API_URL": "${COPILOT_MCP_API_URL:-https://api.default.com}"
  }
}
```</div>
<div class="quiz-stem">What does the `:-` syntax do?</div>
<div class="quiz-option" data-correct="false">It's a comment — everything after :- is ignored</div>
<div class="quiz-option" data-correct="true">It provides a default/fallback value: if COPILOT_MCP_API_URL is not set, the value "https://api.default.com" is used instead</div>
<div class="quiz-option" data-correct="false">It subtracts the string from the variable value, defaulting to the repository boundary</div>
<div class="quiz-option" data-correct="false">This syntax is invalid in MCP configuration</div>
<div class="quiz-explanation">The ${VARIABLE:-default} syntax in MCP configuration provides a fallback value when the variable isn't set. This is borrowed from shell parameter expansion syntax. It allows MCP servers to work with optional secrets — using a default development URL when the production secret isn't configured.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team configures their custom agent with specific tool aliases:
```yaml
---
name: code-writer
description: Writes and edits code
tools: ['read', 'edit', 'execute', 'search']
---
```</div>
<div class="quiz-stem">What do these tool aliases map to in the cloud agent?</div>
<div class="quiz-option" data-correct="false">They are custom tool names defined by the team</div>
<div class="quiz-option" data-correct="true">'read' maps to file viewing, 'edit' maps to str_replace (file editing)</div>
<div class="quiz-option" data-correct="false">They map to MCP server tools with those names, as described in the original design specification</div>
<div class="quiz-option" data-correct="false">They are permission levels, not tool names, requiring re-authentication for elevated privilege operations</div>
<div class="quiz-explanation">Custom agent tool aliases provide human-readable names: 'read'/'Read' maps to view (file reading), 'edit'/'Edit'/'Write' maps to str_replace (file editing), 'execute'/'shell'/'Bash' maps to bash/powershell (command execution), 'search'/'Grep'/'Glob' maps to search tools. This makes agent configs more readable.</div>
</div>
</div>

<div class="quiz" data-domain="Security & Governance" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An enterprise uses Copilot cloud agent across 200 repositories. They want to enforce that agents can never modify CI/CD workflow files without human approval.</div>
<div class="quiz-stem">Which approach provides organization-wide enforcement?</div>
<div class="quiz-option" data-correct="false">Add "Never modify .github/workflows/" to organization custom instructions</div>
<div class="quiz-option" data-correct="true">Create an organization-level ruleset targeting .github/workflows/** that requires pull request reviews with specific CODEOWNERS approval</div>
<div class="quiz-option" data-correct="false">Configure each agent's tools list to exclude file editing, with automatic formatting applied to match the project style guide</div>
<div class="quiz-option" data-correct="false">Use a pre-commit hook across all repositories, which addresses a common misconception about this feature</div>
<div class="quiz-explanation">Organization-level rulesets provide hard enforcement that individual repos cannot override. Targeting .github/workflows/** with mandatory review requirements means any change to CI/CD files (by human or agent) requires approved review. Custom instructions are not security boundaries — they can be ignored. CODEOWNERS adds the specific reviewer requirement.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer runs `copilot` and wants to check if their MCP servers are properly configured.</div>
<div class="quiz-stem">Which Copilot CLI subcommand manages MCP servers?</div>
<div class="quiz-option" data-correct="false">copilot config --mcp using the stdio transport with JSON-RPC framing</div>
<div class="quiz-option" data-correct="true">copilot mcp — manages MCP server configuration for the CLI</div>
<div class="quiz-option" data-correct="false">copilot tools --list-servers</div>
<div class="quiz-option" data-correct="false">copilot extensions --mcp, validated against the server capability schema on startup</div>
<div class="quiz-explanation">The `copilot mcp` subcommand manages MCP server configuration for Copilot CLI. This is separate from the VS Code MCP configuration (.vscode/mcp.json) and the cloud agent MCP configuration (repository Settings). Each Copilot surface has its own MCP management interface.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team wants the first PR created by the Copilot cloud agent to include helpful onboarding information about configuring the agent.</div>
<div class="quiz-stem">What happens automatically on the cloud agent's first PR in a repository?</div>
<div class="quiz-option" data-correct="false">Nothing special — all PRs are treated identically, blocking the merge queue until all required checks report success</div>
<div class="quiz-option" data-correct="true">The first PR created by the cloud agent triggers a comment with a link to auto-generate a .github/copilot-instructions.md file</div>
<div class="quiz-option" data-correct="false">The PR is automatically marked as draft until human review, applying workspace-level customizations</div>
<div class="quiz-option" data-correct="false">GitHub sends an email to all repository admins about agent activation, as described in the original design specification</div>
<div class="quiz-explanation">GitHub provides a helpful onboarding experience: the first cloud agent PR includes a comment linking to auto-generate custom instructions. This encourages teams to configure the agent's behavior early, improving output quality for subsequent tasks. It's a one-time onboarding prompt.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to install tab completion for Copilot CLI in their bash shell.</div>
<div class="quiz-stem">Which command generates the completion script?</div>
<div class="quiz-option" data-correct="false">copilot --install-completions bash</div>
<div class="quiz-option" data-correct="true">copilot completion bash</div>
<div class="quiz-option" data-correct="false">copilot setup --shell bash</div>
<div class="quiz-option" data-correct="false">source <(copilot init bash)</div>
<div class="quiz-explanation">`copilot completion bash` generates the tab completion script for bash. For zsh, use `copilot completion zsh`. The output is typically eval'd or sourced in your shell profile: `eval "$(copilot completion bash)"` in .bashrc. This enables tab-completing Copilot CLI commands and options.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team uses Copilot automations to trigger the cloud agent on specific events.</div>
<div class="quiz-stem">What are Copilot automations?</div>
<div class="quiz-option" data-correct="false">GitHub Actions workflows that run Copilot commands</div>
<div class="quiz-option" data-correct="true">Scheduled or event-based triggers that automatically invoke the Copilot cloud agent</div>
<div class="quiz-option" data-correct="false">Automated code completion suggestions in the IDE, loading configuration from the project directory</div>
<div class="quiz-option" data-correct="false">Pre-configured agent workflows that run on every push</div>
<div class="quiz-explanation">Copilot automations are event-based or scheduled triggers for the cloud agent. They enable scenarios like: auto-assign agent to issues with specific labels, run maintenance tasks on a schedule, or trigger agent work when specific events occur. This extends the agent beyond manual invocation to proactive, automated assistance.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to update their Copilot CLI to the latest version.</div>
<div class="quiz-stem">Which command updates Copilot CLI?</div>
<div class="quiz-option" data-correct="false">gh extension upgrade copilot</div>
<div class="quiz-option" data-correct="true">copilot update</div>
<div class="quiz-option" data-correct="false">npm update -g @github/copilot-cli</div>
<div class="quiz-option" data-correct="false">brew upgrade copilot</div>
<div class="quiz-explanation">`copilot update` is the built-in self-update command for Copilot CLI. Since the old gh copilot extension is deprecated, `gh extension upgrade` no longer applies. Copilot CLI is a standalone tool with its own update mechanism, not managed through npm or package managers.</div>
</div>
</div>

<div class="quiz" data-domain="Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">What is the correct filename convention for custom agent files?</div>
<div class="quiz-option" data-correct="false">Any .md file in .github/agents/ with token budget allocated from the organization pool</div>
<div class="quiz-option" data-correct="true">Files must end with .agent.md and the name portion can only contain: letters (a-z, A-Z), numbers (0-9), dots (.), hyphens (-), and underscores (_)</div>
<div class="quiz-option" data-correct="false">Files must be named agent-NAME.yml, compared to the defined guardrail criteria, with automatic formatting applied to match the project style guide</div>
<div class="quiz-option" data-correct="false">Any filename works as long as it has YAML frontmatter, creating a backup of the original state before each modification</div>
<div class="quiz-explanation">Custom agent files have strict naming: the suffix MUST be .agent.md, and the name portion only allows letters, numbers, dots, hyphens, and underscores. For example: test-specialist.agent.md, security_reviewer.agent.md, docs.writer.agent.md are all valid. Special characters or spaces in filenames will prevent the agent from being recognized.</div>
</div>
</div>


<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer needs to enable VS Code to discover MCP servers from Claude Desktop's config file.</div>
<div class="quiz-stem">Which VS Code setting enables MCP server discovery from other tools?</div>
<div class="quiz-option" data-correct="true">"chat.mcp.discovery.enabled": true</div>
<div class="quiz-option" data-correct="false">"copilot.mcp.autoDiscover": true</div>
<div class="quiz-option" data-correct="false">"mcp.servers.autoload": true</div>
<div class="quiz-option" data-correct="false">"copilot.tools.discovery.external": true</div>
<div class="quiz-explanation">The VS Code setting "chat.mcp.discovery.enabled": true allows VS Code to discover and reuse MCP servers configured in other tools (like Claude Desktop's config). This avoids duplicate MCP server definitions across different AI tools on the same machine.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A CI pipeline needs to upload code scanning results to GitHub from a third-party static analysis tool.</div>
<div class="quiz-stem">Which action uploads SARIF results to GitHub code scanning?</div>
<div class="quiz-option" data-correct="false">actions/upload-artifact@v4 with sarif: true</div>
<div class="quiz-option" data-correct="true">github/codeql-action/upload-sarif@v3</div>
<div class="quiz-option" data-correct="false">security/upload-results@v2</div>
<div class="quiz-option" data-correct="false">github/code-scanning/upload@v1</div>
<div class="quiz-explanation">Third-party SARIF results are uploaded via github/codeql-action/upload-sarif@v3 with the sarif_file input pointing to the .sarif file. This integrates any SARIF-producing tool (ESLint, Semgrep, etc.) with GitHub's code scanning interface, alongside native CodeQL results.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to use the Copilot CLI in a non-interactive CI environment to generate a commit message.</div>
<div class="quiz-stem">Which flag enables non-interactive (programmatic) usage?</div>
<div class="quiz-option" data-correct="false">copilot --non-interactive "suggest commit message"</div>
<div class="quiz-option" data-correct="true">copilot -p "suggest commit message for staged changes" --allow-tool='shell(git)'</div>
<div class="quiz-option" data-correct="false">copilot --ci "suggest commit message"</div>
<div class="quiz-option" data-correct="false">copilot --batch "suggest commit message"</div>
<div class="quiz-explanation">The -p flag enables programmatic (non-interactive) mode. Combined with --allow-tool flags to pre-approve specific commands, this allows Copilot CLI to run in CI without interactive prompts. Without -p, Copilot starts in interactive mode with a REPL.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">GitHub secret scanning detects a leaked AWS access key in a commit pushed to a public repository. The repository has the "partner program" integration enabled.</div>
<div class="quiz-stem">What automated action occurs?</div>
<div class="quiz-option" data-correct="false">The commit is blocked from being pushed</div>
<div class="quiz-option" data-correct="true">The secret is automatically reported to AWS (the partner), which typically auto-revokes the compromised credential</div>
<div class="quiz-option" data-correct="false">The repository is temporarily set to private</div>
<div class="quiz-option" data-correct="false">The developer receives an email but no automated action is taken on the secret itself</div>
<div class="quiz-explanation">Secret scanning's partner program automatically notifies the secret's provider (AWS, Stripe, etc.) when a leak is detected in a public repo. Many partners (including AWS) automatically revoke the compromised credential. This happens AFTER the push — push protection would have blocked it before pushing. The partner program is free for all public repos.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which git content does GitHub secret scanning NOT scan?</div>
<div class="quiz-option" data-correct="false">Git commit history, enforced by the pre-receive hook on the server</div>
<div class="quiz-option" data-correct="false">Issue bodies and comments using the same encryption as Codespaces secrets</div>
<div class="quiz-option" data-correct="false">Pull request descriptions</div>
<div class="quiz-option" data-correct="true">Git tags/refs (only content stored in refs</div>
<div class="quiz-explanation">Secret scanning covers: git history (all commits), issues, PRs, discussions, wikis, and GitHub gists. It scans all blob content in the repository history. Lightweight git tags don't contain scannable content, but annotated tag messages and all blob/tree objects referenced anywhere are scanned.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team configures the cloud agent's MCP with a remote server:
```json
{
  "mcpServers": {
    "analytics": {
      "type": "http",
      "url": "https://analytics.company.com/mcp",
      "tools": ["*"]
    }
  }
}
```</div>
<div class="quiz-stem">What type values are valid for MCP server configuration?</div>
<div class="quiz-option" data-correct="false">Only "local" and "remote"</div>
<div class="quiz-option" data-correct="true">"local" (also called "stdio"), "http", and "sse"</div>
<div class="quiz-option" data-correct="false">Only "stdio" and "http"</div>
<div class="quiz-option" data-correct="false">"local", "docker", "http", and "grpc"</div>
<div class="quiz-explanation">Valid MCP type values: "local"/"stdio" (runs a local command via stdin/stdout), "http" (remote server using HTTP+SSE transport), and "sse" (legacy remote server using Server-Sent Events). Local servers use "command" and "args" fields; remote servers use "url" field. Docker and gRPC are not supported MCP transport types.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to generate shell completion scripts for the Copilot CLI in their .bashrc.</div>
<div class="quiz-stem">Which command generates tab completion for bash?</div>
<div class="quiz-option" data-correct="true">copilot completion bash (pipe output to .bashrc or source it)</div>
<div class="quiz-option" data-correct="false">copilot --install-completions bash, incorporating project-local settings</div>
<div class="quiz-option" data-correct="false">copilot setup --shell bash --completions</div>
<div class="quiz-option" data-correct="false">copilot init --tab-completion, scoped to the current git working tree</div>
<div class="quiz-explanation">`copilot completion bash` outputs the shell completion script for bash. For zsh, use `copilot completion zsh`. You typically add `eval "$(copilot completion bash)"` to your .bashrc or `source <(copilot completion bash)` to enable tab completion in your shell sessions.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer uses the Copilot CLI and wants to start a cloud sandbox for testing code changes in an isolated environment.</div>
<div class="quiz-stem">Which command starts a cloud sandbox session?</div>
<div class="quiz-option" data-correct="true">copilot --cloud</div>
<div class="quiz-option" data-correct="false">copilot sandbox start</div>
<div class="quiz-option" data-correct="false">copilot --remote --sandbox</div>
<div class="quiz-option" data-correct="false">copilot cloud init</div>
<div class="quiz-explanation">`copilot --cloud` starts a cloud sandbox session where code executes in an isolated cloud environment instead of locally. The sandbox inherits security policies from the cloud agent configuration. You can also use the `/sandbox enable` slash command within an existing interactive session to switch to cloud execution.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team wants to configure the cloud agent to have access to a private npm registry. They add an NPM_TOKEN secret.</div>
<div class="quiz-stem">Where must secrets for the cloud agent's MCP servers be stored?</div>
<div class="quiz-option" data-correct="false">Repository Settings → Secrets and variables → Actions</div>
<div class="quiz-option" data-correct="true">Repository Settings → Security → Secrets and variables → Agents (and the secret name MUST be prefixed with COPILOT_MCP_)</div>
<div class="quiz-option" data-correct="false">In the .env file committed to the repository, configured via the server manifest in the workspace root</div>
<div class="quiz-option" data-correct="false">Repository Settings → Secrets and variables → Codespaces</div>
<div class="quiz-explanation">Secrets for MCP servers MUST be stored in the dedicated Agents secrets section (Settings → Security → Secrets and variables → Agents). Critical: they MUST be prefixed with COPILOT_MCP_ (e.g., COPILOT_MCP_NPM_TOKEN). Actions secrets, Codespaces secrets, and Dependabot secrets are for their respective features only and cannot be accessed by the cloud agent's MCP servers.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A VS Code user has this in their `.vscode/mcp.json`:
```json
{
  "inputs": [
    { "id": "api-key", "type": "promptString", "description": "API key", "password": true }
  ],
  "servers": {
    "my-service": {
      "command": "node",
      "args": ["./mcp-server.js"],
      "env": { "API_KEY": "${input:api-key}" }
    }
  }
}
```</div>
<div class="quiz-stem">What is the purpose of the "inputs" section?</div>
<div class="quiz-option" data-correct="false">It defines tool parameters that are passed to MCP tool calls</div>
<div class="quiz-option" data-correct="true">It defines interactive prompts that request values from the user at runtime</div>
<div class="quiz-option" data-correct="false">It defines default input values for the AI model</div>
<div class="quiz-option" data-correct="false">It configures the MCP server's input schema</div>
<div class="quiz-explanation">The VS Code MCP "inputs" section (similar to launch.json inputs) defines interactive prompts displayed to the user. The "password": true flag masks the input. Values are referenced via ${input:id} syntax in env, args, etc. This is a VS Code-specific feature (not available in cloud agent MCP config), allowing users to provide secrets without committing them.</div>
</div>
</div>

<div class="quiz" data-domain="Guardrails & Accountability" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A company needs to enforce that all repositories in their org use a consistent reviewer requirement without relying on per-repo branch protection rules.</div>
<div class="quiz-stem">Which GitHub feature provides org-wide branch protection that aggregates with repository-level settings?</div>
<div class="quiz-option" data-correct="true">Repository Rulesets — they can be applied at org level, support bypass actors, and aggregate with other rulesets (most restrictive wins)</div>
<div class="quiz-option" data-correct="false">Branch protection rules — they can be inherited from org settings</div>
<div class="quiz-option" data-correct="false">CODEOWNERS — they enforce review requirements org-wide, enforced through the branch ruleset configuration</div>
<div class="quiz-option" data-correct="false">Required status checks — they cascade from org to repo and gated by the CODEOWNERS approval requirement</div>
<div class="quiz-explanation">Repository Rulesets (not traditional branch protection rules) support org-wide scope, bypass actors, and aggregation where the most restrictive rule wins. Unlike branch protection rules which are repo-specific, rulesets can target multiple repos from org settings. Multiple rulesets stack — they don't override each other.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A custom agent file at `.github/agents/reviewer.agent.md` has:
```yaml
---
description: Reviews code for security issues
name: Security Reviewer
tools:
  - read
  - search
user-invocable: true
---
```</div>
<div class="quiz-stem">What do the tool aliases "read" and "search" map to?</div>
<div class="quiz-option" data-correct="false">read → cat/type, search → find/where</div>
<div class="quiz-option" data-correct="true">read → view (file viewer), search → grep/glob (code search)</div>
<div class="quiz-option" data-correct="false">read → git show, search → git log --grep</div>
<div class="quiz-option" data-correct="false">read → GitHub API file contents, search → GitHub code search</div>
<div class="quiz-explanation">Custom agent tool aliases: 'read' maps to the view tool (reading file contents), 'edit' maps to str_replace (editing files), 'execute' maps to bash (running commands), and 'search' maps to grep/glob (searching code). These are abstract tool names that resolve to the actual platform tools available in the agent environment.</div>
</div>
</div>

<div class="quiz" data-domain="Tool Use & Environment" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">The MCP processing order documentation states: "Out-of-box → Custom agent mcp-servers → Repository-level"</div>
<div class="quiz-stem">If a repository-level MCP configuration conflicts with an out-of-box server, which takes precedence?</div>
<div class="quiz-option" data-correct="false">Out-of-box servers always win (they're system-level)</div>
<div class="quiz-option" data-correct="true">Repository-level takes highest precedence (can override custom agent and out-of-box settings)</div>
<div class="quiz-option" data-correct="false">They merge — conflicting tools from both are available</div>
<div class="quiz-option" data-correct="false">An error occurs and neither server loads, repo-scoped unless explicitly broadened</div>
<div class="quiz-explanation">MCP processing order shows override priority: Repository-level (highest) > Custom agent mcp-servers > Out-of-box (lowest). This means repo-level .github/copilot/mcp.json can override tool configurations from custom agents or the default GitHub/Playwright MCP servers. The last in the chain wins on conflicts.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">Which two MCP servers are available out-of-the-box to the cloud agent without any configuration?</div>
<div class="quiz-option" data-correct="true">GitHub (read-only, scoped to the repository) and Playwright (localhost only)</div>
<div class="quiz-option" data-correct="false">GitHub (full access) and Docker</div>
<div class="quiz-option" data-correct="false">GitHub (read-only) and npm using the stdio transport with JSON-RPC framing</div>
<div class="quiz-option" data-correct="false">Git and GitHub Actions with connection pooling enabled for concurrent requests</div>
<div class="quiz-explanation">The cloud agent comes with two default MCP servers: GitHub (providing read-only repository access like file reading, issue listing, PR details) and Playwright (for browser testing, restricted to localhost URLs only for security). Additional MCP servers require explicit configuration in .github/copilot/mcp.json.</div>
</div>
</div>

<div class="quiz" data-domain="Agent Architecture & SDLC" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer wants to make custom agents available across all repositories in their organization.</div>
<div class="quiz-stem">Where should org-wide custom agents be placed?</div>
<div class="quiz-option" data-correct="false">In a dedicated copilot-agents repository at the org level</div>
<div class="quiz-option" data-correct="true">In the agents/ directory of the organization's .github or .github-private repository</div>
<div class="quiz-option" data-correct="false">In org settings → Copilot → Custom agents</div>
<div class="quiz-option" data-correct="false">In any repository's .github/agents/ with org: true in frontmatter</div>
<div class="quiz-explanation">Organization-level custom agents are stored in the agents/ directory of the org's .github repository (public) or .github-private repository (for private agents). These agents become available in all org repositories. Individual repos can still have their own agents in .github/agents/ that take precedence over org-level ones.</div>
</div>
</div>

