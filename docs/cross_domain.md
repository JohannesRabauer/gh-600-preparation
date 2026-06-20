# Cross-Domain Connections

## Relationship Diagram

The following diagram shows how high-priority concepts (Priority_Score ≥ 7) relate across exam domains.

```mermaid
graph LR
    subgraph domain_3[Evaluate and optimize agent performance]
        t_a[Shared Concept]
        t_b[Related Concept]
    end
    subgraph domain_5[Collaborate with AI agents in the development workflow]
        t_a[Shared Concept]
        t_b[Related Concept]
    end
    t_b -.- |spans| domain_3 & domain_5
    t_a -.- |spans| domain_3 & domain_5
```

## Cross-Domain Concepts

Concepts that appear in multiple exam domains with links to their coverage in each domain.

| Concept | Domains | Priority Score |
|---------|---------|---------------|
| [Related Concept](study_notes.md#related-concept) | [Evaluate and optimize agent performance](study_notes.md#related-concept), [Collaborate with AI agents in the development workflow](study_notes.md#related-concept) | 9/10 |
| [Shared Concept](study_notes.md#shared-concept) | [Evaluate and optimize agent performance](study_notes.md#shared-concept), [Collaborate with AI agents in the development workflow](study_notes.md#shared-concept) | 8/10 |
