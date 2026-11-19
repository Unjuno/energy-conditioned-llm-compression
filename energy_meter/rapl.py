"""Linux CPU-package RAPL meter. Not whole-system or GPU energy.

Reads top-level RAPL zones only; package subzones are excluded to avoid
double counting. Does not subtract idle energy. Permissions vary by host.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re


class NoEnergyMeterError(RuntimeError):
    """No readable physical energy counter is available."""


def counter_delta_uj(start: int, end: int, max_range: int) -> int:
    """Difference in microjoules for an interval with at most one rollover."""
    if not (max_range > 0 and 0 <= start < max_range and 0 <= end < max_range):
        raise ValueError("invalid counter reading or max_energy_range_uj")
    return end - start if end >= start else max_range - start + end


@dataclass(frozen=True)
class Zone:
    name: str
    counter: Path
    max_range: int


class RaplMeter:
    def __init__(self, sysfs_root: str | Path = "/sys/class/powercap"):
        root = Path(sysfs_root)
        if not root.exists():
            raise NoEnergyMeterError(f"powercap sysfs not found: {root}")
        zones = []
        for path in sorted(root.iterdir()):
            if not re.fullmatch(r"(?:intel|amd)-rapl:\d+", path.name):
                continue
            energy = path / "energy_uj"
            maximum = path / "max_energy_range_uj"
            if not energy.exists() or not maximum.exists():
                continue
            try:
                current = int(energy.read_text().strip())
                mx = int(maximum.read_text().strip())
                if not 0 <= current < mx:
                    continue
            except (PermissionError, OSError, ValueError):
                continue
            label = path / "name"
            try:
                name = label.read_text().strip() if label.exists() else path.name
            except OSError:
                name = path.name
            zones.append(Zone(name, energy, mx))
        if not zones:
            raise NoEnergyMeterError("no readable CPU-package RAPL energy counters")
        self.zones = tuple(zones)

    def snapshot(self) -> tuple[int, ...]:
        return tuple(int(zone.counter.read_text().strip()) for zone in self.zones)

    def joules_between(self, before: tuple[int, ...], after: tuple[int, ...]) -> float:
        if len(before) != len(self.zones) or len(after) != len(self.zones):
            raise ValueError("snapshot length differs from number of RAPL zones")
        return sum(
            counter_delta_uj(s, e, zone.max_range)
            for s, e, zone in zip(before, after, self.zones)
        ) / 1_000_000.0
