# Implementation Plan: GH-600 Exam Prep Generator

## Overview

This plan implements a Python-based pipeline that ingests GH-600 certification source materials, processes them through ten phases, and produces a complete static study website deployed to GitHub Pages via MkDocs Material. Each task builds incrementally on prior work, wiring components together progressively to avoid orphaned code.

## Tasks

- [x] 1. Set up project structure, dependencies, and core configuration
  - [x] 1.1 Initialize project with pyproject.toml, directory structure, and dependencies
    - Create `pyproject.toml` with dependencies: httpx, beautifulsoup4, pydantic, jinja2, mkdocs-material, pymdown-extensions, hypothesis, pytest
    - Create directory structure: `src/`, `src/models/`, `src/phases/`, `src/rendering/`, `src/rendering/templates/`, `src/utils/`, `artifacts/`, `docs/`, `tests/unit/`, `tests/property/`, `tests/integration/`
    - Add `__init__.py` files to all Python packages
    - _Requirements: 11.1, 14.2, 14.7_

  - [x] 1.2 Create configuration module and exam domain constants
    - Create `src/config.py` with ExamDomain data for all 6 official GH-600 domains including names, weight ranges, and sub-topics
    - Define pipeline constants: max link depth (2), max links per level (50), rate limit settings, scoring parameters
    - Define source URLs list for Microsoft Learn GH-600 materials
    - _Requirements: 1.2, 3.2_

  - [x] 1.3 Create all Pydantic data models
    - Create `src/models/knowledge.py` with KnowledgePoint, ParsedDocument, ExtractionResult, ExtractionLog models
    - Create `src/models/topic_map.py` with Topic, Dependency, CrossReference, TopicHierarchy models
    - Create `src/models/scoring.py` with ScoredTopic, ScoredTopicList, ExamDomain, ExamObjective models
    - Create `src/models/study_notes.py` with TopicNotes, StudyNotesCollection models
    - Create `src/models/curriculum.py` with Module, Curriculum models
    - Create `src/models/revision.py` with Flashcard, CheatSheet, Mnemonic, RevisionPackage models
    - Create `src/models/questions.py` with Question, QuestionBank, QuestionFormat, DifficultyLevel models
    - Create `src/models/mock_exam.py` with MockExam, GradingRubric models
    - Create `src/models/gap_analysis.py` with Gap, GapReport, CoverageStatus models
    - Create `src/models/readiness.py` with ReadinessAssessment, HighRiskTopic, TimeBlock, RemediationPlan models
    - _Requirements: 1.1–1.6, 2.1–2.6, 3.1–3.5, 4.1–4.7, 5.1–5.6, 6.1–6.6, 7.1–7.7, 8.1–8.8, 9.1–9.5, 10.1–10.5_

- [x] 2. Implement Phase 1: Knowledge Extractor
  - [x] 2.1 Create HTTP scraper utility with rate limiting and error handling
    - Create `src/utils/scraper.py` with async HTTP client using httpx.AsyncClient
    - Implement rate limiting: max 5 concurrent requests, 1s delay between same-domain requests
    - Implement retry logic: 1 retry after 5s timeout, exponential backoff for HTTP 429
    - Log inaccessible resources with URL, error, and referrer
    - _Requirements: 1.3_

  - [x] 2.2 Create URL deduplication utility
    - Create `src/utils/dedup.py` with URL normalization and visited-URL tracking
    - Normalize URLs by removing fragments, sorting query params, lowercasing scheme/host
    - _Requirements: 1.6_

  - [x] 2.3 Implement KnowledgeExtractor phase
    - Create `src/phases/phase01_extractor.py` with KnowledgeExtractor class
    - Implement `extract()` to process source URLs, follow links up to depth 2 (max 50 per level)
    - Implement `_fetch_and_parse()` to fetch documents and extract HTML content using BeautifulSoup
    - Implement `_extract_knowledge_points()` to identify concepts, definitions, facts, theories, procedures, and frameworks
    - Implement `_reconstruct_prerequisites()` for prerequisite concepts not in sources (limited scope)
    - Only follow links within `learn.microsoft.com` and `docs.github.com` domains
    - Write ExtractionResult artifact to `artifacts/phase01_extraction.json`
    - _Requirements: 1.1, 1.2, 1.4, 1.5, 1.6_

  - [x] 2.4 Write property tests for Knowledge Extractor
    - **Property 1: Link Traversal Depth and Breadth Constraints**
    - **Property 2: URL Deduplication**
    - **Validates: Requirements 1.2, 1.6**

