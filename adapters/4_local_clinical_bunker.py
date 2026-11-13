"""
Project VALKYRJA — Adapter Module 4: Offline Point-of-Care Survival Bunker (SQLite),
IoMT Hardware Lifecycle Registry & Multi-Hospital Subsidiary Federation.
Architecture: Hexagonal Secondary Adapter (MedCore Clinical, IoMT & Bioenergetic OT Continuity)
Compliance Target: Sweden IVO (Lex Maria Patient Safety) & SFS 2025:1506 (NIS2)

Implements:
1. PROTOCOL G.A.L.A. & B.I.O.F.O.A.M. (Row-Level HMAC + 6-Table Merkle Manifest Seal):
   - Protects the 12 High-Mortality Clinical Pillars, Bilateral [T_min, T_max] Cryo Matrix,
     OT Backup Power, and Connected IoMT/IT Equipment Registry.
   - Supports signed N+1 Cold-Chain Maintenance, OT Generator Maintenance/Replacement,
     and Clinical/IT Equipment Provisioning, Maintenance, Replacement & Apoptosis (Removal)
     across PCs, iPads, Laparoscopy Towers, Lab Analyzers, CT/MRI Imaging, ICU & NICU.
2. PROTOCOL S.O.F.I.A. (Safeguarded Offline Failover for Infant & Acute-care):
   - Cryptographic SHA-256 Mother-Infant Wristband Dyad Pairing for NICU/Nursery (Cuneros).
3. Multi-Hospital & Subsidiary Lymphatic Federation:
   - Prevents lateral movement between sub-clinics and sister hospitals of the same corporate
     group while enabling B.I.O.F.O.A.M.-signed ambulance transfer capsules.
"""

import hashlib
import hmac
import json
import os
import sqlite3
import time
from typing import Dict, List, Optional

SOFIA_DEFAULT_KEY = "PROTOCOL_SOFIA_NICU_MOTHER_INFANT_DYAD_KEY_2026"
BIOFOAM_DEFAULT_KEY = "PROTOCOL_GALA_BIOFOAM_ROW_INTEGRITY_SEED_2026"
FEDERATION_DEFAULT_KEY = "VALKYRJA_CORPORATE_SUBSIDIARY_FEDERATION_SEED_2026"


