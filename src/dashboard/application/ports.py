from typing import Protocol

from ..domain.entities import Sale


class SalesRepository(Protocol):
    def find_all(self) -> list[Sale]:
        """Return every sale available to the dashboard."""
