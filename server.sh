#!/bin/bash
# Launch Lithium II dedicated server in WSL
# Connect from Windows Q2 client with: connect 127.0.0.1
#
# Usage: ./server.sh              - start server on q2dm1
#        ./server.sh q2dm3        - start on a specific map
#        ./server.sh build        - rebuild mod then start

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER="$SCRIPT_DIR/engine/release/q2ded"
MOD_NAME="lithium"
MAP="${1:-q2dm1}"

# Build first if requested
if [ "$1" = "build" ]; then
    echo "Building mod..."
    cd "$SCRIPT_DIR/mod" && make && make install || exit 1
    MAP="${2:-q2dm1}"
fi

echo "Starting Lithium II dedicated server..."
echo "  Map: $MAP"
echo "  Connect from Windows Q2: connect 127.0.0.1"
echo ""

exec "$SERVER" \
    +set basedir "$HOME/.yq2" \
    +set game "$MOD_NAME" \
    +set dedicated 1 \
    +set deathmatch 1 \
    +set hostname "Lithium II WSL" \
    +map "$MAP"
