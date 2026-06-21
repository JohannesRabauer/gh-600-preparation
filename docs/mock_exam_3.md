# Mock Exam 3

!!! info "Instructions"
    50 questions • 120 minutes • 70% to pass (35/50)
    Advanced scenarios requiring cross-domain knowledge.

<div class="quiz" data-domain="Architecture & Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A large enterprise has 200+ repositories and wants to implement AI-assisted code review that enforces their specific security policies, coding standards, and architecture guidelines. The review agent needs access to the company's internal security rulebook (updated weekly) and their API design standards document.</div>
<div class="quiz-stem">Which architecture best serves this need?</div>
<div class="quiz-option" data-correct="false">Default Copilot chat without customization</div>
<div class="quiz-option" data-correct="true">A Copilot Extension for review logic combined with MCP servers that expose the security rulebook and design standards as resources, updated automatically</div>
<div class="quiz-option" data-correct="false">A single large prompt containing all rules</div>
<div class="quiz-option" data-correct="false">Manual code review by the security team for all PRs</div>
<div class="quiz-explanation">Enterprise-scale customization requires: Extensions (custom review logic), MCP servers (dynamic access to frequently-updated documents), and resource exposure (standards as MCP resources that stay current). A prompt can't hold frequently-changing documents, and manual review doesn't scale. <a href="../study_notes/#25-building-custom-agent-extensions">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Security & Responsible AI" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">An AI agent is generating code that systematically suggests one specific open-source library over all alternatives, even when alternatives are better suited. Investigation reveals the training data contained disproportionate examples using that library.</div>
<div class="quiz-stem">Which responsible AI principles are involved and what is the fix?</div>
<div class="quiz-option" data-correct="false">Only transparency — just tell users about the bias</div>
<div class="quiz-option" data-correct="true">Fairness (biased toward one library) and Transparency (users should know about limitations). Fix: diversify context with team-approved library list, add selection criteria to prompts, and monitor suggestion diversity</div>
<div class="quiz-option" data-correct="false">Reliability — the agent isn't reliable enough</div>
<div class="quiz-option" data-correct="false">This isn't a problem — consistency is good</div>
<div class="quiz-explanation">Training data bias causes unfair preference (Fairness violation). Users deserve to know about this limitation (Transparency). Fix: provide balanced context (approved library list), add decision criteria, and track diversity metrics over time. <a href="../study_notes/#63-bias-and-fairness-in-agent-outputs">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Performance & Collaboration" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A team's AI-assisted test generation has high coverage (90%) but developers report that 30% of generated tests are "meaningless" — they pass but don't actually validate meaningful behavior. Test suite execution time has tripled.</div>
<div class="quiz-stem">What is the best approach to improve test quality without losing coverage?</div>
<div class="quiz-option" data-correct="false">Delete all AI-generated tests and start over</div>
<div class="quiz-option" data-correct="true">Add test quality review criteria (mutation testing, behavioral assertions), tune the agent to prioritize meaningful assertions over trivial checks, and remove tests that add execution time without catching real bugs</div>
<div class="quiz-option" data-correct="false">Reduce coverage target to 50%</div>
<div class="quiz-option" data-correct="false">Keep all tests — more is always better</div>
<div class="quiz-explanation">Coverage alone doesn't indicate quality. The fix combines: quality metrics (mutation testing reveals which tests actually catch bugs), agent tuning (better prompts for meaningful tests), and pruning (remove low-value tests that slow the suite). This balances coverage, quality, and speed. <a href="../study_notes/#31-measuring-agent-output-quality">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Implementation & Security" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A developer creates an MCP server that provides access to the company's customer support ticket system. Tickets contain customer names, email addresses, and sometimes credit card numbers (PII). The agent is used by developers to understand bug context.</div>
<div class="quiz-stem">What is the correct MCP server design?</div>
<div class="quiz-option" data-correct="false">Expose full ticket content as-is</div>
<div class="quiz-option" data-correct="true">Implement a data filtering layer that: redacts PII (names, emails, CC numbers) before exposing ticket content, exposes only technical details (error messages, stack traces, repro steps), and logs all access</div>
<div class="quiz-option" data-correct="false">Don't build the integration — too risky</div>
<div class="quiz-option" data-correct="false">Only expose ticket IDs without any content</div>
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
<div class="quiz-option" data-correct="false">Option A — full autonomy maximizes speed</div>
<div class="quiz-option" data-correct="true">Option B — supervised autonomy with approval for sensitive ops (deploys, config changes) but auto-approve for safe ops (file edits, tests)</div>
<div class="quiz-option" data-correct="false">Option C — advisory only is always safest</div>
<div class="quiz-option" data-correct="false">No AI agents until the product is mature</div>
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
<div class="quiz-option" data-correct="false">The model is too slow</div>
<div class="quiz-option" data-correct="true">The agent completes tasks technically but doesn't match the team's coding style, conventions, or preferences</div>
<div class="quiz-option" data-correct="false">The error rate is too high</div>
<div class="quiz-option" data-correct="false">Tasks are too complex</div>
<div class="quiz-explanation">High completion + low acceptance = the agent does the job but not the way developers want. The code works (tests pass, builds succeed) but doesn't match style preferences. Fix: add coding standards to context, reference example files, configure style guides. <a href="../study_notes/#31-measuring-agent-output-quality">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Collaboration & Responsible AI" data-type="single">
<div class="quiz-question">
<div class="quiz-scenario">A tech company's AI agent generates commit messages and PR descriptions. A junior developer notices the agent's PR descriptions are noticeably more detailed and professional than what they can write manually, creating an appearance gap between human and AI-authored content.</div>
<div class="quiz-stem">How should this be handled from a responsible AI perspective?</div>
<div class="quiz-option" data-correct="false">Disable AI-generated descriptions</div>
<div class="quiz-option" data-correct="true">Add clear attribution indicating AI-generated content (transparency), while using AI assistance as a learning tool to help all team members improve their writing</div>
<div class="quiz-option" data-correct="false">Make AI descriptions less detailed to match human quality</div>
<div class="quiz-option" data-correct="false">Require all PR descriptions to be AI-generated for consistency</div>
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
<div class="quiz-option" data-correct="false">Ship first, address concerns later</div>
<div class="quiz-option" data-correct="true">1) Define agent boundaries and permissions (CISO), 2) Document capabilities and limitations (compliance), 3) Start with supervised autonomy for a pilot team (dev speed), 4) Communicate that agents augment (not replace) developers (HR)</div>
<div class="quiz-option" data-correct="false">Wait until all concerns are fully resolved before any deployment</div>
<div class="quiz-option" data-correct="false">Ignore non-technical stakeholders</div>
<div class="quiz-explanation">Successful deployment addresses all stakeholders: security first (boundaries), compliance second (documentation), controlled rollout third (pilot with supervision), and clear communication fourth (agents augment humans). This balances safety, governance, speed, and organizational change. <a href="../study_notes/#64-compliance-with-responsible-ai-policies">📖 Study Guide</a></div>
</div>
</div>

<div class="quiz" data-domain="Performance & Implementation" data-type="single">
<div class="quiz-question">
<div class="quiz-stem">An agent is making parallel tool calls to speed up a multi-file refactoring task. What risk does this introduce?</div>
<div class="quiz-option" data-correct="false">Higher cost per token</div>
<div class="quiz-option" data-correct="true">Race conditions where parallel edits to related files may conflict or create inconsistencies</div>
<div class="quiz-option" data-correct="false">Slower overall completion</div>
<div class="quiz-option" data-correct="false">No risks — parallel is always better</div>
<div class="quiz-explanation">Parallel tool calls can cause conflicts when editing related files — one edit might depend on the state created by another. The fix: identify dependencies between edits and only parallelize truly independent operations. <a href="../study_notes/#23-multi-step-agent-workflows">📖 Study Guide</a></div>
</div>
</div>
</div>
