"""Climate-health risk scoring for Zimbabwe.

Scores climate-related health risks based on weather conditions and
district, providing stage-specific advisories for maternal-child health.
"""

from __future__ import annotations

from .types import Stage


# Zimbabwe climate zones and baseline risks.
# Districts are grouped by province/risk profile.
_MALARIA_HIGH_RISK_DISTRICTS: set[str] = {
    "binga", "kariba", "hurungwe", "guruve", "muzarabani", "mbire",
    "centenary", "rushinga", "mount_darwin", "mudzi", "mutoko",
    "chipinge", "chiredzi", "mwenezi", "beitbridge", "gwanda",
    "mangwe", "matobo", "plumtree", "lupane", "hwange", "tsholotsho",
    "nkayi", "gokwe_north", "gokwe_south", "zhombe",
}

_FLOOD_PRONE_DISTRICTS: set[str] = {
    "muzarabani", "mbire", "chiredzi", "binga", "tsholotsho",
    "chipinge", "chimanimani", "mutare", "nyanga",
}

_DROUGHT_PRONE_DISTRICTS: set[str] = {
    "beitbridge", "chiredzi", "mwenezi", "gwanda", "mangwe",
    "matobo", "binga", "kariba", "gokwe_south", "lupane",
    "nkayi", "tsholotsho",
}

# Zimbabwe seasons.
_WET_SEASON_MONTHS = {11, 12, 1, 2, 3}
_DRY_SEASON_MONTHS = {4, 5, 6, 7, 8, 9, 10}
_HOT_MONTHS = {10, 11, 12, 1, 2}
_COLD_MONTHS = {5, 6, 7}

# Risk category thresholds.
_HEAT_STRESS_TEMP_C = 35.0
_COLD_STRESS_TEMP_C = 10.0
_HEAVY_RAINFALL_MM = 50.0


