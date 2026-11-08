"""A pipeline definition of two routes to two approval stages, and one stage's decision in it."""

from typing import Final

from factory.shared.domain.identifiers import WorkItemId
from factory.work.domain.work_item import WorkItemState
from support.proof_support import PASSING_TEST, SOURCE, World, completed, head_state

EVERY_TARGET_MAKEFILE: Final[str] = "".join(
    f"{target}:\n\t@:\n"
    for target in ("sync", "check", "lint", "test", "duplicates", "documents", "secrets")
)
STAGE_WRITES: Final[dict[str, dict[str, str]]] = {
    "tests": {"tests/test_example.py": PASSING_TEST},
    "doing": {"src/example.py": SOURCE},
}

TWO_ROUTES: Final[str] = """\
contract: "1.0"
attempts_cap: 2
crash_cap: 2
acceptance_stage: acceptance
project_commands:
  check: {time_limit: 8}
  lint: {time_limit: 5}
  test: {time_limit: 10}
  duplicates: {time_limit: 2}
  documents: {time_limit: 2}
  secrets: {time_limit: 3}
  sync: {time_limit: 5}
roles:
  intake: {write_paths: ["{work_item}"], time_limit: 40, lease_duration: 60}
  tester: {write_paths: ["tests/*"], time_limit: 40, lease_duration: 60}
  coder: {write_paths: ["src/*"], time_limit: 40, lease_duration: 60}
  reviewer: {write_paths: ["{work_item}"], time_limit: 40, lease_duration: 60}
  documenter: {write_paths: ["README.md", "docs/*"], time_limit: 40, lease_duration: 60}
  smoke-tester: {write_paths: ["{work_item}"], time_limit: 40, lease_duration: 60}
  acceptance-reviewer:
    write_paths: ["{work_item}", "{feature}/backlog/*"]
    time_limit: 40
    lease_duration: 60
stages:
  intake: {role: intake, next: [tests, docs-only]}
  tests: {role: tester, next: [doing], checks: [lint]}
  doing: {role: coder, next: [review, tests], checks: [check], reports: [duplicates]}
  review: {role: reviewer, next: [docs, doing], round_cap: 2}
  docs:
    role: documenter
    next: [smoke-test, doing]
    checks: [check, secrets, documents]
    round_cap: 2
  smoke-test: {role: smoke-tester, next: [approval, doing, docs], round_cap: 2}
  docs-only: {role: documenter, next: [docs-review, tests], checks: [check, secrets, documents]}
  docs-review: {role: reviewer, next: [docs-approval, docs-only], round_cap: 2}
  docs-approval: {approval: true, next: [done, docs-only]}
  acceptance: {role: acceptance-reviewer, next: [approval]}
  approval: {approval: true, next: [done, doing]}
  done: {}
"""


def decide(world: World, work_item: WorkItemId, decision: str, stage: str) -> WorkItemState:
    """One tick in which the agent of `stage` ends with `decision`; the state after it."""
    run = completed(decision, f"{stage}: {decision}.", writes=STAGE_WRITES.get(stage))
    world.agent_runtime.queue(run)
    world.tick.run()
    return head_state(world, work_item)
