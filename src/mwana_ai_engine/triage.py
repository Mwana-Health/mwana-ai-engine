"""Symptom triage engine for maternal-child health.

Maps reported symptoms to urgency levels (GREEN, YELLOW, RED) with
stage-specific rules for pregnancy, newborn, infant, toddler, and
early childhood.
"""

from __future__ import annotations

from .types import Stage, TriageLevel, TriageResult


# Symptoms that always indicate RED (immediate clinic/hospital) regardless of stage.
_UNIVERSAL_RED_SYMPTOMS: set[str] = {
    "convulsions",
    "seizures",
    "unconscious",
    "unresponsive",
    "unable_to_drink",
    "unable_to_feed",
    "severe_bleeding",
}

# Stage-specific RED symptoms.
_STAGE_RED_SYMPTOMS: dict[Stage, set[str]] = {
    Stage.PREGNANT: {
        "severe_headache_with_blurred_vision",
        "severe_abdominal_pain",
        "vaginal_bleeding",
        "gush_of_fluid",
        "reduced_fetal_movement",
        "swelling_face_hands",
        "high_blood_pressure",
        "eclampsia",
    },
    Stage.NEWBORN: {
        "cord_infection",
        "cord_redness",
        "cord_pus",
        "cord_smell",
        "severe_jaundice",
        "jaundice_palms_soles",
        "hypothermia",
        "fever_newborn",
        "fast_breathing_newborn",
        "chest_indrawing",
        "bleeding_from_cord",
        "not_feeding",
        "lethargy",
        "bulging_fontanelle",
    },
    Stage.INFANT: {
        "chest_indrawing",
        "severe_dehydration",
        "sunken_fontanelle",
        "bloody_diarrhea",
        "vomits_everything",
        "lethargy",
        "severe_wasting",
        "edema_both_feet",
        "muac_red",
        "stiff_neck",
    },
    Stage.TODDLER: {
        "chest_indrawing",
        "severe_dehydration",
        "bloody_diarrhea",
        "vomits_everything",
        "lethargy",
        "severe_wasting",
        "edema_both_feet",
        "muac_red",
        "stiff_neck",
        "severe_burn",
        "poisoning",
        "drowning_signs",
    },
    Stage.EARLY_CHILDHOOD: {
        "chest_indrawing",
        "severe_dehydration",
        "bloody_diarrhea",
        "vomits_everything",
        "lethargy",
        "severe_wasting",
        "edema_both_feet",
        "muac_red",
        "stiff_neck",
        "severe_burn",
        "poisoning",
        "drowning_signs",
    },
    # SCHOOL_AGE (6-12y) and ADOLESCENT (13-17y) use GENERAL danger signs.
    # No IMCI breathing-rate or age cutoffs. See danger_signs.py.
    Stage.SCHOOL_AGE: {
        "severe_difficulty_breathing",
        "severe_dehydration",
        "high_persistent_fever",
        "severe_injury",
        "severe_burn",
        "poisoning",
        "drowning_signs",
        "severe_abdominal_pain",
        "bloody_diarrhea",
        "stiff_neck",
        "heavy_bleeding",
    },
    Stage.ADOLESCENT: {
        "severe_difficulty_breathing",
        "severe_dehydration",
        "high_persistent_fever",
        "severe_injury",
        "severe_burn",
        "poisoning",
        "severe_abdominal_pain",
        "chest_pain",
        "heavy_bleeding",
        "self_harm_thoughts",
        "stiff_neck",
    },
}

