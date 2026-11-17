# The tools this project's make check needs beyond the factory's stage image: a C compiler, CMake
# and clang-format for the host build and its tests, and gitleaks for the secret scan. Only the
# working branch counts; the build sees no files of the repository.
ARG FACTORY_BASE
FROM ${FACTORY_BASE}
ARG GITLEAKS_VERSION=8.30.1
ARG GITLEAKS_SHA256=551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential cmake clang-format \
 && rm -rf /var/lib/apt/lists/* \
 && curl -fsSL -o /tmp/gitleaks.tgz \
      "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" \
 && echo "${GITLEAKS_SHA256}  /tmp/gitleaks.tgz" | sha256sum -c - \
 && tar -xzf /tmp/gitleaks.tgz -C /usr/local/bin gitleaks \
 && rm /tmp/gitleaks.tgz
