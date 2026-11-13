"""
Project VALKYRJA — Automated Verification & Red-Team v1.5 Regional Command Test Suite
Verifies all 10 Core, Cryptographic, Clinical, IoMT, EMS Fleet, Workforce & Federation Defenses.
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

        key_mgr = mod2.EphemeralRAMKeyManager()
        self.assertTrue(key_mgr.zero_copy_memoryview_enforced)
        key_mgr.execute_crypto_shredding()
        self.assertIn("SUBROUTINE_COLE_SHREDDED", key_mgr.get_key_status_preview())

        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()
        self.assertTrue(bunker.verify_bunker_row_integrity()["biofoam_integrity_verified"])

        bunker.conn.execute(
            "UPDATE er_active_triage SET abo_rh = 'AB+' WHERE patient_token = 'PT-TRAUMA-992A'"
        )
        bunker.conn.commit()
        self.assertFalse(bunker.verify_bunker_row_integrity()["biofoam_integrity_verified"])

    def test_7_red_team_v1_2_elite_hardening(self) -> None:
        ddos_filter = mod1.LymphaticDDoSSinkholeFilter(max_tarpit_slots=3)
        single_use_token = mod1.LymphaticDDoSSinkholeFilter.generate_valid_selectin_header(current_time=3000.000)

        first_use = ddos_filter.inspect_incoming_packet("10.0.10.20", single_use_token, current_time=3000.001)
        self.assertEqual(first_use["routing_decision"], "ALLOW_EXPRESS_CLINICAL_LANE")

        second_use_replay = ddos_filter.inspect_incoming_packet("10.0.10.20", single_use_token, current_time=3000.002)
        self.assertEqual(second_use_replay["routing_decision"], "LYMPHATIC_BLACKHOLE_SINKHOLE_DROP")

        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()
        bunker.conn.execute("DELETE FROM er_active_triage WHERE patient_token = 'PT-CARDIO-441B'")
        bunker.conn.commit()
        self.assertFalse(bunker.verify_bunker_row_integrity()["biofoam_integrity_verified"])

    def test_8_bilateral_cryo_freezing_guard_and_n1_maintenance(self) -> None:
        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()

        auth_token = mod4.LocalClinicalSurvivalBunker.generate_maintenance_auth_token(
            target_fridge_id="ER_FRIDGE_01",
            backup_fridge_id="ER_FRIDGE_BACKUP_02",
            technician_id="BIOMED_ENG_SE_104",
        )
        good_transfer = bunker.execute_signed_cold_chain_maintenance(
            target_fridge_id="ER_FRIDGE_01",
            backup_fridge_id="ER_FRIDGE_BACKUP_02",
            backup_verified_temp_c=4.0,
            technician_id="BIOMED_ENG_SE_104",
            auth_token=auth_token,
        )
        self.assertTrue(good_transfer["maintenance_authorized"])
        self.assertTrue(bunker.verify_bunker_row_integrity()["biofoam_integrity_verified"])

    def test_9_generator_swap_iomt_lifecycle_and_subsidiary_federation(self) -> None:
        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()

        gen_auth = mod4.LocalClinicalSurvivalBunker.generate_power_lifecycle_auth_token(
            "ATS-DIESEL-GENSET-A", "REPLACE_WITH_NEW_GENERATOR", "CHIEF_OT_ENG_01"
        )
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

    def test_10_cdr_trojan_sanitizer_architect_vault_ems_rendezvous_and_workforce(self) -> None:
        """
        Verifies the 5 Regional Hospital Command & Governance capabilities:
        1. Phagocytic CDR strips a Trojan hidden in a lab result from Sub-clinic A while keeping clinical data.
        2. Sub-clinic Confidential Vault requires 2 Board Members + Lead Architect (Dr. Luis Aburto) key share.
        3. EMS Pit-Stop routes a critical distant patient to Sub-clinic B while dispatching O-Neg via Helicopter,
           plus instant lockdown of a stolen ambulance.
        4. Workforce & Contractor Registry blocks sanitation/cafeteria staff from ICU EHR tables and
           auto-expires occasional/sporadic locum shifts.
        """
        fed = mod4.MultiHospitalSubsidiaryFederation("SWEDISH_VITALCARE_GROUP_AB")
        fed.register_subsidiary_node(
            "SE_STHLM_MAIN_HOSPITAL",
            "TERTIARY_MAIN_HOSPITAL",
            available_clinical_services=["NEUROSURGERY_OR_ECMO", "TRAUMA_CENTER"],
            available_blood_and_supplies={"O_NEG_RBC": 12, "FIBRINOGEN_CONCENTRATE": 8},
        )
        fed.register_subsidiary_node(
            "SE_UPPSALA_SUBCLINIC_A",
            "PERIPHERAL_SUBCLINIC",
            available_clinical_services=["ER_STABILIZATION"],
            available_blood_and_supplies={"O_NEG_RBC": 0},
        )
        fed.register_subsidiary_node(
            "SE_VASTERAS_SUBCLINIC_B",
            "PERIPHERAL_SUBCLINIC",
            available_clinical_services=["ER_STABILIZATION", "AIRWAY_INTUBATION"],
            available_blood_and_supplies={"O_NEG_RBC": 1},
        )

        # 1. Phagocytic CDR: Sub-clinic A sends a lab result infected with a Trojan macro/PowerShell
        infected_lab = {
            "patient_token": "PT-7741",
            "analyte": "Serum_Potassium",
            "numeric_value": "6.4",
            "unit": "mmol/L <script>powershell.exe -enc MALWARE</script>",
            "hidden_trojan_macro": "VBA_MACRO_AUTOOPEN: DROP TABLE er_active_triage;",
        }
        cdr_res = fed.sanitize_and_verify_interclinic_payload(
            "SE_UPPSALA_SUBCLINIC_A", "SE_VASTERAS_SUBCLINIC_B", infected_lab
        )
        self.assertTrue(cdr_res["trojan_or_exploit_detected"])
        self.assertEqual(
            cdr_res["cdr_action"], "TROJAN_PHAGOCYTOSED_AND_STRIPPED_STERILE_VALUES_EXTRACTED"
        )
        self.assertNotIn("hidden_trojan_macro", cdr_res["sterile_reconstructed_clinical_capsule"])
        self.assertEqual(cdr_res["sterile_reconstructed_clinical_capsule"]["numeric_value"], "6.4")

        # 2. Sub-Clinic Vault Compartmentalization + Board & Lead Architect (Dr. Luis Aburto) Quorum
        board_1 = {
            "signer_id": "BOARD_CHAIR_LINDQVIST",
            "token": fed.generate_architect_or_board_key_share(
                "BOARD_MEMBER", "BOARD_CHAIR_LINDQVIST", "SE_UPPSALA_SUBCLINIC_A"
            ),
        }
        board_2 = {
            "signer_id": "BOARD_DIR_BERGSTROM",
            "token": fed.generate_architect_or_board_key_share(
                "BOARD_MEMBER", "BOARD_DIR_BERGSTROM", "SE_UPPSALA_SUBCLINIC_A"
            ),
        }
        architect_key = {
            "signer_id": "DR_LUIS_ABURTO_ARCHITECT",
            "token": fed.generate_architect_or_board_key_share(
                "ARCHITECT_DEVELOPER", "DR_LUIS_ABURTO_ARCHITECT", "SE_UPPSALA_SUBCLINIC_A"
            ),
        }

        # 2A. Attempt access WITHOUT Lead Architect key -> MUST DENY
        denied_vault = fed.unlock_subclinic_confidential_vault(
            requesting_branch_id="SE_STHLM_MAIN_HOSPITAL",
            target_subclinic_id="SE_UPPSALA_SUBCLINIC_A",
            board_member_signatures=[board_1, board_2],
            architect_dev_signature=None,
            encrypted_subclinic_record="VIP_CONFIDENTIAL_GENOMIC_DOSSIER_SE_01",
        )
        self.assertFalse(denied_vault["vault_access_granted"])

        # 2B. Authorize with 2 Board Members + Dr. Luis Aburto Architect Key -> MUST UNLOCK
        unlocked_vault = fed.unlock_subclinic_confidential_vault(
            requesting_branch_id="SE_STHLM_MAIN_HOSPITAL",
            target_subclinic_id="SE_UPPSALA_SUBCLINIC_A",
            board_member_signatures=[board_1, board_2],
            architect_dev_signature=architect_key,
            encrypted_subclinic_record="VIP_CONFIDENTIAL_GENOMIC_DOSSIER_SE_01",
        )
        self.assertTrue(unlocked_vault["vault_access_granted"])

        # 3. Critical Patient Pit-Stop (50 min to Main Hospital vs 8 min to Sub-clinic B) + Helicopter Blood Dispatch
        rendezvous = fed.orchestrate_critical_patient_and_supply_rendezvous(
            patient_token="PT-CRIT-BLEED-88",
            required_definitive_service="NEUROSURGERY_OR_ECMO",
            required_urgent_supply="O_NEG_RBC",
            required_supply_units=4,
            eta_to_main_hospital_minutes=50,
            nearest_subclinic_id="SE_VASTERAS_SUBCLINIC_B",
            eta_to_nearest_subclinic_minutes=8,
        )
        self.assertEqual(
            rendezvous["tactical_routing_decision"],
            "DAMAGE_CONTROL_PIT_STOP_AT_NEAREST_SUBCLINIC_PLUS_HELI_RENDEZVOUS",
        )
        self.assertEqual(rendezvous["immediate_stabilization_destination"], "SE_VASTERAS_SUBCLINIC_B")
        self.assertEqual(rendezvous["supply_dispatched_from_branch"], "SE_STHLM_MAIN_HOSPITAL")

        # 3B. EMS Fleet Theft Lockdown & Merkle Re-Sealing
        bunker = mod4.LocalClinicalSurvivalBunker()
        bunker.seed_shadow_sync_snapshot()
        theft_auth = mod4.LocalClinicalSurvivalBunker.generate_fleet_lifecycle_auth(
            "REPORT_STOLEN_LOCKDOWN", "AMB-ALS-SUB-04", "EMS_CMD_01"
        )
        theft_res = bunker.manage_ems_fleet_unit_lifecycle(
            action="REPORT_STOLEN_LOCKDOWN",
            unit_id="AMB-ALS-SUB-04",
            vehicle_type="ADVANCED_LIFE_SUPPORT_AMBULANCE",
            home_station_branch="SE_UPPSALA_SUBCLINIC_02",
            capabilities="AIRWAY",
            fleet_commander_id="EMS_CMD_01",
            auth_token=theft_auth,
        )
        self.assertTrue(theft_res["fleet_op_authorized"])
        self.assertTrue(bunker.verify_bunker_row_integrity()["biofoam_integrity_verified"])

        # 4. Workforce, Support Staff, Contractors & Occasional/Sporadic Worker Verification
        # 4A. Cafeteria Contractor attempting to read FULL_CLINICAL_EHR_AND_ORDERS -> BLOCKED
        caf_attempt = bunker.verify_workforce_access_request(
            staff_id="STAFF-CAF-501",
            requested_scope="FULL_CLINICAL_EHR_AND_ORDERS",
            current_unix_time=1763000000.0,
        )
        self.assertFalse(caf_attempt["access_authorized"])
        self.assertIn("HLA_ROLE_COMPARTMENT_VIOLATION", caf_attempt["reason"])

        # 4B. Occasional/Sporadic Weekend Locum Physician after shift expiration -> AUTO-EXPIRED BLOCK
        locum_active = bunker.verify_workforce_access_request(
            staff_id="STAFF-LOCUM-999",
            requested_scope="FULL_CLINICAL_EHR_AND_ORDERS",
            current_unix_time=1763000000.0,
        )
        self.assertTrue(locum_active["access_authorized"])

        locum_expired = bunker.verify_workforce_access_request(
            staff_id="STAFF-LOCUM-999",
            requested_scope="FULL_CLINICAL_EHR_AND_ORDERS",
            current_unix_time=1763090000.0,  # Past 1763050000.0 expiration
        )
        self.assertFalse(locum_expired["access_authorized"])
        self.assertIn("EXPIRED_SPORADIC_OR_CONTRACTOR_WINDOW", locum_expired["reason"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
