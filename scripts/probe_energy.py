#!/usr/bin/env python3
"""Show whether real RAPL package-energy counters are readable."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from energy_meter import RaplMeter, NoEnergyMeterError


def main() -> None:
    try:
        meter = RaplMeter()
        before = meter.snapshot()
        after = meter.snapshot()
        print("available: RAPL CPU package; zones:", ", ".join(z.name for z in meter.zones))
        print("sample read interval (J):", meter.joules_between(before, after))
        print("NOTE: package energy excludes other system components and is not GPU energy")
    except (NoEnergyMeterError, PermissionError, OSError) as exc:
        print("no-accessible-meter:", exc)
        print("Do NOT report timing, MACs or bytes as Joules.")


if __name__ == "__main__":
    main()
