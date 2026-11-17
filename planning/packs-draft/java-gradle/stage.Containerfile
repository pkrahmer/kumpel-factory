# The tools this project's make check needs beyond the factory's stage image: a JDK for Gradle and
# the tests, and gitleaks for the secret scan. Only the working branch counts; the build sees no
# files of the repository. A project adds what its own tests need below (an emulator as a plain
# jar, for example): a stage has no container runtime.
ARG FACTORY_BASE
FROM ${FACTORY_BASE}
# Eclipse Temurin, with the checksum of adoptium.net's release.
ARG JDK_URL=https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.13%2B9/OpenJDK21U-jdk_x64_linux_hotspot_21.0.13_9.tar.gz
ARG JDK_SHA256=d7f5d5cf865a2902b70ff549b97586a7d3f234e016f041ab447ea740c7d66d1c
ARG GITLEAKS_VERSION=8.30.1
ARG GITLEAKS_SHA256=551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb
RUN curl -fsSL -o /tmp/jdk.tgz "${JDK_URL}" \
 && echo "${JDK_SHA256}  /tmp/jdk.tgz" | sha256sum -c - \
 && mkdir -p /opt/java \
 && tar -xzf /tmp/jdk.tgz -C /opt/java --strip-components=1 \
 && rm -rf /tmp/jdk.tgz /opt/java/jmods /opt/java/lib/src.zip /opt/java/man \
 && curl -fsSL -o /tmp/gitleaks.tgz \
      "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" \
 && echo "${GITLEAKS_SHA256}  /tmp/gitleaks.tgz" | sha256sum -c - \
 && tar -xzf /tmp/gitleaks.tgz -C /usr/local/bin gitleaks \
 && rm /tmp/gitleaks.tgz
ENV JAVA_HOME=/opt/java \
    PATH=/opt/java/bin:${PATH}
