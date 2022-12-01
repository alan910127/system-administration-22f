#!/usr/bin/env python3

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Snapshot:
    dataset: str
    created_at: datetime

    @property
    def name(self):
        return f"{self.dataset}@{self.created_at:%Y-%m-%d-%T}"


@dataclass
class SnapshotWithId(Snapshot):
    id: int

    @classmethod
    def from_snapshot(cls, id: int, snapshot: Snapshot):
        return cls(id=id, dataset=snapshot.dataset, created_at=snapshot.created_at)