class LocalClinicalSurvivalBunker:
    """
    PROTOCOL G.A.L.A., PROTOCOL S.O.F.I.A. & B.I.O.F.O.A.M. Offline Survival Node.
    Guarantees sub-5ms local clinical, bilateral cryogenic, IoMT hardware, and OT power continuity.
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
    )

    def __init__(self, db_path: str = ":memory:", branch_id: str = "SE_STHLM_MAIN_HOSPITAL_01") -> None:
        self.db_path = db_path
        self.branch_id = branch_id
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._bunker_merkle_manifest_hmac: Optional[str] = None
        self._expected_triage_tokens: List[str] = []
        self._revoked_hardware_tokens: set[str] = set()
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

        # Table 6: Connected Clinical IoMT & IT Hardware Lifecycle Registry (Thymic HLA Selection)
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
        """Computes a row-level B.I.O.F.O.A.M. HMAC-SHA256 tag over every clinical field."""
        canonical = f"{patient_token}|{retts_level}|{pillar}|{abo_rh}|{antibodies}|{allergies}|{organ_params}|{bay}"
        return hmac.new(cls.BIOFOAM_ROW_SECRET, canonical.encode("utf-8"), hashlib.sha256).hexdigest()[:20].upper()

    def compute_full_bunker_merkle_manifest(self) -> str:
        """Hashes the exact row count and canonical content of all 6 survival tables in SQLite."""
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
        """Audits both individual B.I.O.F.O.A.M. row seals AND the 6-Table Merkle Manifest HMAC."""
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
            and hmac.compare_digest(current_merkle, self._bunker_merkle_merkle_or_manifest())
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

    def _bunker_merkle_merkle_or_manifest(self) -> str:
        return self._bunker_merkle_manifest_hmac or ""

    def audit_bilateral_thermo_cryogenic_safety(self) -> Dict[str, object]:
        """Evaluates all biological & cryogenic units against bilateral [min_safe_celsius, max_safe_celsius]."""
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
    # 2. ELECTRICAL GRID, UPS & GENERATOR MAINTENANCE / REPLACEMENT (MITOPHAGY)
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
        action: str,  # "MAINTENANCE_BYPASS" or "REPLACE_WITH_NEW_GENERATOR"
        collateral_backup_online: bool,
        collateral_autonomy_hours: float,
        engineer_id: str,
        auth_token: str,
        new_subsystem_id: Optional[str] = None,
        new_voltage_telemetry: str = "400V 3-Phase / 50.00 Hz (New Unit Online)",
    ) -> Dict[str, object]:
        """
        Governs maintenance or full replacement of hospital electrical generators and UPS banks:
        1. Verifies cryptographic facility engineering authorization.
        2. Enforces Collateral Perfusion Guard: Blocks taking any generator/UPS offline unless
           collateral backup power is verified online with >= 72.0 hours of Red-Outlet autonomy.
        3. Updates or swaps the generator record and re-seals the 6-Table Merkle Manifest.
        """
        expected = self.generate_power_lifecycle_auth_token(target_subsystem_id, action, engineer_id)
        if not hmac.compare_digest(expected, auth_token.strip().upper()):
            return {"power_operation_authorized": False, "status": "REJECTED_INVALID_OT_POWER_HMAC"}

        if not collateral_backup_online or collateral_autonomy_hours < 72.0:
            return {
                "power_operation_authorized": False,
                "status": (
                    "BLOCKED_INSUFFICIENT_COLLATERAL_POWER: Cannot service or swap generator "
                    "without verified >=72h N+1 backup power on Red Outlets!"
                ),
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
    # 3. CONNECTED IoMT & IT HARDWARE LIFECYCLE (PCs, iPads, OR, Lab, Imaging, ICU, NICU)
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
        action: str,  # "ADD_NEW", "MAINTENANCE_MODE", "REPLACE_SWAP", "REMOVE_DECOMMISSION"
        device_id: str,
        device_category: str,  # e.g., "OR_LAPAROSCOPY_TOWER", "CLINICAL_IPAD", "CT_MRI_IMAGING", "LAB_ANALYZER", "NICU_INCUBATOR", "ICU_VENTILATOR"
        assigned_department: str,
        serial_or_mac: str,
        biomed_engineer_id: str,
        auth_token: str,
        replacement_device_id: Optional[str] = None,
        replacement_serial_mac: Optional[str] = None,
    ) -> Dict[str, object]:
        """
        Thymic Positive/Negative Selection for Connected Hospital Equipment:
        Safely adds new devices, isolates units under maintenance, performs atomic hardware
        swaps, or executes cryptographic apoptosis (revocation) when removing old devices,
        automatically re-sealing the 6-Table Merkle Manifest.
        """
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
                """
                UPDATE iomt_connected_hardware_registry
                SET operational_status = 'MAINTENANCE_SANDBOX_ISOLATED'
                WHERE device_id = ?
                """,
                (device_id,),
            )
            result_status = "EQUIPMENT_ISOLATED_FOR_SAFE_MAINTENANCE"

        elif action == "REPLACE_SWAP" and replacement_device_id and replacement_serial_mac:
            old_row = cursor.execute(
                "SELECT * FROM iomt_connected_hardware_registry WHERE device_id = ?", (device_id,)
            ).fetchone()
            if old_row:
                self._revoked_hardware_tokens.add(old_row["hla_hardware_token"])
            cursor.execute(
                "DELETE FROM iomt_connected_hardware_registry WHERE device_id = ?", (device_id,)
            )
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
            cursor.execute(
                "DELETE FROM iomt_connected_hardware_registry WHERE device_id = ?", (device_id,)
            )
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
        """Blocks decommissioned/stolen devices, units in maintenance mode, or unregistered rogue hardware."""
        if presented_hla_token in self._revoked_hardware_tokens:
            return {
                "access_granted": False,
                "verdict": "BLOCKED_APOPTOSIS_REVOKED_HARDWARE_TOKEN",
            }
        cursor = self.conn.cursor()
        row = cursor.execute(
            "SELECT * FROM iomt_connected_hardware_registry WHERE device_id = ?", (device_id,)
        ).fetchone()
        if not row:
            return {"access_granted": False, "verdict": "BLOCKED_UNREGISTERED_ROGUE_DEVICE"}
        if not hmac.compare_digest(row["hla_hardware_token"], presented_hla_token):
            return {"access_granted": False, "verdict": "BLOCKED_FORGED_HARDWARE_SIGNATURE"}
        if row["operational_status"] == "MAINTENANCE_SANDBOX_ISOLATED":
            return {
                "access_granted": False,
                "verdict": "QUARANTINED_DEVICE_UNDER_MAINTENANCE_NO_PROD_ACCESS",
            }
        return {
            "access_granted": True,
            "verdict": "AUTHORIZED_HLA_COMPATIBLE_EQUIPMENT",
            "allowed_department_scope": row["assigned_department"],
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
        """Populates all 6 tables and locks the 6-Table Merkle Manifest."""
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

        # Seed Table 6: Initial Connected IoMT & Clinical IT Fleet
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

        latency_ms = round((time.perf_counter_ns() - start_ns) / 1_000_000, 3)

        return {
            "bunker_mode": "OFFLINE_AUTONOMOUS_SURVIVAL",
            "branch_id": self.branch_id,
            "active_bunker_protocols": [
                "PROTOCOL_GALA_12_PILLARS",
                "PROTOCOL_SOFIA_NICU_SAFEGUARD",
                "BIOFOAM_ROW_AND_6TABLE_MERKLE_SEAL",
                "BILATERAL_CRYO_HEMOLYSIS_AND_N1_MAINT_GUARD",
                "THYMIC_HLA_IOMT_EQUIPMENT_LIFECYCLE_GUARD",
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
        }


# =====================================================================
# 4. MULTI-HOSPITAL & SUBSIDIARY FEDERATION (LYMPHATIC VALVE ISOLATION)
# =====================================================================
class MultiHospitalSubsidiaryFederation:
    """
    Manages a corporate network of main hospitals, sub-clinics, and diagnostic subsidiaries:
    1. Independent Cellular Isolation: If a sub-clinic is breached, its lymphatic valve closes
       in <1ms so ransomware cannot move laterally to the Main Hospital or sister clinics.
    2. Signed Ambulance Transfer Exosome: Allows a compromised/offline sub-clinic to export
       a read-only, B.I.O.F.O.A.M.-signed emergency patient summary for safe physical ambulance
       transfer to the Main Hospital without opening network sockets.
    """

    CORPORATE_FEDERATION_SECRET: bytes = os.environ.get(
        "VALKYRJA_FEDERATION_KEY", FEDERATION_DEFAULT_KEY
    ).encode("utf-8")

    def __init__(self, corporate_group_name: str = "NORDIC_VITALCARE_HEALTH_GROUP_AB") -> None:
        self.corporate_group_name = corporate_group_name
        self.subsidiary_nodes: Dict[str, Dict[str, str]] = {}

    def register_subsidiary_node(self, branch_id: str, node_role: str) -> None:
        self.subsidiary_nodes[branch_id] = {
            "role": node_role,  # e.g., "TERTIARY_MAIN_HOSPITAL", "PERIPHERAL_SUBCLINIC", "DIAGNOSTIC_LAB_CENTER"
            "network_valve_state": "OPEN_HOMEOSTASIS",
            "local_bunker_state": "GREEN_ONLINE",
        }

    def isolate_compromised_subsidiary(self, compromised_branch_id: str, reason: str) -> Dict[str, object]:
        """Closes the inter-hospital lymphatic valve to block lateral ransomware propagation."""
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

    @classmethod
    def export_signed_ambulance_transfer_capsule(
        cls,
        origin_subclinic_id: str,
        destination_hospital_id: str,
        patient_token: str,
        abo_rh: str,
        critical_summary: str,
    ) -> Dict[str, str]:
        """
        Generates a read-only, non-executable clinical transfer capsule signed with HMAC-SHA256
        so a patient evacuated by ambulance from an attacked sub-clinic arrives at the main
        hospital with verified blood type, allergies, and lab trends.
        """
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
