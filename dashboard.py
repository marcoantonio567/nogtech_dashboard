import csv
import hashlib
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "relatorio_final.csv"
HTML_FILE = ROOT / "dashboard.html"
HOST = "127.0.0.1"
PORT = 8000


def optional_number(value):
    if value is None or value.strip() == "":
        return None
    return float(value)


def anonymous_student_id(masked_cpf):
    return hashlib.sha256(masked_cpf.encode("utf-8")).hexdigest()[:16]


def load_dashboard_data():
    with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return [
            {
                "date": row["data_transacao"],
                "month": row["mes_referencia"],
                "value": float(row["valor"]),
                "student": anonymous_student_id(row["cpf_aluno"]),
                "course": row["curso"] or "Não informado",
                "city": row["cidade"] or "Não informado",
                "uf": row["uf"] or "Não informado",
                "holiday": row["venda_em_feriado"].lower() == "true",
                "hours": optional_number(row["horas_assistidas"]),
                "support": optional_number(row["tickets_suporte"]),
                "nps": optional_number(row["nps_score"]),
            }
            for row in reader
        ]


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path in ("/", "/index.html"):
            html = HTML_FILE.read_text(encoding="utf-8")
            payload = json.dumps(
                load_dashboard_data(),
                ensure_ascii=False,
                separators=(",", ":"),
            ).replace("</", "<\\/")
            body = html.replace("__DASHBOARD_DATA__", payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/health":
            body = b'{"status":"ok"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(404)

    def log_message(self, format, *args):
        print(f"[dashboard] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    if not DATA_FILE.exists():
        raise SystemExit(f"Base tratada não encontrada: {DATA_FILE}")
    if not HTML_FILE.exists():
        raise SystemExit(f"Interface não encontrada: {HTML_FILE}")

    server = ThreadingHTTPServer((HOST, PORT), DashboardHandler)
    print(f"Dashboard disponível em http://{HOST}:{PORT}")
    print(f"Fonte exclusiva: {DATA_FILE.name}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard encerrado.")
    finally:
        server.server_close()
