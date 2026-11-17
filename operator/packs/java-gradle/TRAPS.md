# The Java pack's traps

What cost time when the first Java project ran in the factory (Java 21, Spring Boot, Gradle; November 2026), and what the pack does about each.

- **Java ignores `HOME`.** It takes the home folder from the user's entry in `/etc/passwd`, which in a container can name the working directory. Gradle's cache then follows the working directory, and a check that starts elsewhere than the sync finds no cache and fails offline. The makefile exports `GRADLE_USER_HOME` and passes `-Duser.home` to every JVM.
- **Java ignores `SSL_CERT_FILE`.** A site's CA bundle (`FACTORY_CA_BUNDLE`) reaches curl and git, not the JVM. `make sync` builds a trust store from the bundle with `scripts/trust-store.sh`, and every target points Gradle's JVMs at it.
- **Every target but `sync` is offline.** The build file must register the task `resolveAll`, which resolves every resolvable configuration; otherwise the first offline build misses a dependency. A new dependency shows as a red check until the next sync, which is the wanted signal.
- **A private Maven repository** takes its address and login from environment variables that the build file reads. The site names them in `FACTORY_CONTAINER_ENV` and sets them in the instance's `factory.local.env`; nothing of them is in the repository.
- **A stage has no container runtime.** An image build and Testcontainers stay in the CI pipeline. What the tests need runs as a plain process: add its jar to `factory/stage.Containerfile` with a checksum, and let `make test` start and stop it.
- **A configuration import that needs a login** (a secret manager's, for example) fails a context test even when it is marked optional. Keep it out of the profile the tests and the local run use.
- **Memory.** A container has 4 GB. The makefile gives Gradle's daemon 768 MB and lets it exit on an out-of-memory error instead of hanging until the time limit.
- **The wrapper's jar** is binary and committed: `.gitleaks.toml` lists it among the paths gitleaks leaves out, with `build/` and `.gradle/`.
