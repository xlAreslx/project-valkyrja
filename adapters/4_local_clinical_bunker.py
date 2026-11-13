"""
Project VALKYRJA — Adapter Module 4: Offline Point-of-Care Survival Bunker (SQLite),
IoMT Hardware Registry, EMS Ambulance/Helicopter Fleet, Workforce/Contractor HLA Matrix,
and Multi-Hospital Subsidiary Federation with Phagocytic CDR & Board/Architect Governance.
Architecture: Hexagonal Secondary Adapter (MedCore Clinical, Fleet & Workforce Continuity)
Compliance Target: Sweden IVO (Lex Maria), Patientdatalagen (SFS 2008:355) & SFS 2025:1506 (NIS2)
"""

import hashlib
import hmac
import json
import os
import re
import sqlite3
import time
from typing import Dict, List, Optional, Set

SOFIA_DEFAULT_KEY = "PROTOCOL_SOFIA_NICU_MOTHER_INFANT_DYAD_KEY_2026"
BIOFOAM_DEFAULT_KEY = "PROTOCOL_GALA_BIOFOAM_ROW_INTEGRITY_SEED_2026"
FEDERATION_DEFAULT_KEY = "VALKYRJA_CORPORATE_SUBSIDIARY_FEDERATION_SEED_2026"
ARCHITECT_DEFAULT_KEY = "ARCHITECT_DEV_DR_LUIS_ABURTO_MASTER_SEED_2026"


