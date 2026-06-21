"""Data models for propagation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class PropogationMethod(str, Enum):
    SEED = "seed"
    CUTTING = "cutting"
    DIVISION = "division"
    LAYERING = "layering"
    TISSUE_CULTURE = "tissue_culture"


class NurseryPhase(str, Enum):
    GERMINATION = "germination"
    SEEDLING = "seedling"
    HARDENING = "hardening"


@dataclass
class PropogationSetpoint:
    temp_c: float = 22.0
    humidity_rh: float = 90.0
    light_schedule: str = "16/8"
    misting_interval_min: int = 30

    def __post_init__(self):
        if not -10 <= self.temp_c <= 50:
            raise ValueError("temp_c out of range")
        if not 0 <= self.humidity_rh <= 100:
            raise ValueError("humidity_rh must be 0-100")
        if self.misting_interval_min <= 0:
            raise ValueError("misting_interval_min must be positive")


@dataclass
class GerminationRecord:
    sow_date: date = field(default_factory=date.today)
    method: PropogationMethod = PropogationMethod.SEED
    days_to_germ: int = 0
    success_rate: float = 0.0

    def __post_init__(self):
        if self.days_to_germ < 0:
            raise ValueError("days_to_germ must be non-negative")
        if not 0 <= self.success_rate <= 1.0:
            raise ValueError("success_rate must be 0-1")
