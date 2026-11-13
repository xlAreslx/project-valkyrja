"""
Project VALKYRJA — Automated Verification & Red-Team v1.4 Enterprise Test Suite
Verifies Protocols U.N.I.C.O.R.S.E., S.I.E.R.R.A., G.A.L.A., S.O.F.I.A.,
Subroutine C.O.L.E., B.I.O.F.O.A.M. + 6-Table Merkle Seals, Single-Use JTI Nonces,
Slowloris Tarpit Semaphores, Kernel RAM Page Locking, Bilateral Cryo Hemolysis Guards,
Signed N+1 Refrigerator & OT Generator Maintenance/Swaps, IoMT Hardware Lifecycle,
and Multi-Hospital Subsidiary Federation.
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

    def test_2_protocol_sierra_ram_key_and_clinical_locks(self) -> None:
        key_mgr = mod2.EphemeralRAMKeyManager()
        encrypted = key_mgr.encrypt_record_in_ram("PATIENT_BLOOD_GROUP:O_NEG")
        self.assertEqual(key_mgr.decrypt_record_in_ram(encrypted), "PATIENT_BLOOD_GROUP:O_NEG")

        key_mgr.execute_crypto_shredding()
        with self.assertRaises(PermissionError):
            key_mgr.decrypt_record_in_ram(encrypted)

        dka_blocked = mod2.ProtocolSierraClinicalLocks.verify_dka_insulin_potassium_lock(2.9, 25.0)
        self.assertFalse(dka_blocked["iv_insulin_pump_authorized"])

    def test_3_verbal_shield_anti_deepfake_mhc1(self) -> None:
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
        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()
        snapshot = bunker.query_emergency_survival_snapshot()

        self.assertIn("PROTOCOL_GALA_12_PILLARS", snapshot["active_bunker_protocols"])
        self.assertIn("PROTOCOL_SOFIA_NICU_SAFEGUARD", snapshot["active_bunker_protocols"])
        self.assertGreaterEqual(len(snapshot["active_resuscitation_patients"]), 9)

        valid_token = mod4.LocalClinicalSurvivalBunker.generate_sofia_dyad_token("MOM-SE-8821", "NEO-SOFIA-001")
        sofia_ok = mod4.LocalClinicalSurvivalBunker.verify_protocol_sofia_nursery_lock(
            "MOM-SE-8821", "NEO-SOFIA-001", valid_token
        )
        self.assertTrue(sofia_ok["mother_infant_match_verified"])

    def test_5_lymphatic_ddos_sinkhole_and_bioenergetic_power_guard(self) -> None:
        ddos_filter = mod1.LymphaticDDoSSinkholeFilter()

        first_pkt = ddos_filter.inspect_incoming_packet("198.51.100.44", current_time=1000.000)
        self.assertEqual(first_pkt["routing_decision"], "STANDARD_INSPECTION")

        burst_pkt = ddos_filter.inspect_incoming_packet("198.51.100.44", current_time=1000.002)
        self.assertEqual(burst_pkt["routing_decision"], "LYMPHATIC_BLACKHOLE_SINKHOLE_DROP")

        valid_selectin = mod1.LymphaticDDoSSinkholeFilter.generate_valid_selectin_header(current_time=1000.003)
        vip_pkt = ddos_filter.inspect_incoming_packet(
            "10.0.10.5", hla_selectin_header=valid_selectin, current_time=1000.003
        )
        self.assertEqual(vip_pkt["routing_decision"], "ALLOW_EXPRESS_CLINICAL_LANE")

        power_failover = mod4.LocalClinicalSurvivalBunker.evaluate_bioenergetic_power_and_shed_loads(
            external_grid_online=False, ups_battery_pct=98.0, diesel_fuel_liters_pct=85.0
        )
        self.assertEqual(power_failover["load_shedding_action"], "HEMODYNAMIC_CENTRALIZATION_LOAD_SHEDDING_ACTIVE")

    def test_6_red_team_hardening_defenses(self) -> None:
        bounded_filter = mod1.LymphaticDDoSSinkholeFilter(max_tracked_ips=50)
        for i in range(120):
            bounded_filter.inspect_incoming_packet(f"203.0.113.{i}", current_time=5000.0 + i)
        self.assertLessEqual(len(bounded_filter._last_request_timestamp), 50)

        old_captured_token = mod1.LymphaticDDoSSinkholeFilter.generate_valid_selectin_header(current_time=1000.0)
        replay_attempt = bounded_filter.inspect_incoming_packet(
            "10.0.10.99", hla_selectin_header=old_captured_token, current_time=5000.0
        )
        self.assertEqual(replay_attempt["routing_decision"], "LYMPHATIC_BLACKHOLE_SINKHOLE_DROP")
        self.assertIn("REJECTED_SELECTIN_REPLAY_ATTACK", replay_attempt["reason"])

        key_mgr = mod2.EphemeralRAMKeyManager()
        self.assertTrue(key_mgr.zero_copy_memoryview_enforced)
        key_mgr.execute_crypto_shredding()
        self.assertIn("SUBROUTINE_COLE_SHREDDED", key_mgr.get_key_status_preview())

        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()
        clean_audit = bunker.verify_bunker_row_integrity()
        self.assertTrue(clean_audit["biofoam_integrity_verified"])

        bunker.conn.execute(
            "UPDATE er_active_triage SET abo_rh = 'AB+' WHERE patient_token = 'PT-TRAUMA-992A'"
        )
        bunker.conn.commit()

        tamper_audit = bunker.verify_bunker_row_integrity()
        self.assertFalse(tamper_audit["biofoam_integrity_verified"])
        self.assertIn("PT-TRAUMA-992A", tamper_audit["tampered_patient_tokens"])

    def test_7_red_team_v1_2_elite_hardening(self) -> None:
        ddos_filter = mod1.LymphaticDDoSSinkholeFilter(max_tarpit_slots=3)
        single_use_token = mod1.LymphaticDDoSSinkholeFilter.generate_valid_selectin_header(current_time=3000.000)

        first_use = ddos_filter.inspect_incoming_packet("10.0.10.20", single_use_token, current_time=3000.001)
        self.assertEqual(first_use["routing_decision"], "ALLOW_EXPRESS_CLINICAL_LANE")

        second_use_replay = ddos_filter.inspect_incoming_packet("10.0.10.20", single_use_token, current_time=3000.002)
        self.assertEqual(second_use_replay["routing_decision"], "LYMPHATIC_BLACKHOLE_SINKHOLE_DROP")
        self.assertIn("DUPLICATE_NONCE_REPLAY", second_use_replay["reason"])

        self.assertTrue(ddos_filter.try_acquire_tarpit_slot())
        self.assertTrue(ddos_filter.try_acquire_tarpit_slot())
        self.assertTrue(ddos_filter.try_acquire_tarpit_slot())
        self.assertFalse(ddos_filter.try_acquire_tarpit_slot())
        ddos_filter.release_tarpit_slot()

        key_mgr = mod2.EphemeralRAMKeyManager()
        self.assertTrue(
            key_mgr.kernel_swap_lock_status.startswith(("KERNEL_", "VOLATILE_RAM_GUARD_ACTIVE"))
        )

        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()
        bunker.conn.execute("DELETE FROM er_active_triage WHERE patient_token = 'PT-CARDIO-441B'")
        bunker.conn.commit()

        delete_audit = bunker.verify_bunker_row_integrity()
        self.assertFalse(delete_audit["biofoam_integrity_verified"])
        self.assertFalse(delete_audit["merkle_5table_manifest_intact"])
        self.assertIn("DELETED:PT-CARDIO-441B", delete_audit["tampered_patient_tokens"])

    def test_8_bilateral_cryo_freezing_guard_and_n1_maintenance(self) -> None:
        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()

        auth_token = mod4.LocalClinicalSurvivalBunker.generate_maintenance_auth_token(
            target_fridge_id="ER_FRIDGE_01",
            backup_fridge_id="ER_FRIDGE_BACKUP_02",
            technician_id="BIOMED_ENG_SE_104",
        )

        bad_transfer = bunker.execute_signed_cold_chain_maintenance(
            target_fridge_id="ER_FRIDGE_01",
            backup_fridge_id="ER_FRIDGE_BACKUP_02",
            backup_verified_temp_c=-5.0,
            technician_id="BIOMED_ENG_SE_104",
            auth_token=auth_token,
        )
        self.assertFalse(bad_transfer["maintenance_authorized"])

        good_transfer = bunker.execute_signed_cold_chain_maintenance(
            target_fridge_id="ER_FRIDGE_01",
            backup_fridge_id="ER_FRIDGE_BACKUP_02",
            backup_verified_temp_c=4.0,
            technician_id="BIOMED_ENG_SE_104",
            auth_token=auth_token,
        )
        self.assertTrue(good_transfer["maintenance_authorized"])
        self.assertTrue(bunker.verify_bunker_row_integrity()["biofoam_integrity_verified"])

        bunker.conn.execute(
            "UPDATE blood_bank_reserve SET temp_celsius = -3.5 WHERE unit_id = 'BLD-SE-ONEG-001'"
        )
        bunker.conn.commit()

        thermal_audit = bunker.audit_bilateral_thermo_cryogenic_safety()
        self.assertFalse(thermal_audit["all_units_within_bilateral_bounds"])

    def test_9_generator_swap_iomt_lifecycle_and_subsidiary_federation(self) -> None:
        """
        Verifies:
        1. OT Backup Generator replacement requires >=72h collateral autonomy and re-seals Merkle.
        2. Connected IoMT/IT Equipment Lifecycle (Adding Laparoscopy/iPad/Imaging, Maintenance Quarantine,
           Hot-Swap Replacement, and Apoptosis Decommissioning revocation).
        3. Multi-Hospital Subsidiary Federation isolates a compromised sub-clinic while verifying
           a signed emergency ambulance transfer capsule to the main hospital.
        """
        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()

        # 1. OT Diesel Generator Replacement (Mitophagy -> Biogenesis)
        gen_auth = mod4.LocalClinicalSurvivalBunker.generate_power_lifecycle_auth_token(
            "ATS-DIESEL-GENSET-A", "REPLACE_WITH_NEW_GENERATOR", "CHIEF_OT_ENG_01"
        )
        # Attempt swap with insufficient backup fuel (40h < 72h Nordic standard) -> MUST BLOCK
        unsafe_gen_swap = bunker.execute_ot_generator_maintenance_or_swap(
            target_subsystem_id="ATS-DIESEL-GENSET-A",
            action="REPLACE_WITH_NEW_GENERATOR",
            collateral_backup_online=True,
            collateral_autonomy_hours=40.0,
            engineer_id="CHIEF_OT_ENG_01",
            auth_token=gen_auth,
            new_subsystem_id="ATS-DIESEL-GENSET-B-NEW",
        )
        self.assertFalse(unsafe_gen_swap["power_operation_authorized"])

        # Perform swap with verified 96h collateral autonomy -> MUST SUCCEED & RESEAL MERKLE
        safe_gen_swap = bunker.execute_ot_generator_maintenance_or_swap(
            target_subsystem_id="ATS-DIESEL-GENSET-A",
            action="REPLACE_WITH_NEW_GENERATOR",
            collateral_backup_online=True,
            collateral_autonomy_hours=96.0,
            engineer_id="CHIEF_OT_ENG_01",
            auth_token=gen_auth,
            new_subsystem_id="ATS-DIESEL-GENSET-B-NEW",
        )
        self.assertTrue(safe_gen_swap["power_operation_authorized"])
        self.assertTrue(bunker.verify_bunker_row_integrity()["biofoam_integrity_verified"])

        # 2. Connected IoMT / IT Hardware Lifecycle (iPad, Laparoscopy, CT Imaging, ICU, NICU)
        # 2A. Add a new Surgical Laparoscopy Tower
        add_auth = mod4.LocalClinicalSurvivalBunker.generate_equipment_lifecycle_auth(
            "ADD_NEW", "DEV-OR-LAP-02", "BIOMED_ENG_99"
        )
        add_res = bunker.manage_connected_equipment_lifecycle(
            action="ADD_NEW",
            device_id="DEV-OR-LAP-02",
            device_category="OR_LAPAROSCOPY_4K_TOWER",
            assigned_department="SURGICAL_OR_SUITE_04",
            serial_or_mac="MAC:00:1A:2B:OR:02",
            biomed_engineer_id="BIOMED_ENG_99",
            auth_token=add_auth,
        )
        self.assertTrue(add_res["lifecycle_authorized"])
        self.assertTrue(bunker.verify_bunker_row_integrity()["biofoam_integrity_verified"])

        # 2B. Decommission (Apoptosis) an old ER iPad and verify its stolen token is permanently blocked
        old_ipad_token = mod4.LocalClinicalSurvivalBunker.generate_hla_hardware_token(
            "DEV-IPAD-ER-04", "CLINICAL_MOBILE_IPAD_PRO", "EMERGENCY_TRIAGE_BAY", "SER:IPAD-SE-9941"
        )
        rem_auth = mod4.LocalClinicalSurvivalBunker.generate_equipment_lifecycle_auth(
            "REMOVE_DECOMMISSION", "DEV-IPAD-ER-04", "BIOMED_ENG_99"
        )
        bunker.manage_connected_equipment_lifecycle(
            action="REMOVE_DECOMMISSION",
            device_id="DEV-IPAD-ER-04",
            device_category="CLINICAL_MOBILE_IPAD_PRO",
            assigned_department="EMERGENCY_TRIAGE_BAY",
            serial_or_mac="SER:IPAD-SE-9941",
            biomed_engineer_id="BIOMED_ENG_99",
            auth_token=rem_auth,
        )
        stolen_ipad_attempt = bunker.verify_connected_device_access("DEV-IPAD-ER-04", old_ipad_token)
        self.assertFalse(stolen_ipad_attempt["access_granted"])
        self.assertEqual(stolen_ipad_attempt["verdict"], "BLOCKED_APOPTOSIS_REVOKED_HARDWARE_TOKEN")
        self.assertTrue(bunker.verify_bunker_row_integrity()["biofoam_integrity_verified"])

        # 3. Multi-Hospital & Subsidiary Federation (Sub-clinic quarantine + Ambulance Transfer Capsule)
        fed = mod4.MultiHospitalSubsidiaryFederation("SWEDISH_VITALCARE_GROUP_AB")
        fed.register_subsidiary_node("SE_STHLM_MAIN_HOSPITAL", "TERTIARY_MAIN_HOSPITAL")
        fed.register_subsidiary_node("SE_UPPSALA_SUBCLINIC_02", "PERIPHERAL_SUBCLINIC")
        fed.register_subsidiary_node("SE_MALMO_IMAGING_LAB_03", "DIAGNOSTIC_LAB_CENTER")

        isolation = fed.isolate_compromised_subsidiary(
            "SE_UPPSALA_SUBCLINIC_02", "Ransomware detected on sub-clinic reception PC"
        )
        self.assertTrue(isolation["lateral_movement_blocked"])
        self.assertIn("SE_STHLM_MAIN_HOSPITAL", isolation["protected_sister_hospitals_and_subclinics"])

        # Export signed ambulance transfer capsule from the quarantined sub-clinic to the Main Hospital
        capsule = fed.export_signed_ambulance_transfer_capsule(
            origin_subclinic_id="SE_UPPSALA_SUBCLINIC_02",
            destination_hospital_id="SE_STHLM_MAIN_HOSPITAL",
            patient_token="PT-TRANSFER-707",
            abo_rh="O-",
            critical_summary="STEMI_ACTIVE | hs-cTnT: 110 ng/L | Allergy: Penicillin | Heparin IV",
        )
        verify_transfer = fed.verify_incoming_ambulance_transfer_capsule(capsule)
        self.assertTrue(verify_transfer["transfer_capsule_authentic"])
        self.assertEqual(verify_transfer["receiving_action"], "ADMIT_TO_MAIN_HOSPITAL_TRAUMA_OR_ICU_BAY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
