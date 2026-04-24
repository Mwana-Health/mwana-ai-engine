"""WHO Integrated Management of Childhood Illness (IMCI) assessment.

Implements the IMCI clinical algorithms for assessing cough/difficult breathing,
diarrhea, fever, ear problems, nutrition, and general danger signs in children
aged 2 months to 5 years.
"""

from __future__ import annotations

from .types import TriageLevel, TriageResult


class IMCIAssessment:
    """WHO IMCI assessment algorithms for childhood illness.

    Provides structured clinical assessment for the main IMCI conditions:
    cough/difficult breathing, diarrhea, fever, ear problems, and malnutrition.

    All methods return a TriageResult with appropriate classification,
    assessment, and recommended action.

    Example:
        >>> imci = IMCIAssessment()
        >>> result = imci.check_general_danger_signs(
        ...     unable_to_drink=True,
        ...     vomits_everything=False,
        ...     convulsions=False,
        ...     lethargic=False,
        ... )
        >>> result.level
        TriageLevel.RED
    """

    @staticmethod
    def assess_cough(
        child_age_months: int,
        breathing_rate: int,
        chest_indrawing: bool = False,
        stridor: bool = False,
    ) -> TriageResult:
        """Assess cough or difficult breathing using IMCI guidelines.

        Breathing rate cutoffs by age:
        - 0-2 months: fast breathing if >= 60 breaths/min
        - 2-12 months: fast breathing if >= 50 breaths/min
        - 12-60 months: fast breathing if >= 40 breaths/min

        Args:
            child_age_months: Child's age in months.
            breathing_rate: Breaths per minute (counted for a full minute).
            chest_indrawing: Whether lower chest wall draws in when breathing in.
            stridor: Whether there is stridor (harsh noise when breathing in) at rest.

        Returns:
            TriageResult with classification and treatment guidance.

        Example:
            >>> IMCIAssessment.assess_cough(
            ...     child_age_months=8,
            ...     breathing_rate=55,
            ...     chest_indrawing=False,
            ... )
            TriageResult(level=TriageLevel.YELLOW, ...)
        """
        danger_signs: list[str] = []

        if chest_indrawing:
            danger_signs.append("chest_indrawing")
        if stridor:
            danger_signs.append("stridor_at_rest")

        # Severe pneumonia or very severe disease
        if chest_indrawing or stridor:
            return TriageResult(
                level=TriageLevel.RED,
                assessment=(
                    "Severe pneumonia or very severe disease. "
                    "Chest indrawing and/or stridor at rest indicate severe lower "
                    "respiratory tract infection requiring urgent referral."
                ),
                recommended_action=(
                    "Refer URGENTLY to hospital. Give first dose of antibiotic "
                    "(amoxicillin). Keep the child warm. If the child can breastfeed, "
                    "encourage breastfeeding on the way."
                ),
                danger_signs=danger_signs,
                follow_up_hours=0,
            )

        # Check for fast breathing (pneumonia)
        is_fast = _is_fast_breathing(child_age_months, breathing_rate)

        if is_fast:
            threshold = _get_breathing_threshold(child_age_months)
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    f"Pneumonia. Breathing rate of {breathing_rate}/min exceeds the "
                    f"threshold of {threshold}/min for this age group. "
                    f"Antibiotic treatment is needed."
                ),
                recommended_action=(
                    "Give oral amoxicillin for 5 days. Soothe the throat with a safe "
                    "remedy (breast milk for infants, warm water with honey for children "
                    "over 12 months). Return in 2 days for follow-up. Return immediately "
                    "if breathing becomes more difficult or the child cannot drink."
                ),
                danger_signs=[],
                follow_up_hours=48,
            )

        # No pneumonia: cough or cold
        return TriageResult(
            level=TriageLevel.GREEN,
            assessment=(
                f"Cough or cold. Breathing rate of {breathing_rate}/min is within "
                f"normal range for this age. No signs of pneumonia."
            ),
            recommended_action=(
                "No antibiotic needed. Soothe the throat with safe home remedies. "
                "Continue breastfeeding or feeding. Watch for danger signs: "
                "fast breathing, chest indrawing, inability to drink. "
                "Return if the cough persists beyond 14 days or gets worse."
            ),
            danger_signs=[],
            follow_up_hours=72,
        )

    @staticmethod
    def assess_diarrhea(
        duration_days: int,
        blood_in_stool: bool = False,
        sunken_eyes: bool = False,
        skin_pinch_slow: bool = False,
        drinks_eagerly: bool = False,
        unable_to_drink: bool = False,
    ) -> TriageResult:
        """Assess diarrhea using IMCI dehydration classification.

        Classifications:
        - Severe dehydration: 2+ of (lethargic/unconscious, sunken eyes,
          unable to drink, skin pinch very slow)
        - Some dehydration: 2+ of (restless/irritable, sunken eyes,
          drinks eagerly, skin pinch slow)
        - No dehydration: insufficient signs for above classifications

        Args:
            duration_days: How many days the diarrhea has lasted.
            blood_in_stool: Whether there is blood in the stool (dysentery).
            sunken_eyes: Whether the eyes appear sunken.
            skin_pinch_slow: Whether a skin pinch goes back slowly (>2 seconds).
            drinks_eagerly: Whether the child drinks eagerly/thirstily.
            unable_to_drink: Whether the child is unable to drink at all.

        Returns:
            TriageResult with dehydration classification and ORS/zinc guidance.

        Example:
            >>> IMCIAssessment.assess_diarrhea(
            ...     duration_days=2,
            ...     sunken_eyes=True,
            ...     unable_to_drink=True,
            ... )
            TriageResult(level=TriageLevel.RED, ...)
        """
        danger_signs: list[str] = []

        if blood_in_stool:
            danger_signs.append("blood_in_stool")

        # Check for severe dehydration
        severe_signs = sum([
            unable_to_drink,
            sunken_eyes,
            skin_pinch_slow,
        ])

        if unable_to_drink:
            danger_signs.append("unable_to_drink")

        if unable_to_drink or severe_signs >= 2:
            return TriageResult(
                level=TriageLevel.RED,
                assessment=(
                    "Severe dehydration. The child shows signs of significant fluid "
                    "loss requiring immediate IV or nasogastric rehydration. "
                    "This is a life-threatening condition in children."
                ),
                recommended_action=(
                    "Refer URGENTLY to hospital for IV rehydration. If the child "
                    "can drink, give ORS frequently in small sips on the way. "
                    "Continue breastfeeding. Begin zinc supplementation: "
                    "10mg/day for infants under 6 months, 20mg/day for older children, "
                    "for 10-14 days."
                ),
                danger_signs=danger_signs,
                follow_up_hours=0,
            )

        # Check for some dehydration
        some_signs = sum([
            sunken_eyes,
            skin_pinch_slow,
            drinks_eagerly,
        ])

        if some_signs >= 2:
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    "Some dehydration. The child is losing fluids and needs "
                    "supervised ORS treatment at the clinic for 4 hours."
                ),
                recommended_action=(
                    "Give ORS at the clinic over 4 hours. Amount: 75ml/kg body weight. "
                    "Reassess after 4 hours. Continue breastfeeding between ORS sips. "
                    "Begin zinc: 10mg/day (under 6 months) or 20mg/day (6 months+) "
                    "for 10-14 days. Return immediately if the child cannot drink or "
                    "gets worse."
                ),
                danger_signs=danger_signs,
                follow_up_hours=24,
            )

        # Blood in stool (dysentery) is always YELLOW
        if blood_in_stool:
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    "Dysentery (bloody diarrhea). Blood in the stool requires "
                    "antibiotic treatment."
                ),
                recommended_action=(
                    "Give oral antibiotic for dysentery. Give ORS and zinc. "
                    "Continue breastfeeding and feeding. Return in 2 days. "
                    "Return sooner if the child gets worse or cannot drink."
                ),
                danger_signs=danger_signs,
                follow_up_hours=48,
            )

        # Persistent diarrhea (14+ days)
        if duration_days >= 14:
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    "Persistent diarrhea. Diarrhea lasting 14 days or more "
                    "requires clinical assessment for underlying causes."
                ),
                recommended_action=(
                    "Visit the clinic for assessment. Continue feeding with "
                    "nutrient-rich foods. Give ORS after each loose stool. "
                    "Give zinc for 10-14 days. Ensure the child eats enough."
                ),
                danger_signs=[],
                follow_up_hours=48,
            )

        # No dehydration
        return TriageResult(
            level=TriageLevel.GREEN,
            assessment=(
                "Diarrhea with no dehydration. The child is maintaining fluid "
                "balance and can be managed at home."
            ),
            recommended_action=(
                "Give extra fluids including ORS after each loose stool. "
                "Continue breastfeeding and feeding. Give zinc: 10mg/day "
                "(under 6 months) or 20mg/day (6 months+) for 10-14 days. "
                "Return if: blood in stool, unable to drink, not getting better "
                "in 3 days, or diarrhea lasts more than 14 days."
            ),
            danger_signs=[],
            follow_up_hours=72,
        )

    @staticmethod
    def assess_fever(
        child_age_months: int,
        duration_days: int,
        stiff_neck: bool = False,
        malaria_area: bool = False,
    ) -> TriageResult:
        """Assess fever using IMCI guidelines.

        In malaria-endemic areas (most of Zimbabwe), any fever should prompt
        malaria testing. Stiff neck with fever suggests meningitis.

        Args:
            child_age_months: Child's age in months.
            duration_days: Number of days the fever has lasted.
            stiff_neck: Whether the child has a stiff neck.
            malaria_area: Whether the child lives in a malaria-endemic area.

        Returns:
            TriageResult with fever classification and guidance.

        Example:
            >>> IMCIAssessment.assess_fever(
            ...     child_age_months=18,
            ...     duration_days=2,
            ...     malaria_area=True,
            ... )
            TriageResult(level=TriageLevel.YELLOW, ...)
        """
        danger_signs: list[str] = []

        # Very severe febrile disease / meningitis
        if stiff_neck:
            danger_signs.append("stiff_neck")
            return TriageResult(
                level=TriageLevel.RED,
                assessment=(
                    "Very severe febrile disease. Stiff neck with fever suggests "
                    "meningitis or another severe infection requiring immediate "
                    "hospital care."
                ),
                recommended_action=(
                    "Refer URGENTLY to hospital. Give first dose of antibiotic "
                    "and antimalarial (if in malaria area). Treat fever with "
                    "paracetamol. Keep the child comfortable."
                ),
                danger_signs=danger_signs,
                follow_up_hours=0,
            )

        # Young infant with fever - always urgent
        if child_age_months < 2:
            danger_signs.append("fever_young_infant")
            return TriageResult(
                level=TriageLevel.RED,
                assessment=(
                    "Fever in a young infant under 2 months. Any fever in this "
                    "age group is a danger sign requiring immediate assessment."
                ),
                recommended_action=(
                    "Refer URGENTLY to hospital. Fever in a baby under 2 months "
                    "can indicate a serious bacterial infection. Keep the baby "
                    "warm, continue breastfeeding if able."
                ),
                danger_signs=danger_signs,
                follow_up_hours=0,
            )

        # Malaria area or prolonged fever
        if malaria_area:
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    "Fever in a malaria-endemic area. Malaria testing (rapid "
                    "diagnostic test or blood smear) is recommended for any "
                    "child with fever in Zimbabwe."
                ),
                recommended_action=(
                    "Visit the clinic for a malaria test. Give paracetamol for "
                    "fever (15mg/kg every 6 hours as needed). Give extra fluids. "
                    "If the test is positive, complete the full course of "
                    "antimalarial medication. Return immediately if the child "
                    "gets worse, has convulsions, or cannot drink."
                ),
                danger_signs=[],
                follow_up_hours=24,
            )

        if duration_days >= 7:
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    "Prolonged fever lasting 7 or more days. This requires "
                    "clinical investigation for underlying causes."
                ),
                recommended_action=(
                    "Visit the clinic for assessment and investigation. "
                    "Give paracetamol for fever. Give extra fluids. "
                    "Continue feeding normally."
                ),
                danger_signs=[],
                follow_up_hours=24,
            )

        if duration_days >= 3:
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    "Fever persisting for 3 or more days. A clinic visit is "
                    "recommended to identify the cause."
                ),
                recommended_action=(
                    "Visit the clinic within 24-48 hours. Give paracetamol for "
                    "fever. Give extra fluids. Continue breastfeeding and feeding. "
                    "Tepid sponge if temperature is very high."
                ),
                danger_signs=[],
                follow_up_hours=48,
            )

        # Short duration fever, non-malaria area
        return TriageResult(
            level=TriageLevel.GREEN,
            assessment=(
                "Short-duration fever that can be managed at home with "
                "monitoring and supportive care."
            ),
            recommended_action=(
                "Give paracetamol for fever (15mg/kg every 6 hours as needed). "
                "Give extra fluids. Continue breastfeeding and feeding. "
                "Dress the child in light clothing. Return if fever persists "
                "more than 3 days, child has convulsions, or child cannot drink."
            ),
            danger_signs=[],
            follow_up_hours=72,
        )

    @staticmethod
    def assess_ear(
        ear_pain: bool = False,
        discharge: bool = False,
        discharge_duration_days: int = 0,
        tender_swelling: bool = False,
    ) -> TriageResult:
        """Assess ear problems using IMCI guidelines.

        Classifications:
        - Mastoiditis: tender swelling behind the ear (RED)
        - Chronic ear infection: discharge for 14+ days (YELLOW)
        - Acute ear infection: ear pain or discharge < 14 days (YELLOW)

        Args:
            ear_pain: Whether the child has ear pain.
            discharge: Whether there is discharge from the ear.
            discharge_duration_days: Days the discharge has been present.
            tender_swelling: Whether there is tender swelling behind the ear.

        Returns:
            TriageResult with ear problem classification.

        Example:
            >>> IMCIAssessment.assess_ear(
            ...     ear_pain=True,
            ...     tender_swelling=True,
            ... )
            TriageResult(level=TriageLevel.RED, ...)
        """
        # Mastoiditis
        if tender_swelling:
            return TriageResult(
                level=TriageLevel.RED,
                assessment=(
                    "Mastoiditis. Tender swelling behind the ear indicates a "
                    "serious infection of the bone behind the ear requiring "
                    "urgent hospital treatment."
                ),
                recommended_action=(
                    "Refer URGENTLY to hospital. Give first dose of antibiotic "
                    "and paracetamol for pain. This requires injectable antibiotics."
                ),
                danger_signs=["tender_swelling_behind_ear"],
                follow_up_hours=0,
            )

        # Chronic ear infection
        if discharge and discharge_duration_days >= 14:
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    "Chronic ear infection. Ear discharge lasting 14 days or "
                    "more requires clinical treatment and dry ear wicking."
                ),
                recommended_action=(
                    "Visit the clinic. Keep the ear dry by wicking with a clean, "
                    "dry cloth or tissue rolled into a wick, 3 times daily. "
                    "Do not put anything else in the ear. Do not swim or allow "
                    "water to enter the ear."
                ),
                danger_signs=[],
                follow_up_hours=48,
            )

        # Acute ear infection
        if ear_pain or discharge:
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    "Acute ear infection. Ear pain or discharge of less than "
                    "14 days requires antibiotic treatment."
                ),
                recommended_action=(
                    "Give oral amoxicillin for 5 days. Give paracetamol for pain. "
                    "If there is discharge, wick the ear dry 3 times daily. "
                    "Return in 5 days for follow-up."
                ),
                danger_signs=[],
                follow_up_hours=48,
            )

        # No ear problem
        return TriageResult(
            level=TriageLevel.GREEN,
            assessment="No ear problem identified.",
            recommended_action=(
                "No treatment needed for ears. Return if the child develops "
                "ear pain, discharge, or hearing difficulty."
            ),
            danger_signs=[],
            follow_up_hours=None,
        )

    @staticmethod
    def assess_nutrition(
        muac_cm: float,
        edema: bool = False,
        visible_wasting: bool = False,
    ) -> TriageResult:
        """Assess nutritional status using IMCI guidelines.

        Classifications:
        - Severe malnutrition: MUAC < 11.5cm, or edema of both feet,
          or visible severe wasting
        - Moderate malnutrition: MUAC 11.5-12.5cm
        - Normal nutrition: MUAC >= 12.5cm

        Args:
            muac_cm: Mid-upper arm circumference in centimeters.
            edema: Whether there is edema (swelling) of both feet.
            visible_wasting: Whether there is visible severe wasting.

        Returns:
            TriageResult with nutrition classification and feeding guidance.

        Example:
            >>> IMCIAssessment.assess_nutrition(muac_cm=11.0, edema=True)
            TriageResult(level=TriageLevel.RED, ...)
        """
        danger_signs: list[str] = []

        # Severe acute malnutrition (SAM)
        if muac_cm < 11.5 or edema or visible_wasting:
            if muac_cm < 11.5:
                danger_signs.append("muac_red")
            if edema:
                danger_signs.append("edema_both_feet")
            if visible_wasting:
                danger_signs.append("visible_severe_wasting")

            return TriageResult(
                level=TriageLevel.RED,
                assessment=(
                    "Severe acute malnutrition (SAM). The child has signs of "
                    "severe malnutrition requiring immediate therapeutic feeding "
                    "and medical care."
                ),
                recommended_action=(
                    "Refer URGENTLY to hospital or therapeutic feeding centre. "
                    "If the child can eat, give a small amount of food before "
                    "the journey. Keep the child warm. Give vitamin A if not "
                    "given in the last 6 months. Begin ready-to-use therapeutic "
                    "food (RUTF) as soon as appetite allows."
                ),
                danger_signs=danger_signs,
                follow_up_hours=0,
            )

        # Moderate acute malnutrition (MAM)
        if muac_cm < 12.5:
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    "Moderate acute malnutrition (MAM). The child's MUAC is "
                    f"{muac_cm}cm, indicating moderate malnutrition. "
                    "Nutritional support and monitoring are needed."
                ),
                recommended_action=(
                    "Visit the clinic for supplementary feeding programme enrolment. "
                    "Feed the child 5 times a day with energy-dense foods: "
                    "add groundnut butter or oil to porridge, give kapenta, eggs, "
                    "beans, and green vegetables. Continue breastfeeding if under "
                    "2 years. Return in 2 weeks for MUAC re-measurement."
                ),
                danger_signs=[],
                follow_up_hours=48,
            )

        # Normal
        return TriageResult(
            level=TriageLevel.GREEN,
            assessment=(
                f"Nutrition is adequate. MUAC is {muac_cm}cm, which is in "
                "the normal range."
            ),
            recommended_action=(
                "Continue feeding the child a diverse diet. Include foods from "
                "at least 4 food groups daily. Continue breastfeeding if under "
                "2 years. Bring the child for monthly growth monitoring."
            ),
            danger_signs=[],
            follow_up_hours=None,
        )

    @staticmethod
    def check_general_danger_signs(
        unable_to_drink: bool = False,
        vomits_everything: bool = False,
        convulsions: bool = False,
        lethargic: bool = False,
    ) -> TriageResult:
        """Check for IMCI general danger signs.

        ANY single general danger sign means the child has a very severe
        disease and must be referred urgently.

        Args:
            unable_to_drink: Whether the child is unable to drink or breastfeed.
            vomits_everything: Whether the child vomits everything given.
            convulsions: Whether the child has had convulsions.
            lethargic: Whether the child is lethargic or unconscious.

        Returns:
            TriageResult. RED if any danger sign is present, GREEN otherwise.

        Example:
            >>> IMCIAssessment.check_general_danger_signs(convulsions=True)
            TriageResult(level=TriageLevel.RED, ...)
        """
        danger_signs: list[str] = []

        if unable_to_drink:
            danger_signs.append("unable_to_drink_or_breastfeed")
        if vomits_everything:
            danger_signs.append("vomits_everything")
        if convulsions:
            danger_signs.append("convulsions")
        if lethargic:
            danger_signs.append("lethargic_or_unconscious")

        if danger_signs:
            sign_text = ", ".join(s.replace("_", " ") for s in danger_signs)
            return TriageResult(
                level=TriageLevel.RED,
                assessment=(
                    f"GENERAL DANGER SIGN(S) present: {sign_text}. "
                    "Any general danger sign means the child has a very severe "
                    "disease. Complete the rest of the assessment, give "
                    "pre-referral treatment, and refer urgently."
                ),
                recommended_action=(
                    "Refer URGENTLY to hospital. Give pre-referral treatments: "
                    "first dose of antibiotic, antimalarial if appropriate, "
                    "and sugar water to prevent low blood sugar. Keep the child "
                    "warm. If convulsing, protect the child from injury and place "
                    "on their side."
                ),
                danger_signs=danger_signs,
                follow_up_hours=0,
            )

        return TriageResult(
            level=TriageLevel.GREEN,
            assessment="No general danger signs present.",
            recommended_action=(
                "Continue with the specific symptom assessment. No urgent "
                "referral needed based on general danger signs."
            ),
            danger_signs=[],
            follow_up_hours=None,
        )


def _is_fast_breathing(age_months: int, rate: int) -> bool:
    """Check if breathing rate is fast for the child's age.

    WHO IMCI cutoffs:
    - 0-2 months: >= 60 breaths/min
    - 2-12 months: >= 50 breaths/min
    - 12-60 months: >= 40 breaths/min
    """
    threshold = _get_breathing_threshold(age_months)
    return rate >= threshold


def _get_breathing_threshold(age_months: int) -> int:
    """Get the fast breathing threshold for the child's age."""
    if age_months < 2:
        return 60
    if age_months < 12:
        return 50
    return 40
