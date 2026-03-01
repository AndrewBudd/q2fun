#!/usr/bin/env python3
"""Quake 2 protocol test client - verifies server is working."""

import socket
import struct
import time
import sys
import random

SERVER = ("127.0.0.1", 27910)
TIMEOUT = 3.0
Q2_PROTOCOL = 34  # Q2 protocol version

def make_oob(data):
    """Create an out-of-band (connectionless) packet."""
    return b'\xff\xff\xff\xff' + data.encode()

def send_recv(sock, data, label=""):
    """Send packet and receive response."""
    sock.sendto(data, SERVER)
    try:
        resp, addr = sock.recvfrom(4096)
        return resp
    except socket.timeout:
        print(f"  TIMEOUT waiting for {label}")
        return None

def parse_oob_response(resp):
    """Strip the 0xffffffff header and return the payload string."""
    if resp and resp[:4] == b'\xff\xff\xff\xff':
        return resp[4:].decode('latin-1', errors='replace')
    return None

def test_status_query(sock):
    """Test 1: Server status query (like a server browser)."""
    print("\n[TEST 1] Server Status Query")
    print("-" * 40)
    resp = send_recv(sock, make_oob("status\n"), "status")
    payload = parse_oob_response(resp)
    if payload:
        lines = payload.split('\n')
        print(f"  Response type: {lines[0]}")
        if len(lines) > 1:
            # Parse server info string
            info = lines[1]
            pairs = info.split('\\')
            print("  Server info:")
            for i in range(1, len(pairs)-1, 2):
                print(f"    {pairs[i]} = {pairs[i+1]}")
        print("  PASS: Server responds to status queries")
        return True
    else:
        print("  FAIL: No response to status query")
        return False

def test_info_query(sock):
    """Test 2: Server info query."""
    print("\n[TEST 2] Server Info Query")
    print("-" * 40)
    resp = send_recv(sock, make_oob("info 34\n"), "info")
    payload = parse_oob_response(resp)
    if payload:
        print(f"  Response: {payload.strip()[:200]}")
        print("  PASS: Server responds to info queries")
        return True
    else:
        print("  FAIL: No response to info query")
        return False

def test_connect(sock, name="TestBot"):
    """Test 3: Full client connection handshake."""
    print(f"\n[TEST 3] Client Connection ({name})")
    print("-" * 40)

    # Step 1: Get challenge
    resp = send_recv(sock, make_oob("getchallenge\n"), "getchallenge")
    payload = parse_oob_response(resp)
    if not payload:
        print("  FAIL: No challenge response")
        return False, None

    print(f"  Challenge response: {payload.strip()[:80]}")

    # Parse challenge number
    parts = payload.strip().split()
    if len(parts) < 2 or parts[0] != "challenge":
        print(f"  FAIL: Unexpected challenge format")
        return False, None

    challenge = parts[1]
    print(f"  Got challenge: {challenge}")

    # Step 2: Send connect
    qport = random.randint(1000, 60000)
    userinfo = f"\\name\\{name}\\skin\\male/grunt\\rate\\25000\\msg\\1\\hand\\2"
    connect_str = f"connect {Q2_PROTOCOL} {qport} {challenge} \"{userinfo}\"\n"

    resp = send_recv(sock, make_oob(connect_str), "connect")
    payload = parse_oob_response(resp)
    if not payload:
        print("  FAIL: No connect response")
        return False, None

    print(f"  Connect response: {payload.strip()[:80]}")

    if "client_connect" in payload.lower():
        print(f"  PASS: {name} connected successfully!")
        return True, qport
    elif "print" in payload:
        # Server might send a print message (e.g., server full, banned)
        print(f"  Server message: {payload}")
        return False, None
    else:
        print(f"  Response: {payload.strip()}")
        return True, qport

def test_multiple_bots(num_bots=3):
    """Test 4: Connect multiple bots."""
    print(f"\n[TEST 4] Multiple Bot Connections ({num_bots} bots)")
    print("-" * 40)

    sockets = []
    connected = 0

    for i in range(num_bots):
        name = f"LithBot{i+1}"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(TIMEOUT)

        success, qport = test_connect(sock, name)
        if success:
            connected += 1
            sockets.append(sock)
        else:
            sock.close()

        time.sleep(0.5)

    print(f"\n  Connected {connected}/{num_bots} bots")

    # Wait a moment then query status to see them listed
    time.sleep(1)

    print("\n[TEST 5] Verify Bots Appear in Status")
    print("-" * 40)
    check_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    check_sock.settimeout(TIMEOUT)
    resp = send_recv(check_sock, make_oob("status\n"), "status")
    payload = parse_oob_response(resp)
    if payload:
        lines = payload.strip().split('\n')
        player_count = len(lines) - 2  # header + info line
        print(f"  Players listed in status: {max(0, player_count)}")
        for line in lines[2:]:
            print(f"    {line}")
    check_sock.close()

    # Clean up - disconnect bots
    for sock in sockets:
        try:
            sock.sendto(make_oob("disconnect\n"), SERVER)
        except:
            pass
        sock.close()

    return connected > 0

def main():
    print("=" * 50)
    print("Quake 2 Lithium II Server Test")
    print("=" * 50)
    print(f"Target: {SERVER[0]}:{SERVER[1]}")

    results = []

    # Test 1: Status query
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    results.append(("Status Query", test_status_query(sock)))
    sock.close()

    # Test 2: Info query
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    results.append(("Info Query", test_info_query(sock)))
    sock.close()

    # Test 3: Single bot connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    success, _ = test_connect(sock, "TestBot")
    results.append(("Single Connect", success))
    if success:
        sock.sendto(make_oob("disconnect\n"), SERVER)
    sock.close()
    time.sleep(1)

    # Test 4-5: Multiple bots
    results.append(("Multiple Bots", test_multiple_bots(3)))

    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    all_pass = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("All tests passed! Lithium II server is working.")
    else:
        print("Some tests failed.")

    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
