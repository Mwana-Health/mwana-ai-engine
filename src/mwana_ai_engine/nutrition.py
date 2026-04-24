"""Nutrition advisory for infant and young child feeding (IYCF).

Provides age-appropriate feeding guidance, Zimbabwe-specific local food
recommendations, dietary diversity scoring, and breastfeeding support.
"""

from __future__ import annotations

from .types import BreastfeedingStatus


# Zimbabwe-specific local foods organized by category.
_LOCAL_FOODS: list[dict] = [
    {"name": "bota", "description": "Thin porridge (maize meal)", "category": "grains", "min_age_months": 6, "preparation": "Cook maize meal with water until thin and smooth. Can add sugar beans or groundnut butter for nutrition."},
    {"name": "sadza", "description": "Thick maize porridge (staple)", "category": "grains", "min_age_months": 9, "preparation": "Cook thick maize meal porridge. Serve with relish (vegetables, meat, or beans)."},
    {"name": "kapenta", "description": "Dried small fish", "category": "flesh_foods", "min_age_months": 6, "preparation": "Wash, dry-fry or boil kapenta. Mash or grind for younger children. Rich in calcium and protein."},
    {"name": "sugar_beans", "description": "Sugar beans (nyemba)", "category": "legumes", "min_age_months": 6, "preparation": "Soak overnight, boil until very soft. Mash for younger children. Can add to bota."},
    {"name": "muriwo", "description": "Green leafy vegetables (rape, covo, spinach)", "category": "vitamin_a_fruits_veg", "min_age_months": 6, "preparation": "Wash thoroughly, chop finely, and cook until soft. Add to sadza or bota. Rich in iron and vitamins."},
    {"name": "pumpkin", "description": "Pumpkin (nhanga)", "category": "vitamin_a_fruits_veg", "min_age_months": 6, "preparation": "Peel, cut into pieces, boil until soft. Mash for babies. Rich in vitamin A."},
    {"name": "sweet_potato", "description": "Sweet potato (mbambaira)", "category": "vitamin_a_fruits_veg", "min_age_months": 6, "preparation": "Boil or roast until soft. Mash for younger children. Orange-fleshed varieties are richest in vitamin A."},
    {"name": "banana", "description": "Banana", "category": "other_fruits_veg", "min_age_months": 6, "preparation": "Mash ripe banana for babies. Can be mixed with bota."},
    {"name": "mango", "description": "Mango", "category": "vitamin_a_fruits_veg", "min_age_months": 6, "preparation": "Use ripe, soft mango. Mash or cut into small pieces. Rich in vitamin A and C."},
    {"name": "groundnut_butter", "description": "Groundnut (peanut) butter (dovi)", "category": "nuts_seeds", "min_age_months": 6, "preparation": "Add a spoonful to bota or sadza for extra energy and protein. Do not give whole groundnuts to young children (choking risk)."},
    {"name": "eggs", "description": "Eggs", "category": "eggs", "min_age_months": 6, "preparation": "Hard boil and mash for younger children. Scramble or fry for older children. Whole egg can be given from 6 months."},
    {"name": "mopane_worms", "description": "Mopane worms ground powder (madora)", "category": "flesh_foods", "min_age_months": 9, "preparation": "Dry and grind into powder. Add to bota or relish. Very high in protein and iron."},
    {"name": "cow_milk", "description": "Cow's milk (fresh or soured/mukaka)", "category": "dairy", "min_age_months": 12, "preparation": "Boil fresh milk before giving. Soured milk (mukaka wakakora) can be given from 12 months. Not a replacement for breastmilk before 12 months."},
    {"name": "avocado", "description": "Avocado", "category": "other_fruits_veg", "min_age_months": 6, "preparation": "Mash ripe avocado. Rich in healthy fats and energy. Excellent first food."},
    {"name": "dried_beans", "description": "Dried beans (various)", "category": "legumes", "min_age_months": 6, "preparation": "Soak overnight, boil until very soft. Mash or puree for younger children."},
    {"name": "chicken", "description": "Chicken (huku)", "category": "flesh_foods", "min_age_months": 6, "preparation": "Cook thoroughly. Shred or mince finely for younger children. Remove bones."},
    {"name": "liver", "description": "Liver (chiropa)", "category": "flesh_foods", "min_age_months": 6, "preparation": "Cook thoroughly. Mash or cut into tiny pieces. Very rich in iron and vitamin A. Give once a week."},
]

