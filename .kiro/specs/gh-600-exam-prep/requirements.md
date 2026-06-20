# Requirements Document

## Introduction

This document defines the requirements for a comprehensive exam preparation package generator for the GitHub Certified Agentic AI Developer (GH-600) certification. The system transforms source material from Microsoft Learn and related documentation into a complete, multi-phase study resource optimized for exam success, deep understanding, and long-term retention. The final output serves as the student's primary study resource in Markdown format.

## Glossary

- **Exam_Prep_Generator**: The system that processes source materials and produces the complete exam preparation package across all ten phases, deployed as a cohesive website on GitHub Pages
- **Study_Website**: The static website that binds all generated study materials into a single navigable learning resource, deployed via GitHub Pages
- **Source_Material**: Input documents from Microsoft Learn including the GH-600 study guide, certification page, and training modules
- **Knowledge_Extractor**: The component that identifies and extracts all concepts, definitions, facts, theories, procedures, and frameworks from source materials
- **Topic_Mapper**: The component that organizes extracted knowledge into a hierarchical structure with dependencies and learning order
- **Relevance_Analyzer**: The component that scores and ranks topics by exam importance
- **Study_Notes_Generator**: The component that produces detailed study notes for every identified topic
- **Curriculum_Builder**: The component that structures extracted knowledge into a complete learning course
- **Revision_Generator**: The component that produces condensed revision resources including summaries, cheat sheets, flashcards, and mnemonics
- **Question_Generator**: The component that creates practice questions at multiple difficulty levels
- **Mock_Exam_Builder**: The component that assembles realistic exam simulations with grading rubrics
- **Gap_Analyzer**: The component that identifies missing information and weakly covered areas
- **Readiness_Assessor**: The component that evaluates overall exam readiness and produces actionable recommendations
- **Exam_Domain**: One of the six weighted skill areas defined in the GH-600 study guide (e.g., "Prepare agent architecture and SDLC processes 15–20%")
- **Priority_Score**: A numerical ranking from 1 to 10 indicating exam relevance of a topic
- **Flashcard**: A structured question-and-answer pair optimized for spaced repetition review
- **Readiness_Score**: A numerical assessment from 0 to 100 indicating overall exam preparedness

## Requirements

### Requirement 1: Source Material Ingestion

**User Story:** As a certification candidate, I want the system to ingest and process all relevant source materials, so that no exam-relevant content is missed.

#### Acceptance Criteria

1. WHEN source materials are provided, THE Knowledge_Extractor SHALL parse and process the GH-600 study guide, the certification overview page, and all linked Microsoft Learn training modules
2. WHEN a source document contains hyperlinks to documentation within Microsoft Learn or GitHub documentation domains, THE Knowledge_Extractor SHALL follow and process those linked resources up to two levels of depth and a maximum of 50 linked resources per level
3. IF a source document is inaccessible or returns an error, THEN THE Exam_Prep_Generator SHALL log the resource URL, the error encountered, and the referring source document, and continue processing remaining sources
4. THE Knowledge_Extractor SHALL extract all concepts, definitions, facts, theories, procedures, and frameworks present in the source materials
5. WHEN extracted knowledge references prerequisite concepts not explicitly covered in sources, THE Knowledge_Extractor SHALL reconstruct the prerequisite knowledge limited to concepts directly required to understand the extracted topic, without expanding into unrelated domain areas
6. WHEN the same content is reachable through multiple link paths, THE Knowledge_Extractor SHALL process it only once and reference the single extracted result from all linking contexts

### Requirement 2: Topic Mapping and Hierarchy

**User Story:** As a certification candidate, I want a hierarchical topic map with dependencies and learning order, so that I can study topics in a logical progression.

#### Acceptance Criteria

