# Cross-Domain Connections

## Relationship Diagram

The following diagram shows how high-priority concepts (Priority_Score ≥ 7) relate across exam domains.

```mermaid
graph LR
    subgraph domain_1[Prepare agent architecture and SDLC processes]
        topic_001[Exam scoring and score reports | Microsoft Learn
Table...]
        topic_002[Request exam accommodations and frequently asked...]
        topic_006[Study guide for Exam GH-600: Developing in Agentic AI...]
        topic_007[Tooling, MCP, and Agent Execution Environments -...]
        topic_008[Microsoft previous versions of technical documentation |...]
        topic_009[Terms of Use | Microsoft Learn
learn]
        topic_010[Modern Lifecycle Policy - Microsoft Lifecycle |...]
        topic_012[About online exams with Pearson VUE | Microsoft...]
        topic_013[Exercise - Develop with AI-powered code suggestions by...]
        topic_015[Introduction - Training | Microsoft Learn
Read in...]
        topic_016[Mitigate AI risks - Training | Microsoft Learn
Read in...]
    end
    subgraph domain_2[Design and implement agentic solutions]
        topic_001[Exam scoring and score reports | Microsoft Learn
Table...]
        topic_002[Request exam accommodations and frequently asked...]
        topic_006[Study guide for Exam GH-600: Developing in Agentic AI...]
        topic_007[Tooling, MCP, and Agent Execution Environments -...]
        topic_008[Microsoft previous versions of technical documentation |...]
        topic_009[Terms of Use | Microsoft Learn
learn]
        topic_010[Modern Lifecycle Policy - Microsoft Lifecycle |...]
        topic_012[About online exams with Pearson VUE | Microsoft...]
        topic_013[Exercise - Develop with AI-powered code suggestions by...]
        topic_014[Microsoft Certification Renewal | Microsoft...]
        topic_015[Introduction - Training | Microsoft Learn
Read in...]
        topic_016[Mitigate AI risks - Training | Microsoft Learn
Read in...]
    end
    subgraph domain_4[Secure and govern agentic AI solutions]
        topic_001[Exam scoring and score reports | Microsoft Learn
Table...]
        topic_002[Request exam accommodations and frequently asked...]
        topic_006[Study guide for Exam GH-600: Developing in Agentic AI...]
        topic_007[Tooling, MCP, and Agent Execution Environments -...]
        topic_008[Microsoft previous versions of technical documentation |...]
        topic_009[Terms of Use | Microsoft Learn
learn]
        topic_010[Modern Lifecycle Policy - Microsoft Lifecycle |...]
        topic_012[About online exams with Pearson VUE | Microsoft...]
        topic_013[Exercise - Develop with AI-powered code suggestions by...]
        topic_014[Microsoft Certification Renewal | Microsoft...]
        topic_015[Introduction - Training | Microsoft Learn
Read in...]
        topic_016[Mitigate AI risks - Training | Microsoft Learn
Read in...]
    end
    subgraph domain_5[Collaborate with AI agents in the development workflow]
        topic_001[Exam scoring and score reports | Microsoft Learn
Table...]
        topic_006[Study guide for Exam GH-600: Developing in Agentic AI...]
        topic_007[Tooling, MCP, and Agent Execution Environments -...]
        topic_009[Terms of Use | Microsoft Learn
learn]
        topic_010[Modern Lifecycle Policy - Microsoft Lifecycle |...]
        topic_013[Exercise - Develop with AI-powered code suggestions by...]
        topic_015[Introduction - Training | Microsoft Learn
Read in...]
        topic_016[Mitigate AI risks - Training | Microsoft Learn
Read in...]
    end
    subgraph domain_6[Implement responsible AI practices]
        topic_001[Exam scoring and score reports | Microsoft Learn
Table...]
        topic_002[Request exam accommodations and frequently asked...]
        topic_006[Study guide for Exam GH-600: Developing in Agentic AI...]
        topic_007[Tooling, MCP, and Agent Execution Environments -...]
        topic_008[Microsoft previous versions of technical documentation |...]
        topic_009[Terms of Use | Microsoft Learn
learn]
        topic_010[Modern Lifecycle Policy - Microsoft Lifecycle |...]
        topic_012[About online exams with Pearson VUE | Microsoft...]
        topic_013[Exercise - Develop with AI-powered code suggestions by...]
        topic_014[Microsoft Certification Renewal | Microsoft...]
        topic_015[Introduction - Training | Microsoft Learn
Read in...]
        topic_016[Mitigate AI risks - Training | Microsoft Learn
Read in...]
    end
    topic_001 -.- |spans| domain_1 & domain_2
    topic_013 -.- |spans| domain_1 & domain_2
    topic_015 -.- |spans| domain_1 & domain_2
    topic_016 -.- |spans| domain_1 & domain_2
    topic_010 -.- |spans| domain_1 & domain_2
    topic_006 -.- |spans| domain_1 & domain_2
    topic_009 -.- |spans| domain_1 & domain_2
    topic_007 -.- |spans| domain_1 & domain_2
    topic_012 -.- |spans| domain_1 & domain_2
    topic_008 -.- |spans| domain_1 & domain_2
    topic_002 -.- |spans| domain_1 & domain_2
    topic_014 -.- |spans| domain_2 & domain_4
```

