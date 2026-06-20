"""Phase 8: Mock Exam Builder.

Assembles a realistic 50+ question mock exam with domain-weighted distribution,
answer key, detailed solutions, grading rubric, and time limit based on the
official GH-600 exam duration.
"""

from __future__ import annotations

import random
from pathlib import Path

from src.config import (
    ARTIFACTS_DIR,
    ARTIFACT_FILENAMES,
    DOMAIN_BY_ID,
    DOMAIN_DISTRIBUTION_TOLERANCE_PP,
    EXAM_DOMAINS,
    HIGH_PRIORITY_THRESHOLD,
    MIN_FORMAT_PROPORTION,
    MIN_MOCK_EXAM_QUESTIONS,
    PASS_THRESHOLD_MAX,
    PASS_THRESHOLD_SCORE,
)
from src.models.mock_exam import GradingRubric, MockExam
from src.models.questions import Question, QuestionBank, QuestionFormat
from src.models.scoring import ScoredTopic, ScoredTopicList


class MockExamBuilder:
    """Phase 8: Assembles a realistic mock exam from the question bank.

    Selects 50+ questions with domain distribution within ±5pp of target
    weights, ensures each format (MC, MS, scenario) is ≥15% of total,
    and produces a grading rubric with 700/1000 pass threshold.
    """

    def __init__(self) -> None:
        """Initialize the MockExamBuilder."""
        pass

    def build(
        self, question_bank: QuestionBank, scores: ScoredTopicList
    ) -> MockExam:
        """Build a mock exam from the question bank and scores.

        Selects questions, builds answer key, solutions, grading rubric,
        and calculates time limit.

        Args:
            question_bank: QuestionBank from Phase 7.
            scores: ScoredTopicList from Phase 3.

        Returns:
            A complete MockExam ready for practice.
        """
        self._score_map: dict[str, ScoredTopic] = {
            st.topic_id: st for st in scores.topics
        }

        # Pool all available questions
        all_questions = (
            question_bank.easy
            + question_bank.intermediate
            + question_bank.advanced
        )

        # Select questions meeting distribution constraints
        selected = self._select_questions(all_questions)

        # Build answer key
        answer_key = self._build_answer_key(selected)

        # Build solutions with cross-references for high-priority topics
        solutions = self._build_solutions(selected)

        # Build grading rubric
        grading_rubric = self._build_grading_rubric(selected)

        # Calculate time limit
        time_limit = self._calculate_time_limit()

        # Compute distributions
        domain_distribution = self._compute_domain_distribution(selected)
        format_distribution = self._compute_format_distribution(selected)

        exam = MockExam(
            questions=selected,
            answer_key=answer_key,
            solutions=solutions,
            grading_rubric=grading_rubric,
            time_limit_minutes=time_limit,
            domain_distribution=domain_distribution,
            format_distribution=format_distribution,
        )

        # Write artifact to disk
        self._write_artifact(exam)

        return exam

    def _select_questions(
        self, all_questions: list[Question]
    ) -> list[Question]:
        """Select 50+ questions with domain and format distribution constraints.

        Domain distribution must be within ±5pp of target weights.
        Each format (MC, MS, scenario) must be ≥15% of total questions.

        Args:
            all_questions: The full pool of available questions.

        Returns:
            A list of selected Question objects (minimum 50).
        """
        # Determine target count: use MIN_MOCK_EXAM_QUESTIONS as target
        # to leave room for domain distribution optimization.
        # If fewer questions are available, use all of them.
        target_count = min(MIN_MOCK_EXAM_QUESTIONS, len(all_questions))

        # Calculate target questions per domain based on weights
        domain_targets = self._compute_domain_targets(target_count)

        # Calculate minimum per format (≥15%)
        min_per_format = max(1, int(target_count * MIN_FORMAT_PROPORTION))

        # Group available questions by domain
        questions_by_domain: dict[str, list[Question]] = {}
        for domain in EXAM_DOMAINS:
            questions_by_domain[domain.id] = []
        for q in all_questions:
            if q.domain_id not in questions_by_domain:
                questions_by_domain[q.domain_id] = []
            questions_by_domain[q.domain_id].append(q)

        # Group available questions by format
        questions_by_format: dict[str, list[Question]] = {
            QuestionFormat.MULTIPLE_CHOICE.value: [],
            QuestionFormat.MULTIPLE_SELECT.value: [],
            QuestionFormat.SCENARIO_BASED.value: [],
        }
        for q in all_questions:
            questions_by_format[q.format.value].append(q)

        # Selection strategy:
        # 1. First ensure minimum format representation
        # 2. Then fill domain targets within tolerance

        selected: list[Question] = []
        selected_ids: set[str] = set()

        # Step 1: Ensure format minimums are met
        for fmt, fmt_questions in questions_by_format.items():
            # Shuffle for variety
            shuffled = list(fmt_questions)
            random.shuffle(shuffled)
            count_needed = min_per_format
            for q in shuffled:
                if q.id not in selected_ids and count_needed > 0:
                    selected.append(q)
                    selected_ids.add(q.id)
                    count_needed -= 1
                if count_needed <= 0:
                    break

        # Step 2: Fill remaining slots respecting domain targets
        remaining_target = target_count - len(selected)
        if remaining_target > 0:
            # Determine current domain counts
            current_domain_counts: dict[str, int] = {}
            for q in selected:
                current_domain_counts[q.domain_id] = (
                    current_domain_counts.get(q.domain_id, 0) + 1
                )

            # Calculate how many more questions each domain needs
            domain_deficit: dict[str, int] = {}
            for domain_id, target in domain_targets.items():
                current = current_domain_counts.get(domain_id, 0)
                deficit = max(0, target - current)
                domain_deficit[domain_id] = deficit

            # Fill domains with highest deficit first
            for domain_id in sorted(
                domain_deficit, key=lambda d: domain_deficit[d], reverse=True
            ):
                if remaining_target <= 0:
                    break
                deficit = domain_deficit[domain_id]
                available = [
                    q
                    for q in questions_by_domain.get(domain_id, [])
                    if q.id not in selected_ids
                ]
                random.shuffle(available)
                to_add = min(deficit, remaining_target, len(available))
                for q in available[:to_add]:
                    selected.append(q)
                    selected_ids.add(q.id)
                    remaining_target -= 1

        # Step 3: If still below target, add remaining questions
        if len(selected) < target_count:
            remaining = [q for q in all_questions if q.id not in selected_ids]
            random.shuffle(remaining)
            needed = target_count - len(selected)
            for q in remaining[:needed]:
                selected.append(q)
                selected_ids.add(q.id)

        # Step 4: Verify format constraint is still met; if not, swap
        selected = self._enforce_format_minimums(
            selected, all_questions, selected_ids, min_per_format
        )

        # Step 5: Enforce domain distribution within ±5pp tolerance
        selected = self._enforce_domain_distribution(
            selected, all_questions, selected_ids
        )

        return selected

    def _enforce_format_minimums(
        self,
        selected: list[Question],
        all_questions: list[Question],
        selected_ids: set[str],
        min_per_format: int,
    ) -> list[Question]:
        """Ensure each format meets the minimum proportion after selection.

        If a format is underrepresented, swap in questions of that format
        from the pool (replacing questions from overrepresented formats).

        Args:
            selected: Currently selected questions.
            all_questions: Full question pool.
            selected_ids: IDs already selected.
            min_per_format: Minimum questions per format.

        Returns:
            Adjusted list meeting format constraints.
        """
        format_counts = self._count_by_format(selected)

        for fmt in [
            QuestionFormat.MULTIPLE_CHOICE.value,
            QuestionFormat.MULTIPLE_SELECT.value,
            QuestionFormat.SCENARIO_BASED.value,
        ]:
            while format_counts.get(fmt, 0) < min_per_format:
                # Find a question of this format not yet selected
                candidate = None
                for q in all_questions:
                    if q.id not in selected_ids and q.format.value == fmt:
                        candidate = q
                        break

                if candidate is None:
                    # No more available questions of this format
                    break

                # Find overrepresented format to swap out from
                over_fmt = max(
                    format_counts, key=lambda f: format_counts.get(f, 0)
                )
                if format_counts.get(over_fmt, 0) <= min_per_format:
                    # All formats are at minimum, just add
                    selected.append(candidate)
                    selected_ids.add(candidate.id)
                    format_counts[fmt] = format_counts.get(fmt, 0) + 1
                    break

                # Remove one question of the overrepresented format
                for i, q in enumerate(selected):
                    if q.format.value == over_fmt:
                        selected_ids.discard(q.id)
                        selected.pop(i)
                        format_counts[over_fmt] -= 1
                        break

                # Add the candidate
                selected.append(candidate)
                selected_ids.add(candidate.id)
                format_counts[fmt] = format_counts.get(fmt, 0) + 1

        return selected

    def _enforce_domain_distribution(
        self,
        selected: list[Question],
        all_questions: list[Question],
        selected_ids: set[str],
    ) -> list[Question]:
        """Ensure each domain is within ±5pp of its target weight.

        After all selection steps, checks domain percentages against targets.
        If any domain is outside tolerance, swaps questions from over-represented
        domains with unused questions from under-represented domains.

        Args:
            selected: Currently selected questions.
            all_questions: Full question pool.
            selected_ids: IDs already selected.

        Returns:
            Adjusted list meeting domain distribution constraints.
        """
        total = len(selected)
        if total == 0:
            return selected

        # Compute normalized target percentages
        total_weight = sum(
            (d.weight_min + d.weight_max) / 2 for d in EXAM_DOMAINS
        )
        domain_target_pct: dict[str, float] = {}
        for domain in EXAM_DOMAINS:
            avg_weight = (domain.weight_min + domain.weight_max) / 2
            domain_target_pct[domain.id] = (avg_weight / total_weight) * 100.0

        # Build index of available (unselected) questions by domain
        available_by_domain: dict[str, list[Question]] = {
            d.id: [] for d in EXAM_DOMAINS
        }
        for q in all_questions:
            if q.id not in selected_ids:
                if q.domain_id in available_by_domain:
                    available_by_domain[q.domain_id].append(q)

        # Iterative adjustment: repeat until convergence or max iterations
        max_iterations = total * len(EXAM_DOMAINS)
        for _ in range(max_iterations):
            total = len(selected)
            if total == 0:
                break

            # Count current domain distribution
            domain_counts: dict[str, int] = {d.id: 0 for d in EXAM_DOMAINS}
            for q in selected:
                domain_counts[q.domain_id] = domain_counts.get(q.domain_id, 0) + 1

            # Find domains outside tolerance
            over_domains: list[tuple[str, float]] = []  # (domain_id, deviation)
            under_domains: list[tuple[str, float]] = []  # (domain_id, deviation)

            for domain in EXAM_DOMAINS:
                actual_pct = (domain_counts[domain.id] / total) * 100.0
                target_pct = domain_target_pct[domain.id]
                deviation = actual_pct - target_pct

                if deviation > DOMAIN_DISTRIBUTION_TOLERANCE_PP:
                    over_domains.append((domain.id, deviation))
                elif deviation < -DOMAIN_DISTRIBUTION_TOLERANCE_PP:
                    under_domains.append((domain.id, deviation))

            # If all domains are within tolerance, we're done
            if not over_domains or not under_domains:
                break

            # Sort: most over-represented first, most under-represented first
            over_domains.sort(key=lambda x: x[1], reverse=True)
            under_domains.sort(key=lambda x: x[1])

            # Try to swap one question from over to under
            swapped = False
            for over_id, _ in over_domains:
                if swapped:
                    break
                for under_id, _ in under_domains:
                    # Find a candidate from the available pool in under domain
                    if not available_by_domain[under_id]:
                        continue

                    # Find a question to remove from over domain in selected
                    remove_idx = None
                    for i, q in enumerate(selected):
                        if q.domain_id == over_id:
                            remove_idx = i
                            break

                    if remove_idx is None:
                        continue

                    # Perform the swap
                    removed_q = selected.pop(remove_idx)
                    selected_ids.discard(removed_q.id)

                    # Add the removed question back to available pool
                    available_by_domain[over_id].append(removed_q)

                    # Pick a question from the under-represented domain
                    new_q = available_by_domain[under_id].pop(0)
                    selected.append(new_q)
                    selected_ids.add(new_q.id)

                    swapped = True
                    break

            if not swapped:
                # No more swaps possible
                break

        return selected

    def _compute_domain_targets(
        self, total_count: int
    ) -> dict[str, int]:
        """Compute target question count per domain based on weights.

        Each domain gets questions proportional to its average weight.

        Args:
            total_count: Total number of questions to distribute.

        Returns:
            Dictionary mapping domain_id to target question count.
        """
        targets: dict[str, int] = {}
        total_weight = sum(
            (d.weight_min + d.weight_max) / 2 for d in EXAM_DOMAINS
        )

        allocated = 0
        for domain in EXAM_DOMAINS:
            avg_weight = (domain.weight_min + domain.weight_max) / 2
            proportion = avg_weight / total_weight if total_weight > 0 else 1 / 6
            target = max(1, round(total_count * proportion))
            targets[domain.id] = target
            allocated += target

        # Adjust over/under-allocation
        diff = allocated - total_count
        if diff > 0:
            sorted_domains = sorted(
                EXAM_DOMAINS, key=lambda d: (d.weight_min + d.weight_max) / 2
            )
            for domain in sorted_domains:
                if diff <= 0:
                    break
                if targets[domain.id] > 1:
                    targets[domain.id] -= 1
                    diff -= 1
        elif diff < 0:
            sorted_domains = sorted(
                EXAM_DOMAINS,
                key=lambda d: (d.weight_min + d.weight_max) / 2,
                reverse=True,
            )
            for domain in sorted_domains:
                if diff >= 0:
                    break
                targets[domain.id] += 1
                diff += 1

        return targets

    def _build_answer_key(
        self, questions: list[Question]
    ) -> dict[str, list[str]]:
        """Build the answer key mapping question IDs to correct answer IDs.

        Args:
            questions: The selected mock exam questions.

        Returns:
            Dictionary mapping question_id to list of correct option IDs.
        """
        return {q.id: q.correct_answer_ids for q in questions}

    def _build_solutions(
        self, questions: list[Question]
    ) -> list[dict]:
        """Build detailed solutions for each question.

        High-priority topic solutions include cross-reference links
        to the relevant study notes section.

        Args:
            questions: The selected mock exam questions.

        Returns:
            List of solution dictionaries with reasoning, explanations,
            domain, topic, and optional study notes cross-references.
        """
        solutions: list[dict] = []

        for q in questions:
            # Check if any topic in this question is high-priority
            is_high_priority = self._question_has_high_priority_topic(q)

            solution: dict = {
                "question_id": q.id,
                "reasoning": q.explanation,
                "incorrect_explanations": q.incorrect_explanations,
                "domain": q.domain_id,
                "topic": q.topic_ids[0] if q.topic_ids else "",
            }

            # Add cross-reference links for high-priority topics (Req 8.7)
            if is_high_priority:
                cross_refs = self._build_study_notes_cross_references(q)
                solution["study_notes_references"] = cross_refs

            solutions.append(solution)

        return solutions

    def _question_has_high_priority_topic(self, question: Question) -> bool:
        """Check if a question tests any high-priority topic.

        Args:
            question: The question to check.

        Returns:
            True if any topic_id in the question has priority >= 8.
        """
        for topic_id in question.topic_ids:
            scored = self._score_map.get(topic_id)
            if scored and scored.priority_score >= HIGH_PRIORITY_THRESHOLD:
                return True
        return False

    def _build_study_notes_cross_references(
        self, question: Question
    ) -> list[str]:
        """Build cross-reference links to study notes for a question.

        Creates references linking to the study notes sections for
        each high-priority topic tested in the question.

        Args:
            question: The question to build references for.

        Returns:
            List of cross-reference link strings.
        """
        refs: list[str] = []
        for topic_id in question.topic_ids:
            scored = self._score_map.get(topic_id)
            if scored and scored.priority_score >= HIGH_PRIORITY_THRESHOLD:
                domain_name = self._get_domain_name(question.domain_id)
                refs.append(
                    f"See study notes: {scored.topic_name} "
                    f"(Domain: {domain_name}, Priority: {scored.priority_score})"
                )
        return refs

    def _build_grading_rubric(
        self, questions: list[Question]
    ) -> GradingRubric:
        """Build the grading rubric for the mock exam.

        Awards 1 point per single-answer question. Multi-select questions
        use all-or-nothing scoring (full credit only when all correct
        options are selected). Pass threshold is 700/1000.

        Args:
            questions: The selected mock exam questions.

        Returns:
            A GradingRubric instance.
        """
        total_questions = len(questions)

        # Each question is worth equal points, scaled to max_score of 1000
        # points_per_single_answer = 1 (per the requirement)
        # max_score is total_questions (each worth 1 point raw)
        # but we report pass_threshold relative to 1000
        max_score = PASS_THRESHOLD_MAX
        pass_threshold = PASS_THRESHOLD_SCORE
        pass_percentage = pass_threshold / max_score  # 0.70

        return GradingRubric(
            total_questions=total_questions,
            points_per_single_answer=1,
            multi_select_scoring="all or nothing",
            max_score=max_score,
            pass_threshold=pass_threshold,
            pass_percentage=pass_percentage,
        )

    def _calculate_time_limit(self) -> int:
        """Calculate the recommended time limit based on official GH-600 exam duration.

        The official GitHub certification exams typically allow 120 minutes.
        This mirrors that duration for the mock exam.

        Returns:
            Time limit in minutes.
        """
        # Official GH-600 exam duration is 120 minutes
        return 120

    # --- Helper methods ---

    def _count_by_format(
        self, questions: list[Question]
    ) -> dict[str, int]:
        """Count questions by format.

        Args:
            questions: List of questions to count.

        Returns:
            Dictionary mapping format value to count.
        """
        counts: dict[str, int] = {}
        for q in questions:
            counts[q.format.value] = counts.get(q.format.value, 0) + 1
        return counts

    def _compute_domain_distribution(
        self, questions: list[Question]
    ) -> dict[str, int]:
        """Compute the domain distribution of selected questions.

        Args:
            questions: The selected questions.

        Returns:
            Dictionary mapping domain_id to count.
        """
        distribution: dict[str, int] = {}
        for q in questions:
            distribution[q.domain_id] = distribution.get(q.domain_id, 0) + 1
        return distribution

    def _compute_format_distribution(
        self, questions: list[Question]
    ) -> dict[str, int]:
        """Compute the format distribution of selected questions.

        Args:
            questions: The selected questions.

        Returns:
            Dictionary mapping format name to count.
        """
        distribution: dict[str, int] = {}
        for q in questions:
            distribution[q.format.value] = (
                distribution.get(q.format.value, 0) + 1
            )
        return distribution

    def _get_domain_name(self, domain_id: str) -> str:
        """Look up the human-readable domain name.

        Args:
            domain_id: The domain identifier.

        Returns:
            The domain name, or the domain_id if not found.
        """
        domain = DOMAIN_BY_ID.get(domain_id)
        if domain:
            return domain.name
        return domain_id

    def _write_artifact(self, exam: MockExam) -> None:
        """Write the MockExam to the artifacts directory.

        Creates the artifacts directory if it doesn't exist.
        Writes the result as JSON to phase08_mock_exam.json.

        Args:
            exam: The mock exam to persist.
        """
        artifacts_path = Path(ARTIFACTS_DIR)
        artifacts_path.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_path / ARTIFACT_FILENAMES["phase08"]
        output_path.write_text(
            exam.model_dump_json(indent=2),
            encoding="utf-8",
        )

    @classmethod
    def from_artifacts(
        cls,
        questions_path: str | None = None,
        scores_path: str | None = None,
    ) -> MockExam:
        """Load from Phase 7 and Phase 3 artifact files and build mock exam.

        Reads the question bank and scored topic list from disk,
        then assembles the mock exam.

        Args:
            questions_path: Path to phase07_questions.json.
                Defaults to artifacts/phase07_questions.json.
            scores_path: Path to phase03_scores.json.
                Defaults to artifacts/phase03_scores.json.

        Returns:
            The assembled MockExam.
        """
        if questions_path is None:
            questions_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase07"]
            )
        if scores_path is None:
            scores_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase03"]
            )

        question_bank = QuestionBank.model_validate_json(
            Path(questions_path).read_text(encoding="utf-8")
        )
        scores = ScoredTopicList.model_validate_json(
            Path(scores_path).read_text(encoding="utf-8")
        )

        builder = cls()
        return builder.build(question_bank, scores)