- [x] 3. Implement Phase 2: Topic Mapper
  - [x] 3.1 Implement TopicMapper phase
    - Create `src/phases/phase02_mapper.py` with TopicMapper class
    - Implement `map_topics()` to organize knowledge points into hierarchical structure aligned with 6 GH-600 exam domains
    - Implement `_assign_to_domains()` to categorize topics under domains and sub-domains
    - Implement `_identify_prerequisites()` to detect prerequisite relationships between topics
    - Implement `_compute_learning_order()` using Kahn's algorithm (topological sort)
    - Implement `_detect_cycles()` to find circular dependencies and group into learning units
    - Implement `_identify_cross_references()` for topics sharing tools, APIs, patterns, or workflows
    - Read from `artifacts/phase01_extraction.json`, write to `artifacts/phase02_topic_map.json`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [x] 3.2 Write property tests for Topic Mapper
    - **Property 3: Topic Learning Order is Valid Topological Sort**
    - **Property 4: Cycle Detection Groups Mutually Dependent Topics**
    - **Validates: Requirements 2.4, 2.6**

- [x] 4. Implement Phase 3: Relevance Analyzer
  - [x] 4.1 Implement RelevanceAnalyzer phase
    - Create `src/phases/phase03_analyzer.py` with RelevanceAnalyzer class
    - Implement `_compute_base_score()` mapping domain weight ranges to score ranges (20-25% → 8-9, 15-20% → 6-8, 10-15% → 5-7)
    - Implement `_apply_cross_domain_bonus()` adding +1 per additional domain appearance (capped at 10)
    - Implement `_sort_topics()` sorting by descending score, then descending domain count, then alphabetical name
    - Flag topics with score ≥ 8 as high-priority
    - Read from `artifacts/phase02_topic_map.json`, write to `artifacts/phase03_scores.json`
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 4.2 Write property tests for Relevance Analyzer
    - **Property 5: Priority Score Range and Domain Bonus**
    - **Property 6: Domain Weight Influences Base Score Monotonically**
    - **Property 7: Topic Score List Sort Order**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

- [x] 5. Checkpoint - Core extraction and scoring pipeline
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement Phase 4: Study Notes Generator
  - [x] 6.1 Implement StudyNotesGenerator phase
    - Create `src/phases/phase04_notes.py` with StudyNotesGenerator class
    - Implement `_generate_topic_notes()` producing notes with required sections: overview (3+ sentences), explanation (200+ words, 400+ for high-priority), key facts (3+), common mistakes (2+), examples (1+, 2+ for high-priority), exam tips (1+)
    - Include step-by-step instructions for procedure/workflow topics
    - Include code blocks with language identifiers and inline comments for config/code topics
    - Implement `_build_cross_references()` linking related concepts across domains using topic heading anchors
    - Implement `_supplement_sparse_topics()` for topics with < 3 knowledge points, marking supplemented content with visual indicator
    - Read from `artifacts/phase02_topic_map.json` and `artifacts/phase03_scores.json`, write to `artifacts/phase04_notes.json`
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

  - [x] 6.2 Write property tests for Study Notes Generator
    - **Property 8: Study Notes Structural Completeness**
    - **Property 9: Sparse Topic Supplementation**
    - **Property 10: Cross-Reference Referential Integrity**
    - **Validates: Requirements 4.1, 4.2, 4.5, 4.6, 4.7**

