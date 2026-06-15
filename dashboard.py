from src.dashboard.bootstrap import create_server
from src.dashboard.config import settings


def main() -> None:
    if not settings.data_file.exists():
        raise SystemExit(f"Base tratada não encontrada: {settings.data_file}")
    if not settings.template_file.exists():
        raise SystemExit(f"Interface não encontrada: {settings.template_file}")

    server = create_server()
    print(f"Dashboard disponível em http://{settings.host}:{settings.port}")
    print(f"Fonte exclusiva: {settings.data_file.name}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard encerrado.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
