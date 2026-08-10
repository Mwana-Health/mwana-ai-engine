"""Mwana AI Engine - Maternal-child health AI engine for Zimbabwe.

A reusable, open-source library providing clinical decision support for
symptom triage, immunization scheduling, growth monitoring, developmental
milestones, nutrition guidance, postnatal depression screening, and more.

Built on WHO IMCI guidelines, the Zimbabwe EPI schedule, and validated
clinical tools adapted for the Zimbabwean context.

Example:
    >>> from mwana_ai_engine import TriageEngine, Stage
    >>> result = TriageEngine.triage(
    ...     symptoms=["convulsions"],
    ...     stage=Stage.NEWBORN,
    ... )
    >>> result.level
    TriageLevel.RED
"""

from .types import (
    BreastfeedingStatus,
    GrowthAssessment,
    ImmunizationDue,
    MilestoneCheck,
    MilestoneStatus,
    MilestoneType,
    MUACStatus,
    NutritionStatus,
    Stage,
    TriageLevel,
    TriageResult,
)
from .triage import TriageEngine
from .imci import IMCIAssessment
from .immunization import ImmunizationScheduler
from .milestones import DevelopmentalMilestones
from .growth import GrowthMonitor
from .nutrition import NutritionAdvisor
from .epds import EPDSScreening
from .danger_signs import DangerSignDetector
from .climate import ClimateRiskScorer
from .injury_prevention import InjuryPreventionEngine
from .family_planning import FamilyPlanningAdvisor
from .translation import TranslationService
from .stages import StageManager
from .prompts import get_health_system_prompt

__version__ = "0.2.0"

__all__ = [
    # Types and enums
    "Stage",
    "TriageLevel",
    "MilestoneType",
    "MilestoneStatus",
    "MUACStatus",
    "NutritionStatus",
    "BreastfeedingStatus",
    # Dataclasses
    "TriageResult",
    "GrowthAssessment",
    "MilestoneCheck",
    "ImmunizationDue",
    # Engine classes
    "TriageEngine",
    "IMCIAssessment",
    "ImmunizationScheduler",
    "DevelopmentalMilestones",
    "GrowthMonitor",
    "NutritionAdvisor",
    "EPDSScreening",
    "DangerSignDetector",
    "ClimateRiskScorer",
    "InjuryPreventionEngine",
    "FamilyPlanningAdvisor",
    "TranslationService",
    "StageManager",
    # Functions
    "get_health_system_prompt",
]
