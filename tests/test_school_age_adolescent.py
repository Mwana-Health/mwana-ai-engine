"""Tests for the school-age (6-12y) and adolescent (13-17y) stages.

Focus areas:
- Stage boundary determination (5y11m vs 6y0m vs 12y11m vs 13y vs 17y vs 18y).
- Stage transitions across the new boundaries.
- Verified immunization additions (Td booster at 10y, HPV for girls at 10/11y),
  including girl-only filtering.
- General (non-IMCI) danger-sign triage for the new stages, with the
  uncertainty-defaults-YELLOW and RED-always-refers fail-safes.
- Growth for 5-19 year-olds is recorded WITHOUT under-5 z-scores.
- New nutrition and wellbeing content is present and marked pending sign-off.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from mwana_ai_engine import (
    DangerSignDetector,
    DevelopmentalMilestones,
    GrowthMonitor,
    ImmunizationScheduler,
    NutritionAdvisor,
    Stage,
    StageManager,
    TriageEngine,
    TriageLevel,
)


def _dob_years_months_ago(years: int, months: int = 0) -> date:
    """Return a DOB that is exactly `years` years and `months` months ago.

    Uses calendar arithmetic (not 365-day approximation) so month-boundary
    tests are exact.
    """
    today = date.today()
    total_months = years * 12 + months
    y = today.year - (total_months // 12)
    m = today.month - (total_months % 12)
    if m <= 0:
        m += 12
        y -= 1
    # Clamp day to 28 to avoid invalid dates (e.g. 31 -> Feb).
    return date(y, m, min(today.day, 28))


# --------------------------------------------------------------------------- #
# Stage boundaries
# --------------------------------------------------------------------------- #

class TestStageBoundaries:
    def test_five_years_eleven_months_is_early_childhood(self):
        dob = _dob_years_months_ago(5, 11)
        assert StageManager.determine_stage(child_dob=dob) == Stage.EARLY_CHILDHOOD

    def test_six_years_exactly_is_school_age(self):
        dob = _dob_years_months_ago(6, 0)
        assert StageManager.determine_stage(child_dob=dob) == Stage.SCHOOL_AGE

    def test_eight_years_is_school_age(self):
        dob = _dob_years_months_ago(8, 0)
        assert StageManager.determine_stage(child_dob=dob) == Stage.SCHOOL_AGE

    def test_twelve_years_eleven_months_is_school_age(self):
        dob = _dob_years_months_ago(12, 11)
        assert StageManager.determine_stage(child_dob=dob) == Stage.SCHOOL_AGE

    def test_thirteen_years_is_adolescent(self):
        dob = _dob_years_months_ago(13, 0)
        assert StageManager.determine_stage(child_dob=dob) == Stage.ADOLESCENT

    def test_seventeen_years_is_adolescent(self):
        dob = _dob_years_months_ago(17, 0)
        assert StageManager.determine_stage(child_dob=dob) == Stage.ADOLESCENT

    def test_eighteen_years_caps_at_adolescent(self):
        # Beyond the journey; capped so downstream never raises.
        dob = _dob_years_months_ago(18, 0)
        assert StageManager.determine_stage(child_dob=dob) == Stage.ADOLESCENT

    def test_under_five_stages_unchanged(self):
        # Regression: existing stages still map correctly.
        assert StageManager.determine_stage(
            child_dob=date.today()
        ) == Stage.NEWBORN
        assert StageManager.determine_stage(
            child_dob=_dob_years_months_ago(0, 6)
        ) == Stage.INFANT
        assert StageManager.determine_stage(
            child_dob=_dob_years_months_ago(2, 0)
        ) == Stage.TODDLER
        assert StageManager.determine_stage(
            child_dob=_dob_years_months_ago(4, 0)
        ) == Stage.EARLY_CHILDHOOD


class TestStageTransitions:
    def test_early_childhood_transitions_to_school_age(self):
        # A "5y11m" child recorded as EARLY_CHILDHOOD, aged to 6y0m, transitions.
        dob = _dob_years_months_ago(6, 0)
        assert StageManager.should_transition(
            Stage.EARLY_CHILDHOOD, child_dob=dob
        ) == Stage.SCHOOL_AGE

    def test_no_transition_within_school_age(self):
        dob = _dob_years_months_ago(8, 0)
        assert StageManager.should_transition(
            Stage.SCHOOL_AGE, child_dob=dob
        ) is None

    def test_school_age_transitions_to_adolescent(self):
        dob = _dob_years_months_ago(13, 0)
        assert StageManager.should_transition(
            Stage.SCHOOL_AGE, child_dob=dob
        ) == Stage.ADOLESCENT


class TestStageContent:
    @pytest.mark.parametrize("stage", [Stage.SCHOOL_AGE, Stage.ADOLESCENT])
    def test_content_present_and_pending_signoff(self, stage):
        content = StageManager.get_stage_content(stage)
        assert content["themes"]
        assert content["key_topics"]
        assert content["pending_clinical_signoff"] is True

    def test_adolescent_content_is_conservative(self):
        content = StageManager.get_stage_content(Stage.ADOLESCENT)
        topics = content["key_topics"]
        # Conservative: signposts to a health worker, no explicit SRH content.
        assert "talk_to_a_health_worker" in topics
        assert "menstrual_health" in topics
        assert "iron_for_girls" in topics


# --------------------------------------------------------------------------- #
# Immunization
# --------------------------------------------------------------------------- #

class TestImmunizationOlderChildren:
    def test_td_booster_10y_in_schedule(self):
        codes = [d.vaccine_code for d in ImmunizationScheduler().get_schedule(date.today())]
        assert "Td_booster2" in codes

    def test_hpv_present_for_girls(self):
        scheduler = ImmunizationScheduler()
        dob = date.today()
        girl_codes = [d.vaccine_code for d in scheduler.get_schedule(dob, sex="female")]
        assert "HPV1" in girl_codes
        assert "HPV2" in girl_codes

    def test_hpv_excluded_for_boys(self):
        scheduler = ImmunizationScheduler()
        dob = date.today()
        boy_codes = [d.vaccine_code for d in scheduler.get_schedule(dob, sex="male")]
        assert "HPV1" not in boy_codes
        assert "HPV2" not in boy_codes
        # Td booster applies to all.
        assert "Td_booster2" in boy_codes

    def test_hpv_surfaced_when_sex_unknown(self):
        # Never silently dropped when sex is not recorded.
        scheduler = ImmunizationScheduler()
        codes = [d.vaccine_code for d in scheduler.get_schedule(date.today(), sex=None)]
        assert "HPV1" in codes

    def test_hpv_due_dates_10_and_11_years(self):
        scheduler = ImmunizationScheduler()
        dob = date(2015, 1, 1)
        by_code = {d.vaccine_code: d for d in scheduler.get_schedule(dob, sex="female")}
        # Dose 1 at ~10y (520 weeks), dose 2 ~1 year later.
        assert by_code["HPV1"].scheduled_age_weeks == 520
        assert by_code["HPV2"].scheduled_age_weeks == 572
        delta_days = (by_code["HPV2"].scheduled_date - by_code["HPV1"].scheduled_date).days
        assert 360 <= delta_days <= 370  # ~12 months apart

    def test_next_due_for_ten_year_old_girl(self):
        # A 10-year-old girl with early doses done should be due Td/HPV.
        scheduler = ImmunizationScheduler()
        dob = _dob_years_months_ago(10, 1)
        completed = ["BCG", "HepB_birth", "OPV1", "Penta1", "MR1", "MR2", "Td_booster"]
        due = scheduler.get_next_due(dob, completed, sex="female")
        assert due is not None
        assert due.vaccine_code in {"Td_booster2", "HPV1"}

    def test_infant_schedule_regression_unchanged(self):
        # Existing under-2 vaccine behaviour is not altered.
        scheduler = ImmunizationScheduler()
        dob = date.today()
        due = scheduler.get_next_due(dob, completed_codes=["BCG", "HepB_birth"])
        assert due is not None
        assert due.vaccine_code == "OPV1"


# --------------------------------------------------------------------------- #
# Triage / danger signs (general, non-IMCI)
# --------------------------------------------------------------------------- #

class TestDangerSignsOlderChildren:
    @pytest.mark.parametrize("stage", [Stage.SCHOOL_AGE, Stage.ADOLESCENT])
    def test_danger_sign_list_present_and_non_imci(self, stage):
        signs = DangerSignDetector.get_danger_signs(stage)
        assert signs
        symptoms = {s["symptom"] for s in signs}
        # No IMCI breathing-rate cutoffs for older children.
        assert "fast_breathing" not in symptoms
        assert "chest_indrawing" not in symptoms
        # General danger signs are present instead.
        assert "severe_difficulty_breathing" in symptoms
        assert "convulsions" in symptoms

    def test_red_danger_sign_refers(self):
        result = DangerSignDetector.check_symptoms(
            ["convulsions"], Stage.SCHOOL_AGE
        )
        assert result.level == TriageLevel.RED
        assert result.follow_up_hours == 0

    def test_adolescent_self_harm_is_red(self):
        result = DangerSignDetector.check_symptoms(
            ["wants to die"], Stage.ADOLESCENT
        )
        assert result.level == TriageLevel.RED

    def test_wellbeing_concern_is_yellow(self):
        result = DangerSignDetector.check_symptoms(
            ["very sad"], Stage.ADOLESCENT
        )
        assert result.level == TriageLevel.YELLOW


class TestTriageOlderChildren:
    def test_universal_red_symptom(self):
        result = TriageEngine.triage(["convulsions"], Stage.SCHOOL_AGE)
        assert result.level == TriageLevel.RED

    def test_general_red_symptom(self):
        result = TriageEngine.triage(
            ["severe_difficulty_breathing"], Stage.ADOLESCENT
        )
        assert result.level == TriageLevel.RED

    def test_unknown_symptom_defaults_yellow_not_green(self):
        # Fail-safe: uncertainty never returns GREEN for the new stages.
        result = TriageEngine.triage(
            ["some_unrecognised_symptom_xyz"], Stage.SCHOOL_AGE
        )
        assert result.level == TriageLevel.YELLOW

    def test_no_imci_escalation_for_school_age(self):
        # A single yellow-ish concern stays YELLOW; no infant multi-symptom
        # RED escalation applies to older children.
        result = TriageEngine.triage(
            ["persistent_fever", "persistent_cough", "vision_concern"],
            Stage.SCHOOL_AGE,
        )
        assert result.level == TriageLevel.YELLOW

    def test_action_strings_exist_for_new_stages(self):
        for stage in (Stage.SCHOOL_AGE, Stage.ADOLESCENT):
            red = TriageEngine.triage(["convulsions"], stage)
            assert red.recommended_action
            green = TriageEngine.triage(["common_cold"], stage)
            assert green.recommended_action


# --------------------------------------------------------------------------- #
# Growth (5-19y must NOT use under-5 z-scores)
# --------------------------------------------------------------------------- #

class TestGrowthOlderChildren:
    def test_school_age_recorded_without_zscores(self):
        result = GrowthMonitor.assess_growth(
            weight_grams=26000, height_cm=128.0, age_months=96, gender="male"
        )
        assert result.weight_for_age_z == 0.0
        assert result.height_for_age_z == 0.0
        assert result.muac_status is None
        assert "clinical review" in result.interpretation.lower()

    def test_adolescent_recorded_without_zscores(self):
        result = GrowthMonitor.assess_growth(
            weight_grams=50000, height_cm=160.0, age_months=180, gender="female"
        )
        assert result.weight_for_age_z == 0.0
        assert "clinical review" in result.interpretation.lower()

    def test_under_five_growth_still_classified(self):
        # Regression: a young infant still gets a real z-score assessment.
        result = GrowthMonitor.assess_growth(
            weight_grams=7900, height_cm=67.6, age_months=6, gender="male"
        )
        # Real z-scores are computed (interpretation is a real classification).
        assert result.interpretation
        assert "clinical review" not in result.interpretation.lower()


# --------------------------------------------------------------------------- #
# Nutrition + wellbeing content
# --------------------------------------------------------------------------- #

class TestNutritionOlderChildren:
    def test_school_age_feeding_guidance(self):
        g = NutritionAdvisor.get_feeding_guidance(96)  # 8 years
        assert "school-age" in g["description"].lower()
        assert g["key_messages"]

    def test_adolescent_feeding_guidance(self):
        g = NutritionAdvisor.get_feeding_guidance(180)  # 15 years
        assert "adolescent" in g["description"].lower()

    def test_school_meal_guidance(self):
        g = NutritionAdvisor.get_school_meal_guidance()
        assert g["key_messages"]
        assert g["local_ideas"]
        assert g["pending_clinical_signoff"] is True

    def test_iron_guidance_for_girls(self):
        g = NutritionAdvisor.get_adolescent_iron_guidance(is_girl=True)
        joined = " ".join(g["iron_rich_foods"]).lower()
        assert "beans" in joined
        assert any("iron" in m.lower() or "period" in m.lower() for m in g["key_messages"])
        assert g["pending_clinical_signoff"] is True

    def test_no_breastfeeding_message_for_older_children(self):
        g = NutritionAdvisor.get_feeding_guidance(96)
        assert "breastfeed" not in g["breastfeeding_advice"].lower()


class TestWellbeingCheckpoints:
    def test_school_age_checkpoints(self):
        checks = DevelopmentalMilestones().get_school_age_wellbeing_checkpoints()
        domains = {c["domain"] for c in checks}
        assert {"learning", "vision", "hearing", "growth"} <= domains

    def test_adolescent_checkpoints(self):
        checks = DevelopmentalMilestones().get_adolescent_wellbeing_checkpoints()
        domains = {c["domain"] for c in checks}
        assert {"nutrition", "menstrual", "emotional"} <= domains

    def test_assess_wellbeing_concern_returns_guidance(self):
        res = DevelopmentalMilestones.assess_wellbeing("vision", concern=True)
        assert res["concern"] is True
        assert res["guidance"]

    def test_assess_wellbeing_unknown_key_raises(self):
        with pytest.raises(ValueError):
            DevelopmentalMilestones.assess_wellbeing("not_a_key", concern=True)
