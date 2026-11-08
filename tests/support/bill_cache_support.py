"""Helpers for the bill's cache figures: records with known tokens and the reading of its lines."""

import re
from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from factory.agents.domain.agent_runs import TokenCounts
from factory.watching.domain.cost_records import CostRecord

CACHE_PREFIX = "Cache: "
_ALIGNMENT_CELL = re.compile(r":?-+:?")


class CacheRow(BaseModel):
    """One row of the bill's role table: the role and its three cache figures as printed."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    role: str
    read: str
    written: str
    hit_rate: str


class CacheSection(BaseModel):
    """What the bill prints after a work item's cost line: its cache line and role table rows."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    line: str
    rows: list[CacheRow]


def cache_record(
    work_item: str,
    number: int,
    *,
    stage: str,
    role: str,
    tokens: TokenCounts,
) -> CostRecord:
    """A completed record of `work_item`, its run and start told apart by `number`."""
    return CostRecord(
        run=f"{number:x}" * 32,
        work_item=work_item,
        stage=stage,
        role=role,
        attempt=0,
        status="completed",
        started_at=datetime(2026, 10, 12, 9, number, tzinfo=UTC),
        duration_seconds=60.0,
        end_reason="completed",
        turns=1,
        tokens=tokens,
        cost_usd=Decimal("0.5"),
    )


def prompt_tokens(*, input_: int, read: int, written: int, output: int = 7) -> TokenCounts:
    """Token counts with `input_` uncached, `read` from the cache and `written` to it."""
    return TokenCounts(input=input_, output=output, cache_read=read, cache_creation=written)


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_table_line(line: str) -> bool:
    return line.startswith("|")


def _cache_index(lines: list[str]) -> int:
    found = [index for index, line in enumerate(lines) if line.startswith(CACHE_PREFIX)]
    assert len(found) == 1, f"expected one cache line in {lines}"
    return found[0]


def _table_end(lines: list[str], cache_index: int) -> int:
    index = cache_index + 1
    while index < len(lines) and lines[index] == "":
        index += 1
    while index < len(lines) and _is_table_line(lines[index]):
        index += 1
    return index


def cache_section(block: list[str]) -> CacheSection:
    """One block's cache line and role table rows, the header and alignment rows left out."""
    start = _cache_index(block)
    table = [line for line in block[start + 1 : _table_end(block, start)] if line != ""]
    assert table, f"expected a role table after the cache line in {block}"
    assert _cells(table[0]) == ["role", "cache read", "cache written", "hit rate"]
    rows = [
        CacheRow(role=cells[0], read=cells[1], written=cells[2], hit_rate=cells[3])
        for cells in (_cells(line) for line in table[1:])
        if not all(_ALIGNMENT_CELL.fullmatch(cell) for cell in cells)
    ]
    return CacheSection(line=block[start], rows=rows)


def without_cache(block: list[str]) -> list[str]:
    """`block` without its cache line, its role table and the empty lines around them."""
    start = _cache_index(block)
    end = _table_end(block, start)
    before = start
    while before > 0 and block[before - 1] == "":
        before -= 1
    return [*block[:before], *block[end:]]


def blocks_by_work_item(output: list[str], work_items: list[str]) -> dict[str, list[str]]:
    """The lines under each work item's id line in the bill of every work item in flight."""
    starts = [output.index(work_item) for work_item in work_items]
    ends = [*starts[1:], len(output)]
    return {
        work_item: output[start + 1 : end]
        for work_item, start, end in zip(work_items, starts, ends, strict=True)
    }


def without_cache_in_flight(output: list[str], work_items: list[str]) -> list[str]:
    """The bill of every work item in flight, each block without its cache lines."""
    blocks = blocks_by_work_item(output, work_items)
    result: list[str] = []
    for work_item in work_items:
        block = blocks[work_item]
        trailing = len(block) - len(block_without_trailing_blank(block))
        result.extend([work_item, *without_cache(block_without_trailing_blank(block))])
        result.extend([""] * trailing)
    return result


def block_without_trailing_blank(block: list[str]) -> list[str]:
    """`block` without the empty lines at its end, which separate it from the next one."""
    end = len(block)
    while end > 0 and block[end - 1] == "":
        end -= 1
    return block[:end]