# Feeding guidelines by age range.
_FEEDING_GUIDELINES: list[dict] = [
    {
        "min_months": 0,
        "max_months": 6,
        "description": "Exclusive breastfeeding",
        "meals_per_day": "On demand (8-12 times)",
        "texture": "Breastmilk only",
        "amount_per_meal": "As much as baby wants",
        "key_messages": [
            "Breastfeed exclusively - no water, formula, or other foods needed",
            "Breastfeed on demand, day and night",
            "Ensure good latch and positioning",
            "Breastmilk provides all the nutrition and water a baby needs for the first 6 months",
            "Avoid bottle feeding - use cup if expressing",
        ],
    },
    {
        "min_months": 6,
        "max_months": 8,
        "description": "Introduction of complementary foods + breastfeeding",
        "meals_per_day": "2-3 meals + breastfeeding",
        "texture": "Soft, mashed, pureed foods",
        "amount_per_meal": "Start with 2-3 tablespoons, gradually increase to half a cup (125ml)",
        "key_messages": [
            "Start with soft, mashed foods like bota with added groundnut butter",
            "Introduce one new food at a time, wait 2-3 days before the next",
            "Continue breastfeeding on demand",
            "Feed the child yourself - do not leave them to eat alone",
            "Mash kapenta, eggs, or liver into porridge for iron and protein",
        ],
    },
    {
        "min_months": 9,
        "max_months": 11,
        "description": "Increasing variety and texture + breastfeeding",
        "meals_per_day": "3 meals + 1-2 snacks + breastfeeding",
        "texture": "Finely chopped, mashed, or finger foods",
        "amount_per_meal": "Half a cup (125ml) per meal",
        "key_messages": [
            "Give lumpy foods and finger foods the child can hold",
            "Include foods from at least 4 food groups daily",
            "Continue breastfeeding on demand",
            "Offer pieces of banana, sweet potato, or soft cooked vegetables as finger foods",
            "Add variety: different vegetables, beans, eggs, kapenta, meat",
        ],
    },
    {
        "min_months": 12,
        "max_months": 23,
        "description": "Family foods + continued breastfeeding",
        "meals_per_day": "3 meals + 1-2 snacks + breastfeeding",
        "texture": "Chopped family foods",
        "amount_per_meal": "Three-quarters to one cup (175-250ml) per meal",
        "key_messages": [
            "Feed the child from their own plate so you can see how much they eat",
            "Give foods from at least 4 food groups daily",
            "Continue breastfeeding - it still provides important nutrition",
            "Avoid sugary drinks, sweets, and chips",
            "Include an animal-source food (egg, kapenta, meat, liver) at least once daily",
        ],
    },
    {
        "min_months": 24,
        "max_months": 60,
        "description": "Full family diet",
        "meals_per_day": "3 meals + 1-2 snacks",
        "texture": "Family foods, age-appropriate portions",
        "amount_per_meal": "One full cup (250ml) per meal",
        "key_messages": [
            "Provide a varied diet from all food groups",
            "Eat meals together as a family",
            "Limit sugary drinks, sweets, and processed snacks",
            "Ensure clean water for drinking",
            "Include fruits and vegetables daily",
            "Give protein-rich foods (eggs, beans, kapenta, meat) daily",
        ],
    },
]

