import tempfile
import unittest
from pathlib import Path
from energy_meter.rapl import RaplMeter, NoEnergyMeterError, counter_delta_uj


class RaplTests(unittest.TestCase):
    def test_delta_normal(self):
        self.assertEqual(counter_delta_uj(150, 175, 1000), 25)

    def test_delta_rollover(self):
        self.assertEqual(counter_delta_uj(990, 10, 1000), 20)

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            counter_delta_uj(0, 100, 0)

    def test_missing_meter(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(NoEnergyMeterError):
                RaplMeter(directory)

    def test_fake_package_without_subzone_double_counting(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "intel-rapl:0"
            package.mkdir()
            (package / "energy_uj").write_text("900")
            (package / "max_energy_range_uj").write_text("1000")
            (package / "name").write_text("package-0")
            subzone = Path(directory) / "intel-rapl:0:0"
            subzone.mkdir()
            (subzone / "energy_uj").write_text("850")
            (subzone / "max_energy_range_uj").write_text("1000")
            meter = RaplMeter(directory)
            self.assertEqual(len(meter.zones), 1)
            before = meter.snapshot()
            (package / "energy_uj").write_text("10")
            self.assertAlmostEqual(meter.joules_between(before, meter.snapshot()), 0.000110)


if __name__ == "__main__":
    unittest.main()
