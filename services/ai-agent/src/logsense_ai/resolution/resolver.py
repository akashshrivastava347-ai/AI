"""Resolve free text such as "Conv Motor-3" to a machine in the asset register.

A deterministic cascade, cheapest and most certain first:

    exact asset code  ->  exact name  ->  learned alias  ->  fuzzy token match

Every stage is recorded on the record, so a bad mapping can be traced to the stage
that produced it rather than guessed at. The semantic (embedding) stage from the
architecture doc is deliberately absent in this story: it needs an embedding
provider and a backfill job, and the first three stages already carry most plants.

Resolution is always plant-scoped. A machine in another plant is never a candidate,
which is a tenancy guarantee as much as a correctness one.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from rapidfuzz import fuzz
from sqlalchemy import select
from sqlalchemy.orm import Session

from logsense_ai.domain.enums import ResolutionMethod
from logsense_ai.domain.models import Machine, MachineAlias
from logsense_ai.extraction.dictionary import expand_shorthand, normalize


@dataclass(slots=True)
class MachineCandidate:
    machine_id: str
    machine_name: str
    asset_code: str
    score: float
    method: ResolutionMethod


@dataclass(slots=True)
class ResolutionOutcome:
    """Result of one resolution attempt.

    ``candidates`` is kept even on success so a reviewer can see what the resolver
    was choosing between — the difference between a confident match and a coin flip.
    """

    machine_id: str | None
    confidence: float
    method: ResolutionMethod
    candidates: list[MachineCandidate] = field(default_factory=list)

    @property
    def resolved(self) -> bool:
        return self.machine_id is not None

    @property
    def is_ambiguous(self) -> bool:
        """True when the top two candidates are close enough that a human should pick.

        Ambiguity is not the same as low confidence: two 0.85 matches are individually
        confident and jointly useless.
        """
        if len(self.candidates) < 2:
            return False
        return (self.candidates[0].score - self.candidates[1].score) < 0.08


class MachineResolver:
    def __init__(self, session: Session, *, fuzzy_floor: float = 0.60) -> None:
        self._session = session
        self._fuzzy_floor = fuzzy_floor

    def resolve(self, text: str | None, *, plant_id: str) -> ResolutionOutcome:
        if not text or not text.strip():
            return ResolutionOutcome(None, 0.0, ResolutionMethod.UNRESOLVED)

        needle = normalize(text)
        machines = list(
            self._session.scalars(
                select(Machine).where(Machine.plant_id == plant_id, Machine.is_active.is_(True))
            )
        )
        if not machines:
            return ResolutionOutcome(None, 0.0, ResolutionMethod.UNRESOLVED)

        # 1 & 2 — exact code, then exact name. Certain, so we stop immediately.
        for machine in machines:
            if normalize(machine.asset_code) == needle:
                return ResolutionOutcome(
                    machine.id,
                    1.0,
                    ResolutionMethod.EXACT_CODE,
                    [self._candidate(machine, 1.0, ResolutionMethod.EXACT_CODE)],
                )
        for machine in machines:
            if normalize(machine.name) == needle:
                return ResolutionOutcome(
                    machine.id,
                    0.99,
                    ResolutionMethod.EXACT_NAME,
                    [self._candidate(machine, 0.99, ResolutionMethod.EXACT_NAME)],
                )

        # 3 — learned aliases. This is where past human corrections pay off.
        alias = self._session.scalars(
            select(MachineAlias).where(
                MachineAlias.plant_id == plant_id,
                MachineAlias.normalized_text == needle,
            )
        ).first()
        if alias is not None:
            machine = self._session.get(Machine, alias.machine_id)
            if machine is not None and machine.is_active:
                score = min(0.98, max(0.80, alias.confidence))
                return ResolutionOutcome(
                    machine.id,
                    score,
                    ResolutionMethod.ALIAS,
                    [self._candidate(machine, score, ResolutionMethod.ALIAS)],
                )

        # 4 — fuzzy. Shorthand is expanded first so "L3 conv mtr" and
        # "Line 3 Conveyor Motor" share tokens before scoring.
        expanded = normalize(expand_shorthand(text))
        scored: list[MachineCandidate] = []
        for machine in machines:
            # Name and code are scored SEPARATELY, then the best is taken. Concatenating
            # them dilutes the signal: the asset code contributes tokens the technician
            # never wrote, which drags an exact name match down and narrows the gap to
            # the runner-up until everything looks ambiguous.
            name_target = normalize(expand_shorthand(machine.name))
            code_target = normalize(expand_shorthand(machine.asset_code))
            # token_set_ratio ignores word order and duplicated tokens, which suits
            # "Conv Motor-3" vs "Line 3 Conveyor Motor".
            #
            # partial_token_set_ratio is deliberately NOT blended in: it returns 100
            # whenever the token intersection is non-empty, so "Line 3 Conveyor Motor"
            # and "Line 3 Conveyor Gearbox" both score a perfect match and every row
            # becomes ambiguous. WRatio saturates the same way on these strings.
            ratio = max(
                fuzz.token_set_ratio(expanded, name_target),
                fuzz.token_set_ratio(expanded, code_target),
            )
            scored.append(self._candidate(machine, round(ratio / 100.0, 4), ResolutionMethod.FUZZY))

        scored.sort(key=lambda c: c.score, reverse=True)
        top = scored[0]
        if top.score < self._fuzzy_floor:
            # Report nothing rather than guess. An unresolved row goes to a human;
            # a wrongly resolved row silently corrupts that machine's statistics.
            return ResolutionOutcome(None, top.score, ResolutionMethod.UNRESOLVED, scored[:5])

        return ResolutionOutcome(
            top.machine_id,
            # Fuzzy never claims certainty, however good the string match looks.
            min(top.score, 0.95),
            ResolutionMethod.FUZZY,
            scored[:5],
        )

    @staticmethod
    def _candidate(machine: Machine, score: float, method: ResolutionMethod) -> MachineCandidate:
        return MachineCandidate(
            machine_id=machine.id,
            machine_name=machine.name,
            asset_code=machine.asset_code,
            score=score,
            method=method,
        )
