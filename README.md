# 🔐 Private Set Intersection using Diffie–Hellman

A full, educational, and experimentally evaluated implementation of a two-party **Private Set Intersection (PSI)** protocol using Diffie–Hellman–based blinded hashing.

## 📌 Overview

**Private Set Intersection (PSI)** allows two parties—each holding a private dataset—to learn **only the intersection** of their sets, while revealing **nothing else** about the non-intersecting elements.

This repository contains a complete implementation of a Diffie–Hellman-based PSI protocol. It utilizes blinded modular exponentiation to ensure privacy throughout the exchange. The project also provides benchmarking tools, visualization scripts, and generates detailed reports.

**This project is ideal for:**
* Students learning privacy-preserving computation
* Cryptography coursework and assignments
* Researchers testing PSI concepts
* Anyone curious about secure data matching techniques

---

## ✨ Features

* ✔️ **Fully functional DH-based PSI protocol**
* ✔️ **Blinded hashing flow:** Implements the secure exchange `H(x)^a` → `H(x)^ab`
* ✔️ **Privacy First:** Only the intersection is revealed; raw data is never exposed.
* ✔️ **Dataset Generator:** Includes a random dataset generator with configurable overlap (intersection size).
* ✔️ **Benchmarking:** Automated runtime benchmarking for multiple set sizes.
* ✔️ **Data Export:** Automatically saves results to `results.csv`.
* ✔️ **Visualization:** Generates performance graphs (`runtime_plot.png`) via Matplotlib.
* ✔️ **Modular Code:** Clean Python implementation using a `Party` class abstraction.

---

## 📦 Project Structure

```text
psi-dh-project/
│
├── psi_protocol.py   # Simple prototype / Basic logic implementation
├── psi_party.py      # Full implementation + Party class + Benchmarking suite
├── plot_results.py   # Visualization script (generates graphs from CSV)
│
├── results.csv       # Benchmark results (auto-generated)
├── runtime_plot.png  # Runtime graph (auto-generated)
│
└── README.md         # This documentation


---

## ⚙️ Installation

### Requirements
- Python 3.8+
- matplotlib

Install dependencies:
```bash
pip install matplotlib


