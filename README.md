# 🛡️ Project VALKYRJA — Clinical Continuity & Active Cyber-Defense Engine

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Architecture: Hexagonal](https://img.shields.io/badge/Architecture-Hexagonal%20%28Ports%20%26%20Adapters%29-success.svg)]()
[![Cryptography: AES-256-GCM](https://img.shields.io/badge/Cryptography-AES--256--GCM%20%7C%20HMAC--SHA256-indigo.svg)]()
[![Compliance: EU NIS2 / SFS 2025:1506](https://img.shields.io/badge/Compliance-EU%20NIS2%20%7C%20Sweden%20SFS%202025%3A1506-005293.svg)]()

> **Bio-inspired active deception, ephemeral RAM cryptography, and offline point-of-care survival architecture for emergency medicine, blood banks, and critical infrastructure.**

---

## 🇸🇪 Svensk Sammanfattning (Exekutiv Översikt)

**Project VALKYRJA** är en modulär cybersäkerhets- och kontinuitetsplattform utvecklad specifikt för att skydda kritisk vårdinfrastruktur (akutmottagningar, blodbanker och kliniska laboratorier) samt högsäkerhetsmiljöer mot moderna ransomware-attacker, dataexfiltrering och AI-driven röstkloning (*deepfakes*).

Systemet är konstruerat av en legitimerad läkare inom akutsjukvård och mjukvaruutvecklare för att lösa ett livshotande problem inom modern **HealthTech**: *Hur isolerar vi ett pågående dataintrång på millisekunder utan att orsaka "klinisk ischemi" (driftstopp som äventyrar patientsäkerheten)?*

* **Efterlevnad av Cybersäkerhetslagen (SFS 2025:1506 / NIS2):** Automatiserad generering av tekniska incidentrapporter för tidig varning (<24 timmar till MSB).
* **Patientsäkerhet vid nätverksbortfall (IVO / Lex Maria):** Lokalt krypterad *Fail-Safe Bunker* (SQLite) som säkerställer oavbruten tillgång till akuttriagering, blodgruppering (O-negativ reserv) och kritiska laboratorievärden även när centrala servrar kopplas bort.
* **Dataskydd & Noll-exfiltrering (IMY / GDPR):** Aktiv vilseledning (*Asynchronous Tarpits*), syntetisk *Honey-Data* med roterande kryptografiska vattenstämplar samt omedelbar radering av en 32-byte (256-bitars) RAM-nyckel (*Crypto-Shredding*) vid kritiska intrångsförsök.

---

## 🩺 The Clinical & Engineering Problem

Recent cyberattacks against European healthcare providers (such as the pathology and blood-matching disruption in London and hospital ransomware incidents in Barcelona) exposed a critical gap in traditional enterprise cybersecurity:

1. **Conventional IT security uses binary "Kill-Switches":** Shutting down an entire hospital network to stop ransomware halts emergency triage, blood crossmatching, and critical lab reporting—turning an IT incident into a life-safety crisis.
2. **Legacy Deception is static:** Attackers quickly identify static honeypots, while social engineering increasingly relies on real-time **AI voice cloning** to authorize fraudulent emergency procedures or high-value transfers.

**Project VALKYRJA** bridges clinical emergency protocols with defensive software engineering. Inspired by human physiology (**hemostasis and innate/adaptive immunity**), it contains breaches locally while guaranteeing **collateral circulation of vital clinical data**.

---

## 🏗️ System Architecture (Hexagonal MVP)

Built on a **Hexagonal Architecture (Ports & Adapters)** in Python, the system isolates the universal security core (80%) from domain-specific adapters (20%), ensuring clean scalability without code duplication.

```text
valkyrja-mvp/
├── core/                                  # UNIVERSAL SECURITY & DECISION CORE
│   ├── 1_deception_barium_engine.py       # Async Tarpit + Rolling Steganographic Honey-Data
│   ├── 2_clinical_nis2_flowchart.py       # 32-Byte RAM Key Manager + Clinical/NIS2 State Machine
│   ├── 3_verbal_shield_mhc1.py            # 60s Rolling Verbal TOTP against AI Voice Cloning
│   └── ports_future_expansions.py         # Hexagonal Protocol Interfaces (Phase 2 Ready)
│
├── adapters/                              # DOMAIN-SPECIFIC ADAPTERS
│   └── 4_local_clinical_bunker.py         # Offline SQLite Point-of-Care Bunker (ER/Blood/Lab)
│
├── tests/                                 # AUTOMATED PYTEST SUITE
│   └── test_core_defenses.py              # Unit tests for Crypto-Shredding, TOTP & Watermarking
│
└── 5_valkyrja_dashboard_demo.py           # Interactive Command Center & Attack Simulator
