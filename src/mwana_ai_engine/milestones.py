"""Developmental milestone tracking for children 0-60 months.

Based on WHO/CDC developmental milestones adapted for the
Zimbabwean context, covering motor, social, cognitive, and
language domains.
"""

from __future__ import annotations

from .types import MilestoneCheck, MilestoneStatus, MilestoneType


MILESTONES: list[dict] = [
    # 2 months
    {"name": "social_smile", "type": MilestoneType.SOCIAL, "age_months": 2, "description": "Smiles at people"},
    {"name": "coos", "type": MilestoneType.LANGUAGE, "age_months": 2, "description": "Makes cooing sounds"},
    {"name": "lifts_head", "type": MilestoneType.MOTOR, "age_months": 2, "description": "Lifts head when on tummy"},
    # 4 months
    {"name": "laughs", "type": MilestoneType.SOCIAL, "age_months": 4, "description": "Laughs out loud"},
    {"name": "reaches_toys", "type": MilestoneType.MOTOR, "age_months": 4, "description": "Reaches for and grabs toys"},
    {"name": "rolls", "type": MilestoneType.MOTOR, "age_months": 4, "description": "Rolls from tummy to back"},
    # 6 months
    {"name": "sits_with_support", "type": MilestoneType.MOTOR, "age_months": 6, "description": "Sits with support"},
    {"name": "babbles", "type": MilestoneType.LANGUAGE, "age_months": 6, "description": "Babbles (ba-ba, da-da)"},
    {"name": "stranger_anxiety", "type": MilestoneType.SOCIAL, "age_months": 6, "description": "Shows stranger anxiety"},
    # 9 months
    {"name": "sits_alone", "type": MilestoneType.MOTOR, "age_months": 9, "description": "Sits without support"},
    {"name": "crawls", "type": MilestoneType.MOTOR, "age_months": 9, "description": "Crawls or scoots"},
    {"name": "pincer_grasp", "type": MilestoneType.MOTOR, "age_months": 9, "description": "Picks up small objects"},
    {"name": "mama_baba", "type": MilestoneType.LANGUAGE, "age_months": 9, "description": "Says mama or baba"},
    # 12 months
    {"name": "stands", "type": MilestoneType.MOTOR, "age_months": 12, "description": "Pulls to stand, cruises"},
    {"name": "first_words", "type": MilestoneType.LANGUAGE, "age_months": 12, "description": "Says 1-2 words"},
    {"name": "responds_commands", "type": MilestoneType.COGNITIVE, "age_months": 12, "description": "Responds to simple commands"},
    # 18 months
    {"name": "walks_independently", "type": MilestoneType.MOTOR, "age_months": 18, "description": "Walks independently"},
    {"name": "several_words", "type": MilestoneType.LANGUAGE, "age_months": 18, "description": "Says several words"},
    {"name": "points", "type": MilestoneType.SOCIAL, "age_months": 18, "description": "Points to show things"},
    {"name": "scribbles", "type": MilestoneType.MOTOR, "age_months": 18, "description": "Scribbles with crayon"},
    # 24 months
    {"name": "kicks_ball", "type": MilestoneType.MOTOR, "age_months": 24, "description": "Kicks a ball"},
    {"name": "two_word_sentences", "type": MilestoneType.LANGUAGE, "age_months": 24, "description": "Uses 2-4 word sentences"},
    {"name": "stacks_blocks", "type": MilestoneType.MOTOR, "age_months": 24, "description": "Stacks 4+ blocks"},
    {"name": "runs", "type": MilestoneType.MOTOR, "age_months": 24, "description": "Runs"},
    # 36 months
    {"name": "takes_turns", "type": MilestoneType.SOCIAL, "age_months": 36, "description": "Takes turns in play"},
    {"name": "dresses_self", "type": MilestoneType.MOTOR, "age_months": 36, "description": "Dresses self with help"},
    {"name": "walks_stairs", "type": MilestoneType.MOTOR, "age_months": 36, "description": "Walks up/down stairs"},
    {"name": "speech_understood", "type": MilestoneType.LANGUAGE, "age_months": 36, "description": "75% of speech understood by strangers"},
    # 48 months
    {"name": "cooperative_play", "type": MilestoneType.SOCIAL, "age_months": 48, "description": "Cooperative play with others"},
    {"name": "hops", "type": MilestoneType.MOTOR, "age_months": 48, "description": "Hops on one foot"},
    {"name": "draws_shapes", "type": MilestoneType.MOTOR, "age_months": 48, "description": "Draws simple shapes"},
    {"name": "recites_songs", "type": MilestoneType.LANGUAGE, "age_months": 48, "description": "Recites songs and rhymes"},
    # 60 months
    {"name": "real_pretend", "type": MilestoneType.COGNITIVE, "age_months": 60, "description": "Differentiates real from pretend"},
    {"name": "stands_one_foot", "type": MilestoneType.MOTOR, "age_months": 60, "description": "Stands on one foot 10+ seconds"},
    {"name": "tells_stories", "type": MilestoneType.LANGUAGE, "age_months": 60, "description": "Tells stories with beginning, middle, end"},
    {"name": "counts_ten", "type": MilestoneType.COGNITIVE, "age_months": 60, "description": "Counts to 10+"},
]

