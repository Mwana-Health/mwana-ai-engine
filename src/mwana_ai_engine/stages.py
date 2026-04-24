"""Stage management for maternal-child health lifecycle.

Handles automatic determination and transitions between care stages:
PREGNANT -> NEWBORN -> INFANT -> TODDLER -> EARLY_CHILDHOOD.
"""

from __future__ import annotations

from datetime import date, timedelta

from .types import Stage


class StageManager:
    """Manages care stage determination and transitions.

    Stages are determined by the child's age (or pregnancy status):
    - PREGNANT: Has a due date, has not delivered yet.
    - NEWBORN: 0 to 28 days old.
    - INFANT: 1 to 12 months old.
    - TODDLER: 1 to 3 years old.
    - EARLY_CHILDHOOD: 3 to 5 years old.

    Example:
        >>> from datetime import date
        >>> stage = StageManager.determine_stage(child_dob=date(2026, 3, 1))
        >>> print(stage)
        Stage.NEWBORN
    """

    @staticmethod
    def determine_stage(
        due_date: date | None = None,
        delivery_date: date | None = None,
        child_dob: date | None = None,
    ) -> Stage:
        """Determine the current care stage based on dates.

        Args:
            due_date: Expected delivery date (for pregnant mothers).
            delivery_date: Actual delivery date (if delivered).
            child_dob: Child's date of birth.

        Returns:
            The current Stage.

        Raises:
            ValueError: If no dates are provided to determine a stage.

        Example:
            >>> StageManager.determine_stage(due_date=date(2026, 9, 1))
            Stage.PREGNANT
            >>> StageManager.determine_stage(child_dob=date(2025, 1, 1))
            Stage.TODDLER
        """
        today = date.today()

        if due_date is not None and delivery_date is None and child_dob is None:
            return Stage.PREGNANT

        dob = child_dob or delivery_date
        if dob is None:
            raise ValueError(
                "At least one of due_date, delivery_date, or child_dob must be provided"
            )

        age_days = (today - dob).days
        if age_days < 0:
            return Stage.PREGNANT

        if age_days <= 28:
            return Stage.NEWBORN

        age_months = _age_in_months(dob, today)
        if age_months < 12:
            return Stage.INFANT
        if age_months < 36:
            return Stage.TODDLER
        if age_months < 60:
            return Stage.EARLY_CHILDHOOD

        return Stage.EARLY_CHILDHOOD

    @staticmethod
    def should_transition(
        current_stage: Stage,
        child_dob: date | None = None,
        due_date: date | None = None,
    ) -> Stage | None:
        """Check if a stage transition is needed.

        Args:
            current_stage: The current stage.
            child_dob: Child's date of birth.
            due_date: Expected delivery date.

        Returns:
            The new Stage if a transition is needed, None if no change.

        Example:
            >>> new_stage = StageManager.should_transition(
            ...     Stage.NEWBORN, child_dob=date(2025, 12, 1)
            ... )
            >>> print(new_stage)
            Stage.INFANT
        """
        try:
            actual_stage = StageManager.determine_stage(
                due_date=due_date, child_dob=child_dob
            )
        except ValueError:
            return None

        if actual_stage != current_stage:
            return actual_stage
        return None

    @staticmethod
    def get_stage_content(stage: Stage) -> dict:
        """Get stage-specific content themes and focus areas.

        Args:
            stage: The current care stage.

        Returns:
            Dictionary with content themes, key_topics, and check_frequency.

        Example:
            >>> content = StageManager.get_stage_content(Stage.NEWBORN)
            >>> print(content["key_topics"])
            ['breastfeeding', 'cord care', ...]
        """
        content_map: dict[Stage, dict] = {
            Stage.PREGNANT: {
                "themes": [
                    "Antenatal care visits",
                    "Nutrition during pregnancy",
                    "Birth preparedness",
                    "Danger sign awareness",
                    "Mental health",
                ],
                "key_topics": [
                    "antenatal_visits",
                    "pregnancy_nutrition",
                    "birth_plan",
                    "danger_signs",
                    "emotional_wellbeing",
                    "malaria_prevention",
                    "hiv_testing",
                    "tetanus_vaccination",
                ],
                "check_frequency": "Every 2 weeks in third trimester, monthly before",
            },
            Stage.NEWBORN: {
                "themes": [
                    "Breastfeeding initiation",
                    "Cord care",
                    "Thermal care",
                    "Immunization (BCG, HepB birth dose)",
                    "Danger sign recognition",
                    "Postnatal depression screening",
                ],
                "key_topics": [
                    "breastfeeding",
                    "cord_care",
                    "keeping_warm",
                    "immunization",
                    "danger_signs",
                    "postnatal_checkup",
                    "maternal_mental_health",
                    "birth_registration",
                ],
                "check_frequency": "Day 1, Day 3, Week 1, Week 2, Week 4",
            },
            Stage.INFANT: {
                "themes": [
                    "Exclusive breastfeeding (0-6 months)",
                    "Complementary feeding (6+ months)",
                    "Immunization schedule",
                    "Growth monitoring",
                    "Developmental milestones",
                ],
                "key_topics": [
                    "breastfeeding",
                    "complementary_feeding",
                    "immunization",
                    "growth_monitoring",
                    "milestones",
                    "illness_management",
                    "oral_health",
                    "sleep_safety",
                ],
                "check_frequency": "Monthly growth monitoring, immunization schedule",
            },
            Stage.TODDLER: {
                "themes": [
                    "Dietary diversity",
                    "Language development",
                    "Safety and injury prevention",
                    "Immunization boosters",
                    "Social and emotional development",
                ],
                "key_topics": [
                    "nutrition",
                    "language_stimulation",
                    "injury_prevention",
                    "immunization_boosters",
                    "toilet_training",
                    "play_and_learning",
                    "discipline",
                    "dental_care",
                ],
                "check_frequency": "Every 3 months for growth, yearly comprehensive check",
            },
            Stage.EARLY_CHILDHOOD: {
                "themes": [
                    "School readiness",
                    "Social skills",
                    "Nutrition for active children",
                    "Vision and hearing checks",
                    "Emotional regulation",
                ],
                "key_topics": [
                    "school_readiness",
                    "social_skills",
                    "nutrition",
                    "vision_hearing",
                    "emotional_development",
                    "physical_activity",
                    "road_safety",
                    "screen_time",
                ],
                "check_frequency": "Every 6 months, pre-school health check",
            },
        }
        return content_map[stage]


def _age_in_months(dob: date, reference: date) -> int:
    """Calculate age in complete months.

    Args:
        dob: Date of birth.
        reference: Reference date (usually today).

    Returns:
        Age in complete months.
    """
    months = (reference.year - dob.year) * 12 + (reference.month - dob.month)
    if reference.day < dob.day:
        months -= 1
    return max(0, months)