- [x] 7. Implement Phase 5: Curriculum Builder
  - [x] 7.1 Implement CurriculumBuilder phase
    - Create `src/phases/phase05_curriculum.py` with CurriculumBuilder class
    - Implement `_create_modules()` organizing topics into sequential modules respecting prerequisite order
    - Implement `_validate_bloom_verbs()` ensuring 2-7 objectives per module using Bloom's Taxonomy verbs
    - Implement `_estimate_time()` with 15-180 minute range; high-priority modules get 1.5× average non-high-priority time
    - List prerequisites as module IDs or ["none"]
    - Calculate total study time as sum of all module estimates
    - Read from `artifacts/phase02_topic_map.json` and `artifacts/phase03_scores.json`, write to `artifacts/phase05_curriculum.json`
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [x] 7.2 Write property tests for Curriculum Builder
    - **Property 11: Curriculum Module Ordering Respects Prerequisites**
    - **Property 12: Module Objectives and Time Constraints**
    - **Property 13: High-Priority Module Time Multiplier**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6**

- [x] 8. Implement Phase 6: Revision Generator
  - [x] 8.1 Implement RevisionGenerator phase
    - Create `src/phases/phase06_revision.py` with RevisionGenerator class
    - Implement `_generate_executive_summary()` covering all 6 domains in ≤ 2000 words
    - Implement `_generate_cheat_sheets()` with key patterns, commands, and at least 1 table per domain
    - Implement `_generate_flashcards()` producing 100+ flashcards distributed across all 6 domains, tagged with domain name and Priority_Score, formatted with "Q: " / "A: " prefixes
    - Implement `_generate_mnemonics()` for topics with 3+ sequential steps/components
    - Read from `artifacts/phase04_notes.json` and `artifacts/phase03_scores.json`, write to `artifacts/phase06_revision.json`
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

  - [x] 8.2 Write property test for Revision Generator
    - **Property 14: Flashcard Completeness and Format**
    - **Validates: Requirements 6.3, 6.5, 6.6**

- [x] 9. Implement Phase 7: Question Generator
  - [x] 9.1 Implement QuestionGenerator phase
    - Create `src/phases/phase07_questions.py` with QuestionGenerator class
    - Implement question generation at three difficulty levels: easy (single-concept recall), intermediate (applying concepts), advanced (multi-topic analysis)
    - Generate minimum 20 questions per level, distributed proportionally to domain weights
    - Implement all three formats: multiple choice (4 options, 1 correct), multiple select (4-6 options, 2+ correct), scenario-based
    - Advanced level: ≥ 50% scenario-based, each referencing 2+ topics
    - Each question includes correct answer, reasoning, concept reference, study notes link, and explanations for incorrect options
    - Read from `artifacts/phase04_notes.json` and `artifacts/phase03_scores.json`, write to `artifacts/phase07_questions.json`
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7_

  - [x] 9.2 Write property tests for Question Generator
    - **Property 15: Question Bank Distribution and Structure**
    - **Property 16: Advanced Questions Scenario Proportion**
    - **Validates: Requirements 7.2, 7.3, 7.4, 7.5, 7.6, 7.7**

- [x] 10. Implement Phase 8: Mock Exam Builder
  - [x] 10.1 Implement MockExamBuilder phase
    - Create `src/phases/phase08_mock_exam.py` with MockExamBuilder class
    - Implement `_select_questions()` selecting 50+ questions with domain distribution within ±5pp of target weights
    - Ensure each format (MC, MS, scenario) ≥ 15% of total questions
    - Implement `_build_grading_rubric()` with 1 point per single-answer, all-or-nothing for multi-select, 700/1000 pass threshold
    - Implement `_calculate_time_limit()` based on official GH-600 exam duration
    - Include cross-reference links to study notes in high-priority question solutions
    - Read from `artifacts/phase07_questions.json` and `artifacts/phase03_scores.json`, write to `artifacts/phase08_mock_exam.json`
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8_

  - [x] 10.2 Write property tests for Mock Exam Builder
    - **Property 17: Mock Exam Domain and Format Distribution**
    - **Property 18: Mock Exam Answer Key Completeness**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.6**

