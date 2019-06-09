from dataclasses import dataclass


@dataclass
class DBModel:
    def __init__(self, pl_from, pl_namespace, pl_title, pl_from_namespace):
        self.pl_from = pl_from
        self.pl_namespace = pl_namespace
        self.pl_title = pl_title
        self.pl_from_namespace = pl_from_namespace