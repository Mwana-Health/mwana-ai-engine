"""Shared data types, enums, and dataclasses for the Mwana AI Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Stage(str, Enum):
    """Maternal-child health stage from pregnancy through adolescence.

    Age boundaries for child stages:
    - NEWBORN: 0 to 28 days.
    - INFANT: 29 days to under 12 months.
    - TODDLER: 12 to under 36 months (1 to under 3 years).
    - EARLY_CHILDHOOD: 36 to under 72 months (3 to under 6 years).
    - SCHOOL_AGE: 6 years to under 13 years (6 to 12 years).
    - ADOLESCENT: 13 years to under 18 years (13 to 17 years).

    Clinical note: WHO IMCI applies only to under-5 children. SCHOOL_AGE and
    ADOLESCENT stages therefore use general danger-sign guidance, never IMCI
    breathing-rate or age cutoffs (see ``danger_signs`` and ``triage``).
    """

    PREGNANT = "pregnant"
    NEWBORN = "newborn"
    INFANT = "infant"
    TODDLER = "toddler"
    EARLY_CHILDHOOD = "early_childhood"
    SCHOOL_AGE = "school_age"
    ADOLESCENT = "adolescent"


class TriageLevel(str, Enum):
    """Urgency level for symptom triage.

    GREEN: Home care with guidance.
    YELLOW: Clinic visit within 24-48 hours.
    RED: Immediate clinic/hospital visit.
    """

    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class MilestoneType(str, Enum):
    """Category of developmental milestone."""

    MOTOR = "motor"
    SOCIAL = "social"
    COGNITIVE = "cognitive"
    LANGUAGE = "language"


class MilestoneStatus(str, Enum):
    """Status of a developmental milestone check."""

    ACHIEVED = "achieved"
    NOT_YET = "not_yet"
    DELAYED = "delayed"
    REFERRED = "referred"


class MUACStatus(str, Enum):
    """Mid-upper arm circumference classification.

    GREEN: >= 12.5 cm (normal).
    YELLOW: 11.5 - 12.5 cm (moderate acute malnutrition risk).
    RED: < 11.5 cm (severe acute malnutrition risk).
    """

    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class NutritionStatus(str, Enum):
    """Nutritional status classification."""

    NORMAL = "normal"
    MAM = "mam"  # Moderate Acute Malnutrition
    SAM = "sam"  # Severe Acute Malnutrition


class BreastfeedingStatus(str, Enum):
    """Current breastfeeding status."""

    EXCLUSIVE = "exclusive"
    COMPLEMENTARY = "complementary"
    WEANED = "weaned"


@dataclass
class TriageResult:
    """Result of a symptom triage assessment.

    Attributes:
        level: The urgency level (GREEN, YELLOW, RED).
        assessment: A brief clinical assessment summary.
        recommended_action: What the caregiver should do.
        danger_signs: List of identified danger signs.
        follow_up_hours: Recommended follow-up time in hours (None if not applicable).

    Example:
        >>> result = TriageResult(
        ...     level=TriageLevel.RED,
        ...     assessment="Convulsions detected in newborn",
        ...     recommended_action="Go to the nearest clinic or hospital immediately",
        ...     danger_signs=["convulsions"],
        ...     follow_up_hours=0,
        ... )
    """

    level: TriageLevel
    assessment: str
    recommended_action: str
    danger_signs: list[str] = field(default_factory=list)
    follow_up_hours: int | None = None


@dataclass
class GrowthAssessment:
    """Result of a growth monitoring assessment.

    Attributes:
        weight_for_age_z: Weight-for-age z-score.
        height_for_age_z: Height/length-for-age z-score.
        weight_for_height_z: Weight-for-height/length z-score.
        muac_status: MUAC classification (if measured).
        nutrition_status: Overall nutrition status.
        interpretation: Human-readable interpretation.
        recommendations: List of recommended actions.

    Example:
        >>> assessment = GrowthAssessment(
        ...     weight_for_age_z=-1.2,
        ...     height_for_age_z=-0.5,
        ...     weight_for_height_z=-1.0,
        ...     muac_status=MUACStatus.GREEN,
        ...     nutrition_status=NutritionStatus.NORMAL,
        ...     interpretation="Growth is within normal range",
        ...     recommendations=["Continue current feeding practices"],
        ... )
    """

    weight_for_age_z: float
    height_for_age_z: float
    weight_for_height_z: float
    muac_status: MUACStatus | None
    nutrition_status: NutritionStatus
    interpretation: str
    recommendations: list[str] = field(default_factory=list)


@dataclass
class MilestoneCheck:
    """Result of checking a single developmental milestone.

    Attributes:
        milestone_name: Internal identifier for the milestone.
        milestone_type: Category (MOTOR, SOCIAL, COGNITIVE, LANGUAGE).
        expected_age_months: Age in months when this milestone is typically achieved.
        status: Current status of the milestone.
        guidance: Advice for the caregiver.

    Example:
        >>> check = MilestoneCheck(
        ...     milestone_name="social_smile",
        ...     milestone_type=MilestoneType.SOCIAL,
        ...     expected_age_months=2,
        ...     status=MilestoneStatus.ACHIEVED,
        ...     guidance="Great! Your baby is smiling at people.",
        ... )
    """

    milestone_name: str
    milestone_type: MilestoneType
    expected_age_months: int
    status: MilestoneStatus
    guidance: str


@dataclass
class ImmunizationDue:
    """Information about a due or upcoming immunization.

    Attributes:
        vaccine_code: Internal code for the vaccine (e.g. "BCG", "Penta1").
        vaccine_name: Human-readable vaccine name.
        dose_number: Which dose in the series (1, 2, 3, etc.).
        scheduled_age_weeks: Age in weeks when the dose is scheduled.
        scheduled_date: Calculated date when the dose is due.
        is_overdue: Whether the scheduled date has passed.
        days_until_due: Days until (positive) or since (negative) the scheduled date.
        max_age_months: Maximum age in months for catch-up administration.
        sex: Who the dose applies to ("any", "female", or "male"). Used to
            filter sex-specific doses such as HPV for girls.

    Example:
        >>> due = ImmunizationDue(
        ...     vaccine_code="Penta1",
        ...     vaccine_name="Pentavalent (DPT-HepB-Hib)",
        ...     dose_number=1,
        ...     scheduled_age_weeks=6,
        ...     scheduled_date=date(2026, 3, 1),
        ...     is_overdue=False,
        ...     days_until_due=14,
        ...     max_age_months=23,
        ... )
    """

    vaccine_code: str
    vaccine_name: str
    dose_number: int
    scheduled_age_weeks: int
    scheduled_date: date
    is_overdue: bool
    days_until_due: int
    max_age_months: int
    sex: str = "any"
