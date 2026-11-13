"""
Project VALKYRJA — Automated Verification & Unit Test Suite
Verifies Protocols U.N.I.C.O.R.S.E., S.I.E.R.R.A., G.A.L.A., and S.O.F.I.A.
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
    def test_1_barium_watermark_and_protocol_unicorse_maze(self) -> None:
        """Verifies Barium forensic decoding and Protocol UNICORSE infinite mirror labyrinth."""
        token = mod1.generate_rolling_barium_token(
            branch_id="SE_GOTHENBURG_LAB_02",
            terminal_id="LIMS_TERM_09",
            staff_id="STAFF_HLA_777",
            time_window=498500,
        )
        decoded = mod1.verify_barium_watermark(
            leaked_token=token,
            known_branches=["SE_GOTHENBURG_LAB_02"],
            known_terminals=["LIMS_TERM_09"],
            known_staff_ids=["STAFF_HLA_777"],
        )
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded["compromised_branch"], "SE_GOTHENBURG_LAB_02")

        # Verify deterministic infinite labyrinth reflection
        maze_1 = mod1.ProtocolUnicorseMirrorMaze.reflect_infinite_labyrinth_node("/vault/level1/level2")
        maze_2 = mod1.ProtocolUnicorseMirrorMaze.reflect_infinite_labyrinth_node("/vault/level1/level2")
        self.assertEqual(maze_1["synthesized_subdirectories"], maze_2["synthesized_subdirectories"])
        self.assertEqual(len(maze_1["synthesized_subdirectories"]), 4)

    def test_2_protocol_sierra_ram_key_and_clinical_locks(self) -> None:
        """Verifies 32-byte RAM Crypto-Shredding and ESC / Cystatin C / DKA safety locks."""
        key_mgr = mod2.EphemeralRAMKeyManager()
        encrypted = key_mgr.encrypt_record_in_ram("PATIENT_BLOOD_GROUP:O_NEG")
        self.assertEqual(key_mgr.decrypt_record_in_ram(encrypted), "PATIENT_BLOOD_GROUP:O_NEG")

        key_mgr.execute_crypto_shredding()
        with self.assertRaises(PermissionError):
            key_mgr.decrypt_record_in_ram(encrypted)

        # Verify DKA Hypokalemia Hard Lock (K+ < 3.3 must block IV insulin)
        dka_blocked = mod2.ProtocolSierraClinicalLocks.verify_dka_insulin_potassium_lock(2.9, 25.0)
        self.assertFalse(dka_blocked["iv_insulin_pump_authorized"])

        # Verify Swedish Cystatin C + Creatinine eGFR & Hyperkalemia alert
        renal = mod2.ProtocolSierraClinicalLocks.evaluate_swedish_dual_egfr_and_dialysis(500.0, 3.0, 6.8)
        self.assertIn("URGENT_HEMODIALYSIS", renal["nephrology_action"])

    def test_3_verbal_shield_anti_deepfake_mhc1(self) -> None:
        """Confirms valid 60s verbal seed passes while spoofed deepfake phrase is blocked."""
        shield = mod3.RollingVerbalShieldMHC1(b"TEST_SHARED_SECRET_32BYTES_2026")
        fixed_time = 1763000000.0
        valid_phrase = shield.generate_current_verbal_seed(unix_time=fixed_time)

        self.assertTrue(
            shield.verify_nk_cell_self_marker(valid_phrase, "DR_ERIKSSON", "ORDER", fixed_time).is_authentic_self
        )
        self.assertFalse(
            shield.verify_nk_cell_self_marker("FAKE-SEED-00", "IMPOSTOR", "ORDER", fixed_time).is_authentic_self
        )

    def test_4_protocol_gala_and_protocol_sofia_bunker(self) -> None:
        """Verifies 12-Pillar SQLite Bunker, -196C LN2 Cryo matrix, and Protocol SOFIA NICU dyad lock."""
        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()
        snapshot = bunker.query_emergency_survival_snapshot()

        self.assertIn("PROTOCOL_GALA_12_PILLARS", snapshot["active_bunker_protocols"])
        self.assertIn("PROTOCOL_SOFIA_NICU_SAFEGUARD", snapshot["active_bunker_protocols"])
        self.assertGreaterEqual(len(snapshot["active_resuscitation_patients"]), 9)
        self.assertGreaterEqual(len(snapshot["verified_safe_blood_units"]), 6)

        # Verify Protocol SOFIA Mother-Infant Wristband cryptographic check
        valid_token = mod4.LocalClinicalSurvivalBunker.generate_sofia_dyad_token("MOM-SE-8821", "NEO-SOFIA-001")
        sofia_ok = mod4.LocalClinicalSurvivalBunker.verify_protocol_sofia_nursery_lock(
            "MOM-SE-8821", "NEO-SOFIA-001", valid_token
        )
        self.assertTrue(sofia_ok["mother_infant_match_verified"])

        sofia_mismatch = mod4.LocalClinicalSurvivalBunker.verify_protocol_sofia_nursery_lock(
            "MOM-SE-8821", "NEO-SOFIA-001", "SOFIA-DYAD-WRONGTOKEN00"
        )
        self.assertFalse(sofia_mismatch["mother_infant_match_verified"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
