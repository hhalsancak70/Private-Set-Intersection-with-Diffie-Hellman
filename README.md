# 🔐 Private Set Intersection using Diffie–Hellman  
A full, educational, and experimentally evaluated implementation of a two-party Private Set Intersection (PSI) protocol using Diffie–Hellman–based blinded hashing.

## 📌 Overview

**Private Set Intersection (PSI)** allows two parties—each holding a private dataset—to learn **only the intersection** of their sets, while revealing *nothing else*.

This repository contains a complete implementation of a **Diffie–Hellman-based PSI protocol**, using blinded modular exponentiation to ensure privacy.  
It also provides benchmarking tools, visualization scripts, and a detailed academic-style report.

This project is ideal for:
- Students learning privacy-preserving computation  
- Cryptography coursework  
- Researchers testing PSI concepts  
- Anyone curious about secure data matching  

---

## ✨ Features

- ✔️ Fully functional DH-based PSI protocol  
- ✔️ Blinded hashing flow: `H(x)^a → H(x)^{ab}`  
- ✔️ Only the intersection is revealed  
- ✔️ Random dataset generator with overlap control  
- ✔️ Runtime benchmarking for multiple set sizes  
- ✔️ CSV export (`results.csv`)  
- ✔️ Runtime visualization (`runtime_plot.png`)  
- ✔️ Clean modular Python code with `Party` abstraction  

---

## 📦 psi-dh-project
│
├── psi_protocol.py # Simple prototype
├── psi_party.py # Full implementation + Party class + benchmarking
├── plot_results.py # Visualization script
│
├── results.csv # Benchmark results (auto-generated)
├── runtime_plot.png # Runtime graph (auto-generated)
│
└── README.md # This documentation


---

## ⚙️ Installation

### Requirements
- Python 3.8+
- matplotlib

Install dependencies:
```bash
pip install matplotlib