## Cross-Domain Concepts

Concepts that appear in multiple exam domains with links to their coverage in each domain.

| Concept | Domains | Priority Score |
|---------|---------|---------------|
| [Exam scoring and score reports | Microsoft Learn
Table...](study_notes.md#exam-scoring-and-score-reports-|-microsoft-learn
table...) | [Prepare agent architecture and SDLC processes](study_notes.md#exam-scoring-and-score-reports-|-microsoft-learn
table...), [Design and implement agentic solutions](study_notes.md#exam-scoring-and-score-reports-|-microsoft-learn
table...), [Secure and govern agentic AI solutions](study_notes.md#exam-scoring-and-score-reports-|-microsoft-learn
table...), [Collaborate with AI agents in the development workflow](study_notes.md#exam-scoring-and-score-reports-|-microsoft-learn
table...), [Implement responsible AI practices](study_notes.md#exam-scoring-and-score-reports-|-microsoft-learn
table...) | 10/10 |
| [Exercise - Develop with AI-powered code suggestions by...](study_notes.md#exercise---develop-with-ai-powered-code-suggestions-by...) | [Prepare agent architecture and SDLC processes](study_notes.md#exercise---develop-with-ai-powered-code-suggestions-by...), [Design and implement agentic solutions](study_notes.md#exercise---develop-with-ai-powered-code-suggestions-by...), [Secure and govern agentic AI solutions](study_notes.md#exercise---develop-with-ai-powered-code-suggestions-by...), [Collaborate with AI agents in the development workflow](study_notes.md#exercise---develop-with-ai-powered-code-suggestions-by...), [Implement responsible AI practices](study_notes.md#exercise---develop-with-ai-powered-code-suggestions-by...) | 10/10 |
| [Introduction - Training | Microsoft Learn
Read in...](study_notes.md#introduction---training-|-microsoft-learn
read-in...) | [Prepare agent architecture and SDLC processes](study_notes.md#introduction---training-|-microsoft-learn
read-in...), [Design and implement agentic solutions](study_notes.md#introduction---training-|-microsoft-learn
read-in...), [Secure and govern agentic AI solutions](study_notes.md#introduction---training-|-microsoft-learn
read-in...), [Collaborate with AI agents in the development workflow](study_notes.md#introduction---training-|-microsoft-learn
read-in...), [Implement responsible AI practices](study_notes.md#introduction---training-|-microsoft-learn
read-in...) | 10/10 |
| [Mitigate AI risks - Training | Microsoft Learn
Read in...](study_notes.md#mitigate-ai-risks---training-|-microsoft-learn
read-in...) | [Prepare agent architecture and SDLC processes](study_notes.md#mitigate-ai-risks---training-|-microsoft-learn
read-in...), [Design and implement agentic solutions](study_notes.md#mitigate-ai-risks---training-|-microsoft-learn
read-in...), [Secure and govern agentic AI solutions](study_notes.md#mitigate-ai-risks---training-|-microsoft-learn
read-in...), [Collaborate with AI agents in the development workflow](study_notes.md#mitigate-ai-risks---training-|-microsoft-learn
read-in...), [Implement responsible AI practices](study_notes.md#mitigate-ai-risks---training-|-microsoft-learn
read-in...) | 10/10 |
| [Modern Lifecycle Policy - Microsoft Lifecycle |...](study_notes.md#modern-lifecycle-policy---microsoft-lifecycle-|...) | [Prepare agent architecture and SDLC processes](study_notes.md#modern-lifecycle-policy---microsoft-lifecycle-|...), [Design and implement agentic solutions](study_notes.md#modern-lifecycle-policy---microsoft-lifecycle-|...), [Secure and govern agentic AI solutions](study_notes.md#modern-lifecycle-policy---microsoft-lifecycle-|...), [Collaborate with AI agents in the development workflow](study_notes.md#modern-lifecycle-policy---microsoft-lifecycle-|...), [Implement responsible AI practices](study_notes.md#modern-lifecycle-policy---microsoft-lifecycle-|...) | 10/10 |
| [Study guide for Exam GH-600: Developing in Agentic AI...](study_notes.md#study-guide-for-exam-gh-600:-developing-in-agentic-ai...) | [Prepare agent architecture and SDLC processes](study_notes.md#study-guide-for-exam-gh-600:-developing-in-agentic-ai...), [Design and implement agentic solutions](study_notes.md#study-guide-for-exam-gh-600:-developing-in-agentic-ai...), [Secure and govern agentic AI solutions](study_notes.md#study-guide-for-exam-gh-600:-developing-in-agentic-ai...), [Collaborate with AI agents in the development workflow](study_notes.md#study-guide-for-exam-gh-600:-developing-in-agentic-ai...), [Implement responsible AI practices](study_notes.md#study-guide-for-exam-gh-600:-developing-in-agentic-ai...) | 10/10 |
| [Terms of Use | Microsoft Learn
learn](study_notes.md#terms-of-use-|-microsoft-learn
learn) | [Prepare agent architecture and SDLC processes](study_notes.md#terms-of-use-|-microsoft-learn
learn), [Design and implement agentic solutions](study_notes.md#terms-of-use-|-microsoft-learn
learn), [Secure and govern agentic AI solutions](study_notes.md#terms-of-use-|-microsoft-learn
learn), [Collaborate with AI agents in the development workflow](study_notes.md#terms-of-use-|-microsoft-learn
learn), [Implement responsible AI practices](study_notes.md#terms-of-use-|-microsoft-learn
learn) | 10/10 |
| [Tooling, MCP, and Agent Execution Environments -...](study_notes.md#tooling,-mcp,-and-agent-execution-environments--...) | [Prepare agent architecture and SDLC processes](study_notes.md#tooling,-mcp,-and-agent-execution-environments--...), [Design and implement agentic solutions](study_notes.md#tooling,-mcp,-and-agent-execution-environments--...), [Secure and govern agentic AI solutions](study_notes.md#tooling,-mcp,-and-agent-execution-environments--...), [Collaborate with AI agents in the development workflow](study_notes.md#tooling,-mcp,-and-agent-execution-environments--...), [Implement responsible AI practices](study_notes.md#tooling,-mcp,-and-agent-execution-environments--...) | 10/10 |
| [About online exams with Pearson VUE | Microsoft...](study_notes.md#about-online-exams-with-pearson-vue-|-microsoft...) | [Prepare agent architecture and SDLC processes](study_notes.md#about-online-exams-with-pearson-vue-|-microsoft...), [Design and implement agentic solutions](study_notes.md#about-online-exams-with-pearson-vue-|-microsoft...), [Secure and govern agentic AI solutions](study_notes.md#about-online-exams-with-pearson-vue-|-microsoft...), [Implement responsible AI practices](study_notes.md#about-online-exams-with-pearson-vue-|-microsoft...) | 10/10 |
| [Microsoft previous versions of technical documentation |...](study_notes.md#microsoft-previous-versions-of-technical-documentation-|...) | [Prepare agent architecture and SDLC processes](study_notes.md#microsoft-previous-versions-of-technical-documentation-|...), [Design and implement agentic solutions](study_notes.md#microsoft-previous-versions-of-technical-documentation-|...), [Secure and govern agentic AI solutions](study_notes.md#microsoft-previous-versions-of-technical-documentation-|...), [Implement responsible AI practices](study_notes.md#microsoft-previous-versions-of-technical-documentation-|...) | 10/10 |
| [Request exam accommodations and frequently asked...](study_notes.md#request-exam-accommodations-and-frequently-asked...) | [Prepare agent architecture and SDLC processes](study_notes.md#request-exam-accommodations-and-frequently-asked...), [Design and implement agentic solutions](study_notes.md#request-exam-accommodations-and-frequently-asked...), [Secure and govern agentic AI solutions](study_notes.md#request-exam-accommodations-and-frequently-asked...), [Implement responsible AI practices](study_notes.md#request-exam-accommodations-and-frequently-asked...) | 10/10 |
| [Microsoft Certification Renewal | Microsoft...](study_notes.md#microsoft-certification-renewal-|-microsoft...) | [Design and implement agentic solutions](study_notes.md#microsoft-certification-renewal-|-microsoft...), [Secure and govern agentic AI solutions](study_notes.md#microsoft-certification-renewal-|-microsoft...), [Implement responsible AI practices](study_notes.md#microsoft-certification-renewal-|-microsoft...) | 9/10 |

## Integrative Themes

Themes that span 3 or more exam domains, showing how concepts integrate across the certification scope.

### github copilot

**Domains**: Prepare agent architecture and SDLC processes, Design and implement agentic solutions, Secure and govern agentic AI solutions, Collaborate with AI agents in the development workflow, Implement responsible AI practices

- github copilot in Prepare agent architecture and SDLC processes
- github copilot in Design and implement agentic solutions
- github copilot in Secure and govern agentic AI solutions
- github copilot in Collaborate with AI agents in the development workflow
- github copilot in Implement responsible AI practices

### github actions

**Domains**: Prepare agent architecture and SDLC processes, Design and implement agentic solutions, Secure and govern agentic AI solutions, Collaborate with AI agents in the development workflow

- github actions in Prepare agent architecture and SDLC processes
- github actions in Design and implement agentic solutions
- github actions in Secure and govern agentic AI solutions
- github actions in Collaborate with AI agents in the development workflow

### pull request

**Domains**: Prepare agent architecture and SDLC processes, Design and implement agentic solutions, Secure and govern agentic AI solutions

- pull request in Prepare agent architecture and SDLC processes
- pull request in Design and implement agentic solutions
- pull request in Secure and govern agentic AI solutions

### security

**Domains**: Prepare agent architecture and SDLC processes, Design and implement agentic solutions, Secure and govern agentic AI solutions, Implement responsible AI practices

- security in Prepare agent architecture and SDLC processes
- security in Design and implement agentic solutions
- security in Secure and govern agentic AI solutions
- security in Implement responsible AI practices

### api

**Domains**: Design and implement agentic solutions, Secure and govern agentic AI solutions, Implement responsible AI practices

- api in Design and implement agentic solutions
- api in Secure and govern agentic AI solutions
- api in Implement responsible AI practices

### testing

**Domains**: Design and implement agentic solutions, Secure and govern agentic AI solutions, Implement responsible AI practices

- testing in Design and implement agentic solutions
- testing in Secure and govern agentic AI solutions
- testing in Implement responsible AI practices