- [x] 11. Checkpoint - Content generation pipeline
  - Ensure all tests pass, ask the user if questions arise.

- [x] 12. Implement Phase 9: Gap Analyzer
  - [x] 12.1 Implement GapAnalyzer phase
    - Create `src/phases/phase09_gap.py` with GapAnalyzer class
    - Implement `_assess_coverage()` classifying each objective as fully covered (≥3 points), weakly covered (1-2 points), or not covered (0 points or inaccessible)
    - Implement `_identify_critical_gaps()` flagging gaps in high-priority topics (score ≥ 8) as critical, placed in dedicated section
    - Implement `_recommend_resources()` providing at least 2 recommendations per gap with topic area
    - Read from `artifacts/phase04_notes.json`, `artifacts/phase03_scores.json`, and `artifacts/phase01_extraction.json` error log, write to `artifacts/phase09_gap_report.json`
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [x] 12.2 Write property tests for Gap Analyzer
    - **Property 19: Coverage Status Classification Consistency**
    - **Property 20: Critical Gap Prioritization**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5**

- [x] 13. Implement Phase 10: Readiness Assessor
  - [x] 13.1 Implement ReadinessAssessor phase
    - Create `src/phases/phase10_readiness.py` with ReadinessAssessor class
    - Implement `_calculate_score()` as arithmetic mean of: % objectives fully covered, % topics with notes+questions, (100 - % gap topics)
    - Implement `_identify_high_risk()` listing max 10 topics sorted by Priority_Score descending
    - Implement `_build_24h_plan()` with 60-minute blocks specifying topic and resource type (study notes, flashcards, practice questions)
    - Implement `_build_remediation_plan()` for score < 70: recommend deferral with target duration in days and specific modules to revisit
    - Read from `artifacts/phase09_gap_report.json`, `artifacts/phase04_notes.json`, `artifacts/phase03_scores.json`, write to `artifacts/phase10_readiness.json`
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [x] 13.2 Write property tests for Readiness Assessor
    - **Property 21: Readiness Score Calculation**
    - **Property 22: High-Risk Topic Constraints**
    - **Property 23: Readiness Score Triggers Deferral Recommendation**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.5**

- [x] 14. Implement Pipeline Orchestrator
  - [x] 14.1 Create pipeline orchestrator and structured logging
    - Create `src/utils/logging.py` with structured JSON logging to `artifacts/pipeline_errors.json`
    - Create `src/pipeline.py` orchestrating all 10 phases in DAG order
    - Implement graceful error handling: log errors, continue where possible, report execution metrics
    - Produce exit codes: 0 (success), 1 (partial with warnings), 2 (failure)
    - _Requirements: 1.3, 9.3_

- [x] 15. Checkpoint - Full pipeline logic complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 16. Implement Rendering Layer and MkDocs Site
  - [x] 16.1 Create Jinja2 templates for all study material sections
    - Create templates in `src/rendering/templates/` for: landing page, study notes, curriculum, revision resources, practice questions, mock exam, gap report, readiness assessment
    - Templates produce GFM-compatible Markdown with proper heading hierarchy (H1-H4), tables, blockquote callouts (Note, Tip, Warning, Important), code blocks with language IDs, ordered/unordered lists
    - Include master table of contents with anchor links to all H1/H2 sections
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8_

  - [x] 16.2 Implement SiteRenderer and cross-domain content
    - Create `src/rendering/renderer.py` with SiteRenderer class
    - Implement rendering of all 10 phase artifacts into Markdown files in `docs/` directory
    - Generate cross-reference links between sections that resolve to valid pages
    - Generate Mermaid relationship diagram showing concepts with Priority_Score ≥ 7 across 2+ domains
    - Generate integrative summary sections for themes spanning 3+ domains
    - Include Related Topics sections (1-10 entries) for topics with cross-domain connections; omit for topics without
    - Dynamically generate `mkdocs.yml` nav structure from artifacts
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 13.8_

  - [x] 16.3 Write property tests for rendering output
    - **Property 24: Markdown Heading Hierarchy**
    - **Property 25: Cross-Domain Relationship Diagram Completeness**
    - **Property 26: Related Topics Section Bounds**
    - **Validates: Requirements 11.2, 11.5, 12.1, 12.2, 12.3, 12.5**