1. WHEN knowledge extraction is complete, THE Topic_Mapper SHALL organize all extracted topics into a hierarchical structure with domains, sub-domains, and individual topics
2. THE Topic_Mapper SHALL align the top-level hierarchy with the six official GH-600 exam domains and their percentage weights
3. THE Topic_Mapper SHALL identify and document prerequisite relationships between topics using a format that specifies the source topic, the target topic, and the nature of the dependency
4. THE Topic_Mapper SHALL produce a recommended learning order as a numbered sequence of topics where no topic appears before any of its prerequisites
5. WHEN two or more topics share conceptual overlap (defined as referencing the same tool, API, pattern, or workflow), THE Topic_Mapper SHALL document cross-references between the related topics
6. IF a circular prerequisite dependency is detected among topics, THEN THE Topic_Mapper SHALL group the mutually dependent topics into a single learning unit and document the cycle

### Requirement 3: Exam Relevance Analysis

**User Story:** As a certification candidate, I want topics ranked by exam importance, so that I can prioritize my study time effectively.

#### Acceptance Criteria

1. THE Relevance_Analyzer SHALL assign an integer Priority_Score between 1 and 10 (inclusive) to every identified topic, where 10 indicates highest exam relevance
2. WHEN assigning Priority_Scores, THE Relevance_Analyzer SHALL use the official exam domain percentage allocations (15–20%, 20–25%, 10–15%, 15–20%, 15–20%, 10–15%) such that topics belonging to higher-weighted domains receive proportionally higher base scores before cross-domain adjustments
3. WHEN a topic appears in more than one exam domain, THE Relevance_Analyzer SHALL increase that topic's Priority_Score by 1 point for each additional domain in which it appears, up to the maximum score of 10
4. THE Relevance_Analyzer SHALL produce a sorted list of topics from highest to lowest Priority_Score, with ties broken by the number of exam domains in which the topic appears, then alphabetically by topic name
5. WHEN a topic has a Priority_Score of 8 or higher, THE Relevance_Analyzer SHALL flag the topic as "high-priority" in the sorted output list

### Requirement 4: Comprehensive Study Notes

**User Story:** As a certification candidate, I want detailed study notes for every topic, so that I have a complete reference for deep understanding.

#### Acceptance Criteria

1. THE Study_Notes_Generator SHALL produce study notes for every topic identified in the topic map
2. THE Study_Notes_Generator SHALL structure each topic's notes with the following sections: overview (minimum 3 sentences), explanation (minimum 200 words), key facts (minimum 3 items), common mistakes (minimum 2 items), examples (minimum 1 per topic), and exam tips (minimum 1 per topic)
3. WHEN a topic involves a procedure or workflow, THE Study_Notes_Generator SHALL include step-by-step instructions with rationale for each step
4. WHEN a topic involves configuration or code, THE Study_Notes_Generator SHALL include at least one code block with a language identifier and inline comments explaining key lines
5. THE Study_Notes_Generator SHALL connect related concepts across different exam domains using cross-reference links that resolve to existing topic headings in the generated notes
6. WHEN fewer than 3 distinct knowledge points can be extracted from source material for a topic, THE Study_Notes_Generator SHALL supplement with inferred explanation and mark each supplemented paragraph with a visual indicator distinguishing it from source-derived content
7. WHEN a topic has a Priority_Score of 8 or higher, THE Study_Notes_Generator SHALL include at least 2 examples and expand the explanation section to a minimum of 400 words

### Requirement 5: Structured Learning Course

**User Story:** As a certification candidate, I want a complete curriculum with modules, objectives, and time estimates, so that I can plan my study schedule.

#### Acceptance Criteria

1. THE Curriculum_Builder SHALL organize the study material into sequential modules that respect the prerequisite learning order established by the Topic_Mapper
2. THE Curriculum_Builder SHALL specify between 2 and 7 learning objectives for each module using measurable action verbs from Bloom's Taxonomy (e.g., define, explain, implement, evaluate, compare)
3. THE Curriculum_Builder SHALL list prerequisites for each module referencing other modules in the curriculum by module identifier, or explicitly state "none" if the module has no prerequisites
4. THE Curriculum_Builder SHALL provide a study time estimate in minutes for each module, with each estimate between 15 and 180 minutes
5. THE Curriculum_Builder SHALL produce a total study time estimate for the complete curriculum expressed as a sum of all individual module time estimates
6. WHEN a module covers high-priority topics (Priority_Score 8 or higher), THE Curriculum_Builder SHALL assign that module a study time estimate of at least 1.5 times the average study time of modules containing no high-priority topics

