"""Demo plant seed.

Mirrors the reference plant from the prototype so the pipeline can be exercised
end to end without a customer's data. Idempotent: safe to run repeatedly.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from logsense_ai.domain.enums import AliasSource
from logsense_ai.domain.models import Machine, MachineAlias, Plant

DEMO_TENANT_ID = "11111111-1111-1111-1111-111111111111"
DEMO_PLANT_CODE = "PUNE-01"

_MACHINES: list[tuple[str, str, str, str]] = [
    ("Line 3 Conveyor Motor", "CONV-L3-MTR-01", "Line 3", "Motor"),
    ("Line 3 Conveyor Gearbox", "CONV-L3-GBX-01", "Line 3", "Gearbox"),
    ("Line 1 Filling Pump", "FILL-L1-PMP-01", "Line 1", "Pump"),
    ("Line 2 Capping Motor", "CAP-L2-MTR-01", "Line 2", "Motor"),
    ("Line 2 Labeller VFD", "LBL-L2-VFD-01", "Line 2", "VFD"),
    ("Line 4 Packing Conveyor", "PACK-L4-CNV-01", "Line 4", "Conveyor"),
    ("Utilities Air Compressor", "UTIL-CMP-01", "Utilities", "Compressor"),
]

# One pre-seeded alias, so the alias branch of the resolver is demonstrable from a
# fresh database. Everything else is learned from human corrections.
_ALIASES: list[tuple[str, str]] = [
    ("l3 conv mtr", "CONV-L3-MTR-01"),
]


def seed_demo_plant(session: Session) -> Plant:
    plant = session.scalars(
        select(Plant).where(Plant.tenant_id == DEMO_TENANT_ID, Plant.code == DEMO_PLANT_CODE)
    ).first()

    if plant is None:
        plant = Plant(
            tenant_id=DEMO_TENANT_ID,
            name="Demo Pune Manufacturing Plant",
            code=DEMO_PLANT_CODE,
            auto_approve_threshold=0.80,
            downtime_cost_per_hour_inr=125000.0,
        )
        session.add(plant)
        session.flush()

    existing = {
        m.asset_code for m in session.scalars(select(Machine).where(Machine.plant_id == plant.id))
    }
    for name, code, line, machine_type in _MACHINES:
        if code in existing:
            continue
        session.add(
            Machine(
                tenant_id=plant.tenant_id,
                plant_id=plant.id,
                name=name,
                asset_code=code,
                line=line,
                machine_type=machine_type,
            )
        )
    session.flush()

    by_code = {
        m.asset_code: m
        for m in session.scalars(select(Machine).where(Machine.plant_id == plant.id))
    }
    known_aliases = {
        a.normalized_text
        for a in session.scalars(select(MachineAlias).where(MachineAlias.plant_id == plant.id))
    }
    for alias_text, code in _ALIASES:
        if alias_text in known_aliases or code not in by_code:
            continue
        session.add(
            MachineAlias(
                tenant_id=plant.tenant_id,
                plant_id=plant.id,
                machine_id=by_code[code].id,
                alias_text=alias_text,
                normalized_text=alias_text,
                confidence=0.95,
                source=AliasSource.MANUAL,
                created_by="seed",
            )
        )
    session.flush()
    return plant
