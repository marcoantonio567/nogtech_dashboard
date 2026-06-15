from .entities import Sale


WATCHED_HOURS_WEIGHT = 50
NPS_WEIGHT = 30
SUPPORT_WEIGHT = 20


def calculate_engagement_score(sale: Sale) -> float | None:
    weighted_score = 0.0
    available_weight = 0

    if sale.watched_hours is not None:
        weighted_score += min(max(sale.watched_hours, 0) / 160, 1) * WATCHED_HOURS_WEIGHT
        available_weight += WATCHED_HOURS_WEIGHT

    if sale.nps_score is not None:
        weighted_score += min(max(sale.nps_score, 0) / 10, 1) * NPS_WEIGHT
        available_weight += NPS_WEIGHT

    if sale.support_tickets is not None:
        weighted_score += max(0, 1 - max(sale.support_tickets, 0) / 6) * SUPPORT_WEIGHT
        available_weight += SUPPORT_WEIGHT

    if available_weight == 0:
        return None

    return weighted_score / available_weight * 100