class ClimateRiskScorer:
    """Climate-health risk scoring for Zimbabwe.

    Assesses climate-related health risks based on weather data and
    location, providing stage-appropriate health advisories.

    Example:
        >>> scorer = ClimateRiskScorer()
        >>> result = scorer.score_climate_risk(
        ...     district="muzarabani",
        ...     weather_data={"temperature_c": 38, "rainfall_mm": 60, "humidity_pct": 85},
        ... )
        >>> result["score"] > 50
        True
    """

    @staticmethod
    def score_climate_risk(
        district: str,
        weather_data: dict,
    ) -> dict:
        """Score climate-related health risk for a location.

        Args:
            district: Name of the district (case-insensitive).
            weather_data: Dictionary with weather measurements:
                - temperature_c (float): Temperature in Celsius.
                - rainfall_mm (float): Rainfall in millimeters (24h).
                - humidity_pct (float): Relative humidity percentage.
                - flooding (bool, optional): Whether flooding is occurring.

        Returns:
            Dictionary with:
            - score (int): Risk score 0-100.
            - risks (list[dict]): Identified risk factors.
            - advisories (list[str]): Health advisories.

        Example:
            >>> ClimateRiskScorer.score_climate_risk(
            ...     "harare",
            ...     {"temperature_c": 28, "rainfall_mm": 10, "humidity_pct": 60},
            ... )
            {'score': ..., 'risks': [...], 'advisories': [...]}
        """
        district_lower = district.lower().strip().replace(" ", "_")
        temp = weather_data.get("temperature_c", 25.0)
        rainfall = weather_data.get("rainfall_mm", 0.0)
        humidity = weather_data.get("humidity_pct", 50.0)
        flooding = weather_data.get("flooding", False)

        risks: list[dict] = []
        total_score = 0

        # Heat stress risk
        if temp >= _HEAT_STRESS_TEMP_C:
            severity = min(30, int((temp - _HEAT_STRESS_TEMP_C) * 6))
            total_score += severity
            risks.append({
                "type": "heat_stress",
                "severity": severity,
                "description": (
                    f"Temperature of {temp}C exceeds the heat stress threshold. "
                    "Risk of dehydration, heat exhaustion, and heat stroke."
                ),
            })
        elif temp >= 32.0:
            severity = int((temp - 32.0) * 3)
            total_score += severity
            risks.append({
                "type": "heat_stress",
                "severity": severity,
                "description": f"Temperature of {temp}C is elevated. Monitor for heat-related illness.",
            })

        # Cold stress risk
        if temp <= _COLD_STRESS_TEMP_C:
            severity = min(20, int((_COLD_STRESS_TEMP_C - temp) * 4))
            total_score += severity
            risks.append({
                "type": "cold_stress",
                "severity": severity,
                "description": (
                    f"Temperature of {temp}C is low. Risk of hypothermia, "
                    "especially for newborns and young children."
                ),
            })

        # Waterborne disease risk
        if rainfall >= _HEAVY_RAINFALL_MM or flooding:
            severity = 20 if flooding else min(15, int(rainfall / _HEAVY_RAINFALL_MM * 15))
            total_score += severity
            risks.append({
                "type": "waterborne_disease",
                "severity": severity,
                "description": (
                    "Heavy rainfall or flooding increases risk of waterborne "
                    "diseases (cholera, typhoid, diarrheal diseases). "
                    "Contaminated water is a major risk for children."
                ),
            })

        # Vector-borne disease (malaria) risk
        if district_lower in _MALARIA_HIGH_RISK_DISTRICTS:
            malaria_severity = 15
            if humidity >= 70 and temp >= 20:
                malaria_severity = 25
            if rainfall >= 20:
                malaria_severity = min(30, malaria_severity + 5)
            total_score += malaria_severity
            risks.append({
                "type": "vector_borne",
                "severity": malaria_severity,
                "description": (
                    f"{district} is a high malaria-risk district. "
                    "Warm, humid conditions with rainfall increase mosquito breeding."
                ),
            })

        # Flooding risk
        if flooding or (district_lower in _FLOOD_PRONE_DISTRICTS and rainfall >= 40):
            severity = 25 if flooding else 15
            if "waterborne_disease" not in [r["type"] for r in risks]:
                total_score += severity
            risks.append({
                "type": "flooding",
                "severity": severity,
                "description": (
                    "Flooding poses risks of drowning, waterborne disease, "
                    "displacement, and disruption of health services."
                ),
            })

        # Drought / nutrition risk
        if district_lower in _DROUGHT_PRONE_DISTRICTS and rainfall < 5 and temp >= 30:
            severity = 15
            total_score += severity
            risks.append({
                "type": "drought_nutrition",
                "severity": severity,
                "description": (
                    f"{district} is drought-prone. Low rainfall with high "
                    "temperatures increases risk of food insecurity and "
                    "malnutrition in children."
                ),
            })

        # Clamp score to 0-100
        total_score = min(100, max(0, total_score))

        # Generate advisories
        advisories = _generate_advisories(risks)

        return {
            "score": total_score,
            "risks": risks,
            "advisories": advisories,
        }

    @staticmethod
    def get_health_advisory(risk_type: str, stage: Stage) -> str:
        """Get a stage-specific health advisory for a climate risk type.

        Args:
            risk_type: One of "heat_stress", "cold_stress", "waterborne_disease",
                      "vector_borne", "flooding", "drought_nutrition".
            stage: The current care stage.

        Returns:
            Stage-appropriate advisory text.

        Example:
            >>> ClimateRiskScorer.get_health_advisory("heat_stress", Stage.PREGNANT)
            'Drink plenty of clean water...'
        """
        advisories: dict[str, dict[Stage, str]] = {
            "heat_stress": {
                Stage.PREGNANT: (
                    "Drink plenty of clean water. Rest in the shade during the "
                    "hottest part of the day. Wear loose, light clothing. "
                    "Dehydration during pregnancy can cause contractions and "
                    "is dangerous for you and your baby."
                ),
                Stage.NEWBORN: (
                    "Keep your baby in a cool, shaded area. Breastfeed more "
                    "frequently to prevent dehydration. Do not overdress the "
                    "baby. Watch for signs of overheating: flushed skin, "
                    "irritability, or fast breathing."
                ),
                Stage.INFANT: (
                    "Keep your child cool and hydrated. Breastfeed frequently "
                    "or give extra clean water if over 6 months. Stay indoors "
                    "during peak heat. Watch for signs of dehydration."
                ),
                Stage.TODDLER: (
                    "Give your child plenty of clean water to drink. Keep them "
                    "in the shade. Avoid outdoor play during the hottest hours "
                    "(10am-3pm). Dress in light clothing."
                ),
                Stage.EARLY_CHILDHOOD: (
                    "Ensure your child drinks water regularly. Limit outdoor "
                    "activities during peak heat. Wear hats and light clothing. "
                    "Watch for headaches, dizziness, or excessive tiredness."
                ),
            },
            "cold_stress": {
                Stage.PREGNANT: (
                    "Keep warm with layers of clothing. Ensure adequate "
                    "nutrition. Be cautious with open fires for heating "
                    "to avoid carbon monoxide exposure."
                ),
                Stage.NEWBORN: (
                    "Keep your baby warm with skin-to-skin contact (kangaroo "
                    "care). Dress in layers including a hat. Keep the room "
                    "warm. Breastfeed frequently. Hypothermia is very dangerous "
                    "for newborns."
                ),
                Stage.INFANT: (
                    "Dress your child in warm layers. Keep the home warm but "
                    "ventilated. Be careful with open fires and heaters. "
                    "Continue breastfeeding or feeding warm foods."
                ),
                Stage.TODDLER: (
                    "Dress your child warmly, including socks and a hat. "
                    "Supervise children around fires and heaters. "
                    "Give warm foods and drinks."
                ),
                Stage.EARLY_CHILDHOOD: (
                    "Ensure your child wears warm clothing when going outside. "
                    "Supervise around heating sources. Provide warm meals."
                ),
            },
            "waterborne_disease": {
                Stage.PREGNANT: (
                    "Drink only boiled or treated water. Wash hands frequently "
                    "with soap. Avoid walking through flood water. Diarrheal "
                    "illness during pregnancy can cause dehydration."
                ),
                Stage.NEWBORN: (
                    "Breastfeed exclusively, it protects against waterborne illness. "
                    "Wash hands with soap before handling the baby. "
                    "Do not give water or other fluids to the baby."
                ),
                Stage.INFANT: (
                    "Continue breastfeeding. Use only boiled or treated water "
                    "for drinking or preparing food. Wash hands before feeding. "
                    "If diarrhea starts, give ORS and continue breastfeeding."
                ),
                Stage.TODDLER: (
                    "Give only boiled or treated water. Wash all fruits and "
                    "vegetables. Wash hands with soap before eating and after "
                    "using the toilet. Ensure food is properly cooked."
                ),
                Stage.EARLY_CHILDHOOD: (
                    "Teach handwashing with soap. Give only safe water. "
                    "Avoid raw foods from unknown sources. Seek treatment "
                    "immediately if diarrhea or vomiting starts."
                ),
            },
            "vector_borne": {
                Stage.PREGNANT: (
                    "Sleep under an insecticide-treated bed net every night. "
                    "Attend antenatal visits for IPTp (intermittent preventive "
                    "treatment for malaria in pregnancy). Seek treatment "
                    "immediately if you develop fever."
                ),
                Stage.NEWBORN: (
                    "Sleep under an insecticide-treated bed net with your baby. "
                    "If the baby develops fever, go to the clinic immediately. "
                    "Any fever in a newborn is dangerous."
                ),
                Stage.INFANT: (
                    "Sleep under an insecticide-treated bed net. If your child "
                    "has fever, get a malaria test at the clinic immediately. "
                    "Complete the full course of treatment if positive."
                ),
                Stage.TODDLER: (
                    "Use bed nets every night. Wear long sleeves and trousers "
                    "in the evening. If your child has fever, test for malaria "
                    "at the clinic within 24 hours."
                ),
                Stage.EARLY_CHILDHOOD: (
                    "Continue using bed nets. Apply safe insect repellent. "
                    "Seek treatment quickly for any fever. Teach children "
                    "to sleep under nets."
                ),
            },
            "flooding": {
                Stage.PREGNANT: (
                    "Avoid walking through flood water. Move to higher ground "
                    "if your home is flooded. Know the location of the nearest "
                    "health facility in case of emergency."
                ),
                Stage.NEWBORN: (
                    "Keep your baby dry and warm. Avoid flood water. "
                    "If displaced, continue breastfeeding and seek shelter "
                    "at an evacuation centre."
                ),
                Stage.INFANT: (
                    "Keep your child away from flood water. Watch for signs "
                    "of diarrhea. Ensure drinking water is treated or boiled. "
                    "Continue breastfeeding."
                ),
                Stage.TODDLER: (
                    "Supervise your child at all times near water. Young "
                    "children can drown in very shallow water. Do not let "
                    "children play in flood water."
                ),
                Stage.EARLY_CHILDHOOD: (
                    "Keep children away from flood water and drainage channels. "
                    "Teach water safety. Watch for skin infections from "
                    "contaminated water."
                ),
            },
            "drought_nutrition": {
                Stage.PREGNANT: (
                    "Eat whatever nutritious food is available. Attend antenatal "
                    "visits for nutritional support. Iron and folate supplements "
                    "are especially important during food shortages."
                ),
                Stage.NEWBORN: (
                    "Breastfeed exclusively. Breastmilk production is maintained "
                    "even when the mother's diet is limited, though the mother "
                    "should eat and drink what she can."
                ),
                Stage.INFANT: (
                    "Continue breastfeeding. Use available foods to prepare "
                    "enriched porridge. Attend the clinic for growth monitoring "
                    "and nutritional support. Report to the clinic if you cannot "
                    "feed your child."
                ),
                Stage.TODDLER: (
                    "Prioritize feeding your child from available foods. "
                    "Add groundnut butter or oil to porridge for energy. "
                    "Visit the clinic for supplementary feeding if needed."
                ),
                Stage.EARLY_CHILDHOOD: (
                    "Ensure your child eats the most nutritious foods available. "
                    "Attend growth monitoring. Access food aid programmes if "
                    "available in your area."
                ),
            },
        }

        risk_advisories = advisories.get(risk_type, {})
        return risk_advisories.get(
            stage,
            f"Monitor weather conditions and take appropriate precautions for {risk_type.replace('_', ' ')}.",
        )

    @staticmethod
    def get_seasonal_guidance(month: int, district: str = "") -> list[str]:
        """Get seasonal health guidance for Zimbabwe.

        Zimbabwe has two main seasons:
        - Wet/rainy season: November to March (malaria, waterborne disease, flooding)
        - Dry season: April to October (cold June-August, dry heat October)

        Args:
            month: Month number (1-12).
            district: District name (optional, for location-specific advice).

        Returns:
            List of seasonal health guidance messages.

        Example:
            >>> ClimateRiskScorer.get_seasonal_guidance(1)
            ['It is the rainy season...', ...]
        """
        district_lower = district.lower().strip().replace(" ", "_")
        guidance: list[str] = []

        if month in _WET_SEASON_MONTHS:
            guidance.append(
                "It is the rainy season. Ensure your family sleeps under "
                "insecticide-treated bed nets to prevent malaria."
            )
            guidance.append(
                "Treat or boil all drinking water. Waterborne diseases "
                "increase during the rains."
            )
            guidance.append(
                "Watch for flooding in low-lying areas. Keep children away "
                "from swollen rivers and drainage channels."
            )
            if district_lower in _MALARIA_HIGH_RISK_DISTRICTS:
                guidance.append(
                    f"{district or 'Your district'} is a high malaria-risk area. "
                    "Seek immediate treatment for any fever."
                )
            if district_lower in _FLOOD_PRONE_DISTRICTS:
                guidance.append(
                    f"{district or 'Your district'} is prone to flooding. "
                    "Know your evacuation routes and the location of the "
                    "nearest health facility."
                )

        if month in _HOT_MONTHS:
            guidance.append(
                "It is the hot season. Ensure your family drinks plenty "
                "of clean water. Stay in the shade during the hottest hours."
            )
            guidance.append(
                "Breastfeed more frequently in hot weather. Babies and "
                "young children dehydrate more quickly than adults."
            )

        if month in _COLD_MONTHS:
            guidance.append(
                "It is the cold season. Keep babies and children warm, "
                "especially at night. Use layers of clothing and blankets."
            )
            guidance.append(
                "Be careful with open fires and paraffin heaters. "
                "Burns and carbon monoxide poisoning increase in winter. "
                "Never leave children unsupervised near fires."
            )
            guidance.append(
                "Respiratory infections (coughs and colds) are more common "
                "in cold weather. Keep children warm and seek treatment "
                "early if a child develops fast breathing or chest indrawing."
            )

        if month in _DRY_SEASON_MONTHS and district_lower in _DROUGHT_PRONE_DISTRICTS:
            guidance.append(
                f"{district or 'Your district'} may experience food shortages "
                "during the dry season. Prioritize nutritious foods for "
                "pregnant women and young children. Visit the clinic for "
                "growth monitoring and nutritional support."
            )

        if not guidance:
            guidance.append(
                "Continue attending clinic visits. Ensure your family has "
                "clean water, adequate nutrition, and sleeps under bed nets."
            )

        return guidance


def _generate_advisories(risks: list[dict]) -> list[str]:
    """Generate general health advisories from identified risks."""
    advisories: list[str] = []

    risk_types = {r["type"] for r in risks}

    if "heat_stress" in risk_types:
        advisories.append(
            "High temperature alert: Drink plenty of water, stay in shade, "
            "and avoid outdoor activities during peak heat."
        )

    if "cold_stress" in risk_types:
        advisories.append(
            "Cold weather alert: Keep warm with layers. Protect newborns "
            "and young children from hypothermia."
        )

    if "waterborne_disease" in risk_types:
        advisories.append(
            "Waterborne disease risk: Boil or treat all drinking water. "
            "Wash hands frequently with soap."
        )

    if "vector_borne" in risk_types:
        advisories.append(
            "Malaria risk: Sleep under insecticide-treated bed nets. "
            "Seek treatment immediately for fever."
        )

    if "flooding" in risk_types:
        advisories.append(
            "Flooding risk: Avoid flood water. Supervise children near "
            "water. Move to higher ground if necessary."
        )

    if "drought_nutrition" in risk_types:
        advisories.append(
            "Nutrition risk: Prioritize feeding pregnant women and young "
            "children. Visit the clinic for growth monitoring and support."
        )

    return advisories