### Requirement 6: Revision Resources

**User Story:** As a certification candidate, I want condensed revision materials including summaries, cheat sheets, flashcards, and mnemonics, so that I can efficiently review before the exam.

#### Acceptance Criteria

1. THE Revision_Generator SHALL produce an executive summary of no more than 2000 words covering all six exam domains
2. THE Revision_Generator SHALL produce a cheat sheet containing key formulas, patterns, commands, and quick-reference tables organized by exam domain, with at least one table per domain
3. THE Revision_Generator SHALL produce flashcards in question-and-answer format for every key concept, with a minimum of 100 flashcards total distributed across all six exam domains
4. THE Revision_Generator SHALL produce mnemonic devices for complex topics that involve three or more sequential steps or components
5. WHEN generating flashcards, THE Revision_Generator SHALL tag each flashcard with the relevant exam domain name and the topic's Priority_Score
6. THE Revision_Generator SHALL format each flashcard with a "Q:" prefix for the question and an "A:" prefix for the answer, separated by a blank line, to support spaced repetition study methods

### Requirement 7: Practice Questions

**User Story:** As a certification candidate, I want practice questions at multiple difficulty levels with detailed explanations, so that I can test my understanding progressively.

#### Acceptance Criteria

1. THE Question_Generator SHALL produce practice questions at three difficulty levels: easy (single concept recall or definition), intermediate (applying a concept to a specific situation), and advanced (analyzing a scenario requiring knowledge from two or more topics)
2. THE Question_Generator SHALL produce a minimum of 20 questions per difficulty level, distributed across all six exam domains proportionally to their official percentage weights
3. THE Question_Generator SHALL provide a correct answer and an explanation for every practice question, where the explanation includes the reasoning for the correct answer, the relevant concept or rule, and a reference to the corresponding study notes section
4. THE Question_Generator SHALL tag each question with the relevant exam domain and topic
5. WHEN generating advanced-level questions, THE Question_Generator SHALL include scenario-based questions for at least 50% of the advanced-level set, where each scenario requires applying knowledge across two or more topics
6. THE Question_Generator SHALL include questions in the same format as the actual GH-600 exam: multiple choice (4 options, single correct answer), multiple select (4 to 6 options, 2 or more correct answers), and scenario-based (a situational prompt followed by a question with 4 options)
7. IF a question has multiple plausible answers, THEN THE Question_Generator SHALL explain why each incorrect answer is wrong in the explanation

### Requirement 8: Mock Exam

**User Story:** As a certification candidate, I want a realistic mock exam with detailed solutions and grading, so that I can simulate the actual exam experience.

#### Acceptance Criteria

1. THE Mock_Exam_Builder SHALL produce a mock exam containing a minimum of 50 questions
2. THE Mock_Exam_Builder SHALL distribute questions across exam domains proportionally to the official percentage weights, with each domain's question count within ±5 percentage points of its target weight
3. THE Mock_Exam_Builder SHALL produce an answer key with the correct answer for every question
4. THE Mock_Exam_Builder SHALL produce a solution for every answer that includes the correct reasoning, an explanation of why each incorrect option is wrong, and identification of the exam domain and topic tested
5. THE Mock_Exam_Builder SHALL produce a grading rubric that awards one point per question for single-answer questions and awards full credit only when all correct options are selected for multiple-select questions, calculates a percentage score, and maps the result to a pass/fail outcome using the 700/1000 threshold
6. THE Mock_Exam_Builder SHALL include a minimum of three question formats (multiple choice, multiple select, and scenario-based), with each format representing no fewer than 15% of the total question count
7. WHEN a mock exam question tests a high-priority topic (Priority_Score of 8 or higher), THE Mock_Exam_Builder SHALL include a cross-reference link to the relevant study notes section in the solution
8. THE Mock_Exam_Builder SHALL specify a recommended time limit for completing the mock exam, stated in minutes, based on the official GH-600 exam duration

