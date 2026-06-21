# Cross-Domain Connections

## Overview

The GH-600 exam tests integrated knowledge — concepts that span multiple domains. Understanding these connections helps you answer complex scenario-based questions that combine topics from different areas.

---

## Relationship Diagram

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#6366f1', 'primaryTextColor': '#fff', 'lineColor': '#94a3b8', 'fontSize': '13px'}}}%%
graph LR
    subgraph D1[🏗️ Domain 1: Architecture]
        A1[Agent Patterns]:::d1
        A2[SDLC Integration]:::d1
    end
    subgraph D2[⚙️ Domain 2: Implementation]
        B1[Agent Mode]:::d2
        B2[MCP]:::d2
        B3[Extensions]:::d2
    end
    subgraph D3[📊 Domain 3: Performance]
        C1[Quality Metrics]:::d3
        C2[Monitoring]:::d3
    end
    subgraph D4[🛡️ Domain 4: Security]
        D41[Access Control]:::d4
        D42[Secrets Mgmt]:::d4
        D43[Audit Logging]:::d4
    end
    subgraph D5[🤝 Domain 5: Collaboration]
        E1[Code Gen/Review]:::d5
        E2[CI/CD]:::d5
        E3[Testing]:::d5
    end
    subgraph D6[⚖️ Domain 6: Responsible AI]
        F1[6 Principles]:::d6
        F2[Bias/Fairness]:::d6
        F3[Compliance]:::d6
    end

    A1 --> B1
    A1 --> B2
    A2 --> E2
    B1 --> E1
    B2 --> D41
    B2 --> E2
    C1 --> E3
    C2 --> D43
    D41 --> F3
    D43 --> F3
    E1 --> F2
    E2 --> D41

    classDef d1 fill:#6366f1,stroke:#4f46e5,color:#fff
    classDef d2 fill:#06b6d4,stroke:#0891b2,color:#fff
    classDef d3 fill:#10b981,stroke:#059669,color:#fff
    classDef d4 fill:#f59e0b,stroke:#d97706,color:#fff
    classDef d5 fill:#ef4444,stroke:#dc2626,color:#fff
    classDef d6 fill:#8b5cf6,stroke:#7c3aed,color:#fff
```

<p class="diagram-caption">🔗 Arrows show how concepts from one domain connect to and depend on another</p>

---

## Key Cross-Domain Concepts

### MCP (Domains 2, 4, 5)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#06b6d4', 'primaryTextColor': '#fff', 'lineColor': '#94a3b8', 'fontSize': '13px'}}}%%
graph TB
    MCP[🔌 MCP Protocol]:::center
    MCP --> D2[⚙️ Domain 2: Build Servers & Tools]:::d2
    MCP --> D4[🛡️ Domain 4: Secure & Govern Access]:::d4
    MCP --> D5[🤝 Domain 5: CI/CD & Team Sharing]:::d5

    classDef center fill:#06b6d4,stroke:#0891b2,color:#fff,stroke-width:3px
    classDef d2 fill:#818cf8,stroke:#6366f1,color:#fff
    classDef d4 fill:#f59e0b,stroke:#d97706,color:#fff
    classDef d5 fill:#ef4444,stroke:#dc2626,color:#fff
```

| Domain | Aspect | Key Point |
|--------|--------|-----------|
| **2** | Implementation | Building servers, defining tools, configuring transport |
| **4** | Security | Permissions, secret injection, access boundaries |
| **5** | Collaboration | Using MCP tools in CI/CD, team-shared servers |

MCP is the exam's most cross-cutting topic. You need to know how to implement servers (Domain 2), secure them (Domain 4), and use them in team workflows (Domain 5).

---

### Human Oversight (Domains 1, 4, 5, 6)

| Domain | Aspect | Key Point |
|--------|--------|-----------|
| **1** | Architecture | Designing autonomy levels into agent systems |
| **4** | Security | Approval gates for sensitive operations |
| **5** | Collaboration | Human-agent interaction patterns |
| **6** | Responsible AI | Accountability principle requires human control |

Human oversight is a requirement across all domains. The exam tests whether you know WHEN human approval is needed and HOW to implement it.

---

### Security (Domains 2, 4, 5, 6)

| Domain | Aspect | Key Point |
|--------|--------|-----------|
| **2** | Implementation | Secure tool configuration, secret handling in MCP |
| **4** | Core | Access controls, permissions, audit, governance |
| **5** | CI/CD | Security scanning in pipelines, safe automation |
| **6** | Compliance | Regulatory compliance, privacy protection |

Security is never just Domain 4. Every domain has security implications that the exam tests.

---

### Performance Monitoring (Domains 3, 4, 5)

| Domain | Aspect | Key Point |
|--------|--------|-----------|
| **3** | Core | KPIs, metrics, evaluation frameworks |
| **4** | Security | Audit logs, anomaly detection |
| **5** | CI/CD | Build/test metrics, deployment success rates |

Monitoring spans observability (performance), security (audit), and process (CI/CD metrics).

---

## Integrative Themes

### Theme 1: "Defense in Depth" — Layers of Safety

Security and responsible AI create overlapping layers:

1. **Architecture Layer** (D1): Design with least privilege, proper autonomy levels
2. **Implementation Layer** (D2): Tool permissions, MCP access control
3. **Runtime Layer** (D4): Audit logging, approval gates, secret management
4. **Process Layer** (D5): CI/CD security checks, code review
5. **Governance Layer** (D6): Compliance monitoring, bias detection, incident response

### Theme 2: "Measure Everything" — Data-Driven Agent Management

| What to Measure | Why | Where |
|----------------|-----|-------|
| Task completion | Agent effectiveness | D3 |
| Security events | Threat detection | D4 |
| Bias indicators | Fairness compliance | D6 |
| CI/CD metrics | Process efficiency | D5 |
| User satisfaction | Tool adoption | D3, D5 |

### Theme 3: "Context is King" — Information Flow

How agents get, use, and protect information connects Domains 2, 4, and 5:

- **Getting context**: File reads, MCP resources, search (D2)
- **Protecting context**: Access controls, data classification (D4)
- **Sharing context**: Team-shared configs, CI/CD integration (D5)
- **Context quality**: Affects output quality and performance (D3)

---

## Exam Strategy for Cross-Domain Questions

!!! tip "Advanced Question Strategy"
    When you see a scenario-based question that mentions multiple concepts:

    1. Identify which domains are involved
    2. Check if the answer requires balancing competing concerns (security vs. usability)
    3. Look for the answer that addresses ALL mentioned domains, not just one
    4. Eliminate answers that ignore security or responsible AI requirements
    5. The correct answer usually involves multiple controls working together
