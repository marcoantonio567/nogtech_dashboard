import unittest

from src.dashboard.domain.entities import Sale
from src.dashboard.domain.services import calculate_engagement_score


def sale_with_metrics(
    watched_hours: float | None,
    support_tickets: float | None,
    nps_score: float | None,
) -> Sale:
    return Sale(
        date="2026-01-01",
        month="2026-01",
        value=100,
        student_id="student",
        course="Course",
        city="City",
        state="SP",
        holiday=False,
        watched_hours=watched_hours,
        support_tickets=support_tickets,
        nps_score=nps_score,
    )


class EngagementScoreTests(unittest.TestCase):
    def test_returns_none_without_available_metrics(self) -> None:
        self.assertIsNone(calculate_engagement_score(sale_with_metrics(None, None, None)))

    def test_normalizes_weights_when_a_metric_is_missing(self) -> None:
        score = calculate_engagement_score(sale_with_metrics(160, None, 10))
        self.assertEqual(score, 100)

    def test_calculates_weighted_score(self) -> None:
        score = calculate_engagement_score(sale_with_metrics(80, 3, 5))
        self.assertEqual(score, 50)

    def test_limits_metrics_to_their_business_ranges(self) -> None:
        score = calculate_engagement_score(sale_with_metrics(320, -1, 20))
        self.assertEqual(score, 100)


if __name__ == "__main__":
    unittest.main()
