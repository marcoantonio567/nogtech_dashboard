import tempfile
import unittest
from pathlib import Path

from src.dashboard.infrastructure.csv_sales_repository import CsvSalesRepository


class CsvSalesRepositoryTests(unittest.TestCase):
    def test_maps_csv_row_and_keeps_sensitive_fields_out_of_entity(self) -> None:
        content = (
            "data_transacao,mes_referencia,valor,cpf_aluno,curso,cidade,uf,"
            "venda_em_feriado,horas_assistidas,tickets_suporte,nps_score\n"
            "2026-01-10,2026-01,99.90,***.123.456-**,Python,São Paulo,SP,"
            "True,80,2,9\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sales.csv"
            path.write_text(content, encoding="utf-8")
            sales = CsvSalesRepository(path).find_all()

        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0].course, "Python")
        self.assertEqual(sales[0].state, "SP")
        self.assertTrue(sales[0].holiday)
        self.assertNotEqual(sales[0].student_id, "***.123.456-**")
        self.assertEqual(len(sales[0].student_id), 16)


if __name__ == "__main__":
    unittest.main()