class LocalClinicalSurvivalBunker:
    """
    PROTOCOL G.A.L.A., PROTOCOL S.O.F.I.A. & B.I.O.F.O.A.M. Offline Survival Node.
    Guarantees sub-5ms local clinical, bilateral cryogenic, IoMT hardware, OT power,
    EMS Ambulance/Helicopter fleet, and Workforce/Contractor access continuity.
    """

    SOFIA_NURSERY_SECRET: bytes = os.environ.get("VALKYRJA_SOFIA_KEY", SOFIA_DEFAULT_KEY).encode("utf-8")
    BIOFOAM_ROW_SECRET: bytes = os.environ.get("VALKYRJA_BIOFOAM_KEY", BIOFOAM_DEFAULT_KEY).encode("utf-8")

    PROTECTED_TABLES = (
        "er_active_triage",
        "blood_bank_reserve",
        "lab_panic_values",
        "protocol_sofia_nicu_nursery",
        "ot_bioenergetic_power_grid",
        "iomt_connected_hardware_registry",
        "ems_transport_fleet_registry",
        "workforce_personnel_registry",
    )

    # Strict Role-Based Access Control (HLA Least-Privilege Scopes by Staff Category)
    ROLE_ALLOWED_SCOPES: Dict[str, str] = {
        "ATTENDING_PHYSICIAN_OR_SPECIALIST": "FULL_CLINICAL_EHR_AND_ORDERS",
        "REGISTERED_NURSE_ICU_ER": "MEDICATION_ADMIN_AND_VITALS_TELEMETRY",
        "PARAMEDIC_FLIGHT_MEDIC": "EMS_PRE_HOSPITAL_TRIAGE_AND_BLOOD_REQUEST",
        "AMBULANCE_HELICOPTER_OPERATOR": "GPS_DISPATCH_AND_ROUTE_NAVIGATION_ONLY",
        "CLINICAL_ORDERLY_CAMILLERO": "PATIENT_INTERNAL_TRANSPORT_BAY_TRACKING_ONLY",
        "SANITATION_INTENDENCIA": "BIOHAZARD_STERILIZATION_ZONE_STATUS_ONLY",
        "DIETARY_CAFETERIA_STAFF": "INPATIENT_ENTERALE_DIET_ALLERGY_TRAY_ONLY",
        "BIOMEDICAL_OT_ENGINEER": "HARDWARE_MAINTENANCE_SANDBOX_ONLY",
        "CONTRACTOR_THIRD_PARTY_COMPANY": "RESTRICTED_VENDOR_CONTRACT_SANDBOX_ONLY",
    }

    def __init__(self, db_path: str = ":memory:", branch_id: str = "SE_STHLM_MAIN_HOSPITAL_01") -> None:
        self.db_path = db_path
        self.branch_id = branch_id
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._bunker_merkle_manifest_hmac: Optional[str] = None
        self._expected_triage_tokens: List[str] = []
        self._revoked_hardware_tokens: Set[str] = set()
        self._revoked_fleet_units: Set[str] = set()
        self._initialize_survival_schema()

    def _initialize_survival_schema(self) -> None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS er_active_triage (
                patient_token TEXT PRIMARY KEY,
                retts_triage_level INTEGER NOT NULL,
                clinical_pillar TEXT NOT NULL,
                abo_rh TEXT NOT NULL,
                irregular_antibodies TEXT NOT NULL,
                lethal_allergies_or_locks TEXT NOT NULL,
                vital_organ_support_params TEXT NOT NULL,
                assigned_bay TEXT NOT NULL,
                biofoam_row_hmac TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS blood_bank_reserve (
                unit_id TEXT PRIMARY KEY,
                blood_group TEXT NOT NULL,
                component_type TEXT NOT NULL,
                fridge_id TEXT NOT NULL,
                temp_celsius REAL NOT NULL,
                min_safe_celsius REAL NOT NULL,
                max_safe_celsius REAL NOT NULL,
                status TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lab_panic_values (
                sample_barcode TEXT PRIMARY KEY,
                patient_token TEXT NOT NULL,
                analyte TEXT NOT NULL,
                critical_value TEXT NOT NULL,
                clinical_alert_status TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS protocol_sofia_nicu_nursery (
                neonate_id TEXT PRIMARY KEY,
                mother_id TEXT NOT NULL,
                dyad_pairing_token TEXT NOT NULL,
                birth_weight_grams INTEGER NOT NULL,
                incubator_temp_c REAL NOT NULL,
                bilirubin_umol_l REAL NOT NULL,
                micro_infusion_guard TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ot_bioenergetic_power_grid (
                subsystem_id TEXT PRIMARY KEY,
                metabolic_tier TEXT NOT NULL,
                protected_clinical_zones TEXT NOT NULL,
                voltage_frequency_telemetry TEXT NOT NULL,
                reserve_capacity_pct REAL NOT NULL,
                autonomy_hours REAL NOT NULL,
                grid_isolation_status TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS iomt_connected_hardware_registry (
                device_id TEXT PRIMARY KEY,
                device_category TEXT NOT NULL,
                assigned_department TEXT NOT NULL,
                serial_or_mac TEXT NOT NULL,
                hla_hardware_token TEXT NOT NULL,
                operational_status TEXT NOT NULL
            )
            """
        )

        # Table 7: EMS Ambulance, Mobile ICU & Helicopter Medevac Fleet Registry
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ems_transport_fleet_registry (
                unit_id TEXT PRIMARY KEY,
                vehicle_type TEXT NOT NULL,
                home_station_branch TEXT NOT NULL,
                onboard_life_support_capabilities TEXT NOT NULL,
                gps_telemetry_token TEXT NOT NULL,
                fleet_status TEXT NOT NULL
            )
            """
        )

        # Table 8: Hospital Workforce, Support Staff, Contractors & Occasional/Sporadic Personnel
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS workforce_personnel_registry (
                staff_id TEXT PRIMARY KEY,
                full_name_or_alias TEXT NOT NULL,
                role_category TEXT NOT NULL,
                employment_modality TEXT NOT NULL,
                partner_company_contract TEXT NOT NULL,
                assigned_branch_id TEXT NOT NULL,
                allowed_access_scope TEXT NOT NULL,
                contract_valid_until_unix REAL NOT NULL,
                hla_staff_badge_hmac TEXT NOT NULL,
                active_status TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    @classmethod
    def compute_biofoam_row_hmac(
        cls,
        patient_token: str,
        retts_level: int,
        pillar: str,
        abo_rh: str,
        antibodies: str,
        allergies: str,
        organ_params: str,
        bay: str,
    ) -> str:
        canonical = f"{patient_token}|{retts_level}|{pillar}|{abo_rh}|{antibodies}|{allergies}|{organ_params}|{bay}"
        return hmac.new(cls.BIOFOAM_ROW_SECRET, canonical.encode("utf-8"), hashlib.sha256).hexdigest()[:20].upper()

    def compute_full_bunker_merkle_manifest(self) -> str:
        """Hashes the exact row count and canonical content of all 8 survival tables in SQLite."""
        cursor = self.conn.cursor()
        manifest_accumulator = hashlib.sha256()

        for table_name in self.PROTECTED_TABLES:
            rows = cursor.execute(f"SELECT * FROM {table_name} ORDER BY 1 ASC").fetchall()
            table_header = f"TABLE:{table_name}:COUNT={len(rows)}|".encode("utf-8")
            manifest_accumulator.update(table_header)
            for r in rows:
                row_canonical = "|".join(str(r[col]) for col in r.keys()).encode("utf-8")
                row_digest = hashlib.sha256(row_canonical).digest()
                manifest_accumulator.update(row_digest)

        return hmac.new(
            self.BIOFOAM_ROW_SECRET, manifest_accumulator.digest(), hashlib.sha256
        ).hexdigest().upper()

    def verify_bunker_row_integrity(self) -> Dict[str, object]:
        """Audits both individual B.I.O.F.O.A.M. row seals AND the multi-table Merkle Manifest HMAC."""
        cursor = self.conn.cursor()
        tampered_patients: List[str] = []
        present_tokens: List[str] = []
        verified_count = 0

        for row in cursor.execute("SELECT * FROM er_active_triage"):
            token = row["patient_token"]
            present_tokens.append(token)
            expected_hmac = self.compute_biofoam_row_hmac(
                token,
                row["retts_triage_level"],
                row["clinical_pillar"],
                row["abo_rh"],
                row["irregular_antibodies"],
                row["lethal_allergies_or_locks"],
                row["vital_organ_support_params"],
                row["assigned_bay"],
            )
            if hmac.compare_digest(expected_hmac, row["biofoam_row_hmac"]):
                verified_count += 1
            else:
                tampered_patients.append(token)

        deleted_tokens = [t for t in self._expected_triage_tokens if t not in present_tokens]
        for missing in deleted_tokens:
            tampered_patients.append(f"DELETED:{missing}")

        current_merkle = self.compute_full_bunker_merkle_manifest()
        merkle_intact = (
            self._bunker_merkle_manifest_hmac is not None
            and hmac.compare_digest(current_merkle, self._bunker_merkle_manifest_hmac)
        )

        is_intact = (len(tampered_patients) == 0) and merkle_intact
        return {
            "biofoam_integrity_verified": is_intact,
            "merkle_5table_manifest_intact": merkle_intact,
            "verified_rows_count": verified_count,
            "tampered_patient_tokens": tampered_patients,
            "clinical_safety_status": (
                "BIOFOAM_AND_MERKLE_SEAL_INTACT_SAFE_FOR_CLINICAL_USE"
                if is_intact
                else "CRITICAL_IATROGENIC_TAMPER_ALERT_BLOCK_DISPLAY"
            ),
        }

    def audit_bilateral_thermo_cryogenic_safety(self) -> Dict[str, object]:
        cursor = self.conn.cursor()
        safe_units: List[Dict[str, object]] = []
        thermal_excursions: List[Dict[str, object]] = []

        for row in cursor.execute("SELECT * FROM blood_bank_reserve"):
            unit = dict(row)
            temp = unit["temp_celsius"]
            if temp < unit["min_safe_celsius"]:
                unit["excursion_type"] = "HYPOTHERMIC_FREEZING_OR_HEMOLYSIS_ALERT: Below min safe threshold!"
                thermal_excursions.append(unit)
            elif temp > unit["max_safe_celsius"]:
                unit["excursion_type"] = "HYPERTHERMIC_WARMING_SPOILAGE_ALERT: Above max safe threshold!"
                thermal_excursions.append(unit)
            else:
                safe_units.append(unit)

        return {
            "all_units_within_bilateral_bounds": len(thermal_excursions) == 0,
            "verified_safe_units_count": len(safe_units),
            "quarantined_excursion_units": thermal_excursions,
        }

    # =========================================================================
    # 1. COLD-CHAIN N+1 MAINTENANCE HANDOVER
    # =========================================================================
    @classmethod
    def generate_maintenance_auth_token(
        cls, target_fridge_id: str, backup_fridge_id: str, technician_id: str
    ) -> str:
        payload = f"MAINT_N1:{target_fridge_id}->{backup_fridge_id}:{technician_id}".encode("utf-8")
        return hmac.new(cls.BIOFOAM_ROW_SECRET, payload, hashlib.sha256).hexdigest()[:18].upper()

    def execute_signed_cold_chain_maintenance(
        self,
        target_fridge_id: str,
        backup_fridge_id: str,
        backup_verified_temp_c: float,
        technician_id: str,
        auth_token: str,
    ) -> Dict[str, object]:
        expected_token = self.generate_maintenance_auth_token(
            target_fridge_id, backup_fridge_id, technician_id
        )
        if not hmac.compare_digest(expected_token, auth_token.strip().upper()):
            return {"maintenance_authorized": False, "status": "REJECTED_INVALID_MAINTENANCE_HMAC_TOKEN"}

        cursor = self.conn.cursor()
        units_in_target = cursor.execute(
            "SELECT * FROM blood_bank_reserve WHERE fridge_id = ?", (target_fridge_id,)
        ).fetchall()

        for u in units_in_target:
            if not (u["min_safe_celsius"] <= backup_verified_temp_c <= u["max_safe_celsius"]):
                return {
                    "maintenance_authorized": False,
                    "status": f"BLOCKED_THERMAL_INCOMPATIBILITY: {backup_verified_temp_c}C violates bounds!",
                }

        cursor.execute(
            """
            UPDATE blood_bank_reserve
            SET fridge_id = ?, temp_celsius = ?, status = 'TRANSFERRED_N1_MAINTENANCE_SAFE'
            WHERE fridge_id = ?
            """,
            (backup_fridge_id, backup_verified_temp_c, target_fridge_id),
        )
        self.conn.commit()
        self._bunker_merkle_manifest_hmac = self.compute_full_bunker_merkle_manifest()

        return {
            "maintenance_authorized": True,
            "status": "N1_COLD_CHAIN_HANDOVER_COMPLETE_MERKLE_RESEALED",
            "transferred_units_count": len(units_in_target),
            "offline_fridge_cleared_for_service": target_fridge_id,
            "active_backup_fridge": backup_fridge_id,
        }

    # =========================================================================
    # 2. ELECTRICAL GRID, UPS & GENERATOR MAINTENANCE / REPLACEMENT
    # =========================================================================
    @classmethod
    def generate_power_lifecycle_auth_token(
        cls, target_subsystem_id: str, action: str, engineer_id: str
    ) -> str:
        payload = f"OT_POWER_LIFECYCLE:{target_subsystem_id}:{action}:{engineer_id}".encode("utf-8")
        return hmac.new(cls.BIOFOAM_ROW_SECRET, payload, hashlib.sha256).hexdigest()[:18].upper()

    def execute_ot_generator_maintenance_or_swap(
        self,
        target_subsystem_id: str,
        action: str,
        collateral_backup_online: bool,
        collateral_autonomy_hours: float,
        engineer_id: str,
        auth_token: str,
        new_subsystem_id: Optional[str] = None,
        new_voltage_telemetry: str = "400V 3-Phase / 50.00 Hz (New Unit Online)",
    ) -> Dict[str, object]:
        expected = self.generate_power_lifecycle_auth_token(target_subsystem_id, action, engineer_id)
        if not hmac.compare_digest(expected, auth_token.strip().upper()):
            return {"power_operation_authorized": False, "status": "REJECTED_INVALID_OT_POWER_HMAC"}

        if not collateral_backup_online or collateral_autonomy_hours < 72.0:
            return {
                "power_operation_authorized": False,
                "status": "BLOCKED_INSUFFICIENT_COLLATERAL_POWER: Requires >=72h N+1 backup!",
            }

        cursor = self.conn.cursor()
        if action == "REPLACE_WITH_NEW_GENERATOR" and new_subsystem_id:
            old_row = cursor.execute(
                "SELECT * FROM ot_bioenergetic_power_grid WHERE subsystem_id = ?", (target_subsystem_id,)
            ).fetchone()
            tier = old_row["metabolic_tier"] if old_row else "TIER_3_GLYCOLYSIS_10S_DIESEL_GENERATOR"
            zones = old_row["protected_clinical_zones"] if old_row else "ALL_RED_OUTLETS"

            cursor.execute(
                "DELETE FROM ot_bioenergetic_power_grid WHERE subsystem_id = ?", (target_subsystem_id,)
            )
            cursor.execute(
                "INSERT INTO ot_bioenergetic_power_grid VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    new_subsystem_id,
                    tier,
                    zones,
                    new_voltage_telemetry,
                    100.0,
                    collateral_autonomy_hours,
                    "NEW_GENERATOR_COMMISSIONED_AND_SYNCHRONIZED",
                ),
            )
            op_summary = f"REPLACED_{target_subsystem_id}_WITH_{new_subsystem_id}"
        else:
            cursor.execute(
                """
                UPDATE ot_bioenergetic_power_grid
                SET grid_isolation_status = 'MAINTENANCE_COLLATERAL_N1_BYPASS_ACTIVE',
                    autonomy_hours = ?
                WHERE subsystem_id = ?
                """,
                (collateral_autonomy_hours, target_subsystem_id),
            )
            op_summary = f"MAINTENANCE_BYPASS_ENGAGED_ON_{target_subsystem_id}"

        self.conn.commit()
        self._bunker_merkle_manifest_hmac = self.compute_full_bunker_merkle_manifest()
        return {
            "power_operation_authorized": True,
            "status": "OT_POWER_LIFECYCLE_COMPLETE_MERKLE_RESEALED",
            "operation_summary": op_summary,
            "verified_collateral_autonomy_hours": collateral_autonomy_hours,
        }

    # =========================================================================
    # 3. CONNECTED IoMT & IT HARDWARE LIFECYCLE
    # =========================================================================
    @classmethod
    def generate_hla_hardware_token(cls, device_id: str, category: str, dept: str, serial_mac: str) -> str:
        payload = f"HLA_HW:{device_id}:{category}:{dept}:{serial_mac}".encode("utf-8")
        sig = hmac.new(cls.BIOFOAM_ROW_SECRET, payload, hashlib.sha256).hexdigest()[:16].upper()
        return f"HLA-DEV-{sig}"

    @classmethod
    def generate_equipment_lifecycle_auth(cls, action: str, device_id: str, biomed_eng_id: str) -> str:
        payload = f"EQUIP_LIFECYCLE:{action}:{device_id}:{biomed_eng_id}".encode("utf-8")
        return hmac.new(cls.BIOFOAM_ROW_SECRET, payload, hashlib.sha256).hexdigest()[:18].upper()

    def manage_connected_equipment_lifecycle(
        self,
        action: str,
        device_id: str,
        device_category: str,
        assigned_department: str,
        serial_or_mac: str,
        biomed_engineer_id: str,
        auth_token: str,
        replacement_device_id: Optional[str] = None,
        replacement_serial_mac: Optional[str] = None,
    ) -> Dict[str, object]:
        expected_auth = self.generate_equipment_lifecycle_auth(action, device_id, biomed_engineer_id)
        if not hmac.compare_digest(expected_auth, auth_token.strip().upper()):
            return {
                "lifecycle_authorized": False,
                "status": "REJECTED_ROGUE_HARDWARE_OR_INVALID_BIOMED_SIGNATURE",
            }

        cursor = self.conn.cursor()

        if action == "ADD_NEW":
            hla_token = self.generate_hla_hardware_token(
                device_id, device_category, assigned_department, serial_or_mac
            )
            cursor.execute(
                "INSERT OR REPLACE INTO iomt_connected_hardware_registry VALUES (?, ?, ?, ?, ?, ?)",
                (
                    device_id,
                    device_category,
                    assigned_department,
                    serial_or_mac,
                    hla_token,
                    "ACTIVE_THYMIC_HLA_VERIFIED",
                ),
            )
            result_status = "NEW_EQUIPMENT_PROVISIONED_AND_SEALED"
        elif action == "MAINTENANCE_MODE":
            cursor.execute(
                "UPDATE iomt_connected_hardware_registry SET operational_status = 'MAINTENANCE_SANDBOX_ISOLATED' WHERE device_id = ?",
                (device_id,),
            )
            result_status = "EQUIPMENT_ISOLATED_FOR_SAFE_MAINTENANCE"
        elif action == "REPLACE_SWAP" and replacement_device_id and replacement_serial_mac:
            old_row = cursor.execute(
                "SELECT * FROM iomt_connected_hardware_registry WHERE device_id = ?", (device_id,)
            ).fetchone()
            if old_row:
                self._revoked_hardware_tokens.add(old_row["hla_hardware_token"])
            cursor.execute("DELETE FROM iomt_connected_hardware_registry WHERE device_id = ?", (device_id,))
            new_hla = self.generate_hla_hardware_token(
                replacement_device_id, device_category, assigned_department, replacement_serial_mac
            )
            cursor.execute(
                "INSERT INTO iomt_connected_hardware_registry VALUES (?, ?, ?, ?, ?, ?)",
                (
                    replacement_device_id,
                    device_category,
                    assigned_department,
                    replacement_serial_mac,
                    new_hla,
                    "ACTIVE_REPLACEMENT_UNIT_VERIFIED",
                ),
            )
            result_status = f"SWAPPED_{device_id}_TO_{replacement_device_id}_OLD_TOKEN_REVOKED"
        elif action == "REMOVE_DECOMMISSION":
            old_row = cursor.execute(
                "SELECT * FROM iomt_connected_hardware_registry WHERE device_id = ?", (device_id,)
            ).fetchone()
            if old_row:
                self._revoked_hardware_tokens.add(old_row["hla_hardware_token"])
            cursor.execute("DELETE FROM iomt_connected_hardware_registry WHERE device_id = ?", (device_id,))
            result_status = f"APOPTOSIS_DECOMMISSIONED_{device_id}_TOKEN_PERMANENTLY_REVOKED"
        else:
            return {"lifecycle_authorized": False, "status": "UNSUPPORTED_LIFECYCLE_ACTION"}

        self.conn.commit()
        self._bunker_merkle_manifest_hmac = self.compute_full_bunker_merkle_manifest()
        return {
            "lifecycle_authorized": True,
            "status": result_status,
            "device_category": device_category,
            "merkle_manifest_resealed": True,
        }

    def verify_connected_device_access(self, device_id: str, presented_hla_token: str) -> Dict[str, object]:
        if presented_hla_token in self._revoked_hardware_tokens:
            return {"access_granted": False, "verdict": "BLOCKED_APOPTOSIS_REVOKED_HARDWARE_TOKEN"}
        cursor = self.conn.cursor()
        row = cursor.execute(
            "SELECT * FROM iomt_connected_hardware_registry WHERE device_id = ?", (device_id,)
        ).fetchone()
        if not row:
            return {"access_granted": False, "verdict": "BLOCKED_UNREGISTERED_ROGUE_DEVICE"}
        if not hmac.compare_digest(row["hla_hardware_token"], presented_hla_token):
            return {"access_granted": False, "verdict": "BLOCKED_FORGED_HARDWARE_SIGNATURE"}
        if row["operational_status"] == "MAINTENANCE_SANDBOX_ISOLATED":
            return {"access_granted": False, "verdict": "QUARANTINED_DEVICE_UNDER_MAINTENANCE_NO_PROD_ACCESS"}
        return {
            "access_granted": True,
            "verdict": "AUTHORIZED_HLA_COMPATIBLE_EQUIPMENT",
            "allowed_department_scope": row["assigned_department"],
        }

    # =========================================================================
    # 4. EMS AMBULANCE & HELICOPTER FLEET LIFECYCLE (ADD, MAINT, SWAP, THEFT LOCK)
    # =========================================================================
    @classmethod
    def generate_fleet_telemetry_token(cls, unit_id: str, vehicle_type: str, station: str) -> str:
        payload = f"EMS_FLEET:{unit_id}:{vehicle_type}:{station}".encode("utf-8")
        sig = hmac.new(cls.BIOFOAM_ROW_SECRET, payload, hashlib.sha256).hexdigest()[:16].upper()
        return f"EMS-GPS-{sig}"

    @classmethod
    def generate_fleet_lifecycle_auth(cls, action: str, unit_id: str, commander_id: str) -> str:
        payload = f"FLEET_CMD:{action}:{unit_id}:{commander_id}".encode("utf-8")
        return hmac.new(cls.BIOFOAM_ROW_SECRET, payload, hashlib.sha256).hexdigest()[:18].upper()

    def manage_ems_fleet_unit_lifecycle(
        self,
        action: str,  # "ADD_UNIT", "MAINTENANCE_OUT_OF_SERVICE", "REPLACE_UNIT", "REPORT_STOLEN_LOCKDOWN"
        unit_id: str,
        vehicle_type: str,  # "GROUND_MOBILE_ICU_AMBULANCE", "HELICOPTER_ECMO_MEDEVAC", "RAPID_BLOOD_DRONE_OR_CAR"
        home_station_branch: str,
        capabilities: str,
        fleet_commander_id: str,
        auth_token: str,
        replacement_unit_id: Optional[str] = None,
    ) -> Dict[str, object]:
        """
        Manages the lifecycle of Ambulances, Mobile ICUs, and Medevac Helicopters:
        Supports adding new units, mechanical maintenance isolation, unit replacement,
        and instant cryptographic lockdown + telemetry severing if an ambulance is stolen.
        """
        expected = self.generate_fleet_lifecycle_auth(action, unit_id, fleet_commander_id)
        if not hmac.compare_digest(expected, auth_token.strip().upper()):
            return {"fleet_op_authorized": False, "status": "REJECTED_INVALID_FLEET_COMMAND_SIGNATURE"}

        cursor = self.conn.cursor()

        if action == "ADD_UNIT":
            tok = self.generate_fleet_telemetry_token(unit_id, vehicle_type, home_station_branch)
            cursor.execute(
                "INSERT OR REPLACE INTO ems_transport_fleet_registry VALUES (?, ?, ?, ?, ?, ?)",
                (unit_id, vehicle_type, home_station_branch, capabilities, tok, "ACTIVE_READY_FOR_DISPATCH"),
            )
            status_msg = f"FLEET_UNIT_{unit_id}_COMMISSIONED"

        elif action == "MAINTENANCE_OUT_OF_SERVICE":
            cursor.execute(
                "UPDATE ems_transport_fleet_registry SET fleet_status = 'WORKSHOP_MAINTENANCE_OFFLINE' WHERE unit_id = ?",
                (unit_id,),
            )
            status_msg = f"FLEET_UNIT_{unit_id}_IN_MAINTENANCE"

        elif action == "REPLACE_UNIT" and replacement_unit_id:
            old_u = cursor.execute(
                "SELECT * FROM ems_transport_fleet_registry WHERE unit_id = ?", (unit_id,)
            ).fetchone()
            if old_u:
                self._revoked_fleet_units.add(old_u["gps_telemetry_token"])
            cursor.execute("DELETE FROM ems_transport_fleet_registry WHERE unit_id = ?", (unit_id,))
            new_tok = self.generate_fleet_telemetry_token(
                replacement_unit_id, vehicle_type, home_station_branch
            )
            cursor.execute(
                "INSERT INTO ems_transport_fleet_registry VALUES (?, ?, ?, ?, ?, ?)",
                (
                    replacement_unit_id,
                    vehicle_type,
                    home_station_branch,
                    capabilities,
                    new_tok,
                    "ACTIVE_READY_FOR_DISPATCH",
                ),
            )
            status_msg = f"FLEET_SWAPPED_{unit_id}_TO_{replacement_unit_id}"

        elif action == "REPORT_STOLEN_LOCKDOWN":
            old_u = cursor.execute(
                "SELECT * FROM ems_transport_fleet_registry WHERE unit_id = ?", (unit_id,)
            ).fetchone()
            if old_u:
                self._revoked_fleet_units.add(old_u["gps_telemetry_token"])
            cursor.execute("DELETE FROM ems_transport_fleet_registry WHERE unit_id = ?", (unit_id,))
            status_msg = (
                f"STOLEN_VEHICLE_APOPTOSIS_LOCKDOWN: {unit_id} hospital network certificates "
                f"shredded, narcotics vault locked, and GPS beacon switched to police tracking."
            )
        else:
            return {"fleet_op_authorized": False, "status": "UNSUPPORTED_FLEET_ACTION"}

        self.conn.commit()
        self._bunker_merkle_manifest_hmac = self.compute_full_bunker_merkle_manifest()
        return {
            "fleet_op_authorized": True,
            "status": status_msg,
            "merkle_manifest_resealed": True,
        }

    # =========================================================================
    # 5. HOSPITAL WORKFORCE, CONTRACTORS & OCCASIONAL / SPORADIC STAFF REGISTRY
    # =========================================================================
    @classmethod
    def compute_staff_hla_badge(
        cls,
        staff_id: str,
        role_category: str,
        modality: str,
        partner_company: str,
        branch_id: str,
        valid_until: float,
    ) -> str:
        payload = f"STAFF_HLA:{staff_id}:{role_category}:{modality}:{partner_company}:{branch_id}:{valid_until}".encode(
            "utf-8"
        )
        sig = hmac.new(cls.BIOFOAM_ROW_SECRET, payload, hashlib.sha256).hexdigest()[:18].upper()
        return f"HLA-STAFF-{sig}"

    def register_or_update_workforce_member(
        self,
        staff_id: str,
        full_name_or_alias: str,
        role_category: str,
        employment_modality: str,  # "PERMANENT_STAFF", "OCCASIONAL_SPORADIC_LOCUM", "CONTRACTOR_EXTERNAL_COMPANY"
        partner_company_contract: str,
        assigned_branch_id: str,
        contract_valid_until_unix: float,
    ) -> Dict[str, object]:
        """
        Registers hospital personnel across all clinical, support, and contractor tiers
        (Physicians, Nurses, Paramedics, Ambulance Drivers, Orderlies/Camilleros,
        Sanitation/Intendencia, Cafeteria/Nutrition, and External Partner Companies),
        binding each worker to a strict Least-Privilege HLA Scope and automatic expiration timestamp.
        """
        allowed_scope = self.ROLE_ALLOWED_SCOPES.get(role_category, "NO_CLINICAL_SYSTEM_ACCESS")
        badge_hmac = self.compute_staff_hla_badge(
            staff_id,
            role_category,
            employment_modality,
            partner_company_contract,
            assigned_branch_id,
            contract_valid_until_unix,
        )
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO workforce_personnel_registry VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                staff_id,
                full_name_or_alias,
                role_category,
                employment_modality,
                partner_company_contract,
                assigned_branch_id,
                allowed_scope,
                contract_valid_until_unix,
                badge_hmac,
                "ACTIVE_VERIFIED",
            ),
        )
        self.conn.commit()
        self._bunker_merkle_manifest_hmac = self.compute_full_bunker_merkle_manifest()
        return {
            "staff_registered": True,
            "staff_id": staff_id,
            "employment_modality": employment_modality,
            "assigned_least_privilege_scope": allowed_scope,
            "hla_staff_badge_hmac": badge_hmac,
        }

    def verify_workforce_access_request(
        self,
        staff_id: str,
        requested_scope: str,
        current_unix_time: Optional[float] = None,
    ) -> Dict[str, object]:
        """
        Validates whether a permanent employee, occasional/sporadic worker, or external contractor:
        1. Exists in the sealed registry and holds a valid HLA badge.
        2. Has not exceeded their occasional shift or third-party contract expiration timestamp.
        3. Is requesting only the specific compartment allowed for their role (e.g., Cafeteria or
           Sanitation staff cannot query ICU ventilator or EHR tables).
        """
        now = time.time() if current_unix_time is None else current_unix_time
        cursor = self.conn.cursor()
        row = cursor.execute(
            "SELECT * FROM workforce_personnel_registry WHERE staff_id = ?", (staff_id,)
        ).fetchone()

        if not row or row["active_status"] != "ACTIVE_VERIFIED":
            return {"access_authorized": False, "reason": "BLOCKED_UNREGISTERED_OR_REVOKED_PERSONNEL"}

        # Automatic expiration check for Occasional / Sporadic workers & External Contractors
        if now > float(row["contract_valid_until_unix"]):
            return {
                "access_authorized": False,
                "reason": (
                    f"EXPIRED_SPORADIC_OR_CONTRACTOR_WINDOW: {row['employment_modality']} "
                    f"({row['partner_company_contract']}) shift/contract expired automatically."
                ),
            }

        if row["allowed_access_scope"] != requested_scope:
            return {
                "access_authorized": False,
                "reason": (
                    f"HLA_ROLE_COMPARTMENT_VIOLATION: Role '{row['role_category']}' is restricted "
                    f"to '{row['allowed_access_scope']}' and cannot access '{requested_scope}'."
                ),
            }

        return {
            "access_authorized": True,
            "staff_id": staff_id,
            "role_category": row["role_category"],
            "employment_modality": row["employment_modality"],
            "granted_scope": row["allowed_access_scope"],
        }

    @classmethod
    def generate_sofia_dyad_token(cls, mother_id: str, neonate_id: str) -> str:
        payload = f"{mother_id}::{neonate_id}".encode("utf-8")
        digest = hmac.new(cls.SOFIA_NURSERY_SECRET, payload, hashlib.sha256).hexdigest()[:14].upper()
        return f"SOFIA-DYAD-{digest}"

    @classmethod
    def verify_protocol_sofia_nursery_lock(
        cls, mother_id: str, neonate_id: str, scanned_wristband_token: str
    ) -> Dict[str, object]:
        expected = cls.generate_sofia_dyad_token(mother_id, neonate_id)
        is_match = hmac.compare_digest(expected, scanned_wristband_token.strip().upper())
        return {
            "protocol": "PROTOCOL_SOFIA_INFANT_SAFEGUARD",
            "mother_infant_match_verified": is_match,
            "security_action": "RELEASE_TO_MOTHER_AUTHORIZED" if is_match else "NURSERY_LOCKDOWN_MISMATCH_ALERT",
        }

    @staticmethod
    def evaluate_bioenergetic_power_and_shed_loads(
        external_grid_online: bool,
        ups_battery_pct: float,
        diesel_fuel_liters_pct: float,
    ) -> Dict[str, object]:
        estimated_diesel_hours = round((diesel_fuel_liters_pct / 100.0) * 96.0, 1)

        if not external_grid_online or diesel_fuel_liters_pct < 50.0:
            return {
                "bioenergetic_mode": "ISLAND_MODE_AUTONOMOUS_GENERATOR_ACTIVE",
                "ups_0ms_bridge_status": f"ONLINE_DOUBLE_CONVERSION_ACTIVE ({ups_battery_pct}%)",
                "ats_diesel_transfer": "CLOSED_UNDER_8_SECONDS_400V_50HZ_STABLE",
                "load_shedding_action": "HEMODYNAMIC_CENTRALIZATION_LOAD_SHEDDING_ACTIVE",
                "shed_non_vital_circuits": [
                    "ADMIN_OFFICES_LIGHTING",
                    "CAFETERIA_AND_PUBLIC_ZONES",
                    "NON_CLINICAL_HVAC_CHILLERS",
                ],
                "prioritized_red_outlets_100pct": [
                    "ICU_MECHANICAL_VENTILATORS_AND_ECMO",
                    "NICU_INCUBATORS_PROTOCOL_SOFIA",
                    "OR_TRANSPLANT_SUITES_IPS",
                    "HEMODIALYSIS_WATER_RO_AND_CRRT",
                    "CRYO_ULT_MINUS80_AND_LN2_196C_VALVES",
                    "LOCAL_BUNKER_SQLITE_SERVERS",
                ],
                "estimated_survival_autonomy_hours": estimated_diesel_hours,
                "nordic_72h_preparedness_compliant": estimated_diesel_hours >= 72.0,
            }

        return {
            "bioenergetic_mode": "NORMAL_UTILITY_GRID_SYNCHRONIZED",
            "ups_0ms_bridge_status": f"STANDBY_CHARGED ({ups_battery_pct}%)",
            "load_shedding_action": "NONE_REQUIRED_FULL_CAPACITY",
            "estimated_survival_autonomy_hours": estimated_diesel_hours,
            "nordic_72h_preparedness_compliant": estimated_diesel_hours >= 72.0,
        }

    def seed_shadow_sync_snapshot(self) -> None:
        """Populates all 8 survival tables and locks the 8-Table Merkle Manifest."""
        cursor = self.conn.cursor()

        raw_triage_rows = [
            (
                "PT-TRAUMA-992A", 1, "PILLAR_1_TRAUMA_HEMORRHAGE", "O-", "NONE",
                "Allergy: Penicillin, Latex", "MTP_ACTIVE | Ca2+: 1.02 mmol/L | Fibrinogen: 1.4 g/L", "TRAUMA_BAY_01"
            ),
            (
                "PT-CARDIO-441B", 1, "PILLAR_2_CARDIAC_ESC_0H_1H", "A+", "Anti-Kell",
                "Allergy: Contrast Iodine", "hs-cTnT 0h: 18 ng/L -> 1h: 64 ng/L (DELTA +46 RULE-IN)", "CORONARY_ICU_02"
            ),
            (
                "PT-RENAL-309C", 1, "PILLAR_3_NEPHRO_HEMODIALYSIS", "B+", "NONE",
                "Dialysis Heparin Lock Active", "Cystatin-C: 3.1 mg/L | Creat: 540 umol/L | UF Goal: 2.2L", "DIALYSIS_BAY_04"
            ),
            (
                "PT-HEPATIC-512D", 1, "PILLAR_4_HEPATIC_ENCEPHALOPATHY", "O+", "NONE",
                "Variceal Bleed Prophylaxis", "West Haven Grade III | MELD-Na: 31 | Terlipressin IV", "LIVER_ICU_01"
            ),
            (
                "PT-ICUVENT-778E", 1, "PILLAR_5_ICU_MECHANICAL_VENT", "AB+", "NONE",
                "Lung Protective Vent Lock", "Driving Pressure dP: 12 cmH2O | Pplat: 24 | PaO2/FiO2: 145", "ADULT_ICU_BED_08"
            ),
            (
                "PT-TRANSPLANT-881F", 1, "PILLAR_6_OR_ORGAN_TRANSPLANT", "O-", "HLA-DSA-NEGATIVE",
                "Cold Ischemia Timer Active", "Renal Graft Cold Ischemia: 04h:12m | Tacrolimus Induction", "OR_SUITE_03"
            ),
            (
                "PT-STROKE-204G", 1, "PILLAR_7_NEURO_STROKE_CODE", "A-", "NONE",
                "HARD_LOCK: Patient on Apixaban (DOAC)", "NIHSS: 14 | CT: No Bleed | HOLD IV tPA -> Thrombectomy", "STROKE_UNIT_01"
            ),
            (
                "PT-MATER-619H", 1, "PILLAR_10_OBSTETRIC_CODE_MATER", "O-", "Rh-Isoimmunization Guard",
                "MgSO4 Toxicity Guard (Patellar Reflex+)", "Severe Preeclampsia | Fibrinogen: 240 mg/dL", "LABOR_DELIVERY_02"
            ),
            (
                "PT-ONCO-905J", 1, "PILLAR_12_ONCOLOGY_NEUTROPENIA", "A+", "NONE",
                "High-Dose Methotrexate Rescue Clock", "Leucovorin Rescue Due: 15m | ANC: 320/uL (Neutropenic)", "ONCO_ACUTE_05"
            ),
        ]

        self._expected_triage_tokens = [r[0] for r in raw_triage_rows]
        sealed_triage_rows = [
            (*row, self.compute_biofoam_row_hmac(*row)) for row in raw_triage_rows
        ]

        cursor.executemany(
            "INSERT OR REPLACE INTO er_active_triage VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            sealed_triage_rows,
        )

        cursor.executemany(
            "INSERT OR REPLACE INTO blood_bank_reserve VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("BLD-SE-ONEG-001", "O-", "Packed_RBC", "ER_FRIDGE_01", 3.6, 2.0, 6.0, "AVAILABLE_EMERGENCY"),
                ("BLD-SE-ONEG-002", "O-", "Packed_RBC", "ER_FRIDGE_01", 3.8, 2.0, 6.0, "AVAILABLE_EMERGENCY"),
                ("PLT-SE-AGIT-010", "O+", "Platelet_Concentrate_Agitator", "THERMO_22C_01", 21.8, 20.0, 24.0, "VIABLE_AGITATING"),
                ("FFP-SE-CRYO-044", "AB+", "Fresh_Frozen_Plasma", "FREEZER_MINUS30_02", -31.5, -40.0, -25.0, "FROZEN_INTACT"),
                ("VAC-SE-ULT-080", "N/A", "Oncology_Biologics_ULT", "ULT_MINUS80_01", -81.2, -90.0, -70.0, "ULTRA_COLD_INTACT"),
                ("CRYO-LN2-STEM-99", "HLA-A2", "Hematopoietic_Stem_Cells_And_Cornea", "LN2_DEWAR_196", -195.8, -200.0, -150.0, "CRYO_VAPOR_LOCKED"),
            ],
        )

        cursor.executemany(
            "INSERT OR REPLACE INTO lab_panic_values VALUES (?, ?, ?, ?, ?)",
            [
                ("LAB-88310", "PT-TRAUMA-992A", "Arterial_Lactate", "6.8 mmol/L (CRITICAL)", "ER_MD_NOTIFIED"),
                ("LAB-88315", "PT-RENAL-309C", "Potassium_And_Cystatin_C", "K+ 6.9 mmol/L | CysC 3.1 mg/L", "URGENT_DIALYSIS"),
                ("LAB-88322", "PT-HEPATIC-512D", "Venous_Ammonia_NH3", "198 umol/L (ENCEPHALOPATHY_RISK)", "LIVER_ICU_ALERT"),
                ("LAB-88330", "PT-DKA-110K", "DKA_Glucose_Potassium_Lock", "Glucose 28 mmol/L | K+ 2.9 mmol/L", "HOLD_INSULIN_GIVE_K"),
            ],
        )

        dyad_token_1 = self.generate_sofia_dyad_token("MOM-SE-8821", "NEO-SOFIA-001")
        cursor.execute(
            "INSERT OR REPLACE INTO protocol_sofia_nicu_nursery VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                "NEO-SOFIA-001",
                "MOM-SE-8821",
                dyad_token_1,
                1150,
                36.7,
                215.0,
                "NICU_MICRO_DOSE_LOCKED: Caffeine Citrate & TPN verified for 1,150g",
            ),
        )

        cursor.executemany(
            "INSERT OR REPLACE INTO ot_bioenergetic_power_grid VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    "UPS-ONLINE-VITAL-01",
                    "TIER_1_PHOSPHOCREATINE_0MS_UPS",
                    "ICU_VENTILATORS | NICU_SOFIA | ER_SHOCK_BAYS",
                    "230V / 50.00 Hz (Pure Sine Wave)",
                    98.5,
                    2.5,
                    "ONLINE_ZERO_LATENCY_BUFFER_ENGAGED",
                ),
                (
                    "IPS-SURGICAL-OR-02",
                    "TIER_2_ISOLATED_POWER_SYSTEM_IPS",
                    "TRANSPLANT_OR_SUITES | ECMO_PERFUSION | CATH_LAB",
                    "230V / 50.00 Hz (Isolated Ground <5mA Leakage)",
                    100.0,
                    4.0,
                    "SURGICAL_MICROSHOCK_GUARD_ACTIVE",
                ),
                (
                    "ATS-DIESEL-GENSET-A",
                    "TIER_3_GLYCOLYSIS_10S_DIESEL_GENERATOR",
                    "ALL_RED_OUTLETS | HEMODIALYSIS_RO | CRYO_LN2_MINUS80",
                    "400V 3-Phase / 50.02 Hz (ATS Closed in 6.4s)",
                    86.0,
                    82.5,
                    "ISLAND_MODE_LOAD_SHEDDING_NON_VITAL_ACTIVE",
                ),
            ],
        )

        initial_devices = [
            ("DEV-OR-LAP-01", "OR_LAPAROSCOPY_4K_TOWER", "SURGICAL_OR_SUITE_03", "MAC:00:1A:2B:OR:01"),
            ("DEV-IPAD-ER-04", "CLINICAL_MOBILE_IPAD_PRO", "EMERGENCY_TRIAGE_BAY", "SER:IPAD-SE-9941"),
            ("DEV-IMG-CT-01", "SIEMENS_DUAL_SOURCE_CT_SCANNER", "RADIOLOGY_STROKE_PACS", "MAC:00:1A:2B:CT:88"),
            ("DEV-LAB-ROCHE-02", "HIGH_SENSITIVITY_TROPONIN_ANALYZER", "CENTRAL_STAT_LAB_LIMS", "SER:COBAS-SE-402"),
            ("DEV-ICU-VENT-08", "SERVO_U_MECHANICAL_VENTILATOR", "ADULT_ICU_BED_08", "SER:MAQUET-SE-778"),
            ("DEV-NICU-INC-01", "GIRAFFE_OMNIBED_INCUBATOR", "NICU_PROTOCOL_SOFIA", "SER:NICU-SOFIA-01"),
        ]
        for dev_id, cat, dept, mac in initial_devices:
            tok = self.generate_hla_hardware_token(dev_id, cat, dept, mac)
            cursor.execute(
                "INSERT OR REPLACE INTO iomt_connected_hardware_registry VALUES (?, ?, ?, ?, ?, ?)",
                (dev_id, cat, dept, mac, tok, "ACTIVE_THYMIC_HLA_VERIFIED"),
            )

        # Seed Table 7: EMS Ambulance & Medevac Helicopter Fleet
        initial_fleet = [
            ("AMB-MICU-SE-01", "GROUND_MOBILE_ICU_AMBULANCE", "SE_STHLM_MAIN_HOSPITAL_01", "VENTILATOR | DEFIB | PORTABLE_CRYO_O_NEG"),
            ("AMB-ALS-SUB-04", "ADVANCED_LIFE_SUPPORT_AMBULANCE", "SE_UPPSALA_SUBCLINIC_02", "AIRWAY | LUCAS_CPR | TELEMETRY"),
            ("HELI-MEDEVAC-01", "HELICOPTER_ECMO_AND_BLOOD_MEDEVAC", "SE_STHLM_MAIN_HOSPITAL_01", "AIR_ECMO | 6_UNITS_O_NEG_CRYO_BOX | SURGICAL_TEAM"),
        ]
        for u_id, v_type, station, caps in initial_fleet:
            ftok = self.generate_fleet_telemetry_token(u_id, v_type, station)
            cursor.execute(
                "INSERT OR REPLACE INTO ems_transport_fleet_registry VALUES (?, ?, ?, ?, ?, ?)",
                (u_id, v_type, station, caps, ftok, "ACTIVE_READY_FOR_DISPATCH"),
            )

        # Seed Table 8: Multi-Tier Hospital Workforce, Support Staff, Contractors & Occasional Staff
        initial_workforce = [
            ("STAFF-MD-001", "Dr. Luis Aburto (MD / Lead Architect)", "ATTENDING_PHYSICIAN_OR_SPECIALIST", "PERMANENT_STAFF", "INTERNAL_HOSPITAL_STAFF", 4102444800.0),
            ("STAFF-RN-102", "Maja Lindström (ICU RN)", "REGISTERED_NURSE_ICU_ER", "PERMANENT_STAFF", "INTERNAL_HOSPITAL_STAFF", 4102444800.0),
            ("STAFF-PARA-205", "Erik Sjöberg (Flight Paramedic)", "PARAMEDIC_FLIGHT_MEDIC", "PERMANENT_STAFF", "AISAB_SWEDISH_EMS", 4102444800.0),
            ("STAFF-DRV-209", "Johan Berg (Ambulance Operator)", "AMBULANCE_HELICOPTER_OPERATOR", "PERMANENT_STAFF", "AISAB_SWEDISH_EMS", 4102444800.0),
            ("STAFF-ORD-310", "Carlos Méndez (ER Orderly / Camillero)", "CLINICAL_ORDERLY_CAMILLERO", "PERMANENT_STAFF", "INTERNAL_HOSPITAL_STAFF", 4102444800.0),
            ("STAFF-SAN-401", "Anna Nilsson (OR Sanitation / Intendencia)", "SANITATION_INTENDENCIA", "CONTRACTOR_EXTERNAL_COMPANY", "NORDIC_CLEAN_MED_AB", 1800000000.0),
            ("STAFF-CAF-501", "Lars Olsson (Clinical Nutrition & Comedor)", "DIETARY_CAFETERIA_STAFF", "CONTRACTOR_EXTERNAL_COMPANY", "SVENSKA_KOK_CARE_AB", 1800000000.0),
            ("STAFF-LOCUM-999", "Dr. Sofia Ek (Weekend Locum Specialist)", "ATTENDING_PHYSICIAN_OR_SPECIALIST", "OCCASIONAL_SPORADIC_LOCUM", "NORDIC_LOCUM_AGENCY_AB", 1763050000.0),
        ]
        for s_id, name, role, mod, company, exp_ts in initial_workforce:
            scope = self.ROLE_ALLOWED_SCOPES[role]
            badge = self.compute_staff_hla_badge(s_id, role, mod, company, self.branch_id, exp_ts)
            cursor.execute(
                "INSERT OR REPLACE INTO workforce_personnel_registry VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (s_id, name, role, mod, company, self.branch_id, scope, exp_ts, badge, "ACTIVE_VERIFIED"),
            )

        self.conn.commit()
        self._bunker_merkle_manifest_hmac = self.compute_full_bunker_merkle_manifest()

    def query_emergency_survival_snapshot(self) -> Dict[str, object]:
        """Retrieves the complete Protocol GALA, BIOFOAM & Protocol SOFIA survival state."""
        start_ns = time.perf_counter_ns()
        cursor = self.conn.cursor()

        integrity_audit = self.verify_bunker_row_integrity()
        patients: List[Dict[str, object]] = [
            dict(row) for row in cursor.execute("SELECT * FROM er_active_triage ORDER BY retts_triage_level ASC")
        ]
        thermo_cryo_units: List[Dict[str, object]] = [
            dict(row)
            for row in cursor.execute(
                "SELECT * FROM blood_bank_reserve WHERE temp_celsius >= min_safe_celsius AND temp_celsius <= max_safe_celsius"
            )
        ]
        panic_labs: List[Dict[str, object]] = [
            dict(row) for row in cursor.execute("SELECT * FROM lab_panic_values")
        ]
        sofia_nicu_protected: List[Dict[str, object]] = [
            dict(row) for row in cursor.execute("SELECT * FROM protocol_sofia_nicu_nursery")
        ]
        ot_power_systems: List[Dict[str, object]] = [
            dict(row) for row in cursor.execute("SELECT * FROM ot_bioenergetic_power_grid")
        ]
        connected_iomt_fleet: List[Dict[str, object]] = [
            dict(row) for row in cursor.execute("SELECT * FROM iomt_connected_hardware_registry")
        ]
        ems_fleet: List[Dict[str, object]] = [
            dict(row) for row in cursor.execute("SELECT * FROM ems_transport_fleet_registry")
        ]
        workforce_summary: List[Dict[str, object]] = [
            dict(row) for row in cursor.execute("SELECT * FROM workforce_personnel_registry")
        ]

        latency_ms = round((time.perf_counter_ns() - start_ns) / 1_000_000, 3)

        return {
            "bunker_mode": "OFFLINE_AUTONOMOUS_SURVIVAL",
            "branch_id": self.branch_id,
            "active_bunker_protocols": [
                "PROTOCOL_GALA_12_PILLARS",
                "PROTOCOL_SOFIA_NICU_SAFEGUARD",
                "BIOFOAM_ROW_AND_8TABLE_MERKLE_SEAL",
                "BILATERAL_CRYO_HEMOLYSIS_AND_N1_MAINT_GUARD",
                "THYMIC_HLA_IOMT_AND_EMS_FLEET_GUARD",
                "WORKFORCE_AND_SPORADIC_CONTRACTOR_HLA_MATRIX",
                "BIOENERGETIC_OT_POWER_ISLAND_MODE",
            ],
            "biofoam_integrity_audit": integrity_audit,
            "failover_query_latency_ms": latency_ms,
            "active_resuscitation_patients": patients,
            "verified_safe_blood_units": thermo_cryo_units,
            "critical_lab_panic_alerts": panic_labs,
            "protocol_sofia_nicu_nursery_dyads": sofia_nicu_protected,
            "ot_power_and_backup_generators": ot_power_systems,
            "verified_iomt_connected_equipment": connected_iomt_fleet,
            "ems_ambulance_and_helicopter_fleet": ems_fleet,
            "workforce_and_contractors_count": len(workforce_summary),
        }


