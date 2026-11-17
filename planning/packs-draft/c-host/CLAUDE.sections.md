## Tests
- The tests build and run on the host, registered with CTest; no test needs a device, a network or a container runtime.
- The logic is tested through its ports: a test gives it a hand-written fake of the port it calls and a clock it can set. No test sleeps.
- The host build runs under the sanitizers `SANITIZERS` names; a sanitizer report is a failed test.

## Checks
- `make check` must be green before any stage reports done. It runs `make lint` (clang-format over the C sources the project writes), `make secrets` (gitleaks over the working tree) and `make test` (the host build, then CTest). Each target ends with the line `<target>: green (<seconds> s)`; `make check` ends with `check: green`.
- The factory's targets are in `factory/Makefile`. <Either: the root `Makefile` forwards every target to it, so `make check` works at the root. Or: the root `Makefile` is this repository's own, and every target the agents' instructions name is run as `make -f factory/Makefile <target>`, `make check` as `make -f factory/Makefile check`.>
- `make sync` configures the host build and fetches what `CMakeLists.txt` pins.
- Run `make check` and every other make target in the foreground and read its output.

## Review
- The logic names no platform header: what touches hardware, an operating system or a vendor's library sits behind a port in an adapter.
- No dynamic allocation after start-up, no unbounded loop, no blocking call in the logic; every buffer has its size checked where it is filled.
- Every fixed-width quantity has its unit and range in its name or its comment.

## Not without asking (end the stage with `question`)
- A new dependency or fetched source, a change to `CMakeLists.txt`, the makefile, the toolchain files or `factory/`, a change to a test another story wrote, a marker that silences a check.
