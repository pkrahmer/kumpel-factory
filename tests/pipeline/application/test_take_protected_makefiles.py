"""The take leaves out the makefile the definition names and the kit's makefile."""

from pathlib import Path

from factory.pipeline.application.boundaries import Boundaries
from factory.pipeline.application.claims import StageStart
from support.human_clone import HumanClone
from support.take_support import AGENT_TEXT, changes, make_dataset, run_take, write_dataset
from support.undo_support import BRANCH, PIPELINE_FILE, pipeline_text, start_stage
from support.work_item_support import checkout_text

WRITE_PATHS = ["factory/*", "src/*"]
MAKE_FILE = "factory/Makefile"
KIT_MAKE_FILE = "factory/kit.mk"
SOURCE = "src/a.py"


def _start_naming_the_makefile(boundaries: Boundaries, human: HumanClone) -> StageStart:
    start = start_stage(boundaries, human, write_paths=WRITE_PATHS)
    definition = f"make_file: {MAKE_FILE}\n{pipeline_text(WRITE_PATHS)}"
    (boundaries.checkout / PIPELINE_FILE).write_text(definition, encoding="utf-8")
    commit = boundaries.git.commit("name the makefile")
    assert boundaries.git.push(BRANCH) == "pushed"
    return StageStart(commit=commit, claim=start.claim)


def test_the_take_leaves_the_named_makefile_and_the_kit_makefile(
    boundaries: Boundaries, human: HumanClone, tmp_path: Path
) -> None:
    start = _start_naming_the_makefile(boundaries, human)
    mount_point = make_dataset(boundaries, tmp_path)
    written = [MAKE_FILE, KIT_MAKE_FILE, SOURCE]
    write_dataset(mount_point, {f"checkout/{path}": AGENT_TEXT for path in written})

    changed = changes(*((f"checkout/{path}", "added") for path in written))

    report = run_take(boundaries, start, mount_point, changed)

    assert checkout_text(boundaries, SOURCE) == AGENT_TEXT
    assert checkout_text(boundaries, MAKE_FILE) is None
    assert checkout_text(boundaries, KIT_MAKE_FILE) is None
    assert report.left == [MAKE_FILE, KIT_MAKE_FILE]
