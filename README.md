# ContractLens — Visual Contract Intelligence Dashboard (Local AI Powered)

A source-grounded visual contract intelligence system built strictly according to the **Product Development Document (PDD)** and **Technical Design Architecture (TDA)**.

> **Governing Design Principle:** `Traceability > Intelligence > Visual Polish`  
> Every single financial amount, deadline, obligation, and attention finding is deterministically grounded with exact page, section, bounding box (`bbox`), and raw excerpt coordinates.

---

## ⚡ Local AI Integration & Model Selection

ContractLens connects directly to your machine's local AI runtimes (**Ollama** and **LM Studio**):
- **Choose Your Evaluating Model:** Switch seamlessly between models in the header or in the Evaluation Studio:
  - `qwen2.5-coder:7b` (Ollama — Recommended for structured extraction)
  - `qwen2.5-coder:1.5b` (Ollama — High-speed evaluation)
  - `gpt-3.5-turbo:latest` (Ollama)
  - `google/gemma-4-e4b` (LM Studio)
  - Custom local OpenAI-compatible endpoints
- **Zero Cloud Leakage:** 100% of legal analysis runs on your local GPU/CPU.
- **Evidence Substring Gate:** Every claim extracted by the local model is deterministically cross-referenced against the raw contract text before being presented to the user.

---

## 🌟 Core Views

1. **⚡ AI Evaluation Studio (`#view-evaluate`) — *Where You Put Contracts In***
   - **File Upload:** Drag & drop any `.pdf`, `.txt`, `.docx`, or `.md` contract to extract text and page counts.
   - **Interactive Editor:** Paste raw clauses with preset loaders (*Residential Lease*, *Commercial Office Tenancy*, *Employment NDA*, *Standard 2BHK*).
   - **Model Selector & Rigor Controls:** Configure model, extraction depth (*Full 5-View*, *Risk Triage*, *Financials*), and temperature.
   - **Live Pipeline Console:** Real-time progress monitoring through chunking, LLM extraction, Pydantic schema validation, and Contract IR compilation.

2. **Overview View (`#view-overview`)**
   - **Executive Decision Map (3 Pillars):** *What You Agree To*, *What Could Hurt You*, and *What You Must Do*.
   - **Vitals Bar:** Monthly Rent, Security Deposit, Attention Flags, and Escalation Caps.
   - **Technical Provenance Chip:** Pydantic v2.8 schema compliance, SHA-256 hash, and 100% provenance verification status.
   - **Live Grounded Canvas Viewport:** Flash-syncs bounding box coordinates upon clicking any finding.

3. **Attention View (`#view-attention`)**
   - **Ranked Attention Stream:** Categorized by severity tiers (🔴 High, 🟠 Medium, 🟡 Low) without artificial numerical risk scores.
   - **Interactive Filtering:** Filter by tier, category dropdown, or full-text search across titles and clauses.
   - **Deep Finding Inspector Panel (Sticky):**
     - Canonical source ID (e.g. `#SRC-07214`).
     - Verbatim excerpt with `<mark>` visual callouts.
     - Plain-English operational implications.
     - **Ambiguity Diagnostic Flag:** Displays `PASS` or `⚠ The contract does not clearly specify…`.
     - Direct jump to source coordinates in Document viewer.

4. **Money View (`#view-money`)**
   - **Financial Exposure Digest:** Sourced breakdown of Monthly Recurring commitments, Upfront Capital Required, and Maximum Conditional Liabilities.
   - **Itemized Financial Schedule:** Every ₹ amount links to its canonical clause and bounding box.
   - **Escalation Simulator:** Interactive scenario comparison between timely mutual renewal vs unregistered holdover penalty.

5. **Timeline View (`#view-timeline`)**
   - **11-Month Horizon Tracker:** Interactive visual node track (D-0, Monthly 5th, D-180, D-275, D-305, D-335).
   - **Operational Bento Cards:** Side-by-side comparison of *Required Action* vs *Legal Consequence*.
   - **One-Click Calendar Sync (.ics):** Generates and downloads an RFC 5545 `.ics` file for importing all deadlines directly into Google Calendar, Outlook, or Apple Calendar.

6. **Document View (`#view-document`)**
   - **Synchronized Document Surface:** High-fidelity simulation of the lease agreement with interactive bounding boxes (`bbox: [ymin, xmin, ymax, xmax]`).
   - **Bidirectional Highlights:** Clicking a finding in any dashboard jumps directly to the page and flashes the bounding box. Clicking a highlighted clause on the page instantly populates the inspection drawer.

7. **💬 Grounded AI Q&A Assistant**
   - Chat drawer in the bottom right corner allowing users to ask natural-language questions directly to the chosen local AI model with grounded citations.

---

## 🚀 How to Run

### Method 1: Local AI Backend (FastAPI + Ollama) [Recommended]
Double-click `start_dashboard.bat` or run:
```powershell
cd d:\Code\ContractLens
python backend_server.py
```
Then visit [http://localhost:8000](http://localhost:8000) in your browser.

### Method 2: Standalone Browser Mode
Open `d:\Code\ContractLens\index.html` directly in any web browser. It will connect to your local Ollama daemon at `http://localhost:11434` or use the embedded Contract IR engine.

---

## 📂 File Structure
```
d:\Code\ContractLens/
├── backend_server.py    # FastAPI local AI backend (Ollama/LM Studio connector & parser)
├── index.html           # Master 6-view responsive dashboard & AI studio
├── contract-ir.js       # Canonical Contract IR data models & sample leases
├── start_dashboard.bat  # 1-click startup batch script
├── .gitignore           # Git ignore patterns
├── LICENSE              # MIT License
└── README.md            # Technical documentation & guide
```
