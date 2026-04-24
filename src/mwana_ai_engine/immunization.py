"""Zimbabwe Expanded Programme on Immunization (EPI) scheduler.

Provides the full Zimbabwe EPI vaccine schedule, due date calculations,
overdue detection, and catch-up schedule generation.
"""

from __future__ import annotations

from datetime import date, timedelta

from .types import ImmunizationDue


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
]


class ImmunizationScheduler:
    """Manages the Zimbabwe EPI immunization schedule.

    Calculates scheduled dates, identifies overdue vaccines, and generates
    catch-up schedules for children who have missed doses.

    Example:
        >>> from datetime import date
        >>> scheduler = ImmunizationScheduler()
        >>> schedule = scheduler.get_schedule(date_of_birth=date(2026, 1, 15))
        >>> len(schedule)
        20
        >>> schedule[0].vaccine_code
        'BCG'
    """

    def __init__(self) -> None:
        self._schedule = ZIMBABWE_EPI

    def get_schedule(self, date_of_birth: date) -> list[ImmunizationDue]:
        """Get the full immunization schedule with calculated dates.

        Args:
            date_of_birth: The child's date of birth.

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
        result: list[ImmunizationDue] = []

        for vaccine in self._schedule:
            scheduled_date = date_of_birth + timedelta(weeks=vaccine["age_weeks"])
            days_until = (scheduled_date - today).days
            is_overdue = days_until < 0

            result.append(ImmunizationDue(
                vaccine_code=vaccine["code"],
                vaccine_name=vaccine["name"],
                dose_number=vaccine["dose"],
                scheduled_age_weeks=vaccine["age_weeks"],
                scheduled_date=scheduled_date,
                is_overdue=is_overdue,
                days_until_due=days_until,
                max_age_months=vaccine["max_age_months"],
            ))

        return result

    def get_next_due(
        self,
        date_of_birth: date,
        completed_codes: list[str],
    ) -> ImmunizationDue | None:
        """Get the next vaccine that is due.

        Finds the earliest not-yet-completed vaccine whose scheduled date
        is on or after today, or the earliest overdue vaccine that is still
        within the maximum age for catch-up.

        Args:
            date_of_birth: The child's date of birth.
            completed_codes: List of vaccine codes already administered.

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

            scheduled_date = date_of_birth + timedelta(weeks=vaccine["age_weeks"])
            days_until = (scheduled_date - today).days

            candidates.append(ImmunizationDue(
                vaccine_code=vaccine["code"],
                vaccine_name=vaccine["name"],
                dose_number=vaccine["dose"],
                scheduled_age_weeks=vaccine["age_weeks"],
                scheduled_date=scheduled_date,
                is_overdue=days_until < 0,
                days_until_due=days_until,
                max_age_months=vaccine["max_age_months"],
            ))

        if not candidates:
            return None

        # Return the one closest to today (overdue first, then upcoming)
        candidates.sort(key=lambda v: v.scheduled_date)
        return candidates[0]

    def get_overdue(
        self,
        date_of_birth: date,
        completed_codes: list[str],
    ) -> list[ImmunizationDue]:
        """Get all overdue vaccines that are still within catch-up age.

        Args:
            date_of_birth: The child's date of birth.
            completed_codes: List of vaccine codes already administered.

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

            scheduled_date = date_of_birth + timedelta(weeks=vaccine["age_weeks"])
            days_until = (scheduled_date - today).days

            if days_until < 0:
                result.append(ImmunizationDue(
                    vaccine_code=vaccine["code"],
                    vaccine_name=vaccine["name"],
                    dose_number=vaccine["dose"],
                    scheduled_age_weeks=vaccine["age_weeks"],
                    scheduled_date=scheduled_date,
                    is_overdue=True,
                    days_until_due=days_until,
                    max_age_months=vaccine["max_age_months"],
                ))

        result.sort(key=lambda v: v.scheduled_date)
        return result

    def get_catchup_schedule(
        self,
        date_of_birth: date,
        completed_codes: list[str],
    ) -> list[ImmunizationDue]:
        """Get a catch-up schedule for missed vaccines still within max age.

        This includes both overdue vaccines and upcoming vaccines that have
        not been completed. Vaccines where the child has exceeded the
        maximum age for administration are excluded.

        Args:
            date_of_birth: The child's date of birth.
            completed_codes: List of vaccine codes already administered.

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

            scheduled_date = date_of_birth + timedelta(weeks=vaccine["age_weeks"])
            days_until = (scheduled_date - today).days

            result.append(ImmunizationDue(
                vaccine_code=vaccine["code"],
                vaccine_name=vaccine["name"],
                dose_number=vaccine["dose"],
                scheduled_age_weeks=vaccine["age_weeks"],
                scheduled_date=scheduled_date,
                is_overdue=days_until < 0,
                days_until_due=days_until,
                max_age_months=vaccine["max_age_months"],
            ))

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
