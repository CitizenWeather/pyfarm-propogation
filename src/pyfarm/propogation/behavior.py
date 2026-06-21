"""Propagation behavior."""

from __future__ import annotations

from pyfarm.crops.registry import CultivarRegistry
from pyfarm.propogation.calculator import PropogationCalculator
from pyfarm.propogation.models import (
    GerminationRecord,
    NurseryPhase,
    PropogationSetpoint,
)

_PHASE_SETPOINTS: dict[NurseryPhase, PropogationSetpoint] = {
    NurseryPhase.GERMINATION: PropogationSetpoint(
        temp_c=24.0, humidity_rh=95.0, light_schedule="0/24", misting_interval_min=20
    ),
    NurseryPhase.SEEDLING: PropogationSetpoint(
        temp_c=22.0, humidity_rh=85.0, light_schedule="16/8", misting_interval_min=30
    ),
    NurseryPhase.HARDENING: PropogationSetpoint(
        temp_c=20.0, humidity_rh=70.0, light_schedule="14/10", misting_interval_min=60
    ),
}

_GERMINATION_LOG: list[GerminationRecord] = []


class PropogationBehavior:

    def __init__(self, registry: CultivarRegistry):
        self.registry = registry
        self.calculator = PropogationCalculator()

    async def compute_setpoint(
        self, cultivar_id: str, phase: NurseryPhase
    ) -> PropogationSetpoint:
        """Compute propagation setpoint for given phase."""
        cultivar = await self.registry.get_cultivar(cultivar_id)
        if not cultivar:
            raise ValueError(f"Cultivar {cultivar_id} not found")

        base = _PHASE_SETPOINTS.get(phase, _PHASE_SETPOINTS[NurseryPhase.SEEDLING])
        opt_temp = cultivar.optimal_temperature
        adjusted_temp = (opt_temp.min + opt_temp.max) / 2

        return PropogationSetpoint(
            temp_c=adjusted_temp,
            humidity_rh=base.humidity_rh,
            light_schedule=base.light_schedule,
            misting_interval_min=base.misting_interval_min,
        )

    async def record_germination(self, record: GerminationRecord) -> None:
        """Record a germination event."""
        _GERMINATION_LOG.append(record)
