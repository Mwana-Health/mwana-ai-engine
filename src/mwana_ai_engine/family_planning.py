"""Postpartum family planning advisory.

Provides guidance on contraceptive methods appropriate for postpartum
women, with considerations for breastfeeding and timing. Based on
WHO Medical Eligibility Criteria for contraceptive use.
"""

from __future__ import annotations


_METHODS: list[dict] = [
    {
        "name": "Lactational Amenorrhoea Method (LAM)",
        "code": "lam",
        "description": (
            "A natural family planning method that relies on exclusive "
            "breastfeeding to suppress ovulation. Effective only when "
            "ALL three criteria are met."
        ),
        "criteria": [
            "Baby is less than 6 months old",
            "Mother is exclusively breastfeeding (no formula, water, or food)",
            "Mother's menstrual period has not returned",
        ],
        "effectiveness": "98% when all criteria are met",
        "breastfeeding_safe": True,
        "earliest_postpartum_weeks": 0,
        "max_postpartum_months": 6,
        "side_effects": [],
        "notes": (
            "When any of the three criteria are no longer met, switch to "
            "another method. LAM is a bridge method while you decide on "
            "a longer-term option."
        ),
    },
    {
        "name": "Copper IUD (Intrauterine Device)",
        "code": "copper_iud",
        "description": (
            "A small device placed in the uterus by a trained health "
            "worker. Provides long-acting, non-hormonal contraception "
            "for up to 12 years."
        ),
        "criteria": [
            "Can be inserted within 48 hours of delivery, or after 4 weeks postpartum",
            "Safe during breastfeeding",
            "Does not affect milk supply",
        ],
        "effectiveness": "Over 99%",
        "breastfeeding_safe": True,
        "earliest_postpartum_weeks": 0,
        "max_postpartum_months": None,
        "side_effects": [
            "Heavier or longer periods (common in first few months)",
            "Period cramps may increase",
        ],
        "notes": (
            "Can be removed at any time if you want to become pregnant. "
            "Fertility returns immediately. Available at most clinics."
        ),
    },
    {
        "name": "Progestin-Only Pills (Mini-pill)",
        "code": "pop",
        "description": (
            "A daily pill containing only progestin hormone. Safe during "
            "breastfeeding and does not affect milk supply."
        ),
        "criteria": [
            "Safe to start from 6 weeks postpartum (or earlier if not breastfeeding)",
            "Must be taken at the same time every day",
            "Safe during breastfeeding",
        ],
        "effectiveness": "91-99% depending on consistent use",
        "breastfeeding_safe": True,
        "earliest_postpartum_weeks": 6,
        "max_postpartum_months": None,
        "side_effects": [
            "Irregular bleeding or spotting",
            "Headaches (usually mild)",
            "May stop periods completely (this is normal and safe)",
        ],
        "notes": (
            "Must be taken at the same time every day to be effective. "
            "Set a daily alarm as a reminder. Available at clinics and "
            "pharmacies."
        ),
    },
    {
        "name": "Combined Oral Contraceptive Pills",
        "code": "coc",
        "description": (
            "Daily pills containing both estrogen and progestin hormones. "
            "NOT recommended during breastfeeding in the first 6 months."
        ),
        "criteria": [
            "NOT recommended if breastfeeding and baby is under 6 months",
            "Can start from 6 months postpartum if breastfeeding",
            "Can start from 3 weeks postpartum if NOT breastfeeding",
        ],
        "effectiveness": "91-99% depending on consistent use",
        "breastfeeding_safe": False,
        "earliest_postpartum_weeks": 24,
        "max_postpartum_months": None,
        "side_effects": [
            "May reduce milk supply",
            "Nausea (usually goes away after first month)",
            "Headaches",
            "Breast tenderness",
        ],
        "notes": (
            "NOT for breastfeeding mothers with babies under 6 months. "
            "The estrogen can reduce milk supply. Use progestin-only "
            "methods instead if breastfeeding."
        ),
    },
    {
        "name": "Injectable (Depo-Provera / DMPA)",
        "code": "injectable",
        "description": (
            "An injection given every 3 months (12 weeks) at the clinic. "
            "Contains progestin only, safe during breastfeeding."
        ),
        "criteria": [
            "Can start from 6 weeks postpartum",
            "Safe during breastfeeding",
            "Does not affect milk supply",
        ],
        "effectiveness": "Over 99% with on-time injections",
        "breastfeeding_safe": True,
        "earliest_postpartum_weeks": 6,
        "max_postpartum_months": None,
        "side_effects": [
            "Irregular bleeding or spotting (common in first few months)",
            "Periods may stop completely (this is normal and safe)",
            "Weight gain (some women)",
            "Return to fertility may take 6-12 months after stopping",
        ],
        "notes": (
            "Very popular in Zimbabwe. You need to return to the clinic "
            "every 12 weeks for your injection. Set a reminder. If you "
            "are late by more than 2 weeks, use condoms until your "
            "next injection."
        ),
    },
    {
        "name": "Implant (Jadelle / Implanon)",
        "code": "implant",
        "description": (
            "Small flexible rods inserted under the skin of the upper arm "
            "by a trained health worker. Provides long-acting contraception "
            "for 3-5 years."
        ),
        "criteria": [
            "Can be inserted from 6 weeks postpartum",
            "Safe during breastfeeding",
            "Does not affect milk supply",
        ],
        "effectiveness": "Over 99%",
        "breastfeeding_safe": True,
        "earliest_postpartum_weeks": 6,
        "max_postpartum_months": None,
        "side_effects": [
            "Irregular bleeding or spotting (common)",
            "Headaches",
            "Periods may stop completely (this is safe)",
            "Bruising at insertion site",
        ],
        "notes": (
            "Very effective and long-lasting. Can be removed at any time "
            "if you want to become pregnant or switch methods. Fertility "
            "returns quickly after removal. Available at district hospitals "
            "and some clinics."
        ),
    },
    {
        "name": "Male Condom",
        "code": "condom_male",
        "description": (
            "A barrier method worn by the man during intercourse. Also "
            "protects against STIs and HIV."
        ),
        "criteria": [
            "Can be used at any time",
            "Safe during breastfeeding",
            "Also protects against HIV and STIs",
        ],
        "effectiveness": "82-98% depending on correct and consistent use",
        "breastfeeding_safe": True,
        "earliest_postpartum_weeks": 0,
        "max_postpartum_months": None,
        "side_effects": [],
        "notes": (
            "Free condoms are available at clinics, hospitals, and many "
            "public places in Zimbabwe. Can be used alone or with another "
            "method for extra protection. Use a new condom every time."
        ),
    },
    {
        "name": "Female Condom",
        "code": "condom_female",
        "description": (
            "A barrier method inserted by the woman before intercourse. "
            "Also protects against STIs and HIV."
        ),
        "criteria": [
            "Can be used at any time",
            "Safe during breastfeeding",
            "Also protects against HIV and STIs",
            "Can be inserted up to 8 hours before intercourse",
        ],
        "effectiveness": "79-95% depending on correct and consistent use",
        "breastfeeding_safe": True,
        "earliest_postpartum_weeks": 0,
        "max_postpartum_months": None,
        "side_effects": [],
        "notes": (
            "Available at clinics. Gives the woman control over STI/HIV "
            "protection. Can be used if the partner refuses male condoms."
        ),
    },
]