# Delay threshold: if a milestone expected by age X is not achieved by
# age X + this buffer, it is classified as DELAYED rather than NOT_YET.
_DELAY_BUFFER_MONTHS = 3


class DevelopmentalMilestones:
    """Developmental milestone tracking and delay detection.

    Tracks motor, social, cognitive, and language milestones for children
    0-60 months. Identifies achieved milestones, upcoming milestones,
    and potential delays requiring referral.

    Example:
        >>> dm = DevelopmentalMilestones()
        >>> milestones = dm.get_milestones_for_age(6)
        >>> len(milestones)
        6
    """

    def __init__(self) -> None:
        self._milestones = MILESTONES

    def get_milestones_for_age(self, age_months: int) -> list[MilestoneCheck]:
        """Get all milestones expected to be achieved by this age.

        Returns milestones whose expected age is less than or equal to
        the given age, with status NOT_YET (since we do not know which
        have been achieved without an `achieved` list).

        Args:
            age_months: The child's age in months.

        Returns:
            List of MilestoneCheck items expected by this age.

        Example:
            >>> dm = DevelopmentalMilestones()
            >>> checks = dm.get_milestones_for_age(4)
            >>> [c.milestone_name for c in checks]
            ['social_smile', 'coos', 'lifts_head', 'laughs', 'reaches_toys', 'rolls']
        """
        results: list[MilestoneCheck] = []
        for m in self._milestones:
            if m["age_months"] <= age_months:
                results.append(MilestoneCheck(
                    milestone_name=m["name"],
                    milestone_type=m["type"],
                    expected_age_months=m["age_months"],
                    status=MilestoneStatus.NOT_YET,
                    guidance=_get_guidance(m["name"], m["description"], MilestoneStatus.NOT_YET),
                ))
        return results

    def get_next_milestones(self, age_months: int) -> list[MilestoneCheck]:
        """Get upcoming milestones (the next age group after current age).

        Args:
            age_months: The child's current age in months.

        Returns:
            List of MilestoneCheck items for the next milestone age group.

        Example:
            >>> dm = DevelopmentalMilestones()
            >>> upcoming = dm.get_next_milestones(6)
            >>> upcoming[0].expected_age_months
            9
        """
        # Find the next milestone age bracket
        milestone_ages = sorted(set(m["age_months"] for m in self._milestones))
        next_age = None
        for ma in milestone_ages:
            if ma > age_months:
                next_age = ma
                break

        if next_age is None:
            return []

        results: list[MilestoneCheck] = []
        for m in self._milestones:
            if m["age_months"] == next_age:
                results.append(MilestoneCheck(
                    milestone_name=m["name"],
                    milestone_type=m["type"],
                    expected_age_months=m["age_months"],
                    status=MilestoneStatus.NOT_YET,
                    guidance=_get_upcoming_guidance(m["description"], next_age),
                ))
        return results

    def assess_development(
        self, age_months: int, achieved: list[str]
    ) -> dict:
        """Assess overall development across all domains.

        Args:
            age_months: The child's age in months.
            achieved: List of milestone names the child has achieved.

        Returns:
            Dictionary with keys:
            - "overall": "on_track" | "monitor" | "delayed"
            - "domains": dict mapping domain name to status
            - "summary": Human-readable summary
            - "recommendations": List of recommended actions

        Example:
            >>> dm = DevelopmentalMilestones()
            >>> result = dm.assess_development(
            ...     age_months=12,
            ...     achieved=["social_smile", "coos", "lifts_head", "laughs",
            ...               "reaches_toys", "rolls", "sits_with_support",
            ...               "babbles", "stranger_anxiety", "sits_alone",
            ...               "crawls", "pincer_grasp", "mama_baba",
            ...               "stands", "first_words", "responds_commands"],
            ... )
            >>> result["overall"]
            'on_track'
        """
        achieved_set = set(achieved)
        domain_results: dict[str, dict] = {}

        for domain in MilestoneType:
            domain_milestones = [
                m for m in self._milestones
                if m["type"] == domain and m["age_months"] <= age_months
            ]
            if not domain_milestones:
                domain_results[domain.value] = {
                    "status": "on_track",
                    "achieved_count": 0,
                    "expected_count": 0,
                    "missed": [],
                }
                continue

            achieved_count = sum(
                1 for m in domain_milestones if m["name"] in achieved_set
            )
            expected_count = len(domain_milestones)
            missed = [
                m for m in domain_milestones if m["name"] not in achieved_set
            ]

            # Check if any missed milestone is past the delay buffer
            delayed = any(
                (age_months - m["age_months"]) >= _DELAY_BUFFER_MONTHS
                for m in missed
            )

            if delayed:
                status = "delayed"
            elif missed:
                status = "monitor"
            else:
                status = "on_track"

            domain_results[domain.value] = {
                "status": status,
                "achieved_count": achieved_count,
                "expected_count": expected_count,
                "missed": [m["name"] for m in missed],
            }

        # Determine overall status
        statuses = [d["status"] for d in domain_results.values()]
        if "delayed" in statuses:
            overall = "delayed"
        elif "monitor" in statuses:
            overall = "monitor"
        else:
            overall = "on_track"

        summary = _build_development_summary(overall, domain_results, age_months)
        recommendations = _build_development_recommendations(overall, domain_results)

        return {
            "overall": overall,
            "domains": domain_results,
            "summary": summary,
            "recommendations": recommendations,
        }

    def detect_delays(
        self, age_months: int, achieved: list[str]
    ) -> list[MilestoneCheck]:
        """Detect milestones that should be achieved but are not.

        A milestone is considered delayed if it was expected at least
        _DELAY_BUFFER_MONTHS ago and has not been achieved.

        Args:
            age_months: The child's current age in months.
            achieved: List of milestone names the child has achieved.

        Returns:
            List of MilestoneCheck items for delayed milestones.

        Example:
            >>> dm = DevelopmentalMilestones()
            >>> delays = dm.detect_delays(age_months=12, achieved=[])
            >>> len(delays) > 0
            True
        """
        achieved_set = set(achieved)
        delayed: list[MilestoneCheck] = []

        for m in self._milestones:
            if m["age_months"] <= age_months and m["name"] not in achieved_set:
                months_overdue = age_months - m["age_months"]
                if months_overdue >= _DELAY_BUFFER_MONTHS:
                    status = MilestoneStatus.DELAYED
                    if months_overdue >= _DELAY_BUFFER_MONTHS * 2:
                        status = MilestoneStatus.REFERRED

                    delayed.append(MilestoneCheck(
                        milestone_name=m["name"],
                        milestone_type=m["type"],
                        expected_age_months=m["age_months"],
                        status=status,
                        guidance=_get_delay_guidance(
                            m["name"], m["description"], m["type"],
                            months_overdue, status,
                        ),
                    ))

        return delayed


