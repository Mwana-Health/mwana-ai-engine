"""Stage-specific danger sign detection.

Provides checklists of danger signs for each maternal-child health stage
and symptom-based triage assessment.
"""

from __future__ import annotations

from .types import Stage, TriageLevel, TriageResult


_DANGER_SIGNS: dict[Stage, list[dict]] = {
    Stage.PREGNANT: [
        {"symptom": "severe_headache", "description": "Severe headache that does not go away with rest or paracetamol", "urgency": "RED"},
        {"symptom": "blurred_vision", "description": "Blurred vision or seeing spots", "urgency": "RED"},
        {"symptom": "severe_abdominal_pain", "description": "Severe abdominal pain (not normal labour contractions)", "urgency": "RED"},
        {"symptom": "vaginal_bleeding", "description": "Any vaginal bleeding during pregnancy", "urgency": "RED"},
        {"symptom": "gush_of_fluid", "description": "Sudden gush of fluid from the vagina (water breaking before labour)", "urgency": "RED"},
        {"symptom": "reduced_fetal_movement", "description": "Baby moving less than usual or not moving at all", "urgency": "RED"},
        {"symptom": "swelling_face_hands", "description": "Sudden swelling of face and hands (not just feet)", "urgency": "RED"},
        {"symptom": "convulsions", "description": "Fits or convulsions", "urgency": "RED"},
        {"symptom": "high_fever", "description": "High fever (feeling very hot)", "urgency": "YELLOW"},
        {"symptom": "painful_urination", "description": "Pain or burning when urinating", "urgency": "YELLOW"},
        {"symptom": "foul_discharge", "description": "Foul-smelling vaginal discharge", "urgency": "YELLOW"},
        {"symptom": "persistent_vomiting", "description": "Vomiting that does not stop, unable to keep food or water down", "urgency": "YELLOW"},
    ],
    Stage.NEWBORN: [
        {"symptom": "unable_to_feed", "description": "Unable to breastfeed or refusing to feed", "urgency": "RED"},
        {"symptom": "lethargy", "description": "Baby is very sleepy, difficult to wake, or floppy", "urgency": "RED"},
        {"symptom": "fast_breathing", "description": "Breathing very fast (more than 60 breaths per minute)", "urgency": "RED"},
        {"symptom": "fever", "description": "Fever (body feels hot, temperature above 38C)", "urgency": "RED"},
        {"symptom": "hypothermia", "description": "Body feels cold (temperature below 35.5C)", "urgency": "RED"},
        {"symptom": "convulsions", "description": "Fits, jerking, or convulsions", "urgency": "RED"},
        {"symptom": "severe_jaundice", "description": "Yellow colour on palms of hands and soles of feet (severe jaundice)", "urgency": "RED"},
        {"symptom": "cord_redness", "description": "Redness spreading from the umbilical cord to the skin around it", "urgency": "RED"},
        {"symptom": "cord_pus", "description": "Pus or foul smell from the umbilical cord", "urgency": "RED"},
        {"symptom": "cord_smell", "description": "Bad smell from the umbilical cord stump", "urgency": "RED"},
        {"symptom": "bleeding_from_cord", "description": "Bleeding from the umbilical cord that does not stop", "urgency": "RED"},
        {"symptom": "bulging_fontanelle", "description": "Soft spot on head is bulging when baby is not crying", "urgency": "RED"},
    ],
    Stage.INFANT: [
        {"symptom": "unable_to_drink", "description": "Unable to drink or breastfeed", "urgency": "RED"},
        {"symptom": "vomits_everything", "description": "Vomits everything given", "urgency": "RED"},
        {"symptom": "convulsions", "description": "Fits, jerking, or convulsions", "urgency": "RED"},
        {"symptom": "lethargy", "description": "Very sleepy, difficult to wake, or unusually quiet", "urgency": "RED"},
        {"symptom": "fast_breathing", "description": "Breathing fast (more than 50 breaths per minute for 2-12 months)", "urgency": "RED"},
        {"symptom": "chest_indrawing", "description": "Lower chest pulls in when breathing in", "urgency": "RED"},
        {"symptom": "severe_dehydration", "description": "Sunken eyes, very dry mouth, skin pinch goes back very slowly", "urgency": "RED"},
        {"symptom": "bloody_diarrhea", "description": "Blood in the stool", "urgency": "RED"},
        {"symptom": "severe_wasting", "description": "Very thin, ribs and bones visible", "urgency": "RED"},
        {"symptom": "edema_both_feet", "description": "Swelling of both feet", "urgency": "RED"},
        {"symptom": "high_fever", "description": "High fever that does not come down", "urgency": "YELLOW"},
        {"symptom": "persistent_diarrhea", "description": "Diarrhea lasting more than 14 days", "urgency": "YELLOW"},
        {"symptom": "ear_discharge", "description": "Discharge from the ear", "urgency": "YELLOW"},
        {"symptom": "skin_rash_spreading", "description": "Rash that is spreading or has blisters", "urgency": "YELLOW"},
    ],
    Stage.TODDLER: [
        {"symptom": "unable_to_drink", "description": "Unable to drink or eat", "urgency": "RED"},
        {"symptom": "vomits_everything", "description": "Vomits everything given", "urgency": "RED"},
        {"symptom": "convulsions", "description": "Fits, jerking, or convulsions", "urgency": "RED"},
        {"symptom": "lethargy", "description": "Very sleepy, difficult to wake, or unusually quiet", "urgency": "RED"},
        {"symptom": "fast_breathing", "description": "Breathing fast (more than 40 breaths per minute for 1-5 years)", "urgency": "RED"},
        {"symptom": "chest_indrawing", "description": "Lower chest pulls in when breathing in", "urgency": "RED"},
        {"symptom": "severe_dehydration", "description": "Sunken eyes, very dry mouth, skin pinch goes back very slowly", "urgency": "RED"},
        {"symptom": "bloody_diarrhea", "description": "Blood in the stool", "urgency": "RED"},
        {"symptom": "burns", "description": "Burns from fire, hot water, or hot objects", "urgency": "RED"},
        {"symptom": "drowning_signs", "description": "Coughing, difficulty breathing, or blue lips after being in water", "urgency": "RED"},
        {"symptom": "poisoning", "description": "Swallowed poison, paraffin, medicine, or cleaning products", "urgency": "RED"},
        {"symptom": "severe_wasting", "description": "Very thin, ribs and bones visible", "urgency": "RED"},
        {"symptom": "high_fever", "description": "High fever that does not come down", "urgency": "YELLOW"},
        {"symptom": "persistent_diarrhea", "description": "Diarrhea lasting more than 14 days", "urgency": "YELLOW"},
        {"symptom": "limping", "description": "Limping or refusing to walk", "urgency": "YELLOW"},
    ],
    Stage.EARLY_CHILDHOOD: [
        {"symptom": "unable_to_drink", "description": "Unable to drink or eat", "urgency": "RED"},
        {"symptom": "vomits_everything", "description": "Vomits everything given", "urgency": "RED"},
        {"symptom": "convulsions", "description": "Fits, jerking, or convulsions", "urgency": "RED"},
        {"symptom": "lethargy", "description": "Very sleepy, difficult to wake, or unusually quiet", "urgency": "RED"},
        {"symptom": "fast_breathing", "description": "Breathing fast (more than 40 breaths per minute for 1-5 years)", "urgency": "RED"},
        {"symptom": "chest_indrawing", "description": "Lower chest pulls in when breathing in", "urgency": "RED"},
        {"symptom": "severe_dehydration", "description": "Sunken eyes, very dry mouth, skin pinch goes back very slowly", "urgency": "RED"},
        {"symptom": "bloody_diarrhea", "description": "Blood in the stool", "urgency": "RED"},
        {"symptom": "burns", "description": "Burns from fire, hot water, or hot objects", "urgency": "RED"},
        {"symptom": "drowning_signs", "description": "Coughing, difficulty breathing, or blue lips after being in water", "urgency": "RED"},
        {"symptom": "poisoning", "description": "Swallowed poison, paraffin, medicine, or cleaning products", "urgency": "RED"},
        {"symptom": "severe_wasting", "description": "Very thin, ribs and bones visible", "urgency": "RED"},
        {"symptom": "behavioral_regression", "description": "Loss of skills the child previously had (talking, walking, toilet training)", "urgency": "YELLOW"},
        {"symptom": "vision_concern", "description": "Squinting, sitting very close to things, or not seeing well", "urgency": "YELLOW"},
        {"symptom": "hearing_concern", "description": "Not responding to sounds or speech, talking very loudly", "urgency": "YELLOW"},
        {"symptom": "high_fever", "description": "High fever that does not come down", "urgency": "YELLOW"},
        {"symptom": "persistent_diarrhea", "description": "Diarrhea lasting more than 14 days", "urgency": "YELLOW"},
    ],
}

