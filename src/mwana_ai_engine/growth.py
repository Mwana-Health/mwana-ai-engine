"""Growth monitoring using WHO child growth standards.

Provides simplified WHO z-score approximations for weight-for-age,
height-for-age, and weight-for-height, plus MUAC classification
and growth faltering detection.
"""

from __future__ import annotations

from .types import (
    GrowthAssessment,
    MUACStatus,
    NutritionStatus,
    Stage,
)


# Simplified WHO growth standard reference data (median and SD).
# Source: WHO Child Growth Standards (2006).
# Format: {age_months: (median_kg, sd_kg)} for weight-for-age.
_WEIGHT_FOR_AGE_MALE: dict[int, tuple[float, float]] = {
    0: (3.3, 0.55),
    1: (4.5, 0.65),
    2: (5.6, 0.75),
    3: (6.4, 0.80),
    4: (7.0, 0.85),
    5: (7.5, 0.90),
    6: (7.9, 0.92),
    7: (8.3, 0.95),
    8: (8.6, 0.97),
    9: (8.9, 1.00),
    10: (9.2, 1.02),
    11: (9.4, 1.05),
    12: (9.6, 1.07),
    15: (10.3, 1.15),
    18: (10.9, 1.22),
    21: (11.5, 1.30),
    24: (12.2, 1.40),
    30: (13.3, 1.55),
    36: (14.3, 1.68),
    42: (15.3, 1.80),
    48: (16.3, 1.95),
    54: (17.3, 2.10),
    60: (18.3, 2.25),
}

_WEIGHT_FOR_AGE_FEMALE: dict[int, tuple[float, float]] = {
    0: (3.2, 0.50),
    1: (4.2, 0.60),
    2: (5.1, 0.70),
    3: (5.8, 0.75),
    4: (6.4, 0.80),
    5: (6.9, 0.85),
    6: (7.3, 0.88),
    7: (7.6, 0.90),
    8: (7.9, 0.93),
    9: (8.2, 0.95),
    10: (8.5, 0.98),
    11: (8.7, 1.00),
    12: (8.9, 1.03),
    15: (9.6, 1.12),
    18: (10.2, 1.20),
    21: (10.9, 1.28),
    24: (11.5, 1.35),
    30: (12.7, 1.50),
    36: (13.9, 1.65),
    42: (15.0, 1.78),
    48: (16.1, 1.90),
    54: (17.2, 2.05),
    60: (18.2, 2.20),
}

# Height/length-for-age reference (median cm, sd cm).
_HEIGHT_FOR_AGE_MALE: dict[int, tuple[float, float]] = {
    0: (49.9, 2.0),
    1: (54.7, 2.1),
    2: (58.4, 2.2),
    3: (61.4, 2.3),
    4: (63.9, 2.3),
    5: (65.9, 2.4),
    6: (67.6, 2.4),
    7: (69.2, 2.5),
    8: (70.6, 2.5),
    9: (72.0, 2.5),
    10: (73.3, 2.6),
    11: (74.5, 2.6),
    12: (75.7, 2.7),
    15: (79.1, 2.8),
    18: (82.3, 2.9),
    21: (85.1, 3.0),
    24: (87.8, 3.1),
    30: (92.4, 3.3),
    36: (96.1, 3.5),
    42: (99.9, 3.7),
    48: (103.3, 3.9),
    54: (106.7, 4.0),
    60: (110.0, 4.2),
}

_HEIGHT_FOR_AGE_FEMALE: dict[int, tuple[float, float]] = {
    0: (49.1, 1.9),
    1: (53.7, 2.0),
    2: (57.1, 2.1),
    3: (59.8, 2.2),
    4: (62.1, 2.2),
    5: (64.0, 2.3),
    6: (65.7, 2.3),
    7: (67.3, 2.4),
    8: (68.7, 2.4),
    9: (70.1, 2.5),
    10: (71.5, 2.5),
    11: (72.8, 2.5),
    12: (74.0, 2.6),
    15: (77.5, 2.8),
    18: (80.7, 2.9),
    21: (83.7, 3.0),
    24: (86.4, 3.1),
    30: (91.2, 3.3),
    36: (95.1, 3.5),
    42: (99.0, 3.7),
    48: (102.7, 3.8),
    54: (106.2, 4.0),
    60: (109.4, 4.1),
}

