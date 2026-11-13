"""
Project VALKYRJA — Core Module 1: Active Deception, Barium Watermarking & Protocol UNICORSE
Architecture: Hexagonal Core (Domain-Agnostic Deception Engine)
Compliance Target: EU NIS2 Directive / Sweden Cybersäkerhetslagen (SFS 2025:1506)

Implements:
1. Endothelial Honeypot & Vasoconstriction Tarpit (2 bytes / 30s).
2. "Barium Meal" Chaff Stream with rolling HMAC-SHA256 steganographic watermarks.
3. PROTOCOL U.N.I.C.O.R.S.E. (Unending Nested Illusion & Cryptographic Obfuscation
   Reflective Sandbox Engine): Deterministic procedural Mirror Wall that traps attackers
   in an infinite, zero-disk-footprint directory and SQL labyrinth.
"""

import asyncio
import hashlib
import hmac
import json
import time
from datetime import datetime, timezone
from typing import AsyncGenerator, Dict, List, Optional

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
    """Generates a 1-hour rolling HMAC-SHA256 watermark encoding [Branch + Terminal + Staff]."""
    if time_window is None:
        time_window = int(time.time() // 3600)

    payload = f"{branch_id}:{terminal_id}:{staff_id}:{time_window}".encode("utf-8")
    signature = hmac.new(MASTER_SECRET_SEED, payload, hashlib.sha256).hexdigest()[:16]
    return f"TRC-{time_window}-{signature.upper()}"


def verify_barium_watermark(
    leaked_token: str,
    known_branches: List[str],
    known_terminals: List[str],
    known_staff_ids: List[str],
) -> Optional[Dict[str, str]]:
    """Forensic Decoder: Reconstructs leak coordinates from a captured Barium token."""
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
                candidate = generate_rolling_barium_token(branch, terminal, staff, time_window)
                if hmac.compare_digest(candidate, leaked_token):
                    leak_ts = datetime.fromtimestamp(time_window * 3600, tz=timezone.utc).isoformat()
                    return {
                        "compromised_branch": branch,
                        "compromised_terminal": terminal,
                        "implicated_staff_session": staff,
                        "time_window_utc": leak_ts,
                        "forensic_confidence": "100% (HMAC-SHA256 Verified)",
                    }
    return None


# =====================================================================
# PROTOCOL U.N.I.C.O.R.S.E. — INFINITE PROCEDURAL MIRROR WALL LABYRINTH
# =====================================================================
class ProtocolUnicorseMirrorMaze:
    """
    PROTOCOL U.N.I.C.O.R.S.E.:
    Unending Nested Illusion & Cryptographic Obfuscation Reflective Sandbox Engine.
    Generates an infinite, deterministic virtual filesystem and database schema in RAM.
    Regardless of how deep the attacker navigates (10 or 10,000 levels), new plausible
    clinical/vault subdirectories and Barium-watermarked decoy files are synthesized on the fly.
    """

    DECOY_DIR_PREFIXES = (
        "scandiatransplant_hla_archive",
        "karolinska_ecmo_telemetry",
        "lims_cystatin_c_batches",
        "cryo_ln2_stemcell_vault",
        "executive_board_shamir_keys",
        "nicu_incubator_firmware",
    )

    @classmethod
    def reflect_infinite_labyrinth_node(cls, attacker_path_or_cmd: str) -> Dict[str, object]:
        normalized_path = attacker_path_or_cmd.strip() or "/root"
        path_hash = hashlib.sha256(MASTER_SECRET_SEED + normalized_path.encode("utf-8")).hexdigest()
        barium_token = generate_rolling_barium_token()

        # Deterministically synthesize 4 child directories and 3 decoy files from the hash
        virtual_subdirs: List[str] = []
        for i in range(4):
             slice_hex = path_hash[i * 4 : (i + 1) * 4]
             prefix = cls.DECOY_DIR_PREFIXES[(int(slice_hex, 16)) % len(cls.DECOY_DIR_PREFIXES)]
             virtual_subdirs.append(f"{normalized_path.rstrip('/')}/{prefix}_{slice_hex}/")

        decoy_files = [
            {
                "filename": f"confidential_export_{path_hash[:6]}.sql.enc",
                "size_bytes": int(path_hash[6:12], 16),
                "embedded_barium_trace": barium_token,
            },
            {
                "filename": f"patient_hla_crossmatch_{path_hash[12:18]}.fhir.json",
                "size_bytes": int(path_hash[18:24], 16),
                "embedded_barium_trace": barium_token,
            },
        ]

        return {
            "active_defense_protocol": "PROTOCOL_UNICORSE_MIRROR_LABYRINTH",
            "reflected_virtual_path": normalized_path,
            "labyrinth_depth_limit": "INFINITE_PROCEDURAL_RAM",
            "synthesized_subdirectories": virtual_subdirs,
            "barium_seeded_decoy_files": decoy_files,
            "canary_token_injected": barium_token,
        }


async def generate_barium_honey_data_stream(attacker_ip: str) -> AsyncGenerator[bytes, None]:
    """Streams synthetic records from RAM injected with the rolling Barium watermark."""
    rolling_token = generate_rolling_barium_token()
    record_id = 10000
    while True:
        synthetic_record = {
            "record_id": f"SYN-REC-{record_id}",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "defense_layer": "PROTOCOL_UNICORSE_CHAFF_STREAM",
            "integrity_seal": rolling_token,
        }
        yield (json.dumps(synthetic_record) + "\n").encode("utf-8")
        record_id += 1
        await asyncio.sleep(0.05)


async def handle_endothelial_breach(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    peer_info = writer.get_extra_info("peername")
    attacker_ip = peer_info[0] if peer_info else "UNKNOWN_IP"

    try:
        request_bytes = await asyncio.wait_for(reader.read(1024), timeout=5.0)
        request_str = request_bytes.decode("utf-8", errors="ignore").strip()

        exfiltration_keywords = ("GET", "DOWNLOAD", "DUMP", "SELECT", "EXPORT")
        exploration_keywords = ("LS", "CD", "DIR", "TREE", "FIND", "CAT", "/")

        if any(k in request_str.upper() for k in exfiltration_keywords):
            writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/x-ndjson\r\n\r\n")
            await writer.drain()
            async for chunk in generate_barium_honey_data_stream(attacker_ip):
                writer.write(chunk)
                await writer.drain()
        elif any(k in request_str.upper() for k in exploration_keywords):
            # Activate PROTOCOL UNICORSE Infinite Mirror Maze
            maze_node = ProtocolUnicorseMirrorMaze.reflect_infinite_labyrinth_node(request_str)
            writer.write((json.dumps(maze_node, indent=2) + "\n").encode("utf-8"))
            await writer.drain()
        else:
            writer.write(b"HTTP/1.1 100 Continue\r\n")
            await writer.drain()
            while True:
                await asyncio.sleep(30)
                writer.write(b"..\r\n")
                await writer.drain()
    except Exception:
        pass
    finally:
        writer.close()
