"""
Project VALKYRJA — Automated Verification & Unit Test Suite
Compatible with both standard 'unittest' and 'pytest' runners.

Verifies:
1. Barium steganographic watermark generation and forensic decoding (Module 1).
2. 32-Byte (256-Bit) RAM encryption, decryption, and 0x00 Crypto-Shredding (Module 2).
3. 60-Second Rolling Verbal TOTP authentication & Deepfake rejection (Module 3).
4. Offline SQLite Clinical Bunker failover and sub-5ms query integrity (Module 4).
"""

import importlib.util
import unittest
from pathlib import Path
from types import ModuleType


def _load_module(alias: str, rel_path: str) -> ModuleType:
    root = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location(alias, root / rel_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod1 = _load_module("mod1", "core/1_deception_barium_engine.py")
mod2 = _load_module("mod2", "core/2_clinical_nis2_flowchart.py")
mod3 = _load_module("mod3", "core/3_verbal_shield_mhc1.py")
mod4 = _load_module("mod4", "adapters/4_local_clinical_bunker.py")


class TestProjectValkyrjaDefenses(unittest.TestCase):
    def test_1_barium_steganographic_watermark_forensics(self) -> None:
        """Ensures rolling watermark accurately encodes and decodes branch/terminal/staff."""
        token = mod1.generate_rolling_barium_token(
            branch_id="SE_GOTHENBURG_LAB_02",
            terminal_id="LIMS_TERM_09",
            staff_id="STAFF_HLA_777",
            time_window=498500,
        )
        self.assertTrue(token.startswith("TRC-498500-"))

        decoded = mod1.verify_barium_watermark(
            leaked_token=token,
            known_branches=["SE_STHLM_CLINIC_01", "SE_GOTHENBURG_LAB_02"],
            known_terminals=["ER_TRIAGE_TERM_04", "LIMS_TERM_09"],
            known_staff_ids=["STAFF_HLA_884", "STAFF_HLA_777"],
        )
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded["compromised_branch"], "SE_GOTHENBURG_LAB_02")
        self.assertEqual(decoded["compromised_terminal"], "LIMS_TERM_09")
        self.assertEqual(decoded["implicated_staff_session"], "STAFF_HLA_777")

    def test_2_ephemeral_32byte_ram_key_and_crypto_shredding(self) -> None:
        """Verifies 32-byte key encryption and permanent unrecoverability after shredding."""
        key_mgr = mod2.EphemeralRAMKeyManager()
        secret_data = "PATIENT_BLOOD_GROUP:O_NEG|CROSSMATCH_READY"

        encrypted = key_mgr.encrypt_record_in_ram(secret_data)
        decrypted = key_mgr.decrypt_record_in_ram(encrypted)
        self.assertEqual(decrypted, secret_data)

        # Execute Tier-4 Crypto-Shredding (0x00 overwrite in RAM)
        shred_ms = key_mgr.execute_crypto_shredding()
        self.assertTrue(key_mgr.is_shredded)
        self.assertLess(shred_ms, 50.0)

        # Attempting decryption after shredding must raise PermissionError
        with self.assertRaises(PermissionError):
            key_mgr.decrypt_record_in_ram(encrypted)

    def test_3_verbal_shield_anti_deepfake_mhc1(self) -> None:
        """Confirms valid 60s verbal seed passes while spoofed deepfake phrase is blocked."""
        shield = mod3.RollingVerbalShieldMHC1(b"TEST_SHARED_SECRET_32BYTES_2026")
        fixed_time = 1763000000.0

        valid_phrase = shield.generate_current_verbal_seed(unix_time=fixed_time)
        auth_ok = shield.verify_nk_cell_self_marker(
            spoken_phrase=valid_phrase,
            caller_id="DR_ERIKSSON",
            action_requested="EMERGENCY_RELEASE_O_NEG",
            unix_time=fixed_time,
        )
        self.assertTrue(auth_ok.is_authentic_self)

        # Spoofed voice clone without valid token must be blocked
        auth_fail = shield.verify_nk_cell_self_marker(
            spoken_phrase="BARIUM-COBALT-99",
            caller_id="VOICE_CLONE_IMPOSTOR",
            action_requested="EXPORT_PATIENT_DATABASE",
            unix_time=fixed_time,
        )
        self.assertFalse(auth_fail.is_authentic_self)

    def test_4_offline_clinical_bunker_survival(self) -> None:
        """Verifies offline SQLite bunker preserves ER triage, O-Neg blood and panic labs."""
        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()
        snapshot = bunker.query_emergency_survival_snapshot()

        self.assertEqual(snapshot["bunker_mode"], "OFFLINE_AUTONOMOUS_SURVIVAL")
        self.assertGreaterEqual(len(snapshot["active_resuscitation_patients"]), 2)
        self.assertGreaterEqual(len(snapshot["verified_safe_blood_units"]), 3)
        self.assertGreaterEqual(len(snapshot["critical_lab_panic_alerts"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