# Simplified weight-for-height reference (median kg, sd kg) keyed by height in cm.
# Used for wasting assessment. Covers 45-120cm range.
_WEIGHT_FOR_HEIGHT: dict[int, tuple[float, float]] = {
    45: (2.4, 0.3),
    50: (3.2, 0.4),
    55: (4.3, 0.5),
    60: (5.7, 0.6),
    65: (7.0, 0.7),
    70: (8.2, 0.8),
    75: (9.3, 0.9),
    80: (10.2, 1.0),
    85: (11.2, 1.1),
    90: (12.2, 1.2),
    95: (13.4, 1.3),
    100: (14.8, 1.4),
    105: (16.3, 1.5),
    110: (17.9, 1.6),
    115: (19.7, 1.8),
    120: (21.7, 2.0),
}


class GrowthMonitor:
    """WHO-based growth monitoring for children 0-60 months.

    Provides MUAC classification, simplified z-score calculations,
    growth faltering detection, and age/stage-specific recommendations.

    Example:
        >>> monitor = GrowthMonitor()
        >>> assessment = monitor.assess_growth(
        ...     weight_grams=7200,
        ...     height_cm=67.0,
        ...     age_months=6,
        ...     gender="male",
        ... )
        >>> assessment.nutrition_status
        NutritionStatus.NORMAL
    """

    @staticmethod
    def classify_muac(muac_cm: float) -> MUACStatus:
        """Classify mid-upper arm circumference (MUAC).

        MUAC thresholds (for children 6-59 months):
        - Green: >= 12.5 cm (normal)
        - Yellow: 11.5 to < 12.5 cm (moderate acute malnutrition risk)
        - Red: < 11.5 cm (severe acute malnutrition risk)

        Args:
            muac_cm: MUAC measurement in centimeters.

        Returns:
            MUACStatus classification.

        Example:
            >>> GrowthMonitor.classify_muac(13.0)
            MUACStatus.GREEN
            >>> GrowthMonitor.classify_muac(12.0)
            MUACStatus.YELLOW
            >>> GrowthMonitor.classify_muac(11.0)
            MUACStatus.RED
        """
        if muac_cm >= 12.5:
            return MUACStatus.GREEN
        if muac_cm >= 11.5:
            return MUACStatus.YELLOW
        return MUACStatus.RED

    @staticmethod
    def assess_growth(
        weight_grams: int,
        height_cm: float,
        age_months: int,
        gender: str,
        muac_cm: float | None = None,
    ) -> GrowthAssessment:
        """Assess a child's growth using simplified WHO z-score approximations.

        Args:
            weight_grams: Child's weight in grams.
            height_cm: Child's height/length in centimeters.
            age_months: Child's age in months (0-60).
            gender: "male" or "female".
            muac_cm: MUAC in centimeters (optional, for children 6-59 months).

        Returns:
            GrowthAssessment with z-scores, interpretation, and recommendations.

        Example:
            >>> monitor = GrowthMonitor()
            >>> result = monitor.assess_growth(
            ...     weight_grams=5000,
            ...     height_cm=55.0,
            ...     age_months=3,
            ...     gender="female",
            ... )
            >>> result.interpretation
            'Growth is within normal range'
        """
        weight_kg = weight_grams / 1000.0
        gender_lower = gender.lower()

        # Calculate z-scores
        wfa_z = _calculate_z_score(
            weight_kg, age_months,
            _WEIGHT_FOR_AGE_MALE if gender_lower == "male" else _WEIGHT_FOR_AGE_FEMALE,
        )
        hfa_z = _calculate_z_score(
            height_cm, age_months,
            _HEIGHT_FOR_AGE_MALE if gender_lower == "male" else _HEIGHT_FOR_AGE_FEMALE,
        )
        wfh_z = _calculate_wfh_z_score(weight_kg, height_cm)

        # MUAC classification
        muac_status = None
        if muac_cm is not None:
            muac_status = GrowthMonitor.classify_muac(muac_cm)

        # Determine nutrition status
        nutrition_status = _determine_nutrition_status(wfa_z, wfh_z, muac_status)

        # Build interpretation
        interpretation = _build_interpretation(wfa_z, hfa_z, wfh_z, muac_status)

        # Build recommendations
        recommendations = GrowthMonitor.get_recommendations(
            GrowthAssessment(
                weight_for_age_z=round(wfa_z, 1),
                height_for_age_z=round(hfa_z, 1),
                weight_for_height_z=round(wfh_z, 1),
                muac_status=muac_status,
                nutrition_status=nutrition_status,
                interpretation=interpretation,
                recommendations=[],
            ),
            _stage_from_age(age_months),
        )

        return GrowthAssessment(
            weight_for_age_z=round(wfa_z, 1),
            height_for_age_z=round(hfa_z, 1),
            weight_for_height_z=round(wfh_z, 1),
            muac_status=muac_status,
            nutrition_status=nutrition_status,
            interpretation=interpretation,
            recommendations=recommendations,
        )

    @staticmethod
    def detect_growth_faltering(records: list[dict]) -> bool:
        """Detect growth faltering from consecutive measurements.

        Growth faltering is defined as 2 or more consecutive measurements
        showing a declining weight-for-age trajectory (weight gain is
        less than expected or weight is decreasing).

        Args:
            records: List of measurement dicts with at least:
                - "weight_grams" (int)
                - "age_months" (int)
                Sorted chronologically (oldest first).

        Returns:
            True if growth faltering is detected, False otherwise.

        Example:
            >>> GrowthMonitor.detect_growth_faltering([
            ...     {"weight_grams": 6000, "age_months": 3},
            ...     {"weight_grams": 6050, "age_months": 4},
            ...     {"weight_grams": 6060, "age_months": 5},
            ...     {"weight_grams": 6020, "age_months": 6},
            ... ])
            True
        """
        if len(records) < 3:
            return False

        declining_count = 0
        for i in range(1, len(records)):
            current_weight = records[i]["weight_grams"]
            previous_weight = records[i - 1]["weight_grams"]
            age_diff = records[i]["age_months"] - records[i - 1]["age_months"]

            if age_diff <= 0:
                continue

            # Expected minimum weight gain: ~150g/month in first 6 months,
            # ~100g/month for 6-12 months, ~80g/month for 12-24 months,
            # ~60g/month for 24-60 months.
            current_age = records[i]["age_months"]
            if current_age <= 6:
                expected_gain = 150 * age_diff
            elif current_age <= 12:
                expected_gain = 100 * age_diff
            elif current_age <= 24:
                expected_gain = 80 * age_diff
            else:
                expected_gain = 60 * age_diff

            actual_gain = current_weight - previous_weight

            # Faltering if actual gain is less than half expected, or if weight decreased
            if actual_gain < expected_gain * 0.5:
                declining_count += 1
            else:
                declining_count = 0

            if declining_count >= 2:
                return True

        return False

    @staticmethod
    def get_recommendations(
        assessment: GrowthAssessment, stage: Stage
    ) -> list[str]:
        """Get recommendations based on growth assessment and stage.

        Args:
            assessment: The GrowthAssessment result.
            stage: The child's current care stage.

        Returns:
            List of actionable recommendations.

        Example:
            >>> recs = GrowthMonitor.get_recommendations(assessment, Stage.INFANT)
        """
        recommendations: list[str] = []

        # SAM
        if assessment.nutrition_status == NutritionStatus.SAM:
            recommendations.append(
                "URGENT: Your child shows signs of severe malnutrition. "
                "Visit the clinic immediately for therapeutic feeding."
            )
            recommendations.append(
                "Ready-to-use therapeutic food (RUTF) will be provided at the clinic."
            )
            return recommendations

        # MAM
        if assessment.nutrition_status == NutritionStatus.MAM:
            recommendations.append(
                "Your child may be moderately malnourished. Visit the clinic "
                "for a supplementary feeding programme assessment."
            )
            recommendations.append(
                "Increase feeding frequency to 5 times a day. Add oil or "
                "groundnut butter to porridge for extra energy."
            )

        # Underweight (low weight-for-age)
        if assessment.weight_for_age_z < -2.0:
            recommendations.append(
                "Your child is underweight. Increase the amount and frequency "
                "of feeding. Include energy-rich foods like groundnut butter, "
                "oil, avocado, eggs, and kapenta."
            )

        # Stunted (low height-for-age)
        if assessment.height_for_age_z < -2.0:
            recommendations.append(
                "Your child's height is below expected range, which may indicate "
                "chronic undernutrition. Ensure a diverse diet with protein-rich "
                "foods (eggs, beans, kapenta, meat) and foods rich in vitamin A "
                "(pumpkin, mango, dark green vegetables)."
            )

        # Wasted (low weight-for-height)
        if assessment.weight_for_height_z < -2.0:
            recommendations.append(
                "Your child shows signs of wasting (too thin for their height). "
                "Feed more frequently with energy-dense foods. Visit the clinic "
                "for MUAC measurement and assessment."
            )

        # Overweight (high weight-for-height)
        if assessment.weight_for_height_z > 2.0:
            recommendations.append(
                "Your child is above the expected weight for their height. "
                "Ensure a balanced diet with fruits, vegetables, and appropriate "
                "portions. Encourage active play."
            )

        # Stage-specific advice
        if stage == Stage.NEWBORN:
            recommendations.append(
                "Breastfeed exclusively on demand, at least 8-12 times per day. "
                "No water, formula, or other foods are needed."
            )
        elif stage == Stage.INFANT:
            recommendations.append(
                "Continue breastfeeding. If your child is 6 months or older, "
                "introduce soft, mashed complementary foods alongside breastfeeding."
            )
        elif stage in (Stage.TODDLER, Stage.EARLY_CHILDHOOD):
            recommendations.append(
                "Provide a diverse diet from all food groups daily. "
                "Include grains, legumes, vegetables, fruits, and animal-source foods."
            )

        # If everything is normal
        if assessment.nutrition_status == NutritionStatus.NORMAL and not recommendations:
            recommendations.append(
                "Your child's growth is within the normal range. Continue "
                "current feeding practices and attend monthly growth monitoring."
            )

        return recommendations


