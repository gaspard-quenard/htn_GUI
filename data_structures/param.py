from typing import List


class Param:

    def __init__(self, name: str, domain: List[str]) -> None:
        self.name = name
        self.domain = domain