from .dtos import DashboardSale
from .ports import SalesRepository
from ..domain.services import calculate_engagement_score


class GetDashboardData:
    def __init__(self, sales_repository: SalesRepository) -> None:
        self._sales_repository = sales_repository

    def execute(self) -> list[dict[str, object]]:
        return [
            DashboardSale(
                date=sale.date,
                month=sale.month,
                value=sale.value,
                student=sale.student_id,
                course=sale.course,
                city=sale.city,
                uf=sale.state,
                holiday=sale.holiday,
                engagement_score=calculate_engagement_score(sale),
            ).to_dict()
            for sale in self._sales_repository.find_all()
        ]
