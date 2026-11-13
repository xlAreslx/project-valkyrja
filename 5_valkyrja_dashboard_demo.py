"""
Project VALKYRJA — Module 5: Unified Command Center (Protocols SOFIA, GALA, UNICORSE & SIERRA)
"""

import importlib.util
import json
from pathlib import Path
from types import ModuleType


def load_valkyrja_module(module_alias: str, relative_path: str) -> ModuleType:
    base_dir = Path(__file__).resolve().parent
    target_path = base_dir / relative_path
    spec = importlib.util.spec_from_file_location(module_alias, target_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {module_alias}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mod1_barium = load_valkyrja_module("mod1_barium", "core/1_deception_barium_engine.py")
mod2_flowchart = load_valkyrja_module("mod2_flowchart", "core/2_clinical_nis2_flowchart.py")
mod3_verbal = load_valkyrja_module("mod3_verbal", "core/3_verbal_shield_mhc1.py")
mod4_bunker = load_valkyrja_module("mod4_bunker", "adapters/4_local_clinical_bunker.py")


def run_full_valkyrja_simulation() -> None:
    print("=" * 80)
    print("  🛡️  PROJECT VALKYRJA — UNIFIED CLINICAL CYBER-DEFENSE COMMAND CENTER")
    print("  Active Named Protocols: [S.O.F.I.A.]  [G.A.L.A.]  [U.N.I.C.O.R.S.E.]  [S.I.E.R.R.A.]")
    print("=" * 80)

    # STAGE 1: PROTOCOL U.N.I.C.O.R.S.E. (Infinite Mirror Maze & Barium Watermark)
    print("\n[STAGE 1] PROTOCOL U.N.I.C.O.R.S.E. — Mirror Wall Labyrinth & Barium Trace")
    barium_token = mod1_barium.generate_rolling_barium_token()
    maze_reflection = mod1_barium.ProtocolUnicorseMirrorMaze.reflect_infinite_labyrinth_node(
        "/srv/karolinska_vault/cryo_stem_cells"
    )
    print(f"  • Injected Barium Watermark   : {barium_token}")
    print(f"  • Reflected Maze Subfolders   : {len(maze_reflection['synthesized_subdirectories'])} procedural nodes")

    # STAGE 2: Anti-Deepfake Verbal Shield (MHC-I)
    print("\n[STAGE 2] Out-of-Band Verbal Cryptographic Shield (60s Rolling TOTP)")
    verbal_shield = mod3_verbal.RollingVerbalShieldMHC1(b"VALKYRJA_ENCLAVE_HARDWARE_SEED_2026")
    print(f"  • Active Physician Token (60s): {verbal_shield.generate_current_verbal_seed()}")

    # STAGE 3: PROTOCOL S.I.E.R.R.A. (32-Byte RAM Key Shredding & Clinical Locks)
    print("\n[STAGE 3] PROTOCOL S.I.E.R.R.A. — 32-Byte RAM Key Shredding & Clinical Decision Locks")
    ram_key_manager = mod2_flowchart.EphemeralRAMKeyManager()
    flowchart_engine = mod2_flowchart.ClinicalNIS2FlowchartEngine(ram_key_manager)

    esc_check = mod2_flowchart.ProtocolSierraClinicalLocks.evaluate_esc_0h_1h_troponin(18.0, 64.0)
    renal_check = mod2_flowchart.ProtocolSierraClinicalLocks.evaluate_swedish_dual_egfr_and_dialysis(540.0, 3.1, 6.9)
    dka_lock = mod2_flowchart.ProtocolSierraClinicalLocks.verify_dka_insulin_potassium_lock(2.9, 28.0)

    clinical_context = mod2_flowchart.ClinicalVitalContext(
        branch_id="SE_STHLM_KAROLINSKA_ER",
        er_trauma_resuscitation_active=True,
        blood_transfusion_matching_active=True,
        critical_lab_panic_values_pending=True,
    )
    nis2_dossier = flowchart_engine.evaluate_incident_flowchart(
        intrusion_tier=4,
        attacker_ip="185.220.101.77",
        barium_watermark_injected=barium_token,
        clinical_context=clinical_context,
    )
    print(f"  • Post-Breach 32-Byte Key     : {ram_key_manager.get_key_status_preview()}")
    print(f"  • ESC 0h/1h Troponin Verdict  : {esc_check['esc_verdict']}")
    print(f"  • Swedish Dual eGFR / K+ Lock : {renal_check['nephrology_action']}")
    print(f"  • DKA Insulin-Potassium Lock  : {dka_lock['safety_lock_status']}")

    # STAGE 4: PROTOCOL G.A.L.A. & PROTOCOL S.O.F.I.A. (Offline SQLite Survival Bunker)
    print("\n[STAGE 4] PROTOCOL G.A.L.A. & PROTOCOL S.O.F.I.A. — 12-Pillar & NICU Survival Bunker")
    bunker = mod4_bunker.LocalClinicalSurvivalBunker()
    bunker.seed_shadow_sync_snapshot()
    survival_state = bunker.query_emergency_survival_snapshot()

    print(f"  • Active Bunker Protocols     : {survival_state['active_bunker_protocols']}")
    print(f"  • Protected Critical Patients : {len(survival_state['active_resuscitation_patients'])} across acute pillars")
    print(f"  • Thermo-Cryo Units (+22/-196): {len(survival_state['verified_safe_blood_units'])} units monitored")
    print(f"  • Protocol SOFIA NICU Dyads   : {len(survival_state['protocol_sofia_nicu_nursery_dyads'])} mother-infant pairs locked")

    print("\n" + "=" * 80)
    print("  📄 AUTOMATED SWEDISH NIS2 / MSB / IMY / IVO COMPLIANCE DOSSIER (<24H)")
    print("=" * 80)
    print(json.dumps(nis2_dossier, indent=2))


if __name__ == "__main__":
    run_full_valkyrja_simulation()
