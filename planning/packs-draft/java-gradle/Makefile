# The Java pack's makefile (kumpel-factory): the factory's four targets `check`, `lint`, `test` and
# `sync` for a Java project built with the Gradle wrapper. They need a JDK and gitleaks;
# factory/stage.Containerfile installs both. What a project adds for itself (a `run`, an `image`)
# comes below and is never part of `check`: a stage has no container runtime.

# The kit's part: one shell per recipe, `$(start)` and `$(green)`, and the start facts.
include factory/kit.mk

.PHONY: check sync lint secrets test package

# What the project decides: the Gradle tasks behind each target. `resolveAll` is a task the
# project's build file registers; it resolves every configuration, so that the checks run offline.
SYNC_TASKS ?= resolveAll
LINT_TASKS ?= compileJava compileTestJava
TEST_TASKS ?= test
PACKAGE_TASKS ?= assemble

# Java takes its home folder from the user's entry in /etc/passwd, not from HOME, and in a container
# that entry can name the working directory. Gradle's cache would then land in the checkout, and
# each working directory would have its own. So HOME is named to Gradle and to every JVM it starts.
export GRADLE_USER_HOME := $(HOME)/.gradle

# Behind a proxy that re-signs TLS, SSL_CERT_FILE names the site's CA bundle (PEM). Java does not
# read that variable, so `sync` copies the JDK's trust store, adds the bundle's certificates (once
# per bundle) and every target points Gradle's JVMs at the copy. Without SSL_CERT_FILE nothing changes.
TRUST_STORE = $(HOME)/.cache/java-trust-store.p12
jvm = jvm="-Duser.home=$(HOME)"; if [ -f "$(TRUST_STORE)" ]; then jvm="$$jvm -Djavax.net.ssl.trustStore=$(TRUST_STORE) -Djavax.net.ssl.trustStorePassword=changeit"; fi; export GRADLE_OPTS="$$jvm"

# Gradle without its progress output. Every target but `sync` runs offline: what a build needs is
# in Gradle's cache after `make sync`, so a check never depends on the network.
GRADLE = ./gradlew --quiet "-Dorg.gradle.jvmargs=-Xmx768m -XX:+ExitOnOutOfMemoryError $$jvm"
OFFLINE = $(GRADLE) --offline

check: lint secrets test package
	echo "check: green"

# The tools after a checkout: the Gradle distribution the wrapper names, and every dependency.
sync:
	$(start)
	if [ -n "$${SSL_CERT_FILE:-}" ] && [ -f "$${SSL_CERT_FILE}" ]; then
	  bundle=$$(sha256sum < "$${SSL_CERT_FILE}" | cut -d' ' -f1)
	  if [ ! -f "$(TRUST_STORE)" ] || [ "$$(cat "$(TRUST_STORE).sha256" 2>/dev/null)" != "$$bundle" ]; then
	    sh scripts/trust-store.sh "$${SSL_CERT_FILE}" "$(TRUST_STORE)"
	    echo "$$bundle" > "$(TRUST_STORE).sha256"
	  fi
	else
	  for stale in "$(TRUST_STORE)" "$(TRUST_STORE).sha256"; do if [ -f "$$stale" ]; then unlink "$$stale"; fi; done
	fi
	$(jvm)
	$(GRADLE) $(SYNC_TASKS)
	$(green)

# The compiler is the linter: the build file makes every warning of `-Xlint:all` an error.
lint:
	$(start)
	$(jvm)
	$(OFFLINE) $(LINT_TASKS)
	$(green)

# Secrets in the working tree, by gitleaks with the rules of .gitleaks.toml.
secrets:
	$(start)
	gitleaks dir . --config .gitleaks.toml --no-banner --redact --log-level error
	$(green)

test:
	$(start)
	$(jvm)
	$(OFFLINE) $(TEST_TASKS)
	$(green)

# What the project ships, built once so that a broken packaging shows in `check`.
package:
	$(start)
	$(jvm)
	$(OFFLINE) $(PACKAGE_TASKS)
	$(green)