def _calculate_z_score(
    value: float,
    age_months: int,
    reference_table: dict[int, tuple[float, float]],
) -> float:
    """Calculate a simplified z-score using linear interpolation.

    Args:
        value: The measured value (weight in kg or height in cm).
        age_months: Child's age in months.
        reference_table: Reference data mapping age to (median, sd).

    Returns:
        Approximate z-score.
    """
    ages = sorted(reference_table.keys())

    # Clamp to reference range
    if age_months <= ages[0]:
        median, sd = reference_table[ages[0]]
    elif age_months >= ages[-1]:
        median, sd = reference_table[ages[-1]]
    else:
        # Find bracketing ages and interpolate
        lower_age = ages[0]
        upper_age = ages[-1]
        for a in ages:
            if a <= age_months:
                lower_age = a
            if a >= age_months:
                upper_age = a
                break

        if lower_age == upper_age:
            median, sd = reference_table[lower_age]
        else:
            fraction = (age_months - lower_age) / (upper_age - lower_age)
            lower_med, lower_sd = reference_table[lower_age]
            upper_med, upper_sd = reference_table[upper_age]
            median = lower_med + fraction * (upper_med - lower_med)
            sd = lower_sd + fraction * (upper_sd - lower_sd)

    if sd == 0:
        return 0.0
    return (value - median) / sd