### Requirement 9: Knowledge Gap Analysis

**User Story:** As a certification candidate, I want to identify gaps in coverage and areas needing additional study, so that I can address weaknesses before the exam.

#### Acceptance Criteria

1. THE Gap_Analyzer SHALL compare the generated study material against all official exam objectives listed in the GH-600 study guide and produce a coverage report listing each objective with a coverage status (fully covered, weakly covered, or not covered) and the count of distinct knowledge points extracted
2. THE Gap_Analyzer SHALL identify exam objectives that are weakly covered (fewer than 3 distinct knowledge points extracted)
3. THE Gap_Analyzer SHALL identify exam objectives where source material yielded zero knowledge points or where the source document was inaccessible during ingestion
4. THE Gap_Analyzer SHALL recommend at least 2 additional resources or study approaches for each identified gap, specifying the topic area each recommendation addresses
5. WHEN a gap is identified in a high-priority topic (Priority_Score 8 or higher), THE Gap_Analyzer SHALL flag the gap as critical, place it in a dedicated "Critical Gaps" section at the top of the gap report, and recommend immediate attention with a suggested study time allocation in minutes

### Requirement 10: Final Readiness Assessment

**User Story:** As a certification candidate, I want a readiness score and actionable last-minute study recommendations, so that I can gauge my preparedness and focus final review.

#### Acceptance Criteria

1. THE Readiness_Assessor SHALL produce a Readiness_Score between 0 and 100 calculated from three equally weighted factors: percentage of exam objectives with complete coverage, percentage of topics with study notes and practice questions generated, and inverse percentage of topics flagged as gaps by the Gap_Analyzer
2. THE Readiness_Assessor SHALL identify high-risk topics as those flagged by the Gap_Analyzer with a Priority_Score of 8 or higher, or topics where fewer than 3 distinct knowledge points were extracted, and list a maximum of 10 high-risk topics ranked by Priority_Score descending
3. THE Readiness_Assessor SHALL produce a prioritized list of no more than 10 last-minute revision areas sorted by the product of exam domain weight percentage and gap severity (number of missing knowledge points per topic)
4. THE Readiness_Assessor SHALL provide a recommended study plan for the final 24 hours before the exam structured as time blocks of 60 minutes each, where each block specifies the topic to review and the recommended resource type (study notes, flashcards, or practice questions)
5. IF the Readiness_Score is below 70, THEN THE Readiness_Assessor SHALL recommend deferring the exam and provide a remediation study plan covering the identified high-risk topics with a target duration in days and specific modules from the curriculum to revisit

### Requirement 11: Output Format and Structure

**User Story:** As a certification candidate, I want the output in well-structured Markdown with clear navigation, so that the material is easy to read and reference.

#### Acceptance Criteria

1. THE Exam_Prep_Generator SHALL produce all output in GitHub Flavored Markdown (GFM) format with valid syntax that renders without errors in a GFM-compatible renderer
2. THE Exam_Prep_Generator SHALL use hierarchical headings (H1 through H4) to organize content, with exactly one H1 per document, heading levels nested sequentially without skipping levels, and each heading uniquely identifiable within its document
3. THE Exam_Prep_Generator SHALL use tables for comparative information and structured data
4. THE Exam_Prep_Generator SHALL use blockquote-based callout blocks (Note, Tip, Warning, Important) for exam tips, warnings, and important notes
5. THE Exam_Prep_Generator SHALL use code blocks with language identifiers for all code examples
6. THE Exam_Prep_Generator SHALL use ordered (numbered) lists for sequential steps and procedures, and unordered (bullet) lists for non-sequential enumerations
7. THE Exam_Prep_Generator SHALL include a master table of contents at the beginning of the output containing anchor links to all H1 and H2 sections across the generated material
8. THE Exam_Prep_Generator SHALL favor completeness over brevity by covering every identified sub-topic with explanation, examples, and exam relevance rather than providing abbreviated summaries