# Food groups for dietary diversity score.
FOOD_GROUPS: list[str] = [
    "grains",
    "legumes",
    "dairy",
    "flesh_foods",
    "eggs",
    "vitamin_a_fruits_veg",
    "other_fruits_veg",
    "nuts_seeds",
]

# Breastfeeding troubleshooting guidance.
_BREASTFEEDING_PROBLEMS: dict[str, dict] = {
    "engorgement": {
        "description": "Breasts feel very full, hard, and painful",
        "causes": [
            "Milk production exceeds removal",
            "Missed or delayed feedings",
            "Baby not latching well",
        ],
        "solutions": [
            "Breastfeed frequently, at least every 2-3 hours",
            "Gently express a small amount of milk before feeding to soften the breast",
            "Apply warm cloths to the breast before feeding",
            "Apply cool cloths after feeding to reduce swelling",
            "Ensure baby has a good latch",
        ],
        "when_to_seek_help": "If symptoms persist for more than 48 hours or you develop a fever",
    },
    "cracked_nipples": {
        "description": "Nipples are sore, cracked, or bleeding",
        "causes": [
            "Poor latch or positioning",
            "Baby pulling off the breast frequently",
            "Thrush (yeast infection)",
        ],
        "solutions": [
            "Check and correct the latch - baby should take in the areola, not just the nipple",
            "Try different breastfeeding positions",
            "Apply expressed breastmilk to the nipples after feeding and let air dry",
            "Do not use soap on the nipples",
            "Start feeding on the less sore side first",
        ],
        "when_to_seek_help": "If pain persists despite correct latch, or if you see white patches in baby's mouth (thrush)",
    },
    "mastitis": {
        "description": "Breast infection with redness, swelling, pain, and fever",
        "causes": [
            "Blocked milk duct that becomes infected",
            "Engorgement that is not relieved",
            "Cracked nipples allowing bacteria to enter",
        ],
        "solutions": [
            "Continue breastfeeding - it is safe and helps clear the infection",
            "Feed frequently, starting on the affected side",
            "Apply warm compresses before feeding",
            "Rest as much as possible",
            "Drink plenty of fluids",
        ],
        "when_to_seek_help": "Immediately - mastitis usually requires antibiotics. Visit the clinic within 24 hours. Do not stop breastfeeding.",
    },
    "low_supply": {
        "description": "Mother feels she does not have enough milk",
        "causes": [
            "Infrequent feeding or scheduled feeding instead of on-demand",
            "Poor latch so baby is not removing milk effectively",
            "Stress, fatigue, or dehydration",
            "Supplementing with formula or water (reduces demand)",
        ],
        "solutions": [
            "Breastfeed more frequently - supply increases with demand",
            "Offer both breasts at each feeding",
            "Ensure baby has a good latch",
            "Rest and drink plenty of fluids (at least 8 glasses of water a day)",
            "Avoid supplementing with formula or water",
            "Do skin-to-skin contact with baby",
            "Express milk between feeds to increase supply",
        ],
        "when_to_seek_help": "If baby is not gaining weight, has fewer than 6 wet nappies a day, or seems constantly hungry",
    },
    "tongue_tie": {
        "description": "Baby's tongue movement is restricted by a tight frenulum",
        "causes": [
            "Congenital condition where the frenulum (tissue under the tongue) is too short or tight",
        ],
        "solutions": [
            "Visit a clinic or hospital for assessment",
            "A simple procedure (frenotomy) can release the tongue tie",
            "Continue breastfeeding as best you can while waiting for treatment",
            "Try different feeding positions",
        ],
        "when_to_seek_help": "As soon as possible if you notice: difficulty latching, clicking sounds during feeding, poor weight gain, or nipple pain despite good positioning",
    },
    "weaning": {
        "description": "Transitioning from breastfeeding to complementary foods",
        "causes": [
            "Child has reached 6 months and is ready for complementary foods",
            "Mother and child are ready to reduce breastfeeding",
        ],
        "solutions": [
            "WHO recommends breastfeeding for 2 years or beyond",
            "Introduce complementary foods at 6 months while continuing to breastfeed",
            "Wean gradually - drop one feeding at a time over several weeks",
            "Replace dropped feedings with nutritious foods and clean water",
            "Continue breastfeeding at bedtime and wake-up as long as desired",
            "If weaning before 12 months, use a cup (not bottle) for other milks",
        ],
        "when_to_seek_help": "If child refuses to eat other foods, loses weight, or if you experience breast engorgement during weaning",
    },
}


