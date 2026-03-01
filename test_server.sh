#!/bin/bash
# Test script: start dedicated server, feed commands, check output
FIFO=/tmp/q2_test_fifo
rm -f $FIFO
mkfifo $FIFO

# Start server reading from fifo, output to file
/home/budda/Code/q2fun/engine/release/q2ded \
    +set basedir /home/budda/.yq2 \
    +set game lithium \
    +set dedicated 1 \
    +set deathmatch 1 \
    +map q2dm1 \
    < $FIFO > /tmp/q2_test_output.txt 2>&1 &
SERVER_PID=$!

# Open fifo for writing (keep it open)
exec 3> $FIFO

# Wait for server to start
sleep 3

# Send test commands
echo "status" >&3
sleep 1
echo "use_hook" >&3
sleep 1
echo "use_runes" >&3
sleep 1
echo "use_hook" >&3
sleep 1
echo "fraglimit" >&3
sleep 1
echo "ctf" >&3
sleep 1
echo "lithium_version" >&3
sleep 1
echo "quit" >&3
sleep 2

# Close fifo
exec 3>&-

# Kill server if still running
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

rm -f $FIFO

# Show results
cat /tmp/q2_test_output.txt