# Stage-specific YELLOW symptoms (clinic within 24-48 hours).
_STAGE_YELLOW_SYMPTOMS: dict[Stage, set[str]] = {
    Stage.PREGNANT: {
        "persistent_headache",
        "mild_bleeding",
        "reduced_fetal_movement_mild",
        "persistent_vomiting",
        "fever",
        "painful_urination",
        "foul_discharge",
        "swelling_legs",
        "persistent_abdominal_pain",
    },
    Stage.NEWBORN: {
        "poor_feeding",
        "jaundice_mild",
        "skin_rash_spreading",
        "umbilical_redness_mild",
        "persistent_crying",
        "eye_discharge",
        "fever_low",
    },
    Stage.INFANT: {
        "fever_persistent",
        "persistent_fever",
        "fast_breathing",
        "some_dehydration",
        "diarrhea_persistent",
        "skin_pinch_slow",
        "muac_yellow",
        "ear_discharge",
        "reduced_feeding",
        "weight_loss",
        "persistent_cough",
        "wheezing",
    },
    Stage.TODDLER: {
        "fever_persistent",
        "persistent_fever",
        "fast_breathing",
        "some_dehydration",
        "diarrhea_persistent",
        "skin_pinch_slow",
        "muac_yellow",
        "ear_discharge",
        "reduced_feeding",
        "weight_loss",
        "persistent_cough",
        "wheezing",
        "burn_mild",
        "limping",
        "behavioral_change",
    },
    Stage.EARLY_CHILDHOOD: {
        "fever_persistent",
        "persistent_fever",
        "fast_breathing",
        "some_dehydration",
        "diarrhea_persistent",
        "skin_pinch_slow",
        "muac_yellow",
        "ear_discharge",
        "reduced_feeding",
        "weight_loss",
        "persistent_cough",
        "wheezing",
        "burn_mild",
        "limping",
        "behavioral_change",
        "vision_concern",
        "hearing_concern",
        "behavioral_regression",
    },
    Stage.SCHOOL_AGE: {
        "persistent_fever",
        "fever_persistent",
        "persistent_diarrhea",
        "diarrhea_persistent",
        "persistent_cough",
        "vision_concern",
        "hearing_concern",
        "poor_weight_gain",
        "weight_loss",
        "learning_or_mood_concern",
        "ear_discharge",
        "limping",
    },
    Stage.ADOLESCENT: {
        "persistent_fever",
        "fever_persistent",
        "persistent_cough",
        "mood_or_wellbeing_concern",
        "nutrition_concern",
        "weight_loss",
        "menstrual_concern",
        "vision_concern",
        "hearing_concern",
    },
}

# GREEN symptoms (home care + guidance).
_GREEN_SYMPTOMS: set[str] = {
    "common_cold",
    "mild_cough",
    "runny_nose",
    "mild_diarrhea",
    "minor_rash",
    "teething",
    "mild_fever",
    "normal_pregnancy_symptoms",
    "morning_sickness",
    "back_pain",
    "mild_swelling_feet",
    "breast_tenderness",
    "heartburn",
    "constipation",
    "frequent_urination",
    "hiccups",
    "sneezing",
    "cradle_cap",
    "diaper_rash",
    "mild_colic",
    "spitting_up",
}

_RED_ACTIONS: dict[Stage, str] = {
    Stage.PREGNANT: (
        "Go to the nearest clinic or hospital IMMEDIATELY. "
        "Do not wait. Tell them your symptoms. If you cannot walk, "
        "ask someone to help you get there or call for an ambulance."
    ),
    Stage.NEWBORN: (
        "Take your baby to the nearest clinic or hospital IMMEDIATELY. "
        "Keep baby warm on the way. Continue breastfeeding if baby can feed."
    ),
    Stage.INFANT: (
        "Take your child to the nearest clinic or hospital IMMEDIATELY. "
        "If the child can drink, give small sips of ORS on the way."
    ),
    Stage.TODDLER: (
        "Take your child to the nearest clinic or hospital IMMEDIATELY. "
        "If the child can drink, give small sips of ORS on the way. "
        "If poisoning is suspected, bring the container of the substance."
    ),
    Stage.EARLY_CHILDHOOD: (
        "Take your child to the nearest clinic or hospital IMMEDIATELY. "
        "If the child can drink, give small sips of ORS on the way."
    ),
    Stage.SCHOOL_AGE: (
        "Take your child to the nearest clinic or hospital IMMEDIATELY. "
        "Do not wait. Stay with them and keep them calm. If they can drink, "
        "give small sips of water or ORS on the way."
    ),
    Stage.ADOLESCENT: (
        "Get to the nearest clinic or hospital IMMEDIATELY. Do not wait. "
        "If this is about thoughts of self-harm, tell a trusted adult or "
        "health worker today and stay with someone. You are not alone and "
        "help is available."
    ),
}

