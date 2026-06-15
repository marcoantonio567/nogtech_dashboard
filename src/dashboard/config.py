from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    root: Path
    data_file: Path
    template_file: Path
    host: str = "127.0.0.1"
    port: int = 8000


ROOT = Path(__file__).resolve().parents[2]
settings = Settings(
    root=ROOT,
    data_file=ROOT / "relatorio_final.csv",
    template_file=ROOT / "dashboard.html",
)