### Requirement 12: Cross-Domain Knowledge Connection

**User Story:** As a certification candidate, I want related concepts connected across exam domains, so that I build integrated understanding rather than siloed knowledge.

#### Acceptance Criteria

1. WHEN a concept appears in 2 or more exam domains, THE Exam_Prep_Generator SHALL document the connection by including cross-reference links between each domain's coverage of that concept
2. THE Exam_Prep_Generator SHALL produce a relationship diagram in Mermaid format showing how concepts with a Priority_Score of 7 or higher relate across exam domains, including at minimum all concepts that appear in 2 or more domains
3. WHEN generating study notes for a topic that shares a prerequisite relationship, overlapping concept, or common workflow with topics in other domains, THE Study_Notes_Generator SHALL include a "Related Topics" section listing at least 1 and no more than 10 connected concepts from other domains, each with the target domain name and a one-sentence explanation of the relationship
4. THE Exam_Prep_Generator SHALL identify themes that span 3 or more exam domains and present each as an integrative summary section containing a theme description, the list of connected domains, and a brief explanation of how the theme manifests in each domain
5. IF a topic has no identified cross-domain connections, THEN THE Study_Notes_Generator SHALL omit the "Related Topics" section for that topic rather than including an empty section

### Requirement 13: Unified Study Website

**User Story:** As a certification candidate, I want all study materials presented as a single navigable website, so that I can access the entire learning resource from one place without switching between files.

#### Acceptance Criteria

1. THE Study_Website SHALL bind all generated phases (study notes, course, revision resources, practice questions, mock exam, gap analysis, readiness assessment) into a single website with consistent layout, styling, and navigation across all sections
2. THE Study_Website SHALL provide a navigation sidebar or menu visible on every page linking to all major sections and sub-sections up to two levels deep
3. THE Study_Website SHALL include a landing page with an overview of the exam, a visual progress tracker layout showing all study phases and their completion status placeholders, and quick links to each study phase
4. THE Study_Website SHALL support client-side full-text search across all study materials and display matching results within 2 seconds of query submission
5. THE Study_Website SHALL render Markdown content with syntax highlighting for code blocks, bordered and aligned tables, visually distinct callout blocks for tips and warnings, and rendered Mermaid diagrams as inline SVG or image output
6. THE Study_Website SHALL render all content readable and navigable without horizontal scrolling on viewports from 320px to 2560px wide
7. THE Study_Website SHALL provide breadcrumb navigation and previous/next page links following the learning order defined by the Curriculum_Builder
8. THE Study_Website SHALL ensure all internal cross-reference links between sections resolve to valid pages within the site

### Requirement 14: GitHub Pages Deployment

**User Story:** As a certification candidate, I want the study website deployed to GitHub Pages, so that I can access the materials from any device with a web browser.

#### Acceptance Criteria

1. THE Exam_Prep_Generator SHALL produce a static site that is deployable to GitHub Pages without a server-side runtime
2. THE Study_Website SHALL use a static site generator compatible with GitHub Pages (such as MkDocs, Jekyll, Hugo, or VitePress)
3. WHEN a commit is pushed to the main branch, THE GitHub Actions workflow SHALL build the static site and deploy it to GitHub Pages, with the workflow definition located in the `.github/workflows/` directory of the repository
4. THE Study_Website SHALL load all pages without HTTP errors and render all navigation links, content sections, tables, code blocks, and Mermaid diagrams when served from a GitHub Pages subpath URL (https://<username>.github.io/<repo-name>/)
5. THE Study_Website SHALL configure the base URL path prefix to match the repository name so that all internal links and asset references resolve correctly when served from a GitHub Pages subpath
6. IF the build or deployment fails, THEN THE GitHub Actions workflow SHALL report the failure in the workflow logs indicating the failing step name and the error cause
7. THE Study_Website SHALL include all assets (styles, scripts, fonts) bundled locally so that the site functions without external CDN dependencies
