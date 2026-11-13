"""
Project VALKYRJA — Core Module 1: Active Deception & Steganographic Watermarking
Architecture: Hexagonal Core (Domain-Agnostic Defense Engine)
Compliance Target: EU NIS2 Directive / Sweden Cybersäkerhetslagen (SFS 2025:1506)

Implements:
1. Endothelial Honeypot: Asynchronous TCP/HTTP decoy listener.
2. Vasoconstriction Tarpit: Throttles malicious scanners/ransomware (2 bytes / 30s).
3. "Barium Meal" Chaff Stream: Zero-disk-footprint generator (RAM yield) that feeds
   synthetic honey-data injected with a time-rotating HMAC-SHA256 steganographic token
   encoding [Branch_ID + Terminal_ID + Employee_Session].
"""

import asyncio
import hashlib
import hmac
import json
import time
from datetime import datetime, timezone
from typing import AsyncGenerator, Dict, Optional

# =====================================================================
# CRYPTOGRAPHIC CONFIGURATION & NODE TELEMETRY (HLA CONTEXT)
# =====================================================================
# In production, this 32-byte seed lives strictly in volatile RAM and is
# governed by the 3-of-5 Shamir Board License protocol.
MASTER_SECRET_SEED: bytes = b"VALKYRJA_32BYTE_MASTER_SEED_2026"

ACTIVE_BRANCH_ID: str = "SE_STHLM_CLINIC_01"
ACTIVE_TERMINAL_ID: str = "ER_TRIAGE_TERM_04"
ACTIVE_STAFF_SESSION: str = "STAFF_HLA_884"


