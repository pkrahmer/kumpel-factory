# SPDX-License-Identifier: Apache-2.0
"""Bills: the sums of cost records by stage, by role and in total, and their texts."""

from collections.abc import Callable, Sequence
from datetime import timedelta
from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel, ConfigDict, NonNegativeInt

from factory.agents.domain.agent_runs import TokenCounts
from factory.shared.domain.identifiers import Name
from factory.watching.domain.cost_records import CostRecord

_ZERO_TOKENS = TokenCounts(input=0, output=0)
_ONE_DECIMAL = Decimal("0.1")
_TWO_DECIMALS = Decimal("0.01")
_SECONDS_PER_MINUTE = Decimal(60)
_TABLE_HEADER = "| stage | runs | min | model min | turns | in | cached | out | USD |"
_TABLE_ALIGNMENT = "| :-- | --: | --: | --: | --: | --: | --: | --: | --: |"
_TOTAL_CELL = "**total**"
_CACHE_HEADER = "| role | cache read | cache written | hit rate |"
_CACHE_ALIGNMENT = "| :-- | --: | --: | --: |"
_PERCENT = Decimal(100)
_WHOLE = Decimal(1)
_NO_HIT_RATE = "-"


class Bill(BaseModel):
    """The sums of a set of cost records; a value the runtime did not report is not in them."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    runs: NonNegativeInt
    runs_cost_unknown: NonNegativeInt
    duration: timedelta
    turns: NonNegativeInt
    tokens: TokenCounts
    cost_usd: Decimal
    model_duration: timedelta = timedelta(0)


class RoleBill(BaseModel):
    """The bill of one role's records."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    role: Name
    bill: Bill


