"""Smoke tests for pyfarm-propogation."""

import pytest
from datetime import date

from pyfarm.crops import MemoryRegistry
from pyfarm.propogation import (
    PropogationBehavior,
    PropogationCalculator,
    PropogationMethod,
    NurseryPhase,
    PropogationSetpoint,
    GerminationRecord,
)


def test_setpoint_defaults():
    s = PropogationSetpoint()
    assert s.temp_c == 22.0
    assert s.humidity_rh == 90.0


def test_setpoint_validation():
    with pytest.raises(ValueError):
        PropogationSetpoint(humidity_rh=110)
    with pytest.raises(ValueError):
        PropogationSetpoint(misting_interval_min=0)


def test_germination_record():
    r = GerminationRecord(days_to_germ=5, success_rate=0.9)
    assert r.days_to_germ == 5


def test_germination_record_validation():
    with pytest.raises(ValueError):
        GerminationRecord(success_rate=1.5)


def test_expected_germination_days():
    cold = PropogationCalculator.expected_germination_days(12)
    warm = PropogationCalculator.expected_germination_days(25)
    assert cold > warm


def test_misting_frequency_high_vpd():
    assert PropogationCalculator.misting_frequency(2.0) == 15


def test_days_to_transplant():
    seed_days = PropogationCalculator.days_to_transplant(PropogationMethod.SEED)
    cutting_days = PropogationCalculator.days_to_transplant(PropogationMethod.CUTTING)
    assert cutting_days > seed_days


@pytest.mark.asyncio
async def test_compute_setpoint():
    registry = MemoryRegistry()
    behavior = PropogationBehavior(registry)
    setpoint = await behavior.compute_setpoint("oyster-grey-strain-a", NurseryPhase.GERMINATION)
    assert isinstance(setpoint, PropogationSetpoint)
    assert setpoint.humidity_rh == 95.0


@pytest.mark.asyncio
async def test_record_germination():
    registry = MemoryRegistry()
    behavior = PropogationBehavior(registry)
    record = GerminationRecord(days_to_germ=6, success_rate=0.85)
    await behavior.record_germination(record)


@pytest.mark.asyncio
async def test_missing_cultivar():
    registry = MemoryRegistry()
    behavior = PropogationBehavior(registry)
    with pytest.raises(ValueError):
        await behavior.compute_setpoint("nonexistent", NurseryPhase.SEEDLING)
