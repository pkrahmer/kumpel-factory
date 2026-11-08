# SPDX-License-Identifier: Apache-2.0
"""The bill command: the cost and cache figures of one work item, or of every one in flight."""

import re
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

from factory.entry.wiring import build_bill_service
from factory.shared.domain.identifiers import ACCEPTANCE_ID, STORY_ID
from factory.watching.application.costs import BillService, WorkItemBill

_USAGE = "usage: factory-bill [<work item id>]"
_HELP = f"""{_USAGE}

Print the bill of the work item, or of every work item in flight, one block each:
the table of its stages, the Cost: line, then its cache figures in a Cache: line
and a table by role. The cache figures are the tokens read from the cache (cache
read), the tokens written to it (cache written) and the hit rate: cache read
divided by every prompt token (cache read, cache written and uncached input), as
a whole percent, or - when there were no prompt tokens.
"""
_HELP_FLAGS = ("-h", "--help")
_OK = 0
_NO_BILL = 1
_FAILURE = 2


def _block(work_item_bill: WorkItemBill) -> str:
    return (
        f"{work_item_bill.table}\n\nCost: {work_item_bill.line}\n"
        f"Cache: {work_item_bill.cache}\n\n{work_item_bill.cache_by_role}\n"
    )


def _is_work_item_id(argument: str) -> bool:
    return re.fullmatch(f"{STORY_ID}|{ACCEPTANCE_ID}", argument) is not None


def _one(service: BillService, argument: str, out: TextIO) -> int:
    if not _is_work_item_id(argument):
        out.write(f"not a work item id: {argument}\n")
        return _FAILURE
    work_item_bill = service.for_work_item(argument)
    if work_item_bill is None:
        out.write(f"no work item {argument}\n")
        return _NO_BILL
    out.write(_block(work_item_bill))
    return _OK


def _all_in_flight(service: BillService, out: TextIO) -> int:
    blocks: list[str] = []
    for work_item in service.in_flight():
        work_item_bill = service.for_work_item(work_item)
        if work_item_bill is not None:
            blocks.append(f"{work_item}\n{_block(work_item_bill)}")
    out.write("\n".join(blocks))
    return _OK


def run(argv: Sequence[str], service: BillService, out: TextIO) -> int:
    """Write the bill of the one id in `argv`, or of every work item in flight, and return."""
    if len(argv) > 1:
        out.write(f"{_USAGE}\n")
        return _FAILURE
    if argv and argv[0] in _HELP_FLAGS:
        out.write(_HELP)
        return _OK
    if argv:
        return _one(service, argv[0], out)
    return _all_in_flight(service, out)


def main(argv: Sequence[str] | None = None) -> int:
    """Bill from the checkout in the current directory, the arguments `argv` or the command's."""
    arguments = sys.argv[1:] if argv is None else argv
    return run(arguments, build_bill_service(Path.cwd()), sys.stdout)


if __name__ == "__main__":
    raise SystemExit(main())
