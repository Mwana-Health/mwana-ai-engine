"""Age-appropriate injury prevention guidance.

Provides safety messages for each age group and seasonal injury risks
specific to the Zimbabwean context, including open fire burns, paraffin
poisoning, and drowning prevention.
"""

from __future__ import annotations


# Age-specific safety messages.
_SAFETY_MESSAGES: list[dict] = [
    # Newborn (0-1 month)
    {
        "min_age_months": 0,
        "max_age_months": 1,
        "category": "safe_sleeping",
        "message": "Always place your baby on their back to sleep, on a firm flat surface. Remove pillows, blankets, and soft toys from the sleeping area.",
        "risk": "Suffocation and sudden infant death",
    },
    {
        "min_age_months": 0,
        "max_age_months": 1,
        "category": "bed_sharing",
        "message": "If you share a bed with your baby, do not use heavy blankets. Never share a bed if you have been drinking alcohol or taking sedating medication. Keep baby away from pillows.",
        "risk": "Suffocation from overlay",
    },
    {
        "min_age_months": 0,
        "max_age_months": 1,
        "category": "thermal_safety",
        "message": "Keep your baby away from direct sunlight, fires, and hot objects. Test bath water with your elbow before bathing baby.",
        "risk": "Burns and overheating",
    },
    {
        "min_age_months": 0,
        "max_age_months": 1,
        "category": "transport",
        "message": "Support your baby's head and neck when carrying. Never leave a baby unattended on a bed, table, or raised surface.",
        "risk": "Falls and head injury",
    },
    # Infant (2-12 months)
    {
        "min_age_months": 2,
        "max_age_months": 5,
        "category": "choking",
        "message": "Keep small objects (coins, buttons, beads, seeds) away from your baby. Babies put everything in their mouths. Check the floor for small items.",
        "risk": "Choking and airway obstruction",
    },
    {
        "min_age_months": 2,
        "max_age_months": 12,
        "category": "falls",
        "message": "Never leave your baby alone on a bed, chair, or table. Use a safe sleeping mat on the floor if needed. Once baby starts rolling, they can fall from any raised surface.",
        "risk": "Falls and head injury",
    },
    {
        "min_age_months": 2,
        "max_age_months": 12,
        "category": "hot_liquids",
        "message": "Keep hot drinks (tea, porridge) away from your baby. Do not hold your baby while drinking or eating hot food. Place cooking pots at the back of the stove or fire.",
        "risk": "Burns from hot liquids (scalds)",
    },
    {
        "min_age_months": 6,
        "max_age_months": 12,
        "category": "choking_food",
        "message": "Cut food into small pieces. Avoid hard round foods (whole grapes, nuts, popcorn, raw carrots). Always supervise eating. Do not let baby eat lying down.",
        "risk": "Choking on food",
    },
    {
        "min_age_months": 6,
        "max_age_months": 12,
        "category": "water_safety",
        "message": "Never leave your baby alone near water, not even for a moment. Empty buckets, basins, and baths immediately after use. A baby can drown in just a few centimetres of water.",
        "risk": "Drowning",
    },
    {
        "min_age_months": 6,
        "max_age_months": 12,
        "category": "poisoning",
        "message": "Keep paraffin (kerosene), cleaning products, and medicines out of reach. NEVER store paraffin or chemicals in drink bottles - children will drink them.",
        "risk": "Poisoning (paraffin is the leading cause in Zimbabwe)",
    },
    # Toddler (12-36 months)
    {
        "min_age_months": 12,
        "max_age_months": 36,
        "category": "burns_fire",
        "message": "Keep your child away from open cooking fires, stoves, and braai stands. Use a barrier or guard around fires. Never leave a child alone in a room with an open fire or paraffin heater.",
        "risk": "Burns from open fires (leading cause of burns in Zimbabwe)",
    },
    {
        "min_age_months": 12,
        "max_age_months": 36,
        "category": "drowning",
        "message": "Never leave your child alone near water - rivers, dams, wells, buckets, or baths. Cover all water containers with lids. Fence wells and water sources if possible.",
        "risk": "Drowning (children this age are curious and mobile)",
    },
    {
        "min_age_months": 12,
        "max_age_months": 36,
        "category": "poisoning",
        "message": "Store all medicines, paraffin, pesticides, and cleaning products in a locked cupboard or high shelf. NEVER put paraffin or chemicals in drink bottles. If your child swallows something harmful, go to the hospital immediately and bring the container.",
        "risk": "Poisoning (paraffin/kerosene ingestion)",
    },
    {
        "min_age_months": 12,
        "max_age_months": 36,
        "category": "falls",
        "message": "Supervise your child on stairs, near windows, and on furniture. Toddlers climb on everything. Block access to stairs and dangerous areas.",
        "risk": "Falls from heights",
    },
    {
        "min_age_months": 12,
        "max_age_months": 36,
        "category": "choking",
        "message": "Keep small objects, coins, batteries, and nuts out of reach. Cut grapes, sausages, and other round foods in half lengthwise. Always supervise eating.",
        "risk": "Choking",
    },
    {
        "min_age_months": 12,
        "max_age_months": 36,
        "category": "electrical",
        "message": "Cover electrical outlets. Keep electrical cords out of reach. Do not let children play with electrical appliances or pull cords.",
        "risk": "Electrocution",
    },
    # Early Childhood (36-60 months)
    {
        "min_age_months": 36,
        "max_age_months": 60,
        "category": "road_safety",
        "message": "Always hold your child's hand near roads. Teach them to stop, look, and listen before crossing. Children this age cannot judge the speed of vehicles.",
        "risk": "Road traffic injuries",
    },
    {
        "min_age_months": 36,
        "max_age_months": 60,
        "category": "burns_fire",
        "message": "Keep matches and lighters out of reach. Teach children that fire is dangerous. Supervise around cooking fires and heaters. Have a plan for what to do if clothing catches fire (stop, drop, roll).",
        "risk": "Burns from fire",
    },
    {
        "min_age_months": 36,
        "max_age_months": 60,
        "category": "drowning",
        "message": "Teach your child basic water safety. Never let them swim or play near water without adult supervision. Cover wells, tanks, and water storage.",
        "risk": "Drowning",
    },
    {
        "min_age_months": 36,
        "max_age_months": 60,
        "category": "playground",
        "message": "Supervise your child at play. Check that play areas are safe and free from sharp objects, broken glass, and rubbish. Teach them about safe play with others.",
        "risk": "Playground injuries",
    },
    {
        "min_age_months": 36,
        "max_age_months": 60,
        "category": "poisoning",
        "message": "Continue to store chemicals and medicines out of reach. Teach your child not to eat unknown berries, mushrooms, or plants. If poisoning is suspected, go to hospital immediately with the substance container.",
        "risk": "Poisoning from chemicals or plants",
    },
    {
        "min_age_months": 36,
        "max_age_months": 60,
        "category": "animal_bites",
        "message": "Teach your child not to approach stray dogs or unfamiliar animals. If bitten by a dog, wash the wound with soap and water immediately and go to the clinic for rabies assessment.",
        "risk": "Animal bites and rabies",
    },
]

