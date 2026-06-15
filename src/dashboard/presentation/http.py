import json
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from ..application.use_cases import GetDashboardData


def create_dashboard_handler(
    get_dashboard_data: GetDashboardData,
    template_file: Path,
) -> type[BaseHTTPRequestHandler]:
    class DashboardHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            path = urlparse(self.path).path

            if path in ("/", "/index.html"):
                self._send_dashboard()
                return

            if path == "/health":
                self._send_response(200, b'{"status":"ok"}', "application/json")
                return

            self.send_error(404)

        def _send_dashboard(self) -> None:
            payload = json.dumps(
                get_dashboard_data.execute(),
                ensure_ascii=False,
                separators=(",", ":"),
            ).replace("</", "<\\/")
            html = template_file.read_text(encoding="utf-8")
            body = html.replace("__DASHBOARD_DATA__", payload).encode("utf-8")
            self._send_response(200, body, "text/html; charset=utf-8")

        def _send_response(
            self,
            status: int,
            body: bytes,
            content_type: str,
        ) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            print(f"[dashboard] {self.address_string()} - {format % args}")

    return DashboardHandler
