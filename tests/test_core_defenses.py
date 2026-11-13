"""
Project VALKYRJA — Automated Verification & Unit Test Suite
Verifies Protocols U.N.I.C.O.R.S.E., S.I.E.R.R.A., G.A.L.A., S.O.F.I.A.,
Lymphatic DDoS Sinkholing, and Bioenergetic OT Backup Power Failover.
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

        dka_blocked = mod2.ProtocolSierraClinicalLocks.verify_dka_insulin_potassium_lock(2.9, 25.0)
        self.assertFalse(dka_blocked["iv_insulin_pump_authorized"])

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

        valid_token = mod4.LocalClinicalSurvivalBunker.generate_sofia_dyad_token("MOM-SE-8821", "NEO-SOFIA-001")
        sofia_ok = mod4.LocalClinicalSurvivalBunker.verify_protocol_sofia_nursery_lock(
            "MOM-SE-8821", "NEO-SOFIA-001", valid_token
        )
        self.assertTrue(sofia_ok["mother_infant_match_verified"])

    def test_5_lymphatic_ddos_sinkhole_and_bioenergetic_power_guard(self) -> None:
        """Verifies DDoS micro-burst sinkholing, Selectin VIP lane, and OT Generator Load Shedding."""
        ddos_filter = mod1.LymphaticDDoSSinkholeFilter()

        # 1. Unverified IP firing two requests separated by 2ms (0.002s < 10ms threshold) -> SINKHOLE
        first_pkt = ddos_filter.inspect_incoming_packet("198.51.100.44", current_time=1000.000)
        self.assertEqual(first_pkt["routing_decision"], "STANDARD_INSPECTION")

        burst_pkt = ddos_filter.inspect_incoming_packet("198.51.100.44", current_time=1000.002)
        self.assertEqual(burst_pkt["routing_decision"], "LYMPHATIC_BLACKHOLE_SINKHOLE_DROP")
        self.assertEqual(ddos_filter.sinkholed_drops_count, 1)

        # 2. Verified Hospital Terminal with Selectin HMAC Header -> EXPRESS CLINICAL LANE (even at 1ms)
        valid_selectin = mod1.LymphaticDDoSSinkholeFilter.generate_valid_selectin_header()
        vip_pkt = ddos_filter.inspect_incoming_packet(
            "10.0.10.5", hla_selectin_header=valid_selectin, current_time=1000.003
        )
        self.assertEqual(vip_pkt["routing_decision"], "ALLOW_EXPRESS_CLINICAL_LANE")

        # 3. Bioenergetic OT Power & Backup Diesel Generator Failover + Load Shedding
        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()
        snapshot = bunker.query_emergency_survival_snapshot()
        self.assertEqual(len(snapshot["ot_power_and_backup_generators"]), 3)

        power_failover = mod4.LocalClinicalSurvivalBunker.evaluate_bioenergetic_power_and_shed_loads(
            external_grid_online=False, ups_battery_pct=98.0, diesel_fuel_liters_pct=85.0
        )
        self.assertEqual(power_failover["load_shedding_action"], "HEMODYNAMIC_CENTRALIZATION_LOAD_SHEDDING_ACTIVE")
        self.assertTrue(power_failover["nordic_72h_preparedness_compliant"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