def _get_guidance(name: str, description: str, status: MilestoneStatus) -> str:
    """Get guidance text for a milestone check."""
    if status == MilestoneStatus.ACHIEVED:
        return f"Great progress! Your child can: {description.lower()}."
    return (
        f"By this age, most children can: {description.lower()}. "
        "Try encouraging this through play and interaction."
    )


def _get_upcoming_guidance(description: str, expected_age: int) -> str:
    """Get guidance for an upcoming milestone."""
    return (
        f"Around {expected_age} months, your child will start to: "
        f"{description.lower()}. You can encourage this through play "
        "and interaction."
    )


def _get_delay_guidance(
    name: str,
    description: str,
    milestone_type: MilestoneType,
    months_overdue: int,
    status: MilestoneStatus,
) -> str:
    """Get guidance for a delayed milestone."""
    type_activities: dict[MilestoneType, str] = {
        MilestoneType.MOTOR: (
            "Give your child safe space to move and explore. "
            "Place toys just out of reach to encourage movement."
        ),
        MilestoneType.LANGUAGE: (
            "Talk, sing, and read to your child often. "
            "Name objects and describe what you are doing throughout the day."
        ),
        MilestoneType.SOCIAL: (
            "Play face-to-face games with your child. "
            "Respond to your child's sounds and expressions."
        ),
        MilestoneType.COGNITIVE: (
            "Play simple games like peekaboo and hiding toys. "
            "Let your child explore safe objects of different shapes and textures."
        ),
    }

    activity = type_activities.get(milestone_type, "Engage with your child through play.")

    if status == MilestoneStatus.REFERRED:
        return (
            f"Your child has not yet achieved: {description.lower()}. "
            f"This was expected by {months_overdue} months ago. "
            "It is recommended to visit a clinic for a developmental assessment. "
            f"In the meantime: {activity}"
        )

    return (
        f"Your child has not yet achieved: {description.lower()}. "
        f"This was expected around {months_overdue} months ago. "
        f"Keep encouraging this through activities: {activity} "
        "If you are concerned, discuss with your health worker at the next visit."
    )