# Seasonal injury risks for Zimbabwe.
_SEASONAL_RISKS: dict[str, list[dict]] = {
    "winter": [
        {
            "risk": "Burns from open fires and heaters",
            "description": (
                "Winter in Zimbabwe (May-August) brings increased use of open "
                "fires and paraffin heaters. Burns are the leading cause of "
                "childhood injury death during this period."
            ),
            "prevention": [
                "Use guards or barriers around all fires and heaters",
                "Never leave children alone in a room with an open fire",
                "Keep paraffin heaters stable and away from curtains and bedding",
                "Do not dry clothes over open fires",
                "Teach children about fire safety",
            ],
        },
        {
            "risk": "Carbon monoxide poisoning",
            "description": (
                "Burning charcoal or wood in enclosed rooms for warmth can "
                "cause carbon monoxide poisoning, which is invisible and "
                "odourless."
            ),
            "prevention": [
                "Always ensure adequate ventilation when using fires for heating",
                "Never use a brazier (mbawula) in a closed room",
                "Open a window slightly even in cold weather",
                "If family members have headaches and drowsiness together, suspect CO poisoning",
            ],
        },
    ],
    "summer": [
        {
            "risk": "Drowning",
            "description": (
                "Summer rains (November-March) fill rivers, dams, and drainage "
                "channels. Flash floods create dangerous water conditions. "
                "Children are at highest risk of drowning."
            ),
            "prevention": [
                "Never let children play near swollen rivers or flooded areas",
                "Cover all water storage containers with lids",
                "Supervise children at all times near water",
                "Teach older children to swim if possible",
                "Empty buckets and baths after use",
            ],
        },
        {
            "risk": "Snakebite",
            "description": (
                "Snakes are more active during the warm, wet summer months. "
                "Children playing outside are at risk of snakebite."
            ),
            "prevention": [
                "Teach children to look where they walk and not reach into holes",
                "Clear tall grass and debris around the home",
                "Wear shoes outside, especially in the evening",
                "If bitten, keep calm, immobilise the limb, and go to hospital immediately",
                "Do not try traditional remedies or cut the bite - go to hospital",
            ],
        },
    ],
    "rainy": [
        {
            "risk": "Electrical injury",
            "description": (
                "During the rainy season, downed power lines and flooded "
                "electrical installations pose electrocution risks."
            ),
            "prevention": [
                "Keep children away from downed power lines",
                "Do not touch electrical equipment with wet hands",
                "Stay away from flooded areas near electrical infrastructure",
                "Report downed lines to ZESA",
            ],
        },
    ],
}


class InjuryPreventionEngine:
    """Age-appropriate injury prevention guidance for Zimbabwe.

    Provides safety messages based on the child's age and seasonal
    injury risks specific to the Zimbabwean context.

    Example:
        >>> engine = InjuryPreventionEngine()
        >>> messages = engine.get_safety_messages(child_age_months=18)
        >>> len(messages) > 0
        True
    """

    @staticmethod
    def get_safety_messages(child_age_months: int) -> list[dict]:
        """Get age-appropriate safety messages.

        Args:
            child_age_months: The child's age in months.

        Returns:
            List of safety message dictionaries with category, message,
            and risk description.

        Example:
            >>> messages = InjuryPreventionEngine.get_safety_messages(8)
            >>> categories = [m["category"] for m in messages]
            >>> "choking_food" in categories
            True
        """
        return [
            {
                "category": msg["category"],
                "message": msg["message"],
                "risk": msg["risk"],
            }
            for msg in _SAFETY_MESSAGES
            if msg["min_age_months"] <= child_age_months <= msg["max_age_months"]
        ]

    @staticmethod
    def get_seasonal_injury_risks(season: str) -> list[dict]:
        """Get seasonal injury risks for Zimbabwe.

        Args:
            season: One of "winter" (May-August), "summer" (November-March),
                   or "rainy" (November-March, overlaps with summer).

        Returns:
            List of seasonal risk dictionaries with risk, description,
            and prevention measures.

        Example:
            >>> risks = InjuryPreventionEngine.get_seasonal_injury_risks("winter")
            >>> risks[0]["risk"]
            'Burns from open fires and heaters'
        """
        season_lower = season.lower().strip()
        return list(_SEASONAL_RISKS.get(season_lower, []))
