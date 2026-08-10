"""Developmental milestone tracking for children 0-60 months, plus
school-age (6-12y) and adolescent (13-17y) wellbeing checkpoints.

The 0-60 month milestones are based on WHO/CDC developmental milestones
adapted for the Zimbabwean context, covering motor, social, cognitive, and
language domains.

For school-age and adolescent children the concept of "milestone by month X"
does not apply the same way, so those stages use WELLBEING CHECKPOINTS
instead: caregiver/self check-in prompts on learning, vision and hearing,
healthy weight, activity, and emotional wellbeing. These are guidance
prompts, NOT a clinical developmental screen, and are marked
pending_clinical_signoff until the advisory panel reviews them.
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


# School-age (6-12y) wellbeing checkpoints. These are caregiver check-in
# prompts, NOT a developmental screen. A "no" (concern) is a prompt to
# discuss with a health worker, never an automatic clinical classification.
# pending_clinical_signoff: awaits advisory panel review.
SCHOOL_AGE_WELLBEING: list[dict] = [
    {"key": "learning", "domain": "learning", "prompt": "Is your child keeping up with learning and enjoying school?", "concern_guidance": "If your child is struggling to keep up, seems bored, or does not want to go to school, talk to their teacher and a health worker. Vision or hearing problems can also affect learning."},
    {"key": "vision", "domain": "vision", "prompt": "Can your child see the board and read without squinting or headaches?", "concern_guidance": "Trouble seeing the board, squinting, sitting very close, or headaches when reading can be signs of a vision problem. A simple eye check at the clinic can help."},
    {"key": "hearing", "domain": "hearing", "prompt": "Does your child hear well and respond when spoken to normally?", "concern_guidance": "Asking you to repeat things, turning up sound, or ear pain and discharge can be signs of a hearing problem. Ask for a hearing check at the clinic."},
    {"key": "healthy_weight", "domain": "growth", "prompt": "Is your child growing well, neither too thin nor gaining weight too fast?", "concern_guidance": "Big changes in weight, being much thinner or heavier than other children the same age, or always being tired are worth discussing at a health check. Record weight and height for clinical review rather than judging it at home."},
    {"key": "physical_activity", "domain": "activity", "prompt": "Is your child active and playing most days?", "concern_guidance": "Children this age do best with about an hour of active play each day. If your child is not active, encourage safe play, walking, and helping with age-appropriate tasks."},
    {"key": "emotional_wellbeing", "domain": "emotional", "prompt": "Does your child seem happy, settled, and able to make friends?", "concern_guidance": "Being very withdrawn, a big change in mood or behaviour, or trouble making friends can be worth a gentle chat and, if it lasts, a word with a health worker."},
    {"key": "dental", "domain": "dental", "prompt": "Does your child brush their teeth twice a day and have no tooth pain?", "concern_guidance": "Encourage brushing twice a day. Tooth pain, holes, or bleeding gums need a clinic or dental visit."},
]


# Adolescent (13-17y) wellbeing checkpoints. Conservative content: nutrition,
# activity, puberty basics, menstrual-health basics, mental wellbeing. Anything
# beyond basics signposts to a health worker or caregiver. pending_clinical_signoff.
ADOLESCENT_WELLBEING: list[dict] = [
    {"key": "nutrition", "domain": "nutrition", "prompt": "Is the young person eating balanced meals most days?", "concern_guidance": "Adolescents grow fast and need balanced meals with enough energy, protein, fruit, and vegetables. Always tired, very pale, or eating very little is worth discussing with a health worker."},
    {"key": "iron_for_girls", "domain": "nutrition", "prompt": "For girls: are they eating iron-rich foods (beans, green leafy vegetables, meat, liver)?", "concern_guidance": "Girls need extra iron once periods start, to avoid anaemia. Iron-rich foods help. If they are often tired, dizzy, or very pale, a health worker can check for anaemia."},
    {"key": "physical_activity", "domain": "activity", "prompt": "Is the young person active most days and getting enough rest?", "concern_guidance": "Regular activity and about 8-10 hours of sleep support growth, mood, and concentration. Encourage a balance of activity, study, and rest."},
    {"key": "puberty", "domain": "puberty", "prompt": "Does the young person understand the body changes of puberty?", "concern_guidance": "Body changes during puberty are normal. Answer questions simply and honestly. For anything you are unsure about, a health worker can give trusted, private information."},
    {"key": "menstrual_health", "domain": "menstrual", "prompt": "For girls who have started periods: are their periods manageable and hygiene supported?", "concern_guidance": "Basic period hygiene and pain relief usually help. Very painful, very heavy, or missed periods that worry you are worth a visit to a health worker."},
    {"key": "emotional_wellbeing", "domain": "emotional", "prompt": "Does the young person seem to be coping emotionally?", "concern_guidance": "Feeling very sad, anxious, or overwhelmed for two weeks or more is worth talking about. A trusted adult or health worker can help. Any thoughts of self-harm need help the same day."},
    {"key": "health_check", "domain": "clinic", "prompt": "Has the young person had a health check this year and any due vaccines?", "concern_guidance": "An annual check is a good chance to review growth, nutrition, mood, and any due vaccines (for example the Td booster, and HPV for girls)."},
]


class DevelopmentalMilestones:
    """Developmental milestone tracking and delay detection.

    Tracks motor, social, cognitive, and language milestones for children
    0-60 months. Identifies achieved milestones, upcoming milestones,
    and potential delays requiring referral.

    Example:
        >>> dm = DevelopmentalMilestones()
        >>> milestones = dm.get_milestones_for_age(6)
        >>> len(milestones)
        9
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

    @staticmethod
    def get_school_age_wellbeing_checkpoints() -> list[dict]:
        """Get the school-age (6-12y) wellbeing check-in prompts.

        These are caregiver check-in prompts on learning, vision, hearing,
        healthy weight, activity, emotional wellbeing, and dental health.
        They are guidance prompts, NOT a clinical developmental screen.

        Returns:
            List of checkpoint dicts with key, domain, prompt, and
            concern_guidance.

        Example:
            >>> dm = DevelopmentalMilestones()
            >>> checks = dm.get_school_age_wellbeing_checkpoints()
            >>> checks[0]["domain"]
            'learning'
        """
        return [dict(c) for c in SCHOOL_AGE_WELLBEING]

    @staticmethod
    def get_adolescent_wellbeing_checkpoints() -> list[dict]:
        """Get the adolescent (13-17y) wellbeing check-in prompts.

        Conservative content: nutrition (including iron for girls), physical
        activity and rest, puberty basics, menstrual-health basics, emotional
        wellbeing, and an annual health check. Guidance prompts, not a screen.

        Returns:
            List of checkpoint dicts with key, domain, prompt, and
            concern_guidance.

        Example:
            >>> dm = DevelopmentalMilestones()
            >>> checks = dm.get_adolescent_wellbeing_checkpoints()
            >>> checks[0]["domain"]
            'nutrition'
        """
        return [dict(c) for c in ADOLESCENT_WELLBEING]

    @staticmethod
    def assess_wellbeing(checkpoint_key: str, concern: bool) -> dict:
        """Return guidance for a single wellbeing checkpoint response.

        A "concern" response never produces an automatic clinical
        classification. It returns supportive guidance and, where relevant,
        a prompt to involve a health worker or caregiver.

        Args:
            checkpoint_key: The checkpoint key (e.g. "vision", "nutrition").
            concern: True if the caregiver/young person flagged a concern.

        Returns:
            Dict with keys: key, concern (bool), guidance (str).

        Raises:
            ValueError: If the checkpoint key is not recognised.

        Example:
            >>> dm = DevelopmentalMilestones()
            >>> res = dm.assess_wellbeing("vision", concern=True)
            >>> res["concern"]
            True
        """
        all_checks = {c["key"]: c for c in (SCHOOL_AGE_WELLBEING + ADOLESCENT_WELLBEING)}
        check = all_checks.get(checkpoint_key)
        if check is None:
            available = ", ".join(sorted(all_checks.keys()))
            raise ValueError(
                f"Unknown wellbeing checkpoint '{checkpoint_key}'. "
                f"Available: {available}"
            )
        if concern:
            guidance = check["concern_guidance"]
        else:
            guidance = "Great. Keep it up, and mention anything new at your next health check."
        return {"key": checkpoint_key, "concern": concern, "guidance": guidance}


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