def generate_rolling_barium_token(
    branch_id: str = ACTIVE_BRANCH_ID,
    terminal_id: str = ACTIVE_TERMINAL_ID,
    staff_id: str = ACTIVE_STAFF_SESSION,
    time_window: Optional[int] = None,
) -> str:
    """
    Generates a time-rotating cryptographic watermark (changes every hour).
    To external attackers or dark-web buyers, it looks like an opaque serial hash.
    To authorized governance tools holding the Master Seed, it identifies the exact
    compromised branch, physical terminal, and active staff session.
    """
    if time_window is None:
        time_window = int(time.time() // 3600)  # 1-hour rotation window

    payload = f"{branch_id}:{terminal_id}:{staff_id}:{time_window}".encode("utf-8")
    signature = hmac.new(MASTER_SECRET_SEED, payload, hashlib.sha256).hexdigest()[:16]
    return f"TRC-{time_window}-{signature.upper()}"


def verify_barium_watermark(
    leaked_token: str,
    known_branches: list[str],
    known_terminals: list[str],
    known_staff_ids: list[str],
) -> Optional[Dict[str, str]]:
    """
    High-Privilege Forensic Decoder (Board / Zero-Knowledge Admin Tool).
    Reconstructs the exact leak coordinates from a captured honey-data watermark.
    """
    try:
        parts = leaked_token.split("-")
        if len(parts) != 3 or parts[0] != "TRC":
            return None
        time_window = int(parts[1])
    except ValueError:
        return None

    for branch in known_branches:
        for terminal in known_terminals:
            for staff in known_staff_ids:
                candidate = generate_rolling_barium_token(
                    branch, terminal, staff, time_window
                )
                if hmac.compare_digest(candidate, leaked_token):
                    leak_Timestamp = datetime.fromtimestamp(
                        time_window * 3600, tz=timezone.utc
                    ).isoformat()
                    return {
                        "compromised_branch": branch,
                        "compromised_terminal": terminal,
                        "implicated_staff_session": staff,
                        "time_window_utc": leak_Timestamp,
                        "forensic_confidence": "100% (HMAC-SHA256 Verified)",
                    }
    return None


# =====================================================================
# IN-MEMORY SYNTHETIC HONEY-DATA GENERATOR (CHAFF STREAM)
# =====================================================================
async def generate_barium_honey_data_stream(
    attacker_ip: str,
) -> AsyncGenerator[bytes, None]:
    """
    Streams realistic synthetic clinical/VIP records directly from RAM using 'yield'.
    Consumes <1 MB of server memory while saturating the attacker's storage with
    traceable honey-data and active canary traps.
    """
    rolling_token = generate_rolling_barium_token()
    print(
        f"[BARIUM-TRACE] Injecting rolling steganographic watermark: {rolling_token} "
        f"for intruder {attacker_ip}"
    )

    record_id = 10000
    while True:
        synthetic_record = {
            "record_id": f"SYN-REC-{record_id}",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "classification": "RESTRICTED_CLINICAL_OR_VAULT_ASSET",
            "blood_reserve_or_asset_status": "O_NEG_VERIFIED_SYNTHETIC",
            "canary_verification_endpoint": f"https://audit-telemetry.example.se/verify/{rolling_token}",
            "integrity_seal": rolling_token,  # <- Rolling Steganographic Watermark
        }
        yield (json.dumps(synthetic_record) + "\n").encode("utf-8")
        record_id += 1
        await asyncio.sleep(0.05)  # High-throughput stream to saturate exfiltration


# =====================================================================
# DUAL-RESPONSE ENGINE: VASOCONSTRICTION TARPIT VS. BARIUM CHAFF
# =====================================================================
async def handle_endothelial_breach(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    """
    Evaluates incoming connections on decoy ports with 0% false-positive tolerance.
    - Exfiltration attempt ('GET', 'DUMP', 'SELECT') -> Diverts to Barium Honey-Data.
    - Reconnaissance / Ransomware scan -> Traps in Asynchronous Tarpit (2 bytes / 30s).
    """
    peer_info = writer.get_extra_info("peername")
    attacker_ip = peer_info[0] if peer_info else "UNKNOWN_IP"
    timestamp = datetime.now(timezone.utc).isoformat()

    print(
        f"\n[ENDOTHELIAL-ALERT] {timestamp} | Decoy port touched by: {peer_info}"
    )

    try:
        request_bytes = await asyncio.wait_for(reader.read(1024), timeout=5.0)
        request_str = request_bytes.decode("utf-8", errors="ignore").strip()
        print(f"[TELEMETRY] Captured payload from {attacker_ip}: '{request_str}'")

        exfiltration_keywords = ("GET", "DOWNLOAD", "DUMP", "SELECT", "EXPORT")

        if any(keyword in request_str.upper() for keyword in exfiltration_keywords):
            # MODE B: Data Exfiltration Detected -> Activate Barium Honey-Data Stream
            print(
                f"[DECEPTION-MODE: BARIUM] Diverting {attacker_ip} to synthetic "
                f"honey-data stream (NIS2 Early Warning logged)."
            )
            writer.write(
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: application/x-ndjson\r\n"
                b"X-Node-Status: PRODUCTION_REPLICA\r\n\r\n"
            )
            await writer.drain()

            async for chunk in generate_barium_honey_data_stream(attacker_ip):
                writer.write(chunk)
                await writer.drain()
        else:
            # MODE A: Automated Scan / Ransomware -> Activate Vasoconstriction Tarpit
            print(
                f"[DECEPTION-MODE: TARPIT] Applying digital vasoconstriction to "
                f"{attacker_ip} (throttling socket to 2 bytes / 30s)..."
            )
            writer.write(b"HTTP/1.1 100 Continue\r\n")
            await writer.drain()

            while True:
                await asyncio.sleep(30)
                writer.write(b"..\r\n")
                await writer.drain()

    except asyncio.TimeoutError:
        print(
            f"[TARPIT-HOLD] {attacker_ip} sent no initial payload; holding socket in slow tarpit..."
        )
        try:
            for _ in range(10):
                await asyncio.sleep(30)
                writer.write(b"\x00\x00")
                await writer.drain()
        except Exception:
            pass
    except (ConnectionResetError, BrokenPipeError):
        print(f"[CONTAINMENT] Intruder {attacker_ip} disconnected from trap.")
    except Exception as exc:
        print(f"[INFO] Session closed ({attacker_ip}): {exc}")
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        print(f"[STATE-GREEN] Decoy session for {attacker_ip} safely terminated.")


# =====================================================================
# ENTRY POINT: ENDOTHELIAL HONEYPOT SERVER
# =====================================================================
async def main() -> None:
    host = "127.0.0.1"
    port = 8443

    # Quick self-test of the Steganographic Barium Watermark & Forensic Decoder
    sample_token = generate_rolling_barium_token()
    decoded_leak = verify_barium_watermark(
        sample_token,
        known_branches=[ACTIVE_BRANCH_ID],
        known_terminals=[ACTIVE_TERMINAL_ID],
        known_staff_ids=[ACTIVE_STAFF_SESSION],
    )

    server = await asyncio.start_server(handle_endothelial_breach, host, port)
    addr = server.sockets[0].getsockname()

    print("=" * 68)
    print("  PROJECT VALKYRJA — MODULE 1: DECEPTION & BARIUM ENGINE ACTIVE")
    print(f"  Listening on Decoy Endpoint : {addr[0]}:{addr[1]}")
    print(f"  Active Rolling Watermark    : {sample_token}")
    print(f"  Forensic Decoder Self-Test  : {decoded_leak}")
    print("=" * 68)
    print("Local Verification Instructions:")
    print(f"  1. Open a second terminal and run: nc {host} {port}")
    print("  2. Type 'DUMP DATA' + Enter to trigger the Barium Honey-Data stream.")
    print("  3. Or type 'SCAN' + Enter to trigger the 30s Vasoconstriction Tarpit.\n")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Project VALKYRJA Deception Engine stopped cleanly.")
