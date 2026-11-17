# The C pack's makefile (kumpel-factory): the factory's four targets `check`, `lint`, `test` and
# `sync` for C code that builds and tests on the host with CMake and CTest, firmware logic
# included, as long as its tests need no device. They need a C compiler, CMake, clang-format and
# gitleaks; factory/stage.Containerfile installs them. A cross build, a flash or a monitor is the
# project's own target below and never part of `check`.

# The kit's part: one shell per recipe, `$(start)` and `$(green)`, and the start facts.
include factory/kit.mk

.PHONY: check sync lint secrets test

# What the project decides: the folder of the host build's CMakeLists.txt, the build folder, the
# sanitizers of the host build, and the C sources the format check covers (what the project
# writes, nothing fetched).
HOST ?= .
BUILD ?= build/host
SANITIZERS ?= undefined
C_SOURCES ?= $(shell git ls-files --cached --others --exclude-standard -- '*.c' '*.h')
CONFIGURE = cmake -S $(HOST) -B $(BUILD) -DCMAKE_BUILD_TYPE=Debug -DSANITIZERS=$(SANITIZERS) > /dev/null

check: lint secrets test
	echo "check: green"

# The tools after a checkout: the host build's configuration, which also fetches what the
# CMakeLists.txt pins (a test framework by its hash, for example).
sync:
	$(start)
	$(CONFIGURE)
	$(green)

lint:
	$(start)
	if [ -n "$(strip $(C_SOURCES))" ]; then clang-format --dry-run --Werror $(C_SOURCES); fi
	$(green)

# Secrets in the working tree, by gitleaks with its own rules; a project with exceptions adds
# `--config .gitleaks.toml`.
secrets:
	$(start)
	gitleaks dir . --no-banner --redact --log-level error
	$(green)

# The host build, then its tests under the sanitizers.
test:
	$(start)
	$(CONFIGURE)
	cmake --build $(BUILD) -j > /dev/null
	ASAN_OPTIONS=detect_leaks=0 ctest --test-dir $(BUILD) --output-on-failure -j
	$(green)