_YELLOW_ACTIONS: dict[Stage, str] = {
    Stage.PREGNANT: (
        "Visit your clinic within 24 hours. Monitor your symptoms closely. "
        "If they get worse, go to the hospital immediately."
    ),
    Stage.NEWBORN: (
        "Visit your clinic within 24 hours. Keep your baby warm and continue "
        "breastfeeding. Watch for any worsening signs."
    ),
    Stage.INFANT: (
        "Visit your clinic within 24-48 hours. Continue breastfeeding. "
        "Give ORS if there is diarrhea. Monitor temperature."
    ),
    Stage.TODDLER: (
        "Visit your clinic within 24-48 hours. Ensure your child drinks "
        "enough fluids. Give ORS if there is diarrhea. Monitor temperature."
    ),
    Stage.EARLY_CHILDHOOD: (
        "Visit your clinic within 24-48 hours. Ensure your child drinks "
        "enough fluids. Give ORS if there is diarrhea. Monitor temperature."
    ),
    Stage.SCHOOL_AGE: (
        "Visit your clinic within 24-48 hours. Make sure your child rests, "
        "drinks enough fluids, and eats well. If the symptoms get worse, "
        "go to the hospital immediately."
    ),
    Stage.ADOLESCENT: (
        "Visit your clinic within 24-48 hours, and involve a caregiver. "
        "Encourage rest, fluids, and good meals. For worries about mood, "
        "periods, or body changes, a health worker can help. If things get "
        "worse, go to the hospital immediately."
    ),
}

_GREEN_ACTIONS: dict[Stage, str] = {
    Stage.PREGNANT: (
        "These are common pregnancy symptoms. Rest, drink plenty of fluids, "
        "and eat small frequent meals. Attend your next antenatal visit as scheduled. "
        "If symptoms worsen or new symptoms appear, contact your clinic."
    ),
    Stage.NEWBORN: (
        "Continue breastfeeding on demand. Keep your baby warm and clean. "
        "Watch for any changes. If symptoms persist beyond 3 days or worsen, "
        "visit your clinic."
    ),
    Stage.INFANT: (
        "Continue breastfeeding and feeding as normal. Ensure your child "
        "drinks enough fluids. If symptoms persist beyond 3 days or worsen, "
        "visit your clinic."
    ),
    Stage.TODDLER: (
        "Your child can be cared for at home. Ensure they drink enough fluids "
        "and eat well. If symptoms persist beyond 3 days or worsen, visit your clinic."
    ),
    Stage.EARLY_CHILDHOOD: (
        "Your child can be cared for at home. Ensure they drink enough fluids "
        "and eat well. If symptoms persist beyond 3 days or worsen, visit your clinic."
    ),
    Stage.SCHOOL_AGE: (
        "Your child can be cared for at home. Ensure they rest, drink enough "
        "fluids, and eat well. If symptoms persist beyond 3 days or worsen, "
        "visit your clinic."
    ),
    Stage.ADOLESCENT: (
        "This can usually be managed at home with rest, fluids, and good "
        "meals. If symptoms persist beyond a few days or worsen, or if you "
        "are worried, talk to a health worker."
    ),
}


class TriageEngine:
    """Maps symptoms to triage levels with stage-specific clinical rules.

    This is the primary entry point for symptom assessment. It classifies
    symptoms into RED (immediate), YELLOW (24-48h), or GREEN (home care)
    and provides stage-appropriate action recommendations.

    Example:
        >>> result = TriageEngine.triage(
        ...     symptoms=["convulsions"],
        ...     stage=Stage.NEWBORN,
        ... )
        >>> result.level.value
        'red'
        >>> result = TriageEngine.triage(
        ...     symptoms=["common_cold", "runny_nose"],
        ...     stage=Stage.INFANT,
        ...     child_age_months=8,
        ... )
        >>> result.level.value
        'green'
    """

    @staticmethod
    def triage(
        symptoms: list[str],
        stage: Stage,
        pregnancy_week: int | None = None,
        child_age_months: int | None = None,
    ) -> TriageResult:
        """Triage a list of symptoms for a given care stage.

        Args:
            symptoms: List of symptom identifiers (e.g. ["fever", "fast_breathing"]).
            stage: Current care stage.
            pregnancy_week: Gestational week (only for PREGNANT stage).
            child_age_months: Child's age in months (for child stages).

        Returns:
            A TriageResult with level, assessment, action, and danger signs.

        Example:
            >>> result = TriageEngine.triage(
            ...     symptoms=["severe_bleeding"],
            ...     stage=Stage.PREGNANT,
            ...     pregnancy_week=32,
            ... )
            >>> result.level.value
            'red'
        """
        symptom_set = set(s.lower().strip() for s in symptoms)

        found_red: list[str] = []
        found_yellow: list[str] = []
        found_green: list[str] = []

        stage_red = _STAGE_RED_SYMPTOMS.get(stage, set())
        stage_yellow = _STAGE_YELLOW_SYMPTOMS.get(stage, set())

        for symptom in symptom_set:
            if symptom in _UNIVERSAL_RED_SYMPTOMS or symptom in stage_red:
                found_red.append(symptom)
            elif symptom in stage_yellow:
                found_yellow.append(symptom)
            elif symptom in _GREEN_SYMPTOMS:
                found_green.append(symptom)
            else:
                found_yellow.append(symptom)

        # Apply stage-specific adjustments
        found_red, found_yellow = _apply_stage_adjustments(
            found_red, found_yellow, found_green, symptom_set,
            stage, pregnancy_week, child_age_months,
        )

        if found_red:
            return TriageResult(
                level=TriageLevel.RED,
                assessment=_build_assessment(found_red, found_yellow, stage, "red"),
                recommended_action=_RED_ACTIONS[stage],
                danger_signs=found_red,
                follow_up_hours=0,
            )

        if found_yellow:
            follow_up = 24 if stage in (Stage.PREGNANT, Stage.NEWBORN) else 48
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=_build_assessment(found_red, found_yellow, stage, "yellow"),
                recommended_action=_YELLOW_ACTIONS[stage],
                danger_signs=[],
                follow_up_hours=follow_up,
            )

        return TriageResult(
            level=TriageLevel.GREEN,
            assessment=_build_assessment(found_red, found_yellow, stage, "green"),
            recommended_action=_GREEN_ACTIONS[stage],
            danger_signs=[],
            follow_up_hours=72,
        )


