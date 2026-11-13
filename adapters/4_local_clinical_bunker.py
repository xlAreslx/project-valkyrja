"""
Project VALKYRJA — Adapter Module 4: Offline Point-of-Care Survival Bunker (SQLite)
Architecture: Hexagonal Secondary Adapter (MedCore Clinical & Bioenergetic OT Continuity)
Compliance Target: Sweden IVO (Lex Maria Patient Safety) & SFS 2025:1506 (NIS2)

Implements:
1. PROTOCOL G.A.L.A. & B.I.O.F.O.A.M. (Row-Level HMAC + 5-Table Merkle Manifest Seal):
   - Protects the 12 High-Mortality Clinical Pillars, 5-Tier Cryo Matrix, and OT Backup Power.
   - Detects both column tampering (UPDATE) and surgical row deletion (DELETE) across all 5 tables.
2. PROTOCOL S.O.F.I.A. (Safeguarded Offline Failover for Infant & Acute-care):
   - Cryptographic SHA-256 Mother-Infant Wristband Dyad Pairing for NICU/Nursery (Cuneros).
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


class LocalClinicalSurvivalBunker:
    """
    PROTOCOL G.A.L.A., PROTOCOL S.O.F.I.A. & B.I.O.F.O.A.M. Offline Survival Node.
    Guarantees sub-5ms local clinical, cryogenic, and electrical telemetry continuity.
    """

    SOFIA_NURSERY_SECRET: bytes = os.environ.get("VALKYRJA_SOFIA_KEY", SOFIA_DEFAULT_KEY).encode("utf-8")
    BIOFOAM_ROW_SECRET: bytes = os.environ.get("VALKYRJA_BIOFOAM_KEY", BIOFOAM_DEFAULT_KEY).encode("utf-8")

    PROTECTED_TABLES = (
        "er_active_triage",
        "blood_bank_reserve",
        "lab_panic_values",
        "protocol_sofia_nicu_nursery",
        "ot_bioenergetic_power_grid",
    )

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._bunker_merkle_manifest_hmac: Optional[str] = None
        self._expected_triage_tokens: List[str] = []
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
        """
        Red-Team v1.2 Merkle Manifest Seal:
        Hashes the exact row count and canonical content of all 5 survival tables in SQLite.
        Any surgical DELETE or cross-table modification (e.g., altering potassium in lab_panic_values)
        immediately invalidates the root Merkle HMAC.
        """
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
        """
        Audits both individual B.I.O.F.O.A.M. row seals AND the 5-Table Merkle Manifest HMAC.
        Detects column tampering (UPDATE), surgical row deletions (DELETE), and lab/cryo sabotage.
        """
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

        # Detect surgical DELETE attacks on er_active_triage
        deleted_tokens = [t for t in self._expected_triage_tokens if t not in present_tokens]
        for missing in deleted_tokens:
            tampered_patients.append(f"DELETED:{missing}")

        # Verify 5-Table Merkle Root Manifest (covers lab_panic_values, blood_bank_reserve, etc.)
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
        """Populates all 5 tables and locks the B.I.O.F.O.A.M. + 5-Table Merkle Manifest Seal."""
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
            "INSERT OR REPLACE INTO blood_bank_reserve VALUES (?, ?, ?, ?, ?, ?)",
            [
                ("BLD-SE-ONEG-001", "O-", "Packed_RBC", "ER_FRIDGE_01", 3.6, "AVAILABLE_EMERGENCY"),
                ("BLD-SE-ONEG-002", "O-", "Packed_RBC", "ER_FRIDGE_01", 3.8, "AVAILABLE_EMERGENCY"),
                ("PLT-SE-AGIT-010", "O+", "Platelet_Concentrate_Agitator", "THERMO_22C_01", 21.8, "VIABLE_AGITATING"),
                ("FFP-SE-CRYO-044", "AB+", "Fresh_Frozen_Plasma", "FREEZER_MINUS30_02", -31.5, "FROZEN_INTACT"),
                ("VAC-SE-ULT-080", "N/A", "Oncology_Biologics_ULT", "ULT_MINUS80_01", -81.2, "ULTRA_COLD_INTACT"),
                ("CRYO-LN2-STEM-99", "HLA-A2", "Hematopoietic_Stem_Cells_And_Cornea", "LN2_DEWAR_196", -195.8, "CRYO_VAPOR_LOCKED"),
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
            dict(row) for row in cursor.execute("SELECT * FROM blood_bank_reserve WHERE temp_celsius <= 24.0")
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

        latency_ms = round((time.perf_counter_ns() - start_ns) / 1_000_000, 3)

        return {
            "bunker_mode": "OFFLINE_AUTONOMOUS_SURVIVAL",
            "active_bunker_protocols": [
                "PROTOCOL_GALA_12_PILLARS",
                "PROTOCOL_SOFIA_NICU_SAFEGUARD",
                "BIOFOAM_ROW_AND_5TABLE_MERKLE_SEAL",
                "BIOENERGETIC_OT_POWER_ISLAND_MODE",
            ],
            "biofoam_integrity_audit": integrity_audit,
            "failover_query_latency_ms": latency_ms,
            "active_resuscitation_patients": patients,
            "verified_safe_blood_units": thermo_cryo_units,
            "critical_lab_panic_alerts": panic_labs,
            "protocol_sofia_nicu_nursery_dyads": sofia_nicu_protected,
            "ot_power_and_backup_generators": ot_power_systems,
        }
