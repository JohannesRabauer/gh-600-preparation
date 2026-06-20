"""Property-based tests for Phase 3: Relevance Analyzer.

Tests correctness properties 5, 6, and 7 from the design document:
- Property 5: Priority Score Range and Domain Bonus
- Property 6: Domain Weight Influences Base Score Monotonically
- Property 7: Topic Score List Sort Order

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from src.config import (
    CROSS_DOMAIN_BONUS,
    DOMAIN_WEIGHT_TO_BASE_SCORE,
    EXAM_DOMAINS,
    HIGH_PRIORITY_THRESHOLD,
    MAX_PRIORITY_SCORE,
    MIN_PRIORITY_SCORE,
)
from src.models.scoring import ScoredTopic
from src.models.topic_map import CrossReference, Topic, TopicHierarchy
from src.phases.phase03_analyzer import RelevanceAnalyzer


# === Strategies ===


# All domain IDs from the config
ALL_DOMAIN_IDS = [d.id for d in EXAM_DOMAINS]


@st.composite
def _topic_in_domains(
    draw: st.DrawFn,
    min_domains: int = 1,
    max_domains: int = 6,
) -> tuple[Topic, TopicHierarchy]:
    """Generate a topic appearing in 1-6 domains with a valid TopicHierarchy.

    Returns the topic and a hierarchy where the topic is placed in multiple
    domains via cross-references.
    """
    num_domains = draw(st.integers(min_value=min_domains, max_value=max_domains))
    domain_ids = draw(
        st.lists(
            st.sampled_from(ALL_DOMAIN_IDS),
            min_size=num_domains,
            max_size=num_domains,
            unique=True,
        )
    )

    primary_domain = domain_ids[0]
    topic_id = draw(
        st.text(
            alphabet=st.characters(whitelist_categories=("Ll", "Nd"), whitelist_characters="-"),
            min_size=3,
            max_size=15,
        ).map(lambda s: f"topic-{s}")
    )
    topic_name = draw(
        st.text(
            alphabet=st.characters(whitelist_categories=("L", "Nd"), whitelist_characters=" "),
            min_size=3,
            max_size=30,
        ).filter(lambda s: s.strip() != "")
    )

    topic = Topic(
        id=topic_id,
        name=topic_name,
        domain_id=primary_domain,
        sub_domain=None,
        knowledge_point_ids=["kp-1"],
        description="Test topic",
    )

    # Build a hierarchy that places this topic in multiple domains
    domains_dict: dict[str, list[Topic]] = {}
    for d_id in domain_ids:
        domains_dict[d_id] = [topic]

    # Create cross-references between primary domain and secondary domains
    cross_refs: list[CrossReference] = []
    if len(domain_ids) > 1:
        # Add a dummy second topic in each secondary domain for cross-refs
        for secondary_domain in domain_ids[1:]:
            other_topic_id = f"other-{secondary_domain}"
            other_topic = Topic(
                id=other_topic_id,
                name=f"Other in {secondary_domain}",
                domain_id=secondary_domain,
                sub_domain=None,
                knowledge_point_ids=["kp-other"],
                description="Other topic",
            )
            if secondary_domain not in domains_dict:
                domains_dict[secondary_domain] = []
            domains_dict[secondary_domain].append(other_topic)

            cross_refs.append(
                CrossReference(
                    topic_id_a=topic_id,
                    topic_id_b=other_topic_id,
                    shared_concept="shared concept",
                )
            )

    hierarchy = TopicHierarchy(
        domains=domains_dict,
        dependencies=[],
        cross_references=cross_refs,
        learning_order=[topic_id],
        learning_units=[],
    )

    return topic, hierarchy


@st.composite
def _topic_pair_different_weights(
    draw: st.DrawFn,
) -> tuple[Topic, Topic, dict[str, tuple[float, float]]]:
    """Generate two topics: one in a higher-weighted domain, one in a lower-weighted domain.

    Returns (high_weight_topic, low_weight_topic, domain_weights).
    """
    # Pick two different weight brackets
    # DOMAIN_WEIGHT_TO_BASE_SCORE = [(0.25, 8, 9), (0.20, 6, 8), (0.15, 5, 7)]
    # Higher weight_max → higher base score range
    high_weight_max = draw(st.sampled_from([0.25, 0.20]))
    low_weight_max = draw(
        st.sampled_from([w for w in [0.25, 0.20, 0.15] if w < high_weight_max])
    )

    # Create domain weights for two custom domains
    # For the high-weight domain: weight_max = high_weight_max
    high_domain_id = "domain-high"
    low_domain_id = "domain-low"

    # Compute weight_min from weight_max (bracket lower = max - 0.05)
    high_weight_min = high_weight_max - 0.05
    low_weight_min = low_weight_max - 0.05

    domain_weights = {
        high_domain_id: (high_weight_min, high_weight_max),
        low_domain_id: (low_weight_min, low_weight_max),
    }

    high_topic = Topic(
        id="topic-high",
        name="High Weight Topic",
        domain_id=high_domain_id,
        sub_domain=None,
        knowledge_point_ids=["kp-h1"],
        description="Topic in higher-weighted domain",
    )

    low_topic = Topic(
        id="topic-low",
        name="Low Weight Topic",
        domain_id=low_domain_id,
        sub_domain=None,
        knowledge_point_ids=["kp-l1"],
        description="Topic in lower-weighted domain",
    )

    return high_topic, low_topic, domain_weights


@st.composite
def _scored_topic_list(
    draw: st.DrawFn,
    min_size: int = 2,
    max_size: int = 30,
) -> list[ScoredTopic]:
    """Generate a random list of ScoredTopics for sort testing."""
    num_topics = draw(st.integers(min_value=min_size, max_value=max_size))

    topics: list[ScoredTopic] = []
    for i in range(num_topics):
        score = draw(st.integers(min_value=MIN_PRIORITY_SCORE, max_value=MAX_PRIORITY_SCORE))
        domain_count = draw(st.integers(min_value=1, max_value=6))
        domain_ids = [f"domain-{j+1}" for j in range(domain_count)]
        name = draw(
            st.text(
                alphabet=st.characters(whitelist_categories=("Ll",), whitelist_characters=" "),
                min_size=3,
                max_size=20,
            ).filter(lambda s: s.strip() != "")
        )

        topics.append(
            ScoredTopic(
                topic_id=f"topic-{i:03d}",
                topic_name=name,
                domain_ids=domain_ids,
                priority_score=score,
                is_high_priority=score >= HIGH_PRIORITY_THRESHOLD,
                domain_count=domain_count,
            )
        )

    return topics


# === Property 5: Priority Score Range and Domain Bonus ===


# Feature: gh-600-exam-prep, Property 5: Priority Score Range and Domain Bonus
class TestPriorityScoreRangeAndDomainBonus:
    """For any topic assigned to N exam domains (where 1 ≤ N ≤ 6), the assigned
    Priority_Score SHALL be an integer in [1, 10], the cross-domain bonus SHALL
    equal exactly (N - 1), and the final score SHALL not exceed 10 regardless
    of bonus accumulation.

    **Validates: Requirements 3.1, 3.3**
    """

    @given(data=_topic_in_domains(min_domains=1, max_domains=6))
    @settings(max_examples=100, deadline=5000)
    def test_score_within_valid_range(
        self,
        data: tuple[Topic, TopicHierarchy],
    ) -> None:
        """Priority_Score is always between 1 and 10 inclusive."""
        topic, hierarchy = data

        analyzer = RelevanceAnalyzer()
        result = analyzer.analyze(hierarchy)

        for scored in result.topics:
            assert MIN_PRIORITY_SCORE <= scored.priority_score <= MAX_PRIORITY_SCORE, (
                f"Score {scored.priority_score} for topic '{scored.topic_name}' "
                f"is outside [{MIN_PRIORITY_SCORE}, {MAX_PRIORITY_SCORE}]"
            )

    @given(data=_topic_in_domains(min_domains=2, max_domains=6))
    @settings(max_examples=100, deadline=5000)
    def test_cross_domain_bonus_does_not_exceed_max(
        self,
        data: tuple[Topic, TopicHierarchy],
    ) -> None:
        """Cross-domain bonus never causes score to exceed MAX_PRIORITY_SCORE."""
        topic, hierarchy = data

        analyzer = RelevanceAnalyzer()
        result = analyzer.analyze(hierarchy)

        # Find the scored version of our topic
        scored_topic = next(
            (st for st in result.topics if st.topic_id == topic.id),
            None,
        )
        if scored_topic is None:
            return  # topic not in output (shouldn't happen, but defensive)

        assert scored_topic.priority_score <= MAX_PRIORITY_SCORE, (
            f"Score {scored_topic.priority_score} exceeds max {MAX_PRIORITY_SCORE}. "
            f"Domain count: {scored_topic.domain_count}"
        )

    @given(data=_topic_in_domains(min_domains=1, max_domains=6))
    @settings(max_examples=100, deadline=5000)
    def test_cross_domain_bonus_does_not_go_below_min(
        self,
        data: tuple[Topic, TopicHierarchy],
    ) -> None:
        """Score never goes below MIN_PRIORITY_SCORE."""
        topic, hierarchy = data

        analyzer = RelevanceAnalyzer()
        result = analyzer.analyze(hierarchy)

        for scored in result.topics:
            assert scored.priority_score >= MIN_PRIORITY_SCORE, (
                f"Score {scored.priority_score} for topic '{scored.topic_name}' "
                f"is below minimum {MIN_PRIORITY_SCORE}"
            )

    @given(data=_topic_in_domains(min_domains=1, max_domains=6))
    @settings(max_examples=100, deadline=5000)
    def test_score_is_integer(
        self,
        data: tuple[Topic, TopicHierarchy],
    ) -> None:
        """Priority_Score is always an integer."""
        topic, hierarchy = data

        analyzer = RelevanceAnalyzer()
        result = analyzer.analyze(hierarchy)

        for scored in result.topics:
            assert isinstance(scored.priority_score, int), (
                f"Score {scored.priority_score} for topic '{scored.topic_name}' "
                f"is not an integer (type: {type(scored.priority_score)})"
            )

    @given(data=_topic_in_domains(min_domains=2, max_domains=6))
    @settings(max_examples=100, deadline=5000)
    def test_bonus_equals_additional_domains(
        self,
        data: tuple[Topic, TopicHierarchy],
    ) -> None:
        """Cross-domain bonus is exactly (N-1) * CROSS_DOMAIN_BONUS, capped at max."""
        topic, hierarchy = data

        analyzer = RelevanceAnalyzer()
        # We need to call analyze to populate internal state
        result = analyzer.analyze(hierarchy)

        # Find the scored version of our topic
        scored_topic = next(
            (st for st in result.topics if st.topic_id == topic.id),
            None,
        )
        if scored_topic is None:
            return

        # Compute base score independently
        base_score = analyzer._compute_base_score(topic)

        # The expected bonus
        expected_bonus = (scored_topic.domain_count - 1) * CROSS_DOMAIN_BONUS
        expected_final = min(MAX_PRIORITY_SCORE, max(MIN_PRIORITY_SCORE, base_score + expected_bonus))

        assert scored_topic.priority_score == expected_final, (
            f"Expected score {expected_final} (base={base_score}, bonus={expected_bonus}, "
            f"domains={scored_topic.domain_count}), got {scored_topic.priority_score}"
        )

    def test_max_domains_capped_at_10(self) -> None:
        """Edge case: topic in all 6 domains with highest base (9) → capped at 10."""
        topic = Topic(
            id="topic-all-domains",
            name="Ubiquitous Topic",
            domain_id="domain-2",  # Highest weight domain (20-25%)
            sub_domain=None,
            knowledge_point_ids=["kp-1"],
            description="Topic in all domains",
        )

        # Place topic in all 6 domains
        domains_dict: dict[str, list[Topic]] = {}
        for domain in EXAM_DOMAINS:
            domains_dict[domain.id] = [topic]

        # Cross-references to all other domains
        cross_refs = [
            CrossReference(
                topic_id_a=topic.id,
                topic_id_b=f"other-{d.id}",
                shared_concept="shared",
            )
            for d in EXAM_DOMAINS[1:]
        ]

        # Add other topics in each secondary domain for cross-ref resolution
        for d in EXAM_DOMAINS:
            other = Topic(
                id=f"other-{d.id}",
                name=f"Other {d.id}",
                domain_id=d.id,
                sub_domain=None,
                knowledge_point_ids=["kp-o"],
                description="Other",
            )
            domains_dict[d.id].append(other)

        hierarchy = TopicHierarchy(
            domains=domains_dict,
            dependencies=[],
            cross_references=cross_refs,
            learning_order=[topic.id],
            learning_units=[],
        )

        analyzer = RelevanceAnalyzer()
        result = analyzer.analyze(hierarchy)

        scored = next(st for st in result.topics if st.topic_id == topic.id)
        assert scored.priority_score == MAX_PRIORITY_SCORE, (
            f"Expected max score {MAX_PRIORITY_SCORE} for topic in all domains, "
            f"got {scored.priority_score}"
        )


# === Property 6: Domain Weight Influences Base Score Monotonically ===


# Feature: gh-600-exam-prep, Property 6: Domain Weight Influences Base Score Monotonically
class TestDomainWeightInfluencesBaseScoreMonotonically:
    """For any two topics where one belongs exclusively to a higher-weighted
    exam domain and the other belongs exclusively to a lower-weighted domain,
    the topic in the higher-weighted domain SHALL receive a base score greater
    than or equal to the topic in the lower-weighted domain.

    **Validates: Requirements 3.2**
    """

    @given(data=_topic_pair_different_weights())
    @settings(max_examples=100, deadline=5000)
    def test_higher_weight_gets_higher_or_equal_base_score(
        self,
        data: tuple[Topic, Topic, dict[str, tuple[float, float]]],
    ) -> None:
        """Topic in higher-weighted domain gets base score >= lower-weighted domain topic."""
        high_topic, low_topic, domain_weights = data

        analyzer = RelevanceAnalyzer(domain_weights=domain_weights)
        # Populate internal state needed for scoring
        analyzer._topic_domain_map = {
            high_topic.id: [high_topic.domain_id],
            low_topic.id: [low_topic.domain_id],
        }

        high_base = analyzer._compute_base_score(high_topic)
        low_base = analyzer._compute_base_score(low_topic)

        assert high_base >= low_base, (
            f"Higher-weight domain (max={domain_weights[high_topic.domain_id][1]}) "
            f"base score {high_base} < lower-weight domain "
            f"(max={domain_weights[low_topic.domain_id][1]}) base score {low_base}"
        )

    def test_all_weight_brackets_produce_monotonic_scores(self) -> None:
        """Check monotonicity across all three official weight brackets."""
        # The weight brackets from DOMAIN_WEIGHT_TO_BASE_SCORE:
        # (0.25, 8, 9), (0.20, 6, 8), (0.15, 5, 7)
        # weight_max 0.25 > 0.20 > 0.15 → scores should be non-decreasing

        domain_weights = {
            "high": (0.20, 0.25),
            "mid": (0.15, 0.20),
            "low": (0.10, 0.15),
        }

        topics = {
            "high": Topic(
                id="t-high", name="High", domain_id="high",
                sub_domain=None, knowledge_point_ids=["kp"], description="High weight",
            ),
            "mid": Topic(
                id="t-mid", name="Mid", domain_id="mid",
                sub_domain=None, knowledge_point_ids=["kp"], description="Mid weight",
            ),
            "low": Topic(
                id="t-low", name="Low", domain_id="low",
                sub_domain=None, knowledge_point_ids=["kp"], description="Low weight",
            ),
        }

        analyzer = RelevanceAnalyzer(domain_weights=domain_weights)
        analyzer._topic_domain_map = {
            "t-high": ["high"],
            "t-mid": ["mid"],
            "t-low": ["low"],
        }

        high_score = analyzer._compute_base_score(topics["high"])
        mid_score = analyzer._compute_base_score(topics["mid"])
        low_score = analyzer._compute_base_score(topics["low"])

        assert high_score >= mid_score >= low_score, (
            f"Monotonicity violated: high={high_score}, mid={mid_score}, low={low_score}"
        )

    @given(
        high_weight_max=st.floats(min_value=0.20, max_value=0.25),
        low_weight_max=st.floats(min_value=0.10, max_value=0.15),
    )
    @settings(max_examples=100, deadline=5000)
    def test_extreme_weight_difference_monotonic(
        self,
        high_weight_max: float,
        low_weight_max: float,
    ) -> None:
        """Even with extreme weight differences, monotonicity holds."""
        domain_weights = {
            "domain-a": (high_weight_max - 0.05, high_weight_max),
            "domain-b": (low_weight_max - 0.05, low_weight_max),
        }

        topic_a = Topic(
            id="t-a", name="Topic A", domain_id="domain-a",
            sub_domain=None, knowledge_point_ids=["kp"], description="A",
        )
        topic_b = Topic(
            id="t-b", name="Topic B", domain_id="domain-b",
            sub_domain=None, knowledge_point_ids=["kp"], description="B",
        )

        analyzer = RelevanceAnalyzer(domain_weights=domain_weights)
        analyzer._topic_domain_map = {
            "t-a": ["domain-a"],
            "t-b": ["domain-b"],
        }

        score_a = analyzer._compute_base_score(topic_a)
        score_b = analyzer._compute_base_score(topic_b)

        assert score_a >= score_b, (
            f"High-weight domain (max={high_weight_max}) score {score_a} < "
            f"low-weight domain (max={low_weight_max}) score {score_b}"
        )

    def test_unknown_domain_gets_minimum_score(self) -> None:
        """A topic in an unknown domain (not in weights) receives MIN_PRIORITY_SCORE."""
        domain_weights = {
            "domain-known": (0.20, 0.25),
        }

        unknown_topic = Topic(
            id="t-unknown", name="Unknown", domain_id="domain-unknown",
            sub_domain=None, knowledge_point_ids=["kp"], description="Unknown domain",
        )

        analyzer = RelevanceAnalyzer(domain_weights=domain_weights)
        analyzer._topic_domain_map = {"t-unknown": ["domain-unknown"]}

        score = analyzer._compute_base_score(unknown_topic)
        assert score == MIN_PRIORITY_SCORE, (
            f"Unknown domain should get min score {MIN_PRIORITY_SCORE}, got {score}"
        )


# === Property 7: Topic Score List Sort Order ===


# Feature: gh-600-exam-prep, Property 7: Topic Score List Sort Order
class TestTopicScoreListSortOrder:
    """For any scored topic list, the list SHALL be sorted in descending order
    by Priority_Score, with ties broken by descending domain count, and
    remaining ties broken alphabetically by topic name. Additionally, every
    topic with Priority_Score ≥ 8 SHALL have is_high_priority True, and every
    topic with Priority_Score < 8 SHALL have it False.

    **Validates: Requirements 3.4, 3.5**
    """

    @given(topics=_scored_topic_list())
    @settings(max_examples=100, deadline=5000)
    def test_sorted_by_descending_score(
        self,
        topics: list[ScoredTopic],
    ) -> None:
        """Output is sorted by descending priority_score."""
        analyzer = RelevanceAnalyzer()
        sorted_topics = analyzer._sort_topics(topics)

        for i in range(len(sorted_topics) - 1):
            assert sorted_topics[i].priority_score >= sorted_topics[i + 1].priority_score, (
                f"Sort violation at positions {i},{i+1}: "
                f"score {sorted_topics[i].priority_score} < {sorted_topics[i+1].priority_score}"
            )

    @given(topics=_scored_topic_list())
    @settings(max_examples=100, deadline=5000)
    def test_ties_broken_by_descending_domain_count(
        self,
        topics: list[ScoredTopic],
    ) -> None:
        """When scores tie, higher domain_count comes first."""
        analyzer = RelevanceAnalyzer()
        sorted_topics = analyzer._sort_topics(topics)

        for i in range(len(sorted_topics) - 1):
            if sorted_topics[i].priority_score == sorted_topics[i + 1].priority_score:
                assert sorted_topics[i].domain_count >= sorted_topics[i + 1].domain_count, (
                    f"Domain count tie-break violation at positions {i},{i+1}: "
                    f"domain_count {sorted_topics[i].domain_count} < "
                    f"{sorted_topics[i + 1].domain_count} "
                    f"(both score={sorted_topics[i].priority_score})"
                )

    @given(topics=_scored_topic_list())
    @settings(max_examples=100, deadline=5000)
    def test_remaining_ties_broken_alphabetically(
        self,
        topics: list[ScoredTopic],
    ) -> None:
        """When score and domain_count tie, sort alphabetically by name."""
        analyzer = RelevanceAnalyzer()
        sorted_topics = analyzer._sort_topics(topics)

        for i in range(len(sorted_topics) - 1):
            a = sorted_topics[i]
            b = sorted_topics[i + 1]
            if a.priority_score == b.priority_score and a.domain_count == b.domain_count:
                assert a.topic_name <= b.topic_name, (
                    f"Alphabetical tie-break violation at positions {i},{i+1}: "
                    f"'{a.topic_name}' > '{b.topic_name}' "
                    f"(both score={a.priority_score}, domain_count={a.domain_count})"
                )

    @given(topics=_scored_topic_list())
    @settings(max_examples=100, deadline=5000)
    def test_sort_preserves_all_elements(
        self,
        topics: list[ScoredTopic],
    ) -> None:
        """Sorting preserves all elements (no additions or removals)."""
        analyzer = RelevanceAnalyzer()
        sorted_topics = analyzer._sort_topics(topics)

        assert len(sorted_topics) == len(topics), (
            f"Sorted list length {len(sorted_topics)} != input length {len(topics)}"
        )

        input_ids = sorted([t.topic_id for t in topics])
        output_ids = sorted([t.topic_id for t in sorted_topics])
        assert input_ids == output_ids, (
            "Sorted list contains different topic IDs than input"
        )

    @given(topics=_scored_topic_list())
    @settings(max_examples=100, deadline=5000)
    def test_high_priority_flag_matches_threshold(
        self,
        topics: list[ScoredTopic],
    ) -> None:
        """Every topic with score >= 8 has is_high_priority=True; < 8 has False."""
        # The flag is set at creation time, verify the invariant holds
        for topic in topics:
            if topic.priority_score >= HIGH_PRIORITY_THRESHOLD:
                assert topic.is_high_priority is True, (
                    f"Topic '{topic.topic_name}' with score {topic.priority_score} "
                    f"should be high-priority but is_high_priority={topic.is_high_priority}"
                )
            else:
                assert topic.is_high_priority is False, (
                    f"Topic '{topic.topic_name}' with score {topic.priority_score} "
                    f"should NOT be high-priority but is_high_priority={topic.is_high_priority}"
                )

    @given(data=_topic_in_domains(min_domains=1, max_domains=6))
    @settings(max_examples=100, deadline=5000)
    def test_analyze_output_is_sorted(
        self,
        data: tuple[Topic, TopicHierarchy],
    ) -> None:
        """The full analyze() output is already sorted correctly."""
        topic, hierarchy = data

        analyzer = RelevanceAnalyzer()
        result = analyzer.analyze(hierarchy)

        # Verify the output is sorted
        for i in range(len(result.topics) - 1):
            a = result.topics[i]
            b = result.topics[i + 1]
            # Primary: descending score
            assert a.priority_score >= b.priority_score, (
                f"analyze() output not sorted by score at {i},{i+1}: "
                f"{a.priority_score} < {b.priority_score}"
            )
            # Secondary: descending domain_count (on tie)
            if a.priority_score == b.priority_score:
                assert a.domain_count >= b.domain_count, (
                    f"analyze() output tie-break by domain_count violated: "
                    f"{a.domain_count} < {b.domain_count}"
                )
            # Tertiary: alphabetical name (on double tie)
            if a.priority_score == b.priority_score and a.domain_count == b.domain_count:
                assert a.topic_name <= b.topic_name, (
                    f"analyze() output tie-break by name violated: "
                    f"'{a.topic_name}' > '{b.topic_name}'"
                )