class StageBill(BaseModel):
    """The bill of one stage's records."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    stage: Name
    bill: Bill


def _add_tokens(left: TokenCounts, right: TokenCounts) -> TokenCounts:
    return TokenCounts(
        input=left.input + right.input,
        output=left.output + right.output,
        cache_read=left.cache_read + right.cache_read,
        cache_creation=left.cache_creation + right.cache_creation,
    )


def _known_duration(seconds: float | None) -> timedelta:
    return timedelta(0) if seconds is None else timedelta(seconds=seconds)


def _record_bill(record: CostRecord) -> Bill:
    # An unknown measure contributes nothing; only the run itself is always counted.
    return Bill(
        runs=1,
        runs_cost_unknown=1 if record.cost_usd is None else 0,
        duration=_known_duration(record.duration_seconds),
        turns=0 if record.turns is None else record.turns,
        tokens=_ZERO_TOKENS if record.tokens is None else record.tokens,
        cost_usd=Decimal(0) if record.cost_usd is None else record.cost_usd,
        model_duration=_known_duration(record.model_seconds),
    )


def _add(left: Bill, right: Bill) -> Bill:
    return Bill(
        runs=left.runs + right.runs,
        runs_cost_unknown=left.runs_cost_unknown + right.runs_cost_unknown,
        duration=left.duration + right.duration,
        turns=left.turns + right.turns,
        tokens=_add_tokens(left.tokens, right.tokens),
        cost_usd=left.cost_usd + right.cost_usd,
        model_duration=left.model_duration + right.model_duration,
    )


def _sum(bills: Sequence[Bill]) -> Bill:
    result = Bill(
        runs=0,
        runs_cost_unknown=0,
        duration=timedelta(0),
        turns=0,
        tokens=_ZERO_TOKENS,
        cost_usd=Decimal(0),
    )
    for each in bills:
        result = _add(result, each)
    return result


def bill(records: Sequence[CostRecord]) -> Bill:
    """The bill of every record, whatever its end reason, with unknown values skipped."""
    return _sum([_record_bill(record) for record in records])


def _groups(records: Sequence[CostRecord], key: Callable[[CostRecord], str]) -> dict[str, Bill]:
    # A dict keeps the order of each key's first record, so a returning key joins its group.
    groups: dict[str, list[CostRecord]] = {}
    for record in records:
        groups.setdefault(key(record), []).append(record)
    return {name: bill(group) for name, group in groups.items()}


def bills_by_stage(records: Sequence[CostRecord]) -> list[StageBill]:
    """One bill per stage in the order of its first record; a returning stage joins it."""
    groups = _groups(records, lambda record: record.stage)
    return [StageBill(stage=stage, bill=each) for stage, each in groups.items()]


def bills_by_role(records: Sequence[CostRecord]) -> list[RoleBill]:
    """One bill per role in the order of its first record; a returning role joins it."""
    groups = _groups(records, lambda record: record.role)
    return [RoleBill(role=role, bill=each) for role, each in groups.items()]


def total(stage_bills: Sequence[StageBill]) -> Bill:
    """The field-by-field sum of the stage bills."""
    return _sum([stage_bill.bill for stage_bill in stage_bills])


def one_decimal(value: Decimal) -> str:
    """`value` with one decimal, rounded half up."""
    return str(value.quantize(_ONE_DECIMAL, rounding=ROUND_HALF_UP))


def _minutes(duration: timedelta) -> str:
    seconds = Decimal(str(duration.total_seconds()))
    return one_decimal(seconds / _SECONDS_PER_MINUTE)


def _dollars(bill: Bill) -> str:
    dollars = str(bill.cost_usd.quantize(_TWO_DECIMALS, rounding=ROUND_HALF_UP))
    if bill.runs_cost_unknown > 0:
        return f"{dollars} + {bill.runs_cost_unknown} unknown"
    return dollars


def _tokens_in(tokens: TokenCounts) -> int:
    return tokens.input + tokens.cache_creation


def cost_line(bill: Bill) -> str:
    """The one-line text of a bill: runs, minutes, turns, tokens and dollars."""
    tokens = bill.tokens
    return (
        f"{bill.runs} runs, {_minutes(bill.duration)} min, {bill.turns} turns, "
        f"{_tokens_in(tokens)} tokens in ({tokens.cache_read} more from cache), "
        f"{tokens.output} out, ${_dollars(bill)}"
    )


def _row(first_cell: str, bill: Bill) -> str:
    cells = [
        first_cell,
        str(bill.runs),
        _minutes(bill.duration),
        _minutes(bill.model_duration),
        str(bill.turns),
        str(_tokens_in(bill.tokens)),
        str(bill.tokens.cache_read),
        str(bill.tokens.output),
        _dollars(bill),
    ]
    return "| " + " | ".join(cells) + " |"


def cost_table(stage_bills: Sequence[StageBill]) -> str:
    """The Markdown table of the stage bills, one row each, and their total as the last row."""
    rows = [_row(stage_bill.stage, stage_bill.bill) for stage_bill in stage_bills]
    return "\n".join(
        [_TABLE_HEADER, _TABLE_ALIGNMENT, *rows, _row(_TOTAL_CELL, total(stage_bills))]
    )


def hit_rate(tokens: TokenCounts) -> str:
    """The share of the prompt tokens read from the cache, a whole percent rounded half up.

    The prompt tokens are those read from the cache, those written to it and the uncached
    input; `-` when there are none.
    """
    prompt = tokens.cache_read + tokens.cache_creation + tokens.input
    if prompt == 0:
        return _NO_HIT_RATE
    share = Decimal(tokens.cache_read) * _PERCENT / Decimal(prompt)
    return f"{share.quantize(_WHOLE, rounding=ROUND_HALF_UP)} %"


def cache_line(bill: Bill) -> str:
    """The one-line text of a bill's cache: tokens read from it, written to it, and hit rate."""
    tokens = bill.tokens
    return f"{tokens.cache_read} read, {tokens.cache_creation} written, {hit_rate(tokens)} hit"


def _cache_row(first_cell: str, bill: Bill) -> str:
    tokens = bill.tokens
    cells = [first_cell, str(tokens.cache_read), str(tokens.cache_creation), hit_rate(tokens)]
    return "| " + " | ".join(cells) + " |"


def cache_table(role_bills: Sequence[RoleBill]) -> str:
    """The Markdown table of the roles' cache figures, one row each, and their total last."""
    rows = [_cache_row(role_bill.role, role_bill.bill) for role_bill in role_bills]
    whole = _sum([role_bill.bill for role_bill in role_bills])
    return "\n".join([_CACHE_HEADER, _CACHE_ALIGNMENT, *rows, _cache_row(_TOTAL_CELL, whole)])
