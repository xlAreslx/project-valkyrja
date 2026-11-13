"""
Project VALKYRJA — Core Module 3: Out-of-Band Verbal Cryptographic Shield (MHC-I / NK Cell)
Architecture: Hexagonal Core (Identity & Anti-Deepfake Verification)
Compliance Target: EU NIS2 Directive / Sweden Cybersäkerhetslagen (SFS 2025:1506)

Implements:
1. 60-Second Rolling Verbal Token (RFC 6238 TOTP adapted to a high-clarity clinical/tactical
   phonetic dictionary) to neutralize real-time AI voice cloning (deepfakes).
2. NK-Cell "Missing-Self" Verifier: Rejects any high-stakes verbal command (e.g., emergency
   uncrossmatched blood release or executive wire transfer) lacking a valid MHC-I token.
"""

import hashlib
import hmac
import struct
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Tuple

# High-distinctiveness phonetic dictionary for noisy clinical/emergency environments
TACTICAL_CLINICAL_DICTIONARY: tuple[str, ...] = (
    "ALFA", "ADRENALINE", "ARGON", "BARIUM", "BISTURI", "CADMIUM",
    "COBALT", "CORTEX", "DELTA", "DOPAMINE", "EPINEPHRINE", "FIBRIN",
    "GAMMA", "GLUCAGON", "HEPARIN", "IRIDIUM", "ISOTOPE", "KRYPTON",
    "LACTATE", "LIDOCAINE", "MORPHINE", "NEON", "NITROGEN", "OSMIUM",
    "OXYGEN", "PLASMIN", "PLATINUM", "QUARTZ", "RADIUM", "SERUM",
    "SODIUM", "THROMBIN", "TITANIUM", "URANIUM", "VECTRA", "XENON",
)


@dataclass
class VerbalVerificationResult:
    is_authentic_self: bool
    caller_id: str
    action_requested: str
    verification_status: str
    timestamp_utc: str


class RollingVerbalShieldMHC1:
    """
    Generates and validates time-synchronized verbal tokens that rotate every 60 seconds.
    Acts as the 'MHC-I Self-Marker' checked by Digital NK Cells before executing critical orders.
    """

    def __init__(self, shared_device_secret: bytes, time_step_seconds: int = 60) -> None:
        self._secret = shared_device_secret
        self.time_step = time_step_seconds

    def _compute_totp_integer(self, time_counter: int) -> int:
        counter_bytes = struct.pack(">Q", time_counter)
        digest = hmac.new(self._secret, counter_bytes, hashlib.sha256).digest()
        offset = digest[-1] & 0x0F
        binary_code = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
        return binary_code

    def generate_current_verbal_seed(self, unix_time: Optional[float] = None) -> str:
        """
        Produces a deterministic 3-part verbal phrase: WORD1-WORD2-NN
        Example: 'THROMBIN-COBALT-84'
        """
        current_ts = time.time() if unix_time is None else unix_time
        time_counter = int(current_ts // self.time_step)
        code_int = self._compute_totp_integer(time_counter)

        dict_size = len(TACTICAL_CLINICAL_DICTIONARY)
        word_1 = TACTICAL_CLINICAL_DICTIONARY[code_int % dict_size]
        word_2 = TACTICAL_CLINICAL_DICTIONARY[(code_int // dict_size) % dict_size]
        numeric_pin = (code_int // (dict_size * dict_size)) % 100

        return f"{word_1}-{word_2}-{numeric_pin:02d}"

    def verify_nk_cell_self_marker(
        self,
        spoken_phrase: str,
        caller_id: str,
        action_requested: str,
        unix_time: Optional[float] = None,
    ) -> VerbalVerificationResult:
        """
        NK-Cell 'Missing-Self' Evaluation:
        Checks if the spoken phrase matches the current 60s window (or -1 step for network lag).
        If invalid, flags probable AI Voice Clone / Social Engineering and blocks execution.
        """
        current_ts = time.time() if unix_time is None else unix_time
        normalized_input = spoken_phrase.strip().upper()
        timestamp_str = datetime.now(timezone.utc).isoformat()

        # Check current 60s window and immediate previous window (clock drift tolerance)
        for window_offset in (0, -1):
            check_time = current_ts + (window_offset * self.time_step)
            expected_seed = self.generate_current_verbal_seed(unix_time=check_time)

            if hmac.compare_digest(normalized_input, expected_seed):
                return VerbalVerificationResult(
                    is_authentic_self=True,
                    caller_id=caller_id,
                    action_requested=action_requested,
                    verification_status=(
                        "MHC1_SELF_VERIFIED: Cryptographic verbal seed matched. "
                        "Order authorized."
                    ),
                    timestamp_utc=timestamp_str,
                )

        return VerbalVerificationResult(
            is_authentic_self=False,
            caller_id=caller_id,
            action_requested=action_requested,
            verification_status=(
                "NK_CELL_CYTOTOXIC_BLOCK: Missing or invalid MHC-I verbal seed! "
                "Suspected AI Voice Clone (Deepfake). Diverting session to Honeypot."
            ),
            timestamp_utc=timestamp_str,
        )


# =====================================================================
# LOCAL VERIFICATION SIMULATION
# =====================================================================
if __name__ == "__main__":
    print("=" * 72)
    print("  PROJECT VALKYRJA — MODULE 3: OUT-OF-BAND VERBAL SHIELD (ANTI-DEEPFAKE)")
    print("=" * 72)

    # Shared hardware secret provisioned in the Chief Physician's mobile Secure Enclave
    device_secret = b"SE_KAROLINSKA_CHIEF_MD_ENCLAVE_KEY_2026"
    verbal_shield = RollingVerbalShieldMHC1(shared_device_secret=device_secret)

    live_seed = verbal_shield.generate_current_verbal_seed()
    print(f"[LIVE 60s VERBAL TOKEN ON PHYSICIAN DEVICE] -> '{live_seed}'\n")

    # Scenario 1: Legitimate Emergency Order with valid 60s Verbal Seed
    legit_check = verbal_shield.verify_nk_cell_self_marker(
        spoken_phrase=live_seed,
        caller_id="DR_LINDQVIST_ER_CHIEF",
        action_requested="RELEASE_4_UNITS_O_NEG_TRAUMA_BAY_1",
    )
    print("[SCENARIO 1: LEGITIMATE PHYSICIAN WITH LIVE TOKEN]")
    print(f"  Authentic : {legit_check.is_authentic_self}")
    print(f"  Verdict   : {legit_check.verification_status}\n")

    # Scenario 2: Attacker using real-time AI Voice Cloning without screen access
    deepfake_check = verbal_shield.verify_nk_cell_self_marker(
        spoken_phrase="ALFA-DELTA-00",
        caller_id="SPOOFED_VOICE_CLONE_CALLER",
        action_requested="DISABLE_BLOOD_BANK_FIREWALL_AND_EXPORT_DB",
    )
    print("[SCENARIO 2: AI VOICE CLONE (DEEPFAKE) ATTACK]")
    print(f"  Authentic : {deepfake_check.is_authentic_self}")
    print(f"  Verdict   : {deepfake_check.verification_status}")
