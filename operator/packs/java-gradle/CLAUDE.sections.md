## Tests
- JUnit 5 with AssertJ. Unit tests are in `src/test/java`, mirroring the main packages; a class under test is created with `new` and a hand-written fake of the port it calls. Mockito is for types that cannot be faked by hand.
- No test reaches the network, and none needs a container runtime: a stage has none. What a test needs from outside runs as a plain process that `make test` starts and stops.

## Checks
- `make check` must be green before any stage reports done. It runs `make lint` (the compiler with `-Xlint:all -Werror`), `make secrets` (gitleaks over the working tree), `make test` and `make package`. Each target ends with the line `<target>: green (<seconds> s)`; `make check` ends with `check: green`.
- The factory's targets are in `factory/Makefile`. <Either: the root `Makefile` forwards every target to it, so `make check` works at the root. Or: the root `Makefile` is this repository's own, and every target the agents' instructions name is run as `make -f factory/Makefile <target>`, `make check` as `make -f factory/Makefile check`.>
- `make sync` fetches the Gradle distribution and every dependency; every other target runs Gradle offline. A dependency that is new since the last sync fails until `make sync` ran again.
- Run `make check` and every other make target in the foreground and read its output.

## Review
- No field injection; constructor injection only. Records for values.
- No secret and no host of a real environment in any file; configuration reaches a deployed service from outside.
- A new dependency, plugin or version in the build files is a finding unless the story names it.
- Javadoc: one sentence per public type, and per public method where its signature does not say it all.

## Not without asking (end the stage with `question`)
- A new dependency or plugin, a new version, a change to `build.gradle`, `settings.gradle`, `gradle/`, the makefile or `factory/`, a new top-level package, a change to a test another story wrote, a new entry in `factory/gitleaks.toml`.
