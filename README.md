# mwana-ai-engine

A reusable, open-source maternal-child health AI engine for Zimbabwe. Provides clinical decision support for symptom triage, immunization scheduling, growth monitoring, developmental milestones, nutrition guidance, postnatal depression screening, and more.

Built on WHO IMCI guidelines, the Zimbabwe Expanded Programme on Immunization (EPI), and validated clinical tools adapted for the Zimbabwean context.

## Installation

```bash
pip install mwana-ai-engine
```

## Quick Start

```python
from datetime import date
from mwana_ai_engine import (
    TriageEngine,
    ImmunizationScheduler,
    GrowthMonitor,
    DevelopmentalMilestones,
    NutritionAdvisor,
    EPDSScreening,
    StageManager,
    Stage,
)

# Determine the care stage
stage = StageManager.determine_stage(child_dob=date(2026, 1, 15))

# Triage symptoms
result = TriageEngine.triage(
    symptoms=["fever", "fast_breathing"],
    stage=stage,
    child_age_months=4,
)
print(result.level)  # TriageLevel.YELLOW

# Check immunizations
scheduler = ImmunizationScheduler()
due = scheduler.get_next_due(
    date_of_birth=date(2026, 1, 15),
    completed_codes=["BCG", "HepB_birth"],
)
print(due.vaccine_name)  # "Oral Polio Vaccine"

# Monitor growth
monitor = GrowthMonitor()
assessment = monitor.assess_growth(
    weight_grams=7200,
    height_cm=67.0,
    age_months=6,
    gender="male",
)
print(assessment.interpretation)

# Screen for postnatal depression
epds = EPDSScreening()
score = epds.calculate_score([0, 1, 1, 0, 0, 1, 1, 0, 0, 0])
result = epds.interpret_score(score)
print(result["level"])  # "low"
```

## Care stages

The engine models the maternal-child health journey as a sequence of stages.
`StageManager.determine_stage(...)` selects the stage from pregnancy status or
the child's age.

| Stage | Age range | Notes |
|-------|-----------|-------|
| `PREGNANT` | Before delivery | Antenatal care, danger signs |
| `NEWBORN` | 0 to 28 days | WHO IMCI applies |
| `INFANT` | 29 days to under 12 months | WHO IMCI applies |
| `TODDLER` | 1 to under 3 years | WHO IMCI applies |
| `EARLY_CHILDHOOD` | 3 to under 6 years | WHO IMCI applies (under-5) |
| `SCHOOL_AGE` | 6 to under 13 years (6-12) | General danger signs, **not** IMCI |
| `ADOLESCENT` | 13 to under 18 years (13-17) | General danger signs, conservative content |

**Clinical safety note:** WHO IMCI (breathing-rate and age cutoffs) is designed
for children under 5. The `SCHOOL_AGE` and `ADOLESCENT` stages therefore use
general danger-sign guidance only (severe difficulty breathing, convulsions,
unresponsiveness, severe dehydration, high persistent fever, severe injury),
never IMCI cutoffs. When triage is uncertain the result defaults to `YELLOW`
(never green); `RED` always refers. Growth for 5-19 year-olds uses WHO
BMI-for-age (a different standard, not bundled), so `assess_growth` records
older children's measurements without applying under-5 z-scores and flags them
for clinical review. School-age and adolescent content sets carry a
`pending_clinical_signoff` marker pending advisory-panel review.

## Modules

| Module | Class | Purpose |
|--------|-------|---------|
| `triage` | `TriageEngine` | Symptom to GREEN/YELLOW/RED triage |
| `imci` | `IMCIAssessment` | WHO Integrated Management of Childhood Illness |
| `immunization` | `ImmunizationScheduler` | Zimbabwe EPI schedule and catch-up plans |
| `milestones` | `DevelopmentalMilestones` | Developmental milestone tracking |
| `growth` | `GrowthMonitor` | WHO z-score growth monitoring and MUAC |
| `nutrition` | `NutritionAdvisor` | IYCF feeding guidance with local foods |
| `epds` | `EPDSScreening` | Edinburgh Postnatal Depression Scale |
| `danger_signs` | `DangerSignDetector` | Stage-specific danger sign checklists |
| `climate` | `ClimateRiskScorer` | Climate-health risk scoring |
| `injury_prevention` | `InjuryPreventionEngine` | Age-appropriate safety messages |
| `family_planning` | `FamilyPlanningAdvisor` | Postpartum family planning guidance |
| `translation` | `TranslationService` | EN/SN/ND health translations |
| `stages` | `StageManager` | Automatic stage transitions |
| `prompts` | Clinical guardrail system prompts | LLM safety prompts |

## Design Principles

- **Pure functions**: No database access, no API calls, no side effects
- **Type-safe**: Full type hints with dataclasses and enums
- **Evidence-based**: WHO IMCI, Zimbabwe EPI, validated EPDS
- **Context-aware**: Zimbabwe-specific foods, clinics, and health programmes
- **Language support**: English, Shona, and Ndebele translations
- **Pip-installable**: Standard Python package, no heavy dependencies

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details.

If you use this software, please include the NOTICE file and attribute:

> Powered by [Mwana AI Engine](https://github.com/Mwana-Health/mwana-ai-engine)

"Mwana Health" and the Mwana Health logo are trademarks of Mwana Technologies (Pvt) Ltd. See NOTICE for trademark policy.
