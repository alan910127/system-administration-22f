#!/usr/bin/env python3

from __future__ import annotations

from . import controller


def create_one(dataset: str, rotation_count: int = 12):
    snapshot = controller.create_snapshot(dataset)

    if snapshot is None:
        return

    print(f"Snap {snapshot.name}")

    snapshots = controller.get_snapshots(dataset)

    for snapshot in snapshots[:-rotation_count]:
        if controller.delete_snapshot(snapshot):
            print(f"Destroy {snapshot.name}")


def list_filtered(dataset: str | None = None, id: int | None = None):
    snapshots = controller.get_snapshots(dataset, [id] if id is not None else None)

    print("ID  DATASET             TIME")
    for snapshot in snapshots:
        print(
            f"{snapshot.id:<4d}{snapshot.dataset:20s}{snapshot.created_at:%Y-%m-%d-%T}"
        )


def delete_filtered(dataset: str | None = None, ids: list[int] | None = None):
    snapshots = controller.get_snapshots(dataset, ids)

    for snapshot in snapshots:
        if controller.delete_snapshot(snapshot):
            print(f"Destroy {snapshot.name}")


def export_snapshot(dataset: str | None = None, id: int | None = None):
    raise NotImplementedError()


def import_snapshot(dataset: str | None = None, id: int | None = None):
    raise NotImplementedError()
