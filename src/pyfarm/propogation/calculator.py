"""Propagation calculations."""

from __future__ import annotations

from pyfarm.propogation.models import PropogationMethod


class PropogationCalculator:

    @staticmethod
    def expected_germination_days(temp_c: float, base_days: int = 7) -> int:
        """Estimate germination days based on temperature."""
        if temp_c < 10:
            return base_days * 3
        if temp_c < 15:
            return base_days * 2
        if temp_c >= 25:
            return max(2, base_days - 2)
        return base_days

    @staticmethod
    def misting_frequency(vpd: float, substrate_type: str = "coir") -> int:
        """Misting interval in minutes based on VPD and substrate."""
        base = 30
        if vpd > 1.5:
            base = 15
        elif vpd < 0.5:
            base = 60

        if substrate_type in ("rockwool", "perlite"):
            base = max(10, base - 10)
        return base

    @staticmethod
    def days_to_transplant(method: PropogationMethod, base_days: int = 14) -> int:
        """Days from propagation start to transplant readiness."""
        offsets = {
            PropogationMethod.SEED: 0,
            PropogationMethod.CUTTING: 7,
            PropogationMethod.DIVISION: -3,
            PropogationMethod.LAYERING: 21,
            PropogationMethod.TISSUE_CULTURE: -5,
        }
        return base_days + offsets.get(method, 0)
