"""Zimbabwe Expanded Programme on Immunization (EPI) scheduler.

Provides the full Zimbabwe EPI vaccine schedule, due date calculations,
overdue detection, and catch-up schedule generation.
"""

from __future__ import annotations

from datetime import date, timedelta

from .types import ImmunizationDue


# Every entry carries an optional "sex" key ("any" | "female" | "male").
# When omitted it is treated as "any". This lets consumers filter, for
# example, girl-only HPV doses.
#
# School-age and adolescent entries (Td booster at 10y and HPV for girls at
# 10y and 11y) were added from the Zimbabwe routine immunisation schedule.
# Sources verified 2026-08-10:
#   - Zimbabwe childhood immunisation schedule, Prescribing Companion (Zimbabwe):
#     Td booster at 5 years AND 10 years; HPV for girls dose 1 at 10 years,
#     dose 2 at 11 years (0.5ml IM).
#     https://www.prescribingcompanion.com/zimbabwe/infections-and-infectious-diseases-prescribing/immunisation/immunisation-schedule-for-children/
#   - Zimbabwe national HPV introduction (bivalent, 0/12-month schedule for
#     girls 10-14y), PLOS Global Public Health / ScienceDirect (Vaccine, 2021):
#     https://journals.plos.org/globalpublichealth/article?id=10.1371%2Fjournal.pgph.0000101
# No other older-child doses are included because they could not be verified
# in an authoritative Zimbabwe source (constraint: never invent schedule rows).
ZIMBABWE_EPI: list[dict] = [
    {"code": "BCG", "name": "BCG", "dose": 1, "age_weeks": 0, "max_age_months": 11},
    {"code": "HepB_birth", "name": "Hepatitis B Birth Dose", "dose": 1, "age_weeks": 0, "max_age_months": 1},
    {"code": "OPV1", "name": "Oral Polio Vaccine", "dose": 1, "age_weeks": 6, "max_age_months": 59},
    {"code": "Penta1", "name": "Pentavalent (DPT-HepB-Hib)", "dose": 1, "age_weeks": 6, "max_age_months": 23},
    {"code": "PCV1", "name": "Pneumococcal Conjugate", "dose": 1, "age_weeks": 6, "max_age_months": 11},
    {"code": "Rota1", "name": "Rotavirus", "dose": 1, "age_weeks": 6, "max_age_months": 24},
    {"code": "OPV2", "name": "Oral Polio Vaccine", "dose": 2, "age_weeks": 10, "max_age_months": 59},
    {"code": "Penta2", "name": "Pentavalent", "dose": 2, "age_weeks": 10, "max_age_months": 23},
    {"code": "PCV2", "name": "Pneumococcal Conjugate", "dose": 2, "age_weeks": 10, "max_age_months": 11},
    {"code": "Rota2", "name": "Rotavirus", "dose": 2, "age_weeks": 10, "max_age_months": 24},
    {"code": "OPV3", "name": "Oral Polio Vaccine", "dose": 3, "age_weeks": 14, "max_age_months": 59},
    {"code": "IPV", "name": "Inactivated Polio Vaccine", "dose": 1, "age_weeks": 14, "max_age_months": 59},
    {"code": "Penta3", "name": "Pentavalent", "dose": 3, "age_weeks": 14, "max_age_months": 23},
    {"code": "PCV3", "name": "Pneumococcal Conjugate", "dose": 3, "age_weeks": 14, "max_age_months": 11},
    {"code": "MR1", "name": "Measles-Rubella", "dose": 1, "age_weeks": 36, "max_age_months": 60},
    {"code": "Typhoid", "name": "Typhoid Conjugate", "dose": 1, "age_weeks": 36, "max_age_months": 60},
    {"code": "MR2", "name": "Measles-Rubella", "dose": 2, "age_weeks": 78, "max_age_months": 60},
    {"code": "DPT_booster", "name": "DPT Booster", "dose": 1, "age_weeks": 78, "max_age_months": 60},
    {"code": "OPV_booster", "name": "OPV Booster", "dose": 1, "age_weeks": 78, "max_age_months": 60},
    {"code": "Td_booster", "name": "Tetanus-Diphtheria Booster", "dose": 1, "age_weeks": 260, "max_age_months": 72},
    # --- School-age and adolescent doses (verified, see header note) ---
    # Td booster #2 at 10 years (520 weeks). Catch-up window extends to ~13y.
    {"code": "Td_booster2", "name": "Tetanus-Diphtheria Booster (10 years)", "dose": 2, "age_weeks": 520, "max_age_months": 156, "sex": "any"},
    # HPV for girls: dose 1 at 10 years, dose 2 at 11 years (0/12-month
    # schedule). National eligibility runs 10-14 years, so the catch-up
    # window is set to 15 years (180 months).
    {"code": "HPV1", "name": "HPV Vaccine (girls)", "dose": 1, "age_weeks": 520, "max_age_months": 180, "sex": "female"},
    {"code": "HPV2", "name": "HPV Vaccine (girls)", "dose": 2, "age_weeks": 572, "max_age_months": 180, "sex": "female"},
]