- [x] 17. Configure MkDocs and GitHub Pages deployment
  - [x] 17.1 Create MkDocs configuration
    - Create `mkdocs.yml` with Material theme, search plugin, Mermaid support, admonition extensions, syntax highlighting, responsive design, breadcrumbs, prev/next navigation
    - Configure base URL path prefix for GitHub Pages subpath
    - Ensure all assets (styles, scripts, fonts) are bundled locally with no external CDN dependencies
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 14.1, 14.2, 14.5, 14.7_

  - [x] 17.2 Create GitHub Actions deployment workflow
    - Create `.github/workflows/deploy.yml` with: checkout, Python setup (3.12), dependency install, `mkdocs build --strict`, upload pages artifact, deploy to GitHub Pages
    - Report build/deploy failures in workflow logs with failing step name and error cause
    - _Requirements: 14.3, 14.4, 14.6_

  - [x] 17.3 Write property test for static site output
    - **Property 27: No External CDN Dependencies**
    - **Validates: Requirements 14.7**

- [x] 18. Integration testing and final wiring
  - [x] 18.1 Create integration tests for full pipeline
    - Write integration test executing full pipeline with mocked HTTP responses
    - Verify MkDocs build passes with `mkdocs build --strict`
    - Verify all internal cross-reference links resolve to valid pages
    - Verify search index is generated
    - _Requirements: 13.4, 13.8, 14.4_

  - [x] 18.2 Wire CLI entry point and finalize project
    - Add CLI entry point in `pyproject.toml` scripts for running the pipeline
    - Ensure pipeline reads source URLs from config and produces complete site in `docs/`
    - Verify end-to-end: pipeline → artifacts → rendered Markdown → MkDocs build → static site
    - _Requirements: 14.1_

- [x] 19. Final checkpoint - Complete system verification
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document (27 total)
- Unit tests validate specific examples and edge cases
- The pipeline architecture allows re-running individual phases without full re-execution
- All intermediate artifacts are JSON files in `artifacts/` for debugging and validation
- Python with Hypothesis is used for property-based testing as specified in the design

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "1.3"] },
    { "id": 2, "tasks": ["2.1", "2.2"] },
    { "id": 3, "tasks": ["2.3"] },
    { "id": 4, "tasks": ["2.4", "3.1"] },
    { "id": 5, "tasks": ["3.2", "4.1"] },
    { "id": 6, "tasks": ["4.2", "6.1", "7.1"] },
    { "id": 7, "tasks": ["6.2", "7.2", "8.1"] },
    { "id": 8, "tasks": ["8.2", "9.1"] },
    { "id": 9, "tasks": ["9.2", "10.1"] },
    { "id": 10, "tasks": ["10.2", "12.1"] },
    { "id": 11, "tasks": ["12.2", "13.1"] },
    { "id": 12, "tasks": ["13.2", "14.1"] },
    { "id": 13, "tasks": ["16.1", "17.1", "17.2"] },
    { "id": 14, "tasks": ["16.2"] },
    { "id": 15, "tasks": ["16.3", "17.3", "18.1"] },
    { "id": 16, "tasks": ["18.2"] }
  ]
}
```