def _build_development_summary(
    overall: str, domains: dict[str, dict], age_months: int
) -> str:
    """Build a human-readable development summary."""
    if overall == "on_track":
        return (
            f"At {age_months} months, your child's development is on track "
            "across all areas. Keep up the great work with play and interaction!"
        )

    delayed_domains = [
        d for d, info in domains.items() if info["status"] == "delayed"
    ]
    monitor_domains = [
        d for d, info in domains.items() if info["status"] == "monitor"
    ]

    parts: list[str] = [f"At {age_months} months:"]
    if delayed_domains:
        domain_list = ", ".join(delayed_domains)
        parts.append(
            f"Delays detected in: {domain_list}. "
            "A developmental assessment at the clinic is recommended."
        )
    if monitor_domains:
        domain_list = ", ".join(monitor_domains)
        parts.append(
            f"Some milestones to watch in: {domain_list}. "
            "Continue encouraging development through play."
        )

    return " ".join(parts)


def _build_development_recommendations(
    overall: str, domains: dict[str, dict]
) -> list[str]:
    """Build actionable recommendations based on development assessment."""
    recommendations: list[str] = []

    if overall == "delayed":
        recommendations.append(
            "Visit your clinic for a developmental assessment. Early intervention "
            "can make a significant difference."
        )

    for domain, info in domains.items():
        if info["status"] in ("delayed", "monitor"):
            if domain == "motor":
                recommendations.append(
                    "Motor skills: Give your child safe floor time daily. "
                    "Use toys to encourage reaching, grasping, and movement."
                )
            elif domain == "language":
                recommendations.append(
                    "Language skills: Talk to your child throughout the day. "
                    "Sing songs, tell stories, and name objects you see together."
                )
            elif domain == "social":
                recommendations.append(
                    "Social skills: Play face-to-face games. Respond to your "
                    "child's smiles and sounds. Introduce safe play with other children."
                )
            elif domain == "cognitive":
                recommendations.append(
                    "Thinking skills: Play hiding games (peekaboo). Let your child "
                    "explore objects. Point out colours, shapes, and sizes."
                )

    if overall == "on_track":
        recommendations.append(
            "Continue with regular play, reading, and interaction. "
            "Attend growth monitoring visits as scheduled."
        )

    return recommendations
