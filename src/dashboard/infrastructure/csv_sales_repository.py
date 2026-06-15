import csv
import hashlib
from pathlib import Path

from ..domain.entities import Sale


NOT_INFORMED = "Não informado"


class CsvSalesRepository:
    def __init__(self, data_file: Path) -> None:
        self._data_file = data_file

    def find_all(self) -> list[Sale]:
        with self._data_file.open("r", encoding="utf-8-sig", newline="") as file:
            return [self._to_sale(row) for row in csv.DictReader(file)]

    @staticmethod
    def _to_sale(row: dict[str, str]) -> Sale:
        return Sale(
            date=row["data_transacao"],
            month=row["mes_referencia"],
            value=float(row["valor"]),
            student_id=_anonymous_student_id(row["cpf_aluno"]),
            course=row["curso"] or NOT_INFORMED,
            city=row["cidade"] or NOT_INFORMED,
            state=row["uf"] or NOT_INFORMED,
            holiday=row["venda_em_feriado"].lower() == "true",
            watched_hours=_optional_number(row["horas_assistidas"]),
            support_tickets=_optional_number(row["tickets_suporte"]),
            nps_score=_optional_number(row["nps_score"]),
        )


def _optional_number(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    return float(value)


def _anonymous_student_id(masked_cpf: str) -> str:
    return hashlib.sha256(masked_cpf.encode("utf-8")).hexdigest()[:16]