def _calculate_wfh_z_score(weight_kg: float, height_cm: float) -> float:
    """Calculate weight-for-height z-score using simplified reference."""
    heights = sorted(_WEIGHT_FOR_HEIGHT.keys())
    height_int = int(round(height_cm))

    # Clamp to reference range
    if height_int <= heights[0]:
        median, sd = _WEIGHT_FOR_HEIGHT[heights[0]]
    elif height_int >= heights[-1]:
        median, sd = _WEIGHT_FOR_HEIGHT[heights[-1]]
    else:
        lower_h = heights[0]
        upper_h = heights[-1]
        for h in heights:
            if h <= height_int:
                lower_h = h
            if h >= height_int:
                upper_h = h
                break

        if lower_h == upper_h:
            median, sd = _WEIGHT_FOR_HEIGHT[lower_h]
        else:
            fraction = (height_int - lower_h) / (upper_h - lower_h)
            lower_med, lower_sd = _WEIGHT_FOR_HEIGHT[lower_h]
            upper_med, upper_sd = _WEIGHT_FOR_HEIGHT[upper_h]
            median = lower_med + fraction * (upper_med - lower_med)
            sd = lower_sd + fraction * (upper_sd - lower_sd)

    if sd == 0:
        return 0.0
    return (weight_kg - median) / sd


