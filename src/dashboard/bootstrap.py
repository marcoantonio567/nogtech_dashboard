from http.server import ThreadingHTTPServer

from .application.use_cases import GetDashboardData
from .config import settings
from .infrastructure.csv_sales_repository import CsvSalesRepository
from .presentation.http import create_dashboard_handler


def create_server() -> ThreadingHTTPServer:
    repository = CsvSalesRepository(settings.data_file)
    get_dashboard_data = GetDashboardData(repository)
    handler = create_dashboard_handler(get_dashboard_data, settings.template_file)
    return ThreadingHTTPServer((settings.host, settings.port), handler)
