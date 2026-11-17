#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# usage: trust-store.sh <CA bundle (PEM)> <trust store to write>
# Writes a copy of the JDK's trust store with every certificate of the bundle added, so that
# Gradle and the tests trust a site's own certificate authority. `make sync` runs it.
set -eu
bundle=$1
store=$2
java_home=${JAVA_HOME:-$(dirname "$(dirname "$(readlink -f "$(command -v java)")")")}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

mkdir -p "$(dirname "$store")"
keytool -importkeystore -noprompt \
  -srckeystore "$java_home/lib/security/cacerts" -srcstorepass changeit \
  -destkeystore "$work/store.p12" -deststoretype PKCS12 -deststorepass changeit > /dev/null 2>&1

# One file per certificate of the bundle: keytool imports one certificate at a time.
awk -v dir="$work" '
  /-----BEGIN CERTIFICATE-----/ { n++; file = sprintf("%s/ca-%04d.pem", dir, n) }
  file { print > file }
  /-----END CERTIFICATE-----/ { close(file); file = "" }
' "$bundle"

for certificate in "$work"/ca-*.pem; do
  [ -f "$certificate" ] || continue
  alias=$(basename "$certificate" .pem)
  keytool -importcert -noprompt -trustcacerts -alias "site-$alias" \
    -file "$certificate" -keystore "$work/store.p12" -storepass changeit > /dev/null 2>&1
done
mv "$work/store.p12" "$store"
