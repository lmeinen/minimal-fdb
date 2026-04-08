#!/bin/sh

set -eu
role="${1:-store_1}"

exec env \
    FDB5_CONFIG_FILE="/etc/fdb/config.yaml" \
    FDB5_SUB_TOCS=1 \
    FDB_DEBUG=1 \
    AUTO_LOAD_PLUGINS=1 \
    ECCODES_ECKIT_GEO=1 \
    fdb-server "${role}"
