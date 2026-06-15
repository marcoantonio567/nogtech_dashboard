from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class DashboardSale:
    date: str
    month: str
    value: float
    student: str
    course: str
    city: str
    uf: str
    holiday: bool
    engagement_score: float | None

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["engagementScore"] = payload.pop("engagement_score")
        return payload