# Mapping of common symptom phrases to canonical symptom identifiers.
_SYMPTOM_ALIASES: dict[str, str] = {
    "headache": "severe_headache",
    "cannot see": "blurred_vision",
    "vision problems": "blurred_vision",
    "stomach pain": "severe_abdominal_pain",
    "belly pain": "severe_abdominal_pain",
    "bleeding": "vaginal_bleeding",
    "water broke": "gush_of_fluid",
    "baby not moving": "reduced_fetal_movement",
    "baby not kicking": "reduced_fetal_movement",
    "swollen face": "swelling_face_hands",
    "swollen hands": "swelling_face_hands",
    "fits": "convulsions",
    "seizure": "convulsions",
    "seizures": "convulsions",
    "not feeding": "unable_to_feed",
    "refusing breast": "unable_to_feed",
    "not breastfeeding": "unable_to_feed",
    "floppy": "lethargy",
    "limp": "lethargy",
    "sleepy": "lethargy",
    "breathing fast": "fast_breathing",
    "rapid breathing": "fast_breathing",
    "hot body": "fever",
    "temperature": "fever",
    "cold body": "hypothermia",
    "yellow eyes": "severe_jaundice",
    "yellow skin": "severe_jaundice",
    "cord bleeding": "bleeding_from_cord",
    "cord smells": "cord_smell",
    "cord red": "cord_redness",
    "soft spot bulging": "bulging_fontanelle",
    "not drinking": "unable_to_drink",
    "cannot drink": "unable_to_drink",
    "vomiting": "vomits_everything",
    "chest pulling in": "chest_indrawing",
    "blood in stool": "bloody_diarrhea",
    "bloody stool": "bloody_diarrhea",
    "very thin": "severe_wasting",
    "swollen feet": "edema_both_feet",
    "diarrhea": "persistent_diarrhea",
    "ear discharge": "ear_discharge",
    "rash": "skin_rash_spreading",
    "burn": "burns",
    "burned": "burns",
    "swallowed poison": "poisoning",
    "drank paraffin": "poisoning",
    "kerosene": "poisoning",
    "fell in water": "drowning_signs",
    "cannot walk": "limping",
    "lost skills": "behavioral_regression",
    "cannot see well": "vision_concern",
    "squinting": "vision_concern",
    "not hearing": "hearing_concern",
    "deaf": "hearing_concern",
}


