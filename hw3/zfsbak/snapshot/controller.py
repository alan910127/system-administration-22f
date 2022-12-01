#!/usr/bin/env python3

from __future__ import annotations

import re
import subprocess
from datetime import datetime
from typing import Sequence

from .model import Snapshot, SnapshotWithId

SNAPSHOT_PATTTERN = re.compile(r"([^@]+)@(\S+)")


def parse_snapshot(snapshot: str) -> Snapshot | None:
    """Parse the snapshot to objects.

    Original format: ``poolname/dataset@timestamp size available_size refer moutpoint``
    """
    match = SNAPSHOT_PATTTERN.search(snapshot)

    if match is None:
        return None

    return Snapshot(
        dataset=str(match.group(1)), created_at=datetime.fromisoformat(match.group(2))
    )


def _filter_snapshots(output: str, dataset: str | None):
    for line in output.splitlines(keepends=False):
        snapshot = parse_snapshot(line)
        if snapshot is None:
            continue
        if dataset is None or snapshot.dataset == dataset:
            yield snapshot


def get_snapshots(
    dataset_name: str | None = None, ids: list[int] | None = None
) -> Sequence[SnapshotWithId]:
    """Get snapshots ordered by timestamp and filtered by arguments."""

    output = subprocess.run(
        ["zfs", "list", "-t", "snapshot"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        encoding="utf-8",
    ).stdout

    snapshots = sorted(
        _filter_snapshots(output, dataset_name), key=lambda x: x.created_at
    )

    snapshots_with_id = [
        SnapshotWithId.from_snapshot(idx, snapshot)
        for idx, snapshot in enumerate(snapshots, start=1)
    ]

    if ids is None:
        return snapshots_with_id

    result = list(filter(lambda x: x.id in ids, snapshots_with_id))
    return result


def delete_snapshot(snapshot: SnapshotWithId):
    """Delete the snapshot specified in argument."""

    try:
        subprocess.run(["zfs", "destroy", snapshot.name]).check_returncode()
        return True
    except subprocess.CalledProcessError:
        return False


def create_snapshot(dataset: str):
    """Create a snapshot on ``dataset``."""

    snapshot = Snapshot(dataset, datetime.now())

    try:
        subprocess.run(["zfs", "snapshot", snapshot.name]).check_returncode()
    except subprocess.CalledProcessError:
        return None

    return snapshot
