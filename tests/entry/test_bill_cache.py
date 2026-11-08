"""The bill command's cache figures: the cache line and the role table after each cost line."""

import io

import pytest

from factory.entry.bill import run
from factory.hosting.adapters.git_cli import GitCli
from factory.shared.domain.identifiers import branch_name
from factory.shared.domain.paths import cost_records_path
from factory.watching.adapters.cost_records_jsonl import JsonLinesCostRecordReader
from factory.watching.application.costs import BillService
from factory.watching.domain.bills import bill, bills_by_stage, cost_line, cost_table
from factory.watching.domain.cost_records import CostRecord
from support.bill_cache_support import (
    CacheRow,
    blocks_by_work_item,
    cache_record,
    cache_section,
    prompt_tokens,
    without_cache,
    without_cache_in_flight,
)
from support.bill_support import sidecar_text
from support.human_clone import HumanClone

MIXED = "F0002-S0001"
MIXED_PATH = "factory/features/F0002-cache/in-progress/F0002-S0001-mixed.md"
SMALL = "F0002-S0002"
SMALL_PATH = "factory/features/F0002-cache/in-progress/F0002-S0002-small.md"
PATHS = {MIXED: MIXED_PATH, SMALL: SMALL_PATH}


def _mixed_records() -> list[CostRecord]:
    # The coder returns after the reviewer, under a stage of its own: the role table
    # groups by role in the order each role first ran, never by stage.
    return [
        cache_record(
            MIXED,
            1,
            stage="tests",
            role="tester",
            tokens=prompt_tokens(input_=10, read=60, written=30),
        ),
        cache_record(
            MIXED,
            2,
            stage="doing",
            role="coder",
            tokens=prompt_tokens(input_=5, read=200, written=45),
        ),
        cache_record(
            MIXED,
            3,
            stage="review",
            role="reviewer",
            tokens=prompt_tokens(input_=2, read=90, written=8),
        ),
        cache_record(
            MIXED, 4, stage="fix", role="coder", tokens=prompt_tokens(input_=5, read=140, written=5)
        ),
    ]


MIXED_LINE = "Cache: 490 read, 88 written, 82 % hit"
MIXED_ROWS = [
    CacheRow(role="tester", read="60", written="30", hit_rate="60 %"),
    CacheRow(role="coder", read="340", written="50", hit_rate="85 %"),
    CacheRow(role="reviewer", read="90", written="8", hit_rate="90 %"),
    CacheRow(role="**total**", read="490", written="88", hit_rate="82 %"),
]


def _small_records() -> list[CostRecord]:
    return [
        cache_record(
            SMALL, 1, stage="doing", role="coder", tokens=prompt_tokens(input_=1, read=2, written=0)
        )
    ]


SMALL_LINE = "Cache: 2 read, 0 written, 67 % hit"


def _service(git: GitCli) -> BillService:
    return BillService(git, JsonLinesCostRecordReader())


def _push(checkout: GitCli, human: HumanClone, records_of: dict[str, list[CostRecord]]) -> None:
    for work_item, records in records_of.items():
        path = PATHS[work_item]
        human.push_files(
            branch_name(work_item),
            {path: f"# {work_item}\n", cost_records_path(path): sidecar_text(records)},
        )
    checkout.fetch()


def _output(checkout: GitCli, argv: list[str]) -> list[str]:
    out = io.StringIO()
    status = run(argv, _service(checkout), out)
    assert status == 0
    return out.getvalue().splitlines()


def _line_after_cost(block: list[str]) -> str:
    cost_index = next(index for index, line in enumerate(block) if line.startswith("Cost: "))
    return next(line for line in block[cost_index + 1 :] if line != "")


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        pytest.param([MIXED], {MIXED: MIXED_LINE}, id="one-work-item"),
        pytest.param([], {MIXED: MIXED_LINE, SMALL: SMALL_LINE}, id="every-work-item-in-flight"),
    ],
)
def test_the_cache_line_follows_each_cost_line_with_read_written_and_hit_rate(
    checkout: GitCli, human: HumanClone, argv: list[str], expected: dict[str, str]
) -> None:
    _push(checkout, human, {MIXED: _mixed_records(), SMALL: _small_records()})

    output = _output(checkout, argv)

    blocks = {MIXED: output} if argv else blocks_by_work_item(output, [MIXED, SMALL])
    assert {work_item: _line_after_cost(block) for work_item, block in blocks.items()} == expected
    assert {work_item: cache_section(block).line for work_item, block in blocks.items()} == expected