def _apply_stage_adjustments(
    found_red: list[str],
    found_yellow: list[str],
    found_green: list[str],
    symptom_set: set[str],
    stage: Stage,
    pregnancy_week: int | None,
    child_age_months: int | None,
) -> tuple[list[str], list[str]]:
    """Apply stage-specific and age-specific adjustments to triage levels.

    For example, any fever in a newborn is RED, not YELLOW.
    """
    # Pregnancy-specific: late pregnancy escalations
    if stage == Stage.PREGNANT and pregnancy_week is not None:
        if pregnancy_week >= 37:
            # Gush of fluid at term could be labour but also need assessment
            if "gush_of_fluid" in symptom_set and "gush_of_fluid" not in found_red:
                found_red.append("gush_of_fluid")
                if "gush_of_fluid" in found_yellow:
                    found_yellow.remove("gush_of_fluid")
        if pregnancy_week < 28:
            # Any bleeding before 28 weeks is RED
            if "mild_bleeding" in symptom_set:
                if "mild_bleeding" in found_yellow:
                    found_yellow.remove("mild_bleeding")
                if "mild_bleeding" not in found_red:
                    found_red.append("mild_bleeding")

    # Newborn: any fever is RED (not yellow)
    if stage == Stage.NEWBORN:
        fever_symptoms = {"fever", "mild_fever", "fever_low"}
        for fs in fever_symptoms:
            if fs in symptom_set:
                if fs in found_yellow:
                    found_yellow.remove(fs)
                if fs in found_green:
                    found_green.remove(fs)
                if fs not in found_red:
                    found_red.append(fs)

    # Infant under 2 months: fast breathing threshold is lower, escalate fever
    if stage == Stage.INFANT and child_age_months is not None and child_age_months < 2:
        fever_symptoms = {"fever", "mild_fever"}
        for fs in fever_symptoms:
            if fs in symptom_set:
                if fs in found_yellow:
                    found_yellow.remove(fs)
                if fs in found_green:
                    found_green.remove(fs)
                if fs not in found_red:
                    found_red.append(fs)

    # Multiple YELLOW symptoms in a young infant should escalate
    if stage == Stage.INFANT and child_age_months is not None and child_age_months < 6:
        if len(found_yellow) >= 3:
            # Escalate to RED when multiple concerning symptoms in young infant
            found_red.extend(found_yellow)
            found_yellow = []

    return found_red, found_yellow


def _build_assessment(
    red_signs: list[str],
    yellow_signs: list[str],
    stage: Stage,
    level: str,
) -> str:
    """Build a human-readable assessment summary."""
    stage_label = stage.value.replace("_", " ").title()

    if level == "red":
        sign_list = ", ".join(s.replace("_", " ") for s in red_signs)
        return (
            f"URGENT: Danger signs detected in {stage_label} stage: {sign_list}. "
            f"Immediate medical attention is required."
        )

    if level == "yellow":
        sign_list = ", ".join(s.replace("_", " ") for s in yellow_signs)
        return (
            f"Concerning symptoms in {stage_label} stage: {sign_list}. "
            f"A clinic visit is recommended within 24-48 hours."
        )

    return (
        f"Mild symptoms in {stage_label} stage that can be managed at home "
        f"with guidance. Monitor for any worsening."
    )
