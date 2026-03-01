#!/bin/bash
# Launch Yamagi Quake II with Lithium II mod
# Usage: ./run.sh              - launch with Lithium mod
#        ./run.sh base         - launch vanilla baseq2
#        ./run.sh build        - build mod then launch
#        ./run.sh server       - dedicated server only
#        ./run.sh server q2dm3 - dedicated server on specific map

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE="$SCRIPT_DIR/engine/release/quake2"
SERVER="$SCRIPT_DIR/engine/release/q2ded"
MOD_NAME="lithium"

# Build first if requested
if [ "$1" = "build" ]; then
    echo "Building mod..."
    cd "$SCRIPT_DIR/mod" && make && make install || exit 1
    shift
fi

# Dedicated server mode
if [ "$1" = "server" ]; then
    MAP="${2:-q2dm1}"
    echo "Starting Lithium II dedicated server on $MAP..."
    exec "$SERVER" \
        +set basedir "$HOME/.yq2" \
        +set game "$MOD_NAME" \
        +set dedicated 1 \
        +set deathmatch 1 \
        +set hostname "Lithium II WSL" \
        +map "$MAP"
fi

if [ "$1" = "base" ]; then
    echo "Launching vanilla Quake II..."
    exec "$ENGINE" +set basedir "$HOME/.yq2"
else
    echo "Launching Quake II with Lithium II mod..."
    exec "$ENGINE" +set basedir "$HOME/.yq2" +set game "$MOD_NAME"
fi