class ImmunizationScheduler:
    """Manages the Zimbabwe EPI immunization schedule.

    Calculates scheduled dates, identifies overdue vaccines, and generates
    catch-up schedules for children who have missed doses.

    Example:
        >>> from datetime import date
        >>> scheduler = ImmunizationScheduler()
        >>> schedule = scheduler.get_schedule(date_of_birth=date(2026, 1, 15))
        >>> schedule[0].vaccine_code
        'BCG'
    """

    def __init__(self) -> None:
        self._schedule = ZIMBABWE_EPI

    @staticmethod
    def _applies_to_sex(vaccine: dict, sex: str | None) -> bool:
        """Return True if a vaccine applies given the child's sex.

        A vaccine with sex "any" (or no sex key) applies to everyone. A
        sex-specific vaccine (e.g. HPV "female") is included only when the
        child's sex matches, or when ``sex`` is None/unknown (in which case
        we err on the side of surfacing the dose so it is never silently
        dropped for a child whose sex was not recorded).
        """
        vaccine_sex = vaccine.get("sex", "any")
        if vaccine_sex == "any":
            return True
        if sex is None:
            return True
        return sex.lower().strip() == vaccine_sex

    @staticmethod
    def _build_due(
        vaccine: dict, date_of_birth: date, today: date
    ) -> ImmunizationDue:
        """Construct an ImmunizationDue for a vaccine entry."""
        scheduled_date = date_of_birth + timedelta(weeks=vaccine["age_weeks"])
        days_until = (scheduled_date - today).days
        return ImmunizationDue(
            vaccine_code=vaccine["code"],
            vaccine_name=vaccine["name"],
            dose_number=vaccine["dose"],
            scheduled_age_weeks=vaccine["age_weeks"],
            scheduled_date=scheduled_date,
            is_overdue=days_until < 0,
            days_until_due=days_until,
            max_age_months=vaccine["max_age_months"],
            sex=vaccine.get("sex", "any"),
        )

    def get_schedule(
        self, date_of_birth: date, sex: str | None = None
    ) -> list[ImmunizationDue]:
        """Get the full immunization schedule with calculated dates.

        Args:
            date_of_birth: The child's date of birth.
            sex: Child's sex ("female", "male", or None). When provided,
                sex-specific doses that do not apply are excluded. When None,
                all doses are included.

        Returns:
            List of all scheduled immunizations with calculated due dates.

        Example:
            >>> scheduler = ImmunizationScheduler()
            >>> schedule = scheduler.get_schedule(date(2026, 1, 15))
            >>> schedule[0].vaccine_name
            'BCG'
            >>> schedule[0].scheduled_date
            datetime.date(2026, 1, 15)
        """
        today = date.today()
        return [
            self._build_due(vaccine, date_of_birth, today)
            for vaccine in self._schedule
            if self._applies_to_sex(vaccine, sex)
        ]

    def get_next_due(
        self,
        date_of_birth: date,
        completed_codes: list[str],
        sex: str | None = None,
    ) -> ImmunizationDue | None:
        """Get the next vaccine that is due.

        Finds the earliest not-yet-completed vaccine whose scheduled date
        is on or after today, or the earliest overdue vaccine that is still
        within the maximum age for catch-up.

        Args:
            date_of_birth: The child's date of birth.
            completed_codes: List of vaccine codes already administered.
            sex: Child's sex ("female", "male", or None) to filter
                sex-specific doses such as HPV. None includes all.

        Returns:
            The next ImmunizationDue, or None if all vaccines are completed
            or the child has aged out.

        Example:
            >>> scheduler = ImmunizationScheduler()
            >>> due = scheduler.get_next_due(
            ...     date(2026, 1, 15),
            ...     completed_codes=["BCG", "HepB_birth"],
            ... )
            >>> due.vaccine_code
            'OPV1'
        """
        completed_set = set(completed_codes)
        today = date.today()
        child_age_months = _age_in_months(date_of_birth, today)

        candidates: list[ImmunizationDue] = []

        for vaccine in self._schedule:
            if vaccine["code"] in completed_set:
                continue
            if child_age_months > vaccine["max_age_months"]:
                continue
            if not self._applies_to_sex(vaccine, sex):
                continue

            candidates.append(self._build_due(vaccine, date_of_birth, today))

        if not candidates:
            return None

        # Return the one closest to today (overdue first, then upcoming)
        candidates.sort(key=lambda v: v.scheduled_date)
        return candidates[0]

    def get_overdue(
        self,
        date_of_birth: date,
        completed_codes: list[str],
        sex: str | None = None,
    ) -> list[ImmunizationDue]:
        """Get all overdue vaccines that are still within catch-up age.

        Args:
            date_of_birth: The child's date of birth.
            completed_codes: List of vaccine codes already administered.
            sex: Child's sex ("female", "male", or None) to filter
                sex-specific doses such as HPV. None includes all.

        Returns:
            List of overdue ImmunizationDue items, sorted by scheduled date.

        Example:
            >>> scheduler = ImmunizationScheduler()
            >>> overdue = scheduler.get_overdue(
            ...     date(2025, 6, 1),
            ...     completed_codes=["BCG"],
            ... )
            >>> len(overdue) > 0
            True
        """
        completed_set = set(completed_codes)
        today = date.today()
        child_age_months = _age_in_months(date_of_birth, today)
        result: list[ImmunizationDue] = []

        for vaccine in self._schedule:
            if vaccine["code"] in completed_set:
                continue
            if child_age_months > vaccine["max_age_months"]:
                continue
            if not self._applies_to_sex(vaccine, sex):
                continue

            due = self._build_due(vaccine, date_of_birth, today)
            if due.is_overdue:
                result.append(due)

        result.sort(key=lambda v: v.scheduled_date)
        return result

    def get_catchup_schedule(
        self,
        date_of_birth: date,
        completed_codes: list[str],
        sex: str | None = None,
    ) -> list[ImmunizationDue]:
        """Get a catch-up schedule for missed vaccines still within max age.

        This includes both overdue vaccines and upcoming vaccines that have
        not been completed. Vaccines where the child has exceeded the
        maximum age for administration are excluded.

        Args:
            date_of_birth: The child's date of birth.
            completed_codes: List of vaccine codes already administered.
            sex: Child's sex ("female", "male", or None) to filter
                sex-specific doses such as HPV. None includes all.

        Returns:
            List of vaccines to catch up on, sorted by scheduled date.

        Example:
            >>> scheduler = ImmunizationScheduler()
            >>> catchup = scheduler.get_catchup_schedule(
            ...     date(2025, 1, 1),
            ...     completed_codes=["BCG", "HepB_birth", "OPV1", "Penta1"],
            ... )
        """
        completed_set = set(completed_codes)
        today = date.today()
        child_age_months = _age_in_months(date_of_birth, today)
        result: list[ImmunizationDue] = []

        for vaccine in self._schedule:
            if vaccine["code"] in completed_set:
                continue
            if child_age_months > vaccine["max_age_months"]:
                continue
            if not self._applies_to_sex(vaccine, sex):
                continue

            result.append(self._build_due(vaccine, date_of_birth, today))

        result.sort(key=lambda v: v.scheduled_date)
        return result

    @staticmethod
    def is_within_max_age(vaccine_code: str, child_age_months: int) -> bool:
        """Check if a vaccine can still be administered at the given age.

        Args:
            vaccine_code: The vaccine code (e.g. "BCG", "Penta1").
            child_age_months: The child's current age in months.

        Returns:
            True if the vaccine can still be given, False if the child
            has aged out.

        Example:
            >>> ImmunizationScheduler.is_within_max_age("BCG", 6)
            True
            >>> ImmunizationScheduler.is_within_max_age("BCG", 14)
            False
        """
        for vaccine in ZIMBABWE_EPI:
            if vaccine["code"] == vaccine_code:
                return child_age_months <= vaccine["max_age_months"]
        return False


def _age_in_months(dob: date, reference: date) -> int:
    """Calculate age in complete months."""
    months = (reference.year - dob.year) * 12 + (reference.month - dob.month)
    if reference.day < dob.day:
        months -= 1
    return max(0, months)
