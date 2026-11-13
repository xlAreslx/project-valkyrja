"""
Project VALKYRJA — Core Module 1: Active Deception, Barium Watermarking,
Protocol UNICORSE & Hardened Lymphatic DDoS Sinkhole Filter (Red-Team v1.2).
Architecture: Hexagonal Core (Domain-Agnostic Deception & Traffic Drainage Engine)
Compliance Target: EU NIS2 Directive / Sweden Cybersäkerhetslagen (SFS 2025:1506)
"""

import asyncio
import hashlib
import hmac
import json
import os
import time
from collections import OrderedDict
from datetime import datetime, timezone
from typing import AsyncGenerator, Dict, List, Optional

MASTER_SECRET_SEED: bytes = os.environ.get(
    "VALKYRJA_MASTER_SEED", "VALKYRJA_32BYTE_MASTER_SEED_2026"
).encode("utf-8")

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


# =====================================================================
# HARDENED LYMPHATIC DDoS SINKHOLE & SINGLE-USE JTI SELECTIN FILTER
# =====================================================================
class LymphaticDDoSSinkholeFilter:
    """
    Red-Team v1.2 Hardened DDoS, Anti-Replay & Slowloris Filter:
    1. Bounded FIFO Memory Cache (OrderedDict capped at MAX_TRACKED_IPS).
    2. 60s Time-Bound + Single-Use Nonce (JTI) Selectin Token: Blocks both expired (>60s)
       and intra-minute replayed hospital headers immediately.
    3. Distributed Slowloris Tarpit Cap (MAX_TARPIT_CONCURRENCY = 256): Prevents socket exhaustion.
    """

    MIN_HUMAN_OR_IOMT_DELTA_SECONDS: float = 0.010
    MAX_TRACKED_IPS: int = 10000
    MAX_TRACKED_NONCES: int = 10000
    SELECTIN_WINDOW_SECONDS: int = 60
    MAX_TARPIT_CONCURRENCY: int = 256

    def __init__(self, max_tracked_ips: int = 10000, max_tarpit_slots: int = 256) -> None:
        self.max_tracked_ips = max_tracked_ips
        self.max_tarpit_slots = max_tarpit_slots
        self.active_tarpit_connections: int = 0
        self._tarpit_semaphore = asyncio.Semaphore(max_tarpit_slots)
        self._last_request_timestamp: OrderedDict[str, float] = OrderedDict()
        self._consumed_selectin_nonces: OrderedDict[str, float] = OrderedDict()
        self.sinkholed_drops_count: int = 0
        self.replay_blocks_count: int = 0

    def try_acquire_tarpit_slot(self) -> bool:
        """
        Guards against Distributed Slowloris socket exhaustion.
        Allows at most `max_tarpit_slots` concurrent tarpit holds; drops excess into sinkhole.
        """
        if self.active_tarpit_connections >= self.max_tarpit_slots:
            self.sinkholed_drops_count += 1
            return False
        self.active_tarpit_connections += 1
        return True

    def release_tarpit_slot(self) -> None:
        if self.active_tarpit_connections > 0:
            self.active_tarpit_connections -= 1

    @classmethod
    def generate_valid_selectin_header(
        cls,
        branch_id: str = ACTIVE_BRANCH_ID,
        current_time: Optional[float] = None,
        nonce: Optional[str] = None,
    ) -> str:
        """
        Generates a 60-second time-bound + Single-Use Nonce (JTI) HMAC Selectin header:
        Format: SEL-{window}-{nonce}-{hmac}
        """
        ts = time.time() if current_time is None else current_time
        window = int(ts // cls.SELECTIN_WINDOW_SECONDS)
        unique_nonce = nonce if nonce is not None else os.urandom(6).hex()
        payload = f"SELECTIN_VIP:{branch_id}:{window}:{unique_nonce}".encode("utf-8")
        sig = hmac.new(MASTER_SECRET_SEED, payload, hashlib.sha256).hexdigest()[:16]
        return f"SEL-{window}-{unique_nonce}-{sig}"

    def _verify_selectin_anti_replay(
        self, header_token: str, branch_id: str, check_time: float
    ) -> str:
        """Returns 'VALID', 'EXPIRED_REPLAY', 'DUPLICATE_NONCE_REPLAY', or 'INVALID'."""
        parts = header_token.split("-")
        if len(parts) != 4 or parts[0] != "SEL":
            return "INVALID"
        try:
            token_window = int(parts[1])
        except ValueError:
            return "INVALID"

        nonce = parts[2]
        provided_sig = parts[3]

        expected_payload = f"SELECTIN_VIP:{branch_id}:{token_window}:{nonce}".encode("utf-8")
        expected_sig = hmac.new(MASTER_SECRET_SEED, expected_payload, hashlib.sha256).hexdigest()[:16]
        if not hmac.compare_digest(provided_sig, expected_sig):
            return "INVALID"

        current_window = int(check_time // self.SELECTIN_WINDOW_SECONDS)
        wall_window = int(time.time() // self.SELECTIN_WINDOW_SECONDS)

        if not (abs(current_window - token_window) <= 1 or abs(wall_window - token_window) <= 1):
            return "EXPIRED_REPLAY"

        # Single-Use Nonce (JTI) Anti-Replay Check within the active 60s window
        nonce_key = f"{token_window}:{nonce}"
        if nonce_key in self._consumed_selectin_nonces:
            return "DUPLICATE_NONCE_REPLAY"

        self._consumed_selectin_nonces[nonce_key] = check_time
        while len(self._consumed_selectin_nonces) > self.MAX_TRACKED_NONCES:
            self._consumed_selectin_nonces.popitem(last=False)

        return "VALID"

    def inspect_incoming_packet(
        self,
        source_ip: str,
        hla_selectin_header: Optional[str] = None,
        current_time: Optional[float] = None,
    ) -> Dict[str, object]:
        now = time.time() if current_time is None else current_time

        # 1. Anti-Replay Selectin Priority Lane Check (Window + Single-Use JTI Nonce)
        if hla_selectin_header:
            selectin_status = self._verify_selectin_anti_replay(
                hla_selectin_header, ACTIVE_BRANCH_ID, now
            )
            if selectin_status == "VALID":
                return {
                    "routing_decision": "ALLOW_EXPRESS_CLINICAL_LANE",
                    "reason": "Verified Single-Use Hospital HLA Selectin Token (Zero-Latency Bypass)",
                }
            if selectin_status in ("EXPIRED_REPLAY", "DUPLICATE_NONCE_REPLAY"):
                self.replay_blocks_count += 1
                return {
                    "routing_decision": "LYMPHATIC_BLACKHOLE_SINKHOLE_DROP",
                    "reason": f"REJECTED_SELECTIN_REPLAY_ATTACK: {selectin_status}",
                }

        # 2. Bounded FIFO Cache Management & Cadence Evaluation
        last_ts = self._last_request_timestamp.get(source_ip)
        if source_ip in self._last_request_timestamp:
            self._last_request_timestamp.move_to_end(source_ip)
        self._last_request_timestamp[source_ip] = now

        while len(self._last_request_timestamp) > self.max_tracked_ips:
            self._last_request_timestamp.popitem(last=False)

        if last_ts is not None and (now - last_ts) < self.MIN_HUMAN_OR_IOMT_DELTA_SECONDS:
            self.sinkholed_drops_count += 1
            return {
                "routing_decision": "LYMPHATIC_BLACKHOLE_SINKHOLE_DROP",
                "delta_ms": round((now - last_ts) * 1000, 3),
                "reason": "Sub-10ms DDoS micro-burst detected; discarded in /dev/null sinkhole",
            }

        return {
            "routing_decision": "STANDARD_INSPECTION",
            "reason": "Normal physiological/human request cadence",
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


_ddos_filter = LymphaticDDoSSinkholeFilter()


async def handle_endothelial_breach(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    peer_info = writer.get_extra_info("peername")
    attacker_ip = peer_info[0] if peer_info else "UNKNOWN_IP"

    ddos_verdict = _ddos_filter.inspect_incoming_packet(source_ip=attacker_ip)
    if ddos_verdict["routing_decision"] == "LYMPHATIC_BLACKHOLE_SINKHOLE_DROP":
        writer.close()
        return

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
            maze_node = ProtocolUnicorseMirrorMaze.reflect_infinite_labyrinth_node(request_str)
            writer.write((json.dumps(maze_node, indent=2) + "\n").encode("utf-8"))
            await writer.drain()
        else:
            # Guard Tarpit with bounded concurrency semaphore against Distributed Slowloris
            if not _ddos_filter.try_acquire_tarpit_slot():
                writer.close()
                return
            try:
                writer.write(b"HTTP/1.1 100 Continue\r\n")
                await writer.drain()
                while True:
                    await asyncio.sleep(30)
                    writer.write(b"..\r\n")
                    await writer.drain()
            finally:
                _ddos_filter.release_tarpit_slot()
    except Exception:
        pass
    finally:
        writer.close()