class DangerSignDetector:
    """Stage-specific danger sign detection and triage.

    Provides danger sign checklists for each care stage and a symptom
    checker that maps reported symptoms to triage levels.

    Example:
        >>> detector = DangerSignDetector()
        >>> signs = detector.get_danger_signs(Stage.NEWBORN)
        >>> len(signs)
        12
    """

    @staticmethod
    def get_danger_signs(stage: Stage) -> list[dict]:
        """Get the danger sign checklist for a specific stage.

        Args:
            stage: The current care stage.

        Returns:
            List of danger sign dictionaries with symptom, description,
            and urgency level.

        Example:
            >>> signs = DangerSignDetector.get_danger_signs(Stage.PREGNANT)
            >>> [s["symptom"] for s in signs if s["urgency"] == "RED"]
            ['severe_headache', 'blurred_vision', ...]
        """
        return list(_DANGER_SIGNS.get(stage, []))

    @staticmethod
    def check_symptoms(symptoms: list[str], stage: Stage) -> TriageResult:
        """Check reported symptoms against the danger sign database.

        Normalizes symptom names using aliases, matches against the
        stage-specific danger sign list, and returns a triage result.

        Args:
            symptoms: List of symptom descriptions or identifiers.
            stage: The current care stage.

        Returns:
            TriageResult with the highest urgency level among matched symptoms.

        Example:
            >>> result = DangerSignDetector.check_symptoms(
            ...     ["fits", "not feeding"],
            ...     Stage.NEWBORN,
            ... )
            >>> result.level
            TriageLevel.RED
        """
        stage_signs = _DANGER_SIGNS.get(stage, [])
        sign_map: dict[str, dict] = {s["symptom"]: s for s in stage_signs}

        found_red: list[str] = []
        found_yellow: list[str] = []
        unmatched: list[str] = []

        for symptom in symptoms:
            normalized = symptom.lower().strip()

            # Try direct match first
            canonical = normalized
            if normalized in _SYMPTOM_ALIASES:
                canonical = _SYMPTOM_ALIASES[normalized]

            if canonical in sign_map:
                sign = sign_map[canonical]
                if sign["urgency"] == "RED":
                    found_red.append(sign["description"])
                else:
                    found_yellow.append(sign["description"])
            else:
                # Try partial matching
                matched = False
                for alias, canon in _SYMPTOM_ALIASES.items():
                    if alias in normalized or normalized in alias:
                        if canon in sign_map:
                            sign = sign_map[canon]
                            if sign["urgency"] == "RED":
                                found_red.append(sign["description"])
                            else:
                                found_yellow.append(sign["description"])
                            matched = True
                            break
                if not matched:
                    unmatched.append(normalized)

        if found_red:
            stage_label = stage.value.replace("_", " ").title()
            sign_list = "; ".join(found_red)
            return TriageResult(
                level=TriageLevel.RED,
                assessment=(
                    f"DANGER SIGNS detected for {stage_label}: {sign_list}. "
                    "Immediate medical attention is required."
                ),
                recommended_action=(
                    "Go to the nearest clinic or hospital IMMEDIATELY. "
                    "Do not wait. These are serious danger signs."
                ),
                danger_signs=found_red,
                follow_up_hours=0,
            )

        if found_yellow:
            stage_label = stage.value.replace("_", " ").title()
            sign_list = "; ".join(found_yellow)
            return TriageResult(
                level=TriageLevel.YELLOW,
                assessment=(
                    f"Concerning symptoms for {stage_label}: {sign_list}. "
                    "A clinic visit is recommended within 24-48 hours."
                ),
                recommended_action=(
                    "Visit your clinic within 24-48 hours. Monitor the symptoms "
                    "closely. If they get worse, go to the hospital immediately."
                ),
                danger_signs=[],
                follow_up_hours=48,
            )

        if unmatched:
            symptom_list = ", ".join(unmatched)
            return TriageResult(
                level=TriageLevel.GREEN,
                assessment=(
                    f"The reported symptoms ({symptom_list}) do not match "
                    "known danger signs for this stage. However, if you are "
                    "concerned, always consult a health worker."
                ),
                recommended_action=(
                    "Monitor the symptoms. If they persist or get worse, "
                    "visit your clinic. Trust your instincts as a caregiver."
                ),
                danger_signs=[],
                follow_up_hours=72,
            )

        return TriageResult(
            level=TriageLevel.GREEN,
            assessment="No symptoms reported.",
            recommended_action="No action needed at this time.",
            danger_signs=[],
            follow_up_hours=None,
        )