def test_the_role_table_has_a_row_per_role_in_first_run_order_adding_up_to_the_total_row(
    checkout: GitCli, human: HumanClone
) -> None:
    _push(checkout, human, {MIXED: _mixed_records()})

    section = cache_section(_output(checkout, [MIXED]))

    assert section.rows == MIXED_ROWS
    *roles, total_row = section.rows
    assert sum(int(row.read) for row in roles) == int(total_row.read)
    assert sum(int(row.written) for row in roles) == int(total_row.written)
    assert section.line == (
        f"Cache: {total_row.read} read, {total_row.written} written, {total_row.hit_rate} hit"
    )


@pytest.mark.parametrize(
    ("counts", "hit_rate"),
    [
        pytest.param((1, 2, 0), "67 %", id="two-of-three-rounds-up"),
        pytest.param((1, 1, 1), "33 %", id="one-of-three-rounds-down"),
        pytest.param((7, 1, 0), "13 %", id="one-of-eight-half-rounds-up"),
        pytest.param((199, 1, 0), "1 %", id="one-of-two-hundred-half-rounds-up"),
    ],
)
def test_the_hit_rate_rounds_half_up_to_a_whole_percent(
    checkout: GitCli, human: HumanClone, counts: tuple[int, int, int], hit_rate: str
) -> None:
    input_, read, written = counts
    tokens = prompt_tokens(input_=input_, read=read, written=written)
    record = cache_record(SMALL, 1, stage="doing", role="coder", tokens=tokens)
    _push(checkout, human, {SMALL: [record]})

    section = cache_section(_output(checkout, [SMALL]))

    assert section.line == f"Cache: {read} read, {written} written, {hit_rate} hit"
    assert [row.hit_rate for row in section.rows] == [hit_rate, hit_rate]


@pytest.mark.parametrize(
    ("records", "line", "hit_rates"),
    [
        pytest.param(
            [
                cache_record(
                    SMALL,
                    1,
                    stage="doing",
                    role="coder",
                    tokens=prompt_tokens(input_=0, read=0, written=0),
                )
            ],
            "Cache: 0 read, 0 written, - hit",
            ["-", "-"],
            id="work-item",
        ),
        pytest.param(
            [
                cache_record(
                    SMALL,
                    1,
                    stage="tests",
                    role="tester",
                    tokens=prompt_tokens(input_=0, read=0, written=0),
                ),
                cache_record(
                    SMALL,
                    2,
                    stage="doing",
                    role="coder",
                    tokens=prompt_tokens(input_=1, read=3, written=0),
                ),
            ],
            "Cache: 3 read, 0 written, 75 % hit",
            ["-", "75 %", "75 %"],
            id="role",
        ),
    ],
)
def test_no_prompt_tokens_shows_a_dash_for_the_hit_rate(
    checkout: GitCli,
    human: HumanClone,
    records: list[CostRecord],
    line: str,
    hit_rates: list[str],
) -> None:
    _push(checkout, human, {SMALL: records})

    section = cache_section(_output(checkout, [SMALL]))

    assert section.line == line
    assert [row.hit_rate for row in section.rows] == hit_rates


def _old_block(records: list[CostRecord]) -> list[str]:
    return [
        *cost_table(bills_by_stage(records)).split("\n"),
        "",
        f"Cost: {cost_line(bill(records))}",
    ]


@pytest.mark.parametrize(
    "argv",
    [pytest.param([MIXED], id="one-work-item"), pytest.param([], id="every-work-item-in-flight")],
)
def test_every_earlier_line_of_the_bill_is_unchanged(
    checkout: GitCli, human: HumanClone, argv: list[str]
) -> None:
    _push(checkout, human, {MIXED: _mixed_records(), SMALL: _small_records()})

    output = _output(checkout, argv)

    if argv:
        assert without_cache(output) == _old_block(_mixed_records())
    else:
        assert without_cache_in_flight(output, [MIXED, SMALL]) == [
            MIXED,
            *_old_block(_mixed_records()),
            "",
            SMALL,
            *_old_block(_small_records()),
        ]


@pytest.mark.parametrize("flag", ["--help", "-h"])
def test_the_help_prints_the_usage_naming_the_cache_figures(checkout: GitCli, flag: str) -> None:
    long_help = io.StringIO()
    run(["--help"], _service(checkout), long_help)
    out = io.StringIO()

    status = run([flag], _service(checkout), out)

    text = out.getvalue()
    assert text.startswith("usage: factory-bill")
    for figure in ("cache read", "cache written", "hit rate"):
        assert figure in text
    assert text == long_help.getvalue()
    assert status == 0
