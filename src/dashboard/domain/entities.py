from dataclasses import dataclass


@dataclass(frozen=True)
class Sale:
    date: str
    month: str
    value: float
    student_id: str
    course: str
    city: str
    state: str
    holiday: bool
    watched_hours: float | None
    support_tickets: float | None
    nps_score: float | None