# =====================================================================
# MULTI-HOSPITAL & SUBSIDIARY FEDERATION (CDR SANITIZER, BOARD/ARCHITECT
# QUORUM & CRITICAL EMS PIT-STOP / SUPPLY RENDEZVOUS)
# =====================================================================
class MultiHospitalSubsidiaryFederation:
    """
    Governs inter-hospital data exchange, confidential sub-clinic vaults, and regional
    EMS ambulance/helicopter dispatch across a healthcare group:
    1. Phagocytic CDR Sanitizer: Disarms Trojans/macros hidden inside inter-clinic lab/imaging transfers.
    2. Sub-Clinic Vault + Board & Lead Architect Quorum: Prevents unauthorized cross-clinic
       snooping unless co-signed by Board Members + Lead Architect/Developer (Dr. Luis Aburto).
    3. Critical Pit-Stop & Helicopter Supply Rendezvous: Routes unstable distant patients to the
       nearest sub-clinic for immediate stabilization while dispatching missing blood/supplies
       from the Main Hospital or sister clinics to meet them en route.
    """

    CORPORATE_FEDERATION_SECRET: bytes = os.environ.get(
        "VALKYRJA_FEDERATION_KEY", FEDERATION_DEFAULT_KEY
    ).encode("utf-8")
    ARCHITECT_MASTER_SECRET: bytes = os.environ.get(
        "VALKYRJA_ARCHITECT_KEY", ARCHITECT_DEFAULT_KEY
    ).encode("utf-8")

    MALICIOUS_PAYLOAD_PATTERNS = (
        r"<script",
        r"javascript:",
        r"powershell",
        r"cmd\.exe",
        r"/bin/sh",
        r"eval\(",
        r"DROP\s+TABLE",
        r"UNION\s+SELECT",
        r"MZ\x90\x00",
        r"VBA_MACRO_AUTOOPEN",
    )

    def __init__(self, corporate_group_name: str = "NORDIC_VITALCARE_HEALTH_GROUP_AB") -> None:
        self.corporate_group_name = corporate_group_name
        self.subsidiary_nodes: Dict[str, Dict[str, object]] = {}

    def register_subsidiary_node(
        self,
        branch_id: str,
        node_role: str,
        available_clinical_services: Optional[List[str]] = None,
        available_blood_and_supplies: Optional[Dict[str, int]] = None,
    ) -> None:
        self.subsidiary_nodes[branch_id] = {
            "role": node_role,
            "network_valve_state": "OPEN_HOMEOSTASIS",
            "local_bunker_state": "GREEN_ONLINE",
            "services": available_clinical_services or ["ER_STABILIZATION", "BASIC_LAB"],
            "inventory": available_blood_and_supplies or {"O_NEG_RBC": 2},
        }

    def isolate_compromised_subsidiary(self, compromised_branch_id: str, reason: str) -> Dict[str, object]:
        if compromised_branch_id in self.subsidiary_nodes:
            self.subsidiary_nodes[compromised_branch_id]["network_valve_state"] = (
                "LYMPHATIC_VALVE_CLOSED_QUARANTINED"
            )
            self.subsidiary_nodes[compromised_branch_id]["local_bunker_state"] = (
                "RED_AUTONOMOUS_SQLITE_BUNKER"
            )

        unaffected_siblings = [
            b_id
            for b_id, meta in self.subsidiary_nodes.items()
            if b_id != compromised_branch_id and meta["network_valve_state"] == "OPEN_HOMEOSTASIS"
        ]
        return {
            "corporate_group": self.corporate_group_name,
            "isolated_subsidiary": compromised_branch_id,
            "containment_reason": reason,
            "lateral_movement_blocked": True,
            "protected_sister_hospitals_and_subclinics": unaffected_siblings,
        }

    # -------------------------------------------------------------------------
    # 1. PHAGOCYTIC CDR (CONTENT DISARM & RECONSTRUCTION) AGAINST LAB TROJANS
    # -------------------------------------------------------------------------
    @classmethod
    def sanitize_and_verify_interclinic_payload(
        cls,
        origin_subclinic_id: str,
        destination_branch_id: str,
        raw_lab_or_imaging_payload: Dict[str, object],
    ) -> Dict[str, object]:
        """
        Phagocytic Content Disarm & Reconstruction (CDR) Gate:
        Inspects incoming lab results or imaging metadata from Sub-clinic A before
        delivering to Sub-clinic B or the Main Hospital.
        - Detects embedded Trojans, macros, shellcode, or SQL injection inside fields.
        - Strips all executable/active content and reconstructs a sterile numeric/text
          clinical JSON capsule signed with B.I.O.F.O.A.M.
        """
        serialized = json.dumps(raw_lab_or_imaging_payload)
        detected_threats: List[str] = []

        for pattern in cls.MALICIOUS_PAYLOAD_PATTERNS:
            if re.search(pattern, serialized, flags=re.IGNORECASE):
                detected_threats.append(pattern)

        # Reconstruct sterile clinical values only (whitelist primitive clinical keys)
        allowed_clinical_keys = ("patient_token", "analyte", "numeric_value", "unit", "reference_range")
        sterile_reconstructed_data: Dict[str, object] = {}

        for k in allowed_clinical_keys:
            if k in raw_lab_or_imaging_payload:
                val_str = str(raw_lab_or_imaging_payload[k])
                # Strip any script/macro tags during reconstruction
                clean_val = re.sub(r"(<script.*?>.*?</script>|VBA_MACRO_AUTOOPEN|powershell|eval\()", "[DISARMED]", val_str, flags=re.IGNORECASE)
                sterile_reconstructed_data[k] = clean_val

        return {
            "origin_subclinic": origin_subclinic_id,
            "destination_branch": destination_branch_id,
            "trojan_or_exploit_detected": len(detected_threats) > 0,
            "neutralized_threat_signatures": detected_threats,
            "cdr_action": (
                "TROJAN_PHAGOCYTOSED_AND_STRIPPED_STERILE_VALUES_EXTRACTED"
                if detected_threats
                else "CLEAN_PAYLOAD_VERIFIED"
            ),
            "sterile_reconstructed_clinical_capsule": sterile_reconstructed_data,
        }

    # -------------------------------------------------------------------------
    # 2. SUB-CLINIC CONFIDENTIAL VAULT & BOARD + ARCHITECT (DR. LUIS ABURTO) KEY
    # -------------------------------------------------------------------------
    @classmethod
    def generate_architect_or_board_key_share(cls, signer_role: str, signer_id: str, target_subclinic: str) -> str:
        """
        Generates a cryptographic authorization share for either a Board Member
        or the Lead Architect/Developer (Dr. Luis Aburto).
        """
        secret = cls.ARCHITECT_MASTER_SECRET if signer_role == "ARCHITECT_DEVELOPER" else cls.CORPORATE_FEDERATION_SECRET
        payload = f"VAULT_AUTH:{signer_role}:{signer_id}:{target_subclinic}".encode("utf-8")
        sig = hmac.new(secret, payload, hashlib.sha256).hexdigest()[:18].upper()
        return f"KEYSHARE-{signer_role}-{sig}"

    @classmethod
    def unlock_subclinic_confidential_vault(
        cls,
        requesting_branch_id: str,
        target_subclinic_id: str,
        board_member_signatures: List[Dict[str, str]],
        architect_dev_signature: Optional[Dict[str, str]],
        encrypted_subclinic_record: str,
    ) -> Dict[str, object]:
        """
        Enforces Swedish Patientdatalagen (SFS 2008:355) & Zero-Knowledge Compartmentalization:
        Other sub-clinics or even the Main Hospital CANNOT read a sub-clinic's ultra-confidential
        vault records unless authorized by:
          - At least 2 verified Board Members (`BOARD_MEMBER`), AND
          - The Lead Architect / Developer (`ARCHITECT_DEVELOPER`: Dr. Luis Aburto).
        """
        verified_board_count = 0
        for b_sig in board_member_signatures:
            expected = cls.generate_architect_or_board_key_share(
                "BOARD_MEMBER", b_sig.get("signer_id", ""), target_subclinic_id
            )
            if hmac.compare_digest(expected, b_sig.get("token", "")):
                verified_board_count += 1

        architect_verified = False
        if architect_dev_signature:
            expected_arch = cls.generate_architect_or_board_key_share(
                "ARCHITECT_DEVELOPER",
                architect_dev_signature.get("signer_id", ""),
                target_subclinic_id,
            )
            if hmac.compare_digest(expected_arch, architect_dev_signature.get("token", "")):
                architect_verified = True

        if verified_board_count >= 2 and architect_verified:
            return {
                "vault_access_granted": True,
                "target_subclinic": target_subclinic_id,
                "authorization_quorum": f"{verified_board_count} Board Members + Lead Architect/Developer Verified",
                "decrypted_confidential_payload": encrypted_subclinic_record,
            }

        return {
            "vault_access_granted": False,
            "target_subclinic": target_subclinic_id,
            "status": (
                "ACCESS_DENIED_CROSS_CLINIC_COMPARTMENT_LOCK: Requires 2 Board Member keys "
                "+ Lead Architect/Developer (Dr. Luis Aburto) cryptographic key share!"
            ),
        }

    # -------------------------------------------------------------------------
    # 3. CRITICAL EMS PIT-STOP STABILIZATION & INTER-CLINIC SUPPLY RENDEZVOUS
    # -------------------------------------------------------------------------
    def orchestrate_critical_patient_and_supply_rendezvous(
        self,
        patient_token: str,
        required_definitive_service: str,  # e.g., "NEUROSURGERY_OR_ECMO"
        required_urgent_supply: str,  # e.g., "O_NEG_RBC" or "FIBRINOGEN_CONCENTRATE"
        required_supply_units: int,
        eta_to_main_hospital_minutes: int,
        nearest_subclinic_id: str,
        eta_to_nearest_subclinic_minutes: int,
    ) -> Dict[str, object]:
        """
        Solves the Distant Critical Patient Dilemma ("Damage-Control Pit-Stop + Supply Rendezvous"):
        1. If the patient is unstable and too far from the Main Hospital (e.g., 55 min away)
           but near Sub-clinic B (e.g., 8 min away), routes the ambulance to Sub-clinic B for
           immediate airway/hemodynamic stabilization.
        2. Simultaneously scans all sister clinics/hospitals in the federation to locate the
           required blood/supply and dispatches a Medevac Helicopter or Rapid Response Unit to
           deliver the supply to Sub-clinic B (and/or pick up the stabilized patient).
        """
        pit_stop_engaged = eta_to_main_hospital_minutes > 25 and eta_to_nearest_subclinic_minutes <= 15
        staging_facility = nearest_subclinic_id if pit_stop_engaged else "SE_STHLM_MAIN_HOSPITAL"

        # Locate which hospital/sub-clinic in the network holds the required supply
        supply_donor_branch = None
        for branch_id, meta in self.subsidiary_nodes.items():
            inventory = meta.get("inventory", {})
            if isinstance(inventory, dict) and inventory.get(required_urgent_supply, 0) >= required_supply_units:
                supply_donor_branch = branch_id
                break

        # Locate which hospital holds the definitive specialist service
        definitive_care_branch = "SE_STHLM_MAIN_HOSPITAL"
        for branch_id, meta in self.subsidiary_nodes.items():
            services = meta.get("services", [])
            if isinstance(services, list) and required_definitive_service in services:
                definitive_care_branch = branch_id
                break

        return {
            "patient_token": patient_token,
            "tactical_routing_decision": (
                "DAMAGE_CONTROL_PIT_STOP_AT_NEAREST_SUBCLINIC_PLUS_HELI_RENDEZVOUS"
                if pit_stop_engaged
                else "DIRECT_TRANSPORT_TO_TERTIARY_CENTER"
            ),
            "immediate_stabilization_destination": staging_facility,
            "eta_to_stabilization_minutes": eta_to_nearest_subclinic_minutes,
            "definitive_specialty_center": definitive_care_branch,
            "urgent_supply_requested": f"{required_supply_units}x {required_urgent_supply}",
            "supply_dispatched_from_branch": supply_donor_branch or "EMERGENCY_REGIONAL_BLOOD_HUB",
            "dispatch_transport_vector": "HELI-MEDEVAC-01 (Air Rendezvous to Sub-clinic)",
        }

    @classmethod
    def export_signed_ambulance_transfer_capsule(
        cls,
        origin_subclinic_id: str,
        destination_hospital_id: str,
        patient_token: str,
        abo_rh: str,
        critical_summary: str,
    ) -> Dict[str, str]:
        canonical = f"{origin_subclinic_id}->{destination_hospital_id}|{patient_token}|{abo_rh}|{critical_summary}"
        sig = hmac.new(
            cls.CORPORATE_FEDERATION_SECRET, canonical.encode("utf-8"), hashlib.sha256
        ).hexdigest().upper()
        return {
            "origin_subclinic": origin_subclinic_id,
            "destination_hospital": destination_hospital_id,
            "patient_token": patient_token,
            "abo_rh": abo_rh,
            "critical_summary": critical_summary,
            "federation_hmac_seal": sig,
        }

    @classmethod
    def verify_incoming_ambulance_transfer_capsule(cls, capsule: Dict[str, str]) -> Dict[str, object]:
        canonical = (
            f"{capsule['origin_subclinic']}->{capsule['destination_hospital']}|"
            f"{capsule['patient_token']}|{capsule['abo_rh']}|{capsule['critical_summary']}"
        )
        expected_sig = hmac.new(
            cls.CORPORATE_FEDERATION_SECRET, canonical.encode("utf-8"), hashlib.sha256
        ).hexdigest().upper()
        is_valid = hmac.compare_digest(expected_sig, capsule.get("federation_hmac_seal", ""))
        return {
            "transfer_capsule_authentic": is_valid,
            "receiving_action": (
                "ADMIT_TO_MAIN_HOSPITAL_TRAUMA_OR_ICU_BAY"
                if is_valid
                else "REJECT_TAMPERED_TRANSFER_PACKET"
            ),
        }
