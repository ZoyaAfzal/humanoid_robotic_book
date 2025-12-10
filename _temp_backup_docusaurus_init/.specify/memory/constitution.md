<!-- Sync Impact Report:
Version change: None -> 1.0.0
List of modified principles:
  - I. Content Accuracy & Citation (Added)
  - II. Structured Markdown Format (Added)
  - III. Educational Content & Exercises (Added)
  - IV. Safety & Ethics Compliance (Added)
  - V. Readability & Consistency (Added)
  - VI. Scope Adherence (Added)
Added sections:
  - Constraints & Technical Standards
  - Quality & Review Process
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated
  - .specify/templates/spec-template.md: ✅ updated
  - .specify/templates/tasks-template.md: ✅ updated
  - .specify/templates/commands/sp.git.commit_pr.md: ✅ updated
  - .specify/templates/commands/sp.constitution.md: ✅ updated
  - .specify/templates/commands/sp.clarify.md: ✅ updated
  - .specify/templates/commands/sp.plan.md: ✅ updated
  - .specify/templates/commands/sp.phr.md: ✅ updated
  - .specify/templates/commands/sp.implement.md: ✅ updated
  - .specify/templates/commands/sp.specify.md: ✅ updated
  - .specify/templates/commands/sp.tasks.md: ✅ updated
  - .specify/templates/commands/sp.adr.md: ✅ updated
  - .specify/templates/commands/sp.analyze.md: ✅ updated
  - .specify/templates/commands/sp.checklist.md: ✅ updated
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Content Accuracy & Citation
All factual claims, theoretical derivations, and design examples MUST be backed by citations (≥60% from peer-reviewed textbooks or academic publications such as IEEE, Springer, ACM). All content MUST be original or properly quoted/attributed with APA-style citations. No plagiarism is permitted.

### II. Structured Markdown Format
The textbook MUST be delivered as a single structured Markdown project. Content MUST adhere to Markdown formatting (headings, code blocks, image references for diagrams, tables). Diagrams MUST use placeholders: `![Figure X: Description](path/to/figureX.png)`.

### III. Educational Content & Exercises
Each chapter MUST include learning objectives, theory sections, real-world examples/applications, diagrams or illustrations (Markdown placeholders), at least one lab or hands-on exercise (code or physical robot/simulation), and 5–10 review questions. Code or pseudocode examples MUST be syntactically correct, logically consistent, and include explanatory commentary, using standard, widely accessible tools (Python + open-source robotics/simulation libraries).

### IV. Safety & Ethics Compliance
Safety, ethics, and human-robot interaction sections MUST comply with modern robotics standards and cite relevant norms. The textbook MUST include at least one dedicated chapter or integrated sections on safe robotics practice, HRI ethics, privacy, and misuse prevention.

### V. Readability & Consistency
The textbook MUST be written at an undergraduate-accessible reading level, characterized by clear prose, minimal jargon, and a consistent style. Content MUST be structured Markdown with headings, subheadings, bullet lists, code blocks, figure placeholders, and tables.

### VI. Scope Adherence
The content MUST focus on foundational and core aspects of Physical AI & Humanoid Robotics. It MUST NOT include industrial-scale robot deployment, proprietary hardware designs, vendor-specific tools, detailed manufacturing instructions, hardware procurement guidance, or proprietary licensing. The textbook is NOT a comprehensive research monograph; it focuses on core fundamentals for course use.

## Constraints & Technical Standards

*   **Format:** Markdown only (headings, code blocks, image references for diagrams, tables if needed).
*   **Scope:** Foundational and core aspects of Physical AI & Humanoid Robotics. No industrial-scale robot deployment, proprietary hardware designs, or vendor-specific tools.
*   **Diagrams:** Use placeholders: `![Figure X: Description](path/to/figureX.png)`.
*   **Code examples:** Standard, widely accessible tools (Python + open-source robotics/simulation libraries).
*   **Timeline:** Full draft (all chapters with placeholders) should be conceptually completable in a single `/sp.specify` + subsequent plan/tasks.

## Quality & Review Process

*   Reviewer (robotics instructor or domain expert) MUST be able to follow course flow and clearly see theory + exercises.
*   Diagram placeholders MUST be clearly labeled for later inclusion.
*   All chapters MUST meet uniform structure (objectives, theory, examples, lab/exercise, questions).
*   Citations and references MUST be included; peer-reviewed/authoritative source proportion MUST be ≥ 60%.
*   Code/pseudocode blocks MUST be syntactically valid and logically coherent.
*   Safety/ethics coverage MUST be present, with at least one dedicated chapter or integrated sections on safe robotics practice, HRI ethics, privacy, and misuse prevention.
*   Glossary MUST include ≥50 key terms relevant to Physical AI & Humanoid Robotics.
*   Index MUST cover major topics, terms, and figures.

## Governance

This Constitution supersedes all other project practices. Amendments require documentation, approval, and a migration plan. All Pull Requests (PRs) and reviews MUST verify compliance with these principles. Complexity in any proposed solution MUST be justified.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
