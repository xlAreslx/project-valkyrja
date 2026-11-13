# 🛡️ Project VALKYRJA — Clinical Continuity & Active Cyber-Defense Engine

[![Automated Clinical & Crypto CI](https://github.com/xlAreslx/project-valkyrja/actions/workflows/main.yml/badge.svg)](https://github.com/xlAreslx/project-valkyrja/actions)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Architecture: Hexagonal](https://img.shields.io/badge/Architecture-Hexagonal%20%28Ports%20%26%20Adapters%29-success.svg)]()
[![Cryptography: AES-256 / HMAC-SHA256](https://img.shields.io/badge/Cryptography-256--Bit%20RAM%20Key%20%7C%20HMAC--SHA256-indigo.svg)]()
[![Compliance: EU NIS2 / SFS 2025:1506](https://img.shields.io/badge/Compliance-EU%20NIS2%20%7C%20Sweden%20SFS%202025%3A1506-005293.svg)]()

> **Bio-inspired active deception, lymphatic DDoS sinkholing, ephemeral 32-byte RAM cryptography, OT backup power resilience, and offline point-of-care survival across 12 acute clinical workflows.**

---

## 🇸🇪 Svensk Sammanfattning (Exekutiv Översikt)

**Project VALKYRJA** är en modulär cybersäkerhets- och kontinuitetsplattform utvecklad specifikt för att skydda kritisk vårdinfrastruktur (akutmottagningar, intensivvård/IVA, neonatalvård, blodbanker, transplantationskirurgi, kliniska laboratorier samt reservkraft/OT-system) mot moderna ransomware-attacker, DDoS-överbelastning, dataexfiltrering och AI-driven röstkloning (*deepfakes*).

Systemet är konstruerat av en legitimerad läkare inom akutsjukvård och mjukvaruutvecklare för att lösa ett livshotande problem inom modern **HealthTech**: *Hur isolerar vi ett pågående dataintrång på millisekunder utan att orsaka "klinisk eller bioenergetisk ischemi" (driftstopp eller strömbortfall som äventyrar patientsäkerheten)?*

* **Efterlevnad av Cybersäkerhetslagen (SFS 2025:1506 / NIS2):** Automatiserad generering av tekniska incidentrapporter för tidig varning (<24 timmar till MSB / CERT-SE).
* **Patientsäkerhet & Reservkraft vid nätverksbortfall (IVO / Lex Maria):** Lokalt krypterad *Fail-Safe Bunker* (SQLite) som säkerställer oavbruten tillgång (<1 ms latens) till 12 akuta kliniska flöden (inklusive kombinerat Cystatin C/Kreatinin eGFR vid hemodialys, ESC 0h/1h troponin-algoritm, mekanisk ventilation, organtransplantation och neonatal säkerhet), kryogen övervakning ($+22^\circ\text{C}$ till $-196^\circ\text{C}\text{ LN}_2$) samt autonom telemetri för **UPS-batterier och dieselreservkraftverk**.
* **Dataskydd & Noll-exfiltrering (IMY / GDPR):** Aktiv vilseledning (*Protocol U.N.I.C.O.R.S.E.*), syntetisk *Honey-Data* med roterande kryptografiska vattenstämplar samt omedelbar radering av en 32-byte (256-bitars) RAM-nyckel (*Protocol S.I.E.R.R.A. Crypto-Shredding*) vid kritiska intrångsförsök.

---

## 🧬 Named Tactical Protocols (Core Bio-Inspired Architecture)

Project VALKYRJA translates human survival physiology (**hemostasis, lymphatic drainage, mitochondrial bioenergetics, and innate/adaptive immunity**) into four specialized defensive protocols:

| Protocol Codename | Official Engineering Acronym | Physiological & Technical Function |
| :--- | :--- | :--- |
| **`Protocol S.O.F.I.A.`** | **S**afeguarded **O**ffline **F**ailover for **I**nfant & **A**cute-care | **NICU (UCIN), Nursery & Maternal Protection:** Generates offline-verifiable `HMAC-SHA256` tokens pairing Mother-Newborn wristbands during network blackouts, locks neonatal gram-weight micro-dosing, and guards obstetric *Code Mater* ($\text{MgSO}_4$ toxicity/Rh). |
| **`Protocol G.A.L.A.`** | **G**uarded **A**utonomous **L**ocal-bunker **A**rchitecture | **12-Pillar Point-of-Care Survival, Cryo & OT Power Watchdog:** Maintains sub-5ms local SQLite continuity across ER, ICU, Hemodialysis, Transplant OR, a 5-tier Thermo-Cryogenic matrix ($+22^\circ\text{C}$ down to $-196^\circ\text{C}$), and isolated UPS/Diesel Generator telemetry. |
| **`Protocol U.N.I.C.O.R.S.E.`** | **U**nending **N**ested **I**llusion & **C**ryptographic **O**bfuscation **R**eflective **S**andbox **E**ngine | **Infinite Mirror Labyrinth & Barium Watermarking:** Traps intruders exploring the system inside a deterministic, procedural RAM filesystem of infinite depth seeded with time-rotating steganographic watermarks (`TRC-XXXX`). |
| **`Protocol S.I.E.R.R.A.`** | **S**ub-millisecond **I**n-memory **E**phemeral **R**AM **R**evocation & **A**udit | **32-Byte RAM Crypto-Shredding & Clinical Locks:** Overwrites the 256-bit master key in volatile RAM with `0x00` in **<1 ms** upon Tier-4 breaches, executes offline clinical safety locks (ESC 0h/1h, Swedish Cystatin C eGFR, DKA Insulin-$K^+$ lock), and compiles the NIS2 dossier. |

---

## 🛡️ Defense Against DDoS & High-Frequency Saturation (Lymphatic Sinkhole)

To prevent volumetric or application-layer **DDoS micro-bursts** from exhausting server sockets inside the Tarpit, `core/1_deception_barium_engine.py` implements a **Lymphatic Drainage & Selectin Priority Architecture**:

1. **Selectin Cryptographic Priority Lane (*Zero-Latency Clinical Bypass*):** Legitimate hospital terminals (ER workstations, ICU ventilators, blood bank scanners) attach a pre-shared hardware HMAC header (`X-Valkyrja-HLA-Token`). Validated in nanoseconds, authentic clinical traffic bypasses throttling via a dedicated QoS lane.
2. **Inter-Arrival Cadence Filter ($\Delta t < 10\text{ ms}$) -> Bottomless Pit Sinkhole:** While human clinicians (>120 ms between actions) and IoMT sensors (rhythmic 1,000 ms telemetry) follow physiological cadences, DDoS bots fire bursts separated by fractions of a millisecond. Unverified sources violating the $\Delta t$ threshold are silently dropped into a zero-memory **Blackhole Sinkhole (`/dev/null`)** without allocating sockets or CPU responses.
3. **Autonomous Local Failover:** If an external ISP pipe is completely saturated, local hospital branches operate autonomously on **Protocol G.A.L.A.** and **Protocol S.O.F.I.A.** with zero clinical downtime.

---

## ⚡ Bioenergetic OT Resilience: Electrical Grid, UPS & Backup Generators

Modern hybrid cyberattacks target hospital **Building Management Systems (BMS) and Operational Technology (OT)** to disrupt electrical power or blind facility engineers during blackouts. Modeling **cellular ATP bioenergetics and hemodynamic centralization**, Project VALKYRJA monitors and protects critical hospital power infrastructure offline:

* **0 ms Phosphocreatine Buffer (*Online Double-Conversion UPS & OR Isolated Power Systems*):** Monitors real-time battery autonomy (`%` and remaining minutes) and Surgical Isolated Power Panels (IPS) feeding ICU mechanical ventilators, ECMO, infusion pumps, and NICU incubators during the transition gap before generators reach nominal voltage.
* **<10 s Anaerobic Glycolysis Failover (*Automatic Transfer Switch [ATS] & Diesel Generators*):** Tracks ATS closure latency, 400V/50.0 Hz phase stability, engine oil/coolant telemetry, and physical **Diesel Fuel Tank Reserves** converted into exact hours of autonomous hospital survival (72h+ Nordic civil preparedness standard).
* **Hemodynamic Centralization (*Automated Non-Clinical Load Shedding*):** If external grid power fails or fuel reserves drop below critical thresholds, the decision engine triggers automated load shedding—disconnecting administrative offices and non-essential HVAC to concentrate **100% of electrical capacity on Emergency Red Outlets** (ER Resuscitation, ICU, NICU, Operating Rooms, Hemodialysis, $-80^\circ\text{C}$ Ultra-Freezers, and Local Bunker Servers).

---

## 🏥 The 12 Acute Clinical Pillars Protected Offline

When external connectivity is severed to contain ransomware, `adapters/4_local_clinical_bunker.py` and `core/2_clinical_nis2_flowchart.py` preserve decision support and vital records across 12 time-critical areas:

1. **Acute Coronary Syndrome (ESC 0h/1h Pathway):** High-sensitivity Troponin (`hs-cTnT`) serial delta calculation for immediate NSTEMI Rule-In/Rule-Out.
2. **Nephrology & Active Hemodialysis / CRRT:** Swedish standard combined **Cystatin C + Creatinine eGFR**, Urea, lethal hyperkalemia ($K^+ \ge 6.5\text{ mmol/L}$) alerts, and ultrafiltration targets.
3. **Acute Liver Failure & Hepatic Encephalopathy:** Venous Ammonia ($\text{NH}_3$), MELD-Na score, West Haven grading, INR, and variceal bleed octreotide/terlipressin locks.
4. **Adult ICU & Invasive Mechanical Ventilation:** Lung-protective ventilation telemetry (Driving Pressure $\Delta P < 15\text{ cmH}_2\text{O}$, $P_{\text{plat}}$, PEEP, $\text{PaO}_2/\text{FiO}_2$ Kirby index).
5. **Operating Rooms & Organ Transplantation (*Scandiatransplant*):** Immutable graft **Cold Ischemia Timer**, ABO/HLA crossmatch verification, and induction immunosuppression.
6. **NICU (UCIN) & Nursery (*Protocol S.O.F.I.A.*):** Cryptographic Mother-Infant wristband dyad lock, gram-based micro-infusion guard, incubator thermoregulation, and bilirubin curves.
7. **Acute Ischemic Stroke (*Code Stroke*):** Mandatory **DOAC / Anticoagulant hard-stop lock** (Apixaban/Rivaroxaban/INR) prior to IV thrombolysis (tPA/Tenecteplase).
8. **Major Trauma & Massive Transfusion:** Uncrossmatched O-Negative reserve, irregular antibodies (*Anti-Kell/Duffy*), ionized calcium ($Ca^{2+}$), lactate, and fibrinogen.
9. **Sepsis-3 & Multidrug-Resistant Pathogens:** Historical **MRSA / ESBL (BLEE) / Carbapenemase** colonization alerts, lethal allergies, and norepinephrine titration.
10. **Obstetric Emergencies (*Code Mater*):** Severe preeclampsia $\text{MgSO}_4$ toxicity guard, postpartum hemorrhage fibrinogen alerts, and Rh isoimmunization.
11. **Endocrine Crises (Diabetic Ketoacidosis - DKA):** Automated **Insulin-Potassium Safety Lock** (strictly blocks IV insulin initiation if serum $K^+ < 3.3\text{ mmol/L}$).
12. **Acute Oncology, Cryogenics ($+22^\circ\text{C}$ to $-196^\circ\text{C}$) & OT Backup Power:** High-dose Methotrexate rescue clocks, febrile neutropenia alerts, thermal telemetry down to **$-196^\circ\text{C}$** ($\text{LN}_2$ stem cells/grafts), and **UPS / Diesel Generator failover protection**.

---

## 🏗️ Hexagonal Repository Structure

```text
project-valkyrja/
├── .github/workflows/
│   └── main.yml                           # Automated GitHub Actions CI (Unit Tests + Simulation)
├── core/                                  # UNIVERSAL SECURITY & DECISION CORE (80%)
│   ├── 1_deception_barium_engine.py       # Tarpit, Barium, Protocol UNICORSE & Lymphatic DDoS Filter
│   ├── 2_clinical_nis2_flowchart.py       # Protocol SIERRA 32-Byte RAM Key & Clinical/NIS2 Locks
│   ├── 3_verbal_shield_mhc1.py            # 60s Rolling Verbal TOTP against AI Voice Cloning
│   └── ports_future_expansions.py         # Hexagonal Protocol Interfaces (Shamir 3-of-5, Vaccines)
├── adapters/                              # DOMAIN-SPECIFIC ADAPTERS (20%)
│   └── 4_local_clinical_bunker.py         # Protocols GALA & SOFIA Offline SQLite Bunker & Power Guard
├── tests/                                 # AUTOMATED VERIFICATION SUITE
│   └── test_core_defenses.py              # Unit tests for all 4 Named Protocols, DDoS & Cryptography
└── 5_valkyrja_dashboard_demo.py           # Unified Command Center & End-to-End Breach Simulator