def _determine_nutrition_status(
    wfa_z: float, wfh_z: float, muac_status: MUACStatus | None
) -> NutritionStatus:
    """Determine overall nutrition status from z-scores and MUAC."""
    # SAM: z < -3 or MUAC RED
    if wfh_z < -3.0 or wfa_z < -3.0:
        return NutritionStatus.SAM
    if muac_status == MUACStatus.RED:
        return NutritionStatus.SAM

    # MAM: z between -3 and -2, or MUAC YELLOW
    if wfh_z < -2.0 or wfa_z < -2.0:
        return NutritionStatus.MAM
    if muac_status == MUACStatus.YELLOW:
        return NutritionStatus.MAM

    return NutritionStatus.NORMAL


def _build_interpretation(
    wfa_z: float, hfa_z: float, wfh_z: float, muac_status: MUACStatus | None
) -> str:
    """Build a human-readable interpretation of growth measurements."""
    issues: list[str] = []

    if wfa_z < -3.0:
        issues.append("severely underweight")
    elif wfa_z < -2.0:
        issues.append("underweight")

    if hfa_z < -3.0:
        issues.append("severely stunted")
    elif hfa_z < -2.0:
        issues.append("stunted")

    if wfh_z < -3.0:
        issues.append("severely wasted")
    elif wfh_z < -2.0:
        issues.append("wasted")
    elif wfh_z > 3.0:
        issues.append("obese")
    elif wfh_z > 2.0:
        issues.append("overweight")

    if muac_status == MUACStatus.RED:
        issues.append("MUAC indicates severe acute malnutrition")
    elif muac_status == MUACStatus.YELLOW:
        issues.append("MUAC indicates moderate acute malnutrition risk")

    if not issues:
        return "Growth is within normal range"

    return "Growth concerns: " + ", ".join(issues)


def _stage_from_age(age_months: int) -> Stage:
    """Determine approximate stage from age in months."""
    if age_months < 1:
        return Stage.NEWBORN
    if age_months < 12:
        return Stage.INFANT
    if age_months < 36:
        return Stage.TODDLER
    return Stage.EARLY_CHILDHOOD
