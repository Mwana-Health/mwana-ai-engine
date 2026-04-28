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