_BIRTH_SPACING_GUIDANCE = (
    "The World Health Organization recommends waiting at least 24 months "
    "(2 years) between a live birth and the next pregnancy. This gives "
    "your body time to fully recover and reduces risks for both you and "
    "your next baby. After a miscarriage or abortion, wait at least 6 "
    "months before the next pregnancy. Short intervals between pregnancies "
    "increase the risk of premature birth, low birth weight, and maternal "
    "complications."
)


class FamilyPlanningAdvisor:
    """Postpartum family planning guidance.

    Provides information on contraceptive methods appropriate for
    postpartum women, considering breastfeeding status and timing.

    Example:
        >>> advisor = FamilyPlanningAdvisor()
        >>> methods = advisor.get_methods(breastfeeding=True, postpartum_weeks=8)
        >>> [m["name"] for m in methods]
        ['Lactational Amenorrhoea Method (LAM)', 'Copper IUD ...', ...]
    """

    @staticmethod
    def get_methods(
        breastfeeding: bool,
        postpartum_weeks: int,
    ) -> list[dict]:
        """Get available family planning methods for current circumstances.

        Filters methods based on breastfeeding status and weeks since
        delivery, returning only those that are safe and appropriate.

        Args:
            breastfeeding: Whether the mother is currently breastfeeding.
            postpartum_weeks: Weeks since delivery.

        Returns:
            List of method dictionaries with name, description, criteria,
            effectiveness, side_effects, and notes.

        Example:
            >>> methods = FamilyPlanningAdvisor.get_methods(
            ...     breastfeeding=True,
            ...     postpartum_weeks=4,
            ... )
            >>> any(m["code"] == "coc" for m in methods)
            False
        """
        postpartum_months = postpartum_weeks / 4.33

        available: list[dict] = []
        for method in _METHODS:
            # Skip methods that are not safe during breastfeeding
            if breastfeeding and not method["breastfeeding_safe"]:
                continue

            # Skip methods that cannot be started yet
            if postpartum_weeks < method["earliest_postpartum_weeks"]:
                continue

            # Skip LAM if past 6 months
            if method["code"] == "lam" and postpartum_months > 6:
                continue

            # Skip LAM if not breastfeeding
            if method["code"] == "lam" and not breastfeeding:
                continue

            available.append({
                "name": method["name"],
                "code": method["code"],
                "description": method["description"],
                "criteria": list(method["criteria"]),
                "effectiveness": method["effectiveness"],
                "breastfeeding_safe": method["breastfeeding_safe"],
                "side_effects": list(method["side_effects"]),
                "notes": method["notes"],
            })

        return available

    @staticmethod
    def get_birth_spacing_guidance() -> str:
        """Get WHO birth spacing guidance.

        Returns:
            Birth spacing recommendation text.

        Example:
            >>> guidance = FamilyPlanningAdvisor.get_birth_spacing_guidance()
            >>> "24 months" in guidance
            True
        """
        return _BIRTH_SPACING_GUIDANCE