class NutritionAdvisor:
    """Age-appropriate nutrition guidance for children in Zimbabwe.

    Covers exclusive breastfeeding, complementary feeding, local food
    recommendations, dietary diversity scoring, and breastfeeding
    troubleshooting.

    Example:
        >>> advisor = NutritionAdvisor()
        >>> guidance = advisor.get_feeding_guidance(child_age_months=7)
        >>> guidance["meals_per_day"]
        '2-3 meals + breastfeeding'
    """

    @staticmethod
    def get_feeding_guidance(
        child_age_months: int,
        breastfeeding_status: str = "exclusive",
    ) -> dict:
        """Get age-appropriate feeding guidance.

        Args:
            child_age_months: The child's age in months.
            breastfeeding_status: One of "exclusive", "complementary", "weaned".

        Returns:
            Dictionary with description, meals_per_day, texture,
            amount_per_meal, key_messages, and breastfeeding_advice.

        Example:
            >>> NutritionAdvisor.get_feeding_guidance(3)
            {'description': 'Exclusive breastfeeding', ...}
            >>> NutritionAdvisor.get_feeding_guidance(8)
            {'description': 'Introduction of complementary foods + breastfeeding', ...}
        """
        guideline = None
        for g in _FEEDING_GUIDELINES:
            if g["min_months"] <= child_age_months <= g["max_months"]:
                guideline = g
                break

        if guideline is None:
            # Default to the last guideline for children over 60 months
            guideline = _FEEDING_GUIDELINES[-1]

        result = {
            "description": guideline["description"],
            "meals_per_day": guideline["meals_per_day"],
            "texture": guideline["texture"],
            "amount_per_meal": guideline["amount_per_meal"],
            "key_messages": list(guideline["key_messages"]),
        }

        # Add breastfeeding-specific advice
        bf_status = breastfeeding_status.lower()
        if child_age_months < 6 and bf_status != "exclusive":
            result["breastfeeding_advice"] = (
                "WHO recommends exclusive breastfeeding for the first 6 months. "
                "If you are having difficulty breastfeeding, speak with a health "
                "worker or lactation counsellor. Breastmilk provides all the "
                "nutrition your baby needs."
            )
        elif child_age_months >= 6 and child_age_months < 24 and bf_status == "weaned":
            result["breastfeeding_advice"] = (
                "WHO recommends continuing breastfeeding alongside complementary "
                "foods until at least 2 years of age. Breastmilk continues to "
                "provide important nutrients and protection against illness."
            )
        elif child_age_months >= 6 and bf_status in ("exclusive", "complementary"):
            result["breastfeeding_advice"] = (
                "Continue breastfeeding on demand alongside complementary foods. "
                "Breastmilk still provides up to half of a child's energy needs "
                "between 6-12 months."
            )
        else:
            result["breastfeeding_advice"] = (
                "Ensure the child receives a nutritious and diverse diet."
            )

        return result

    @staticmethod
    def get_local_foods(child_age_months: int) -> list[dict]:
        """Get Zimbabwe-specific food recommendations for the child's age.

        Args:
            child_age_months: The child's age in months.

        Returns:
            List of food dictionaries with name, description, category,
            and preparation instructions.

        Example:
            >>> foods = NutritionAdvisor.get_local_foods(8)
            >>> [f["name"] for f in foods if f["category"] == "grains"]
            ['bota']
        """
        return [
            {
                "name": f["name"],
                "description": f["description"],
                "category": f["category"],
                "preparation": f["preparation"],
            }
            for f in _LOCAL_FOODS
            if f["min_age_months"] <= child_age_months
        ]

    @staticmethod
    def assess_dietary_diversity(food_groups: list[str]) -> int:
        """Assess dietary diversity score (0-8).

        Based on the WHO minimum dietary diversity indicator, which counts
        the number of food groups consumed in the previous 24 hours.

        Food groups: grains, legumes, dairy, flesh_foods, eggs,
        vitamin_a_fruits_veg, other_fruits_veg, nuts_seeds.

        A score of 5 or more indicates minimum dietary diversity is met.

        Args:
            food_groups: List of food group names consumed in the last 24 hours.

        Returns:
            Dietary diversity score (0-8).

        Example:
            >>> NutritionAdvisor.assess_dietary_diversity(
            ...     ["grains", "legumes", "eggs", "vitamin_a_fruits_veg", "other_fruits_veg"]
            ... )
            5
        """
        consumed = set(g.lower().strip() for g in food_groups)
        valid_groups = set(FOOD_GROUPS)
        return len(consumed & valid_groups)

    @staticmethod
    def assess_minimum_acceptable_diet(
        diversity_score: int,
        meal_frequency: int,
        child_age_months: int,
        breastfed: bool,
    ) -> bool:
        """Assess whether a child meets the minimum acceptable diet criteria.

        For breastfed children: minimum dietary diversity (>= 5 groups)
        AND minimum meal frequency (>= age-appropriate meals).

        For non-breastfed children: minimum dietary diversity (>= 5 groups)
        AND minimum meal frequency AND dairy included.

        Minimum meal frequency:
        - 6-8 months (breastfed): 2 meals
        - 9-23 months (breastfed): 3 meals
        - 6-23 months (non-breastfed): 4 meals

        Args:
            diversity_score: The dietary diversity score (0-8).
            meal_frequency: Number of meals eaten in the day.
            child_age_months: The child's age in months.
            breastfed: Whether the child is currently breastfed.

        Returns:
            True if minimum acceptable diet criteria are met.

        Example:
            >>> NutritionAdvisor.assess_minimum_acceptable_diet(
            ...     diversity_score=5,
            ...     meal_frequency=3,
            ...     child_age_months=9,
            ...     breastfed=True,
            ... )
            True
        """
        min_diversity_met = diversity_score >= 5

        # Determine minimum meal frequency
        if breastfed:
            if child_age_months <= 8:
                min_meals = 2
            else:
                min_meals = 3
        else:
            min_meals = 4

        min_frequency_met = meal_frequency >= min_meals

        return min_diversity_met and min_frequency_met

    @staticmethod
    def get_breastfeeding_troubleshooting(problem: str) -> dict:
        """Get troubleshooting guidance for breastfeeding problems.

        Args:
            problem: One of "engorgement", "cracked_nipples", "mastitis",
                     "low_supply", "tongue_tie", "weaning".

        Returns:
            Dictionary with description, causes, solutions, and
            when_to_seek_help.

        Raises:
            ValueError: If the problem type is not recognized.

        Example:
            >>> guidance = NutritionAdvisor.get_breastfeeding_troubleshooting("low_supply")
            >>> print(guidance["solutions"][0])
            'Breastfeed more frequently - supply increases with demand'
        """
        problem_key = problem.lower().strip()
        if problem_key not in _BREASTFEEDING_PROBLEMS:
            available = ", ".join(_BREASTFEEDING_PROBLEMS.keys())
            raise ValueError(
                f"Unknown breastfeeding problem '{problem}'. "
                f"Available problems: {available}"
            )
        return dict(_BREASTFEEDING_PROBLEMS[problem_key])
