# ContractLens — Visual Contract Intelligence Dashboard (Option A Frontend)

A source-grounded visual contract intelligence system built strictly according to the **Product Development Document (PDD)** and **Technical Design Architecture (TDA)**.

> **Governing Design Principle:** `Traceability > Intelligence > Visual Polish`  
> Every single financial amount, deadline, obligation, and attention finding is deterministically grounded with exact page, section, bounding box (`bbox`), and raw excerpt coordinates.

---

## 🌟 Core Features & The Five Synchronized Views

1. **Overview View (`#view-overview`)**
   - **Executive Decision Map (3 Pillars):** *What You Agree To*, *What Could Hurt You*, and *What You Must Do*.
   - **Vitals Bar:** Monthly Rent (₹85,000/mo), Security Deposit (₹3,50,000), 7 Flagged Attention Items, and Escalation Caps.
   - **Technical Provenance Chip:** Pydantic v2.8 schema compliance, SHA-256 verification hash, and coordinate sync indicator.
   - **Live Grounded Canvas Viewport:** Flash-syncs bounding box coordinates upon clicking any finding.

2. **Attention View (`#view-attention`)**
   - **Ranked Attention Stream:** Categorized by severity tiers (🔴 High, 🟠 Medium, 🟡 Low) without artificial numerical risk scores.
   - **Interactive Filtering:** Filter by tier, category dropdown, or full-text search across titles and clauses.
   - **Deep Finding Inspector Panel (Sticky):**
     - Canonical source ID (e.g. `#SRC-07214`).
     - Verbatim excerpt with `<mark>` visual callouts.
     - Plain-English operational implications.
     - **Ambiguity Diagnostic Flag:** Displays `PASS` or `⚠ The contract does not clearly specify…`.
     - Direct jump to source coordinates in Document viewer.

3. **Money View (`#view-money`)**
   - **Financial Exposure Digest:** Sourced breakdown of Monthly Recurring commitments (₹92,500/mo), Upfront Capital Required (₹4,35,000), and Maximum Conditional Liabilities (₹90,000).
   - **Itemized Financial Schedule:** Every ₹ amount links to its canonical clause and bounding box.
   - **Escalation Simulator:** Interactive scenario comparison between timely mutual renewal (5% cap = ₹89,250) vs unregistered holdover penalty (10% surcharge = ₹93,500).

4. **Timeline View (`#view-timeline`)**
   - **11-Month Horizon Tracker:** Interactive visual node track (D-0, Monthly Recurring 5th, D-180, D-275, D-285, D-335).
   - **Operational Bento Cards:** Side-by-side comparison of *Required Action* vs *Legal Consequence*.
   - **One-Click Calendar Sync (.ics):** Generates and downloads an RFC 5545 `.ics` file for importing all 6 deadlines directly into Google Calendar, Outlook, or Apple Calendar.

5. **Document View (`#view-document`)**
   - **Synchronized Document Surface:** High-fidelity simulation of the 22-page residential lease agreement.
   - **Bidirectional Highlights:** Clicking a finding in any dashboard jumps directly to the page and flashes the bounding box. Clicking a highlighted clause on the page instantly populates the inspection drawer.
   - **Page Navigation:** Previous/Next controls, direct page jump, and zoom controls.

---

## 🚀 How to Run

### Method 1: Local HTTP Server (Recommended)
Double-click `start_dashboard.bat` or run:
```bash
cd d:\Code\ContractLens
python -m http.server 8000
```
Then visit [http://localhost:8000](http://localhost:8000) in your browser.

### Method 2: Direct File Open
Open `d:\Code\ContractLens\index.html` directly in any web browser (Chrome, Edge, Firefox, Safari).

---

## 📂 File Structure
```
d:\Code\ContractLens/
├── index.html           # Master 5-view responsive application
├── contract-ir.js       # Canonical Contract IR data models & sample leases
├── start_dashboard.bat  # 1-click startup batch script
└── README.md            # Technical documentation & guide
```
