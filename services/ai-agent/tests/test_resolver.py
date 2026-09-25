"""Machine resolution cascade and its refusal behaviour."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from logsense_ai.domain.enums import ResolutionMethod
from logsense_ai.domain.models import Machine, Plant
from logsense_ai.resolution.resolver import MachineResolver


def _machine(session: Session, plant: Plant, code: str) -> Machine:
    return session.scalars(
        select(Machine).where(Machine.plant_id == plant.id, Machine.asset_code == code)
    ).one()


def test_exact_asset_code_wins(session: Session, plant: Plant) -> None:
    out = MachineResolver(session).resolve("CONV-L3-MTR-01", plant_id=plant.id)
    assert out.method is ResolutionMethod.EXACT_CODE
    assert out.confidence == 1.0
    assert out.machine_id == _machine(session, plant, "CONV-L3-MTR-01").id


def test_exact_name_match(session: Session, plant: Plant) -> None:
    out = MachineResolver(session).resolve("line 3 conveyor motor", plant_id=plant.id)
    assert out.method is ResolutionMethod.EXACT_NAME
    assert out.machine_id == _machine(session, plant, "CONV-L3-MTR-01").id


def test_learned_alias_resolves(session: Session, plant: Plant) -> None:
    """The seeded alias proves past corrections keep paying off."""
    out = MachineResolver(session).resolve("L3 conv mtr", plant_id=plant.id)
    assert out.method is ResolutionMethod.ALIAS
    assert out.machine_id == _machine(session, plant, "CONV-L3-MTR-01").id


def test_fuzzy_handles_hinglish_and_shorthand(session: Session, plant: Plant) -> None:
    out = MachineResolver(session).resolve("Line 3 ka conveyor motor", plant_id=plant.id)
    assert out.resolved
    assert out.machine_id == _machine(session, plant, "CONV-L3-MTR-01").id
    # Fuzzy never claims certainty, however good the string looks.
    assert out.confidence <= 0.95


def test_devanagari_machine_text_resolves(session: Session, plant: Plant) -> None:
    """A Marathi/Hindi technician must reach the same asset as an English one."""
    out = MachineResolver(session).resolve("लाइन 2 कैपिंग मोटर", plant_id=plant.id)
    assert out.resolved
    assert out.machine_id == _machine(session, plant, "CAP-L2-MTR-01").id


def test_unresolvable_text_reports_nothing(session: Session, plant: Plant) -> None:
    """Refusing beats guessing: a wrong mapping corrupts a machine's statistics."""
    out = MachineResolver(session).resolve("something entirely unrelated", plant_id=plant.id)
    assert not out.resolved
    assert out.method is ResolutionMethod.UNRESOLVED


def test_empty_text_is_unresolved(session: Session, plant: Plant) -> None:
    assert not MachineResolver(session).resolve("   ", plant_id=plant.id).resolved
    assert not MachineResolver(session).resolve(None, plant_id=plant.id).resolved


def test_genuine_ambiguity_is_detected(session: Session, plant: Plant) -> None:
    """ "L3 conv" really could be the conveyor motor or the conveyor gearbox.

    Detecting this is the point: a human resolves it once, an alias is written, and
    the question is never asked again.
    """
    out = MachineResolver(session).resolve("L3 conv", plant_id=plant.id)
    assert out.is_ambiguous
    assert {c.asset_code for c in out.candidates[:2]} == {
        "CONV-L3-MTR-01",
        "CONV-L3-GBX-01",
    }


def test_resolution_is_plant_scoped(session: Session, plant: Plant) -> None:
    """A machine in another plant is never a candidate — a tenancy guarantee."""
    other = Plant(tenant_id="other-tenant", name="Other Plant", code="OTHER-01")
    session.add(other)
    session.flush()
    session.add(
        Machine(
            tenant_id=other.tenant_id,
            plant_id=other.id,
            name="Line 3 Conveyor Motor",
            asset_code="CONV-L3-MTR-01",
        )
    )
    session.flush()

    out = MachineResolver(session).resolve("CONV-L3-MTR-01", plant_id=other.id)
    assert out.machine_id != _machine(session, plant, "CONV-L3-MTR-01").id


def test_inactive_machines_are_excluded(session: Session, plant: Plant) -> None:
    machine = _machine(session, plant, "CONV-L3-MTR-01")
    machine.is_active = False
    session.flush()
    out = MachineResolver(session).resolve("CONV-L3-MTR-01", plant_id=plant.id)
    assert out.machine_id != machine.id
