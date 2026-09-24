/**
 * ContractLens - Canonical Contract Intermediate Representation (Contract IR)
 * Strictly conforms to Section 7.4 & Section 10 of the Product Development Document (PDD)
 * and Technical Design Architecture (TDA).
 *
 * Invariant: Every financial term, deadline, obligation, and finding MUST link to a source_id.
 */

const CONTRACT_IR_DATABASE = {
  "doc-palm-meadows-2026": {
    metadata: {
      id: "doc-palm-meadows-2026",
      filename: "Residential Lease Agreement — 4BHK Palm Meadows.pdf",
      title: "Residential Lease Agreement (Unit Villa #42, Palm Meadows)",
      parties: [
        {
          role: "Lessor",
          name: "Brigade Horizon Estates Pvt Ltd",
          rep: "Vikramaditya Rao (Director)",
          reg: "CIN: U70102KA2018PTC118921",
          jurisdiction: "Bengaluru, Karnataka, India"
        },
        {
          role: "Lessee",
          name: "Arjun Sharma & Priya Sharma",
          type: "Joint Tenancy",
          kyc_status: "Verified (Aadhaar / PAN)"
        }
      ],
      effective_date: "2026-10-15",
      expiration_date: "2027-09-14",
      tenure_months: 11,
      page_count: 22,
      sha256: "9b2d87e0fa481e39a5d140e7cb281146fc2019488172901237c81a941bca9082",
      status: "COMPLETED",
      engine_version: "v2.4-GROUNDED",
      pydantic_validation: "Pass (Strict v2.8)",
      traceability_rate: 100
    },

    sources: {
      "SRC-01202": {
        id: "SRC-01202",
        page: 2,
        section_label: "Sec 1.2",
        bbox: [48, 110, 540, 165],
        text: "The demised premises situated at Villa No. 42, Palm Meadows Boulevard, Whitefield, Bengaluru 560066 comprising 4,250 sq.ft built-up area shall be leased strictly for residential purposes of the Lessee and immediate family."
      },
      "SRC-02102": {
        id: "SRC-02102",
        page: 2,
        section_label: "Sec 2.1",
        bbox: [40, 210, 530, 275],
        text: "The lease term shall be for an initial period of eleven (11) consecutive months commencing on the 15th day of October 2026 ('Commencement Date') and concluding automatically on the 14th day of September 2027 ('Expiration Date')."
      },
      "SRC-02303": {
        id: "SRC-02303",
        page: 3,
        section_label: "Sec 2.3",
        bbox: [42, 118, 498, 180],
        text: "The Lessee shall complete and sign the joint move-in inventory report within forty-eight (48) hours of receiving physical keys. Failure to intimate discrepancies in writing within said 48 hours shall deem all woodwork, HVAC, and sanitary fixtures to be accepted in immaculate defect-free order."
      },
      "SRC-03104": {
        id: "SRC-03104",
        page: 4,
        section_label: "Sec 3.1",
        bbox: [50, 95, 520, 155],
        text: "The agreed monthly consideration for the demised premises shall be INR 85,000/- (Rupees Eighty-Five Thousand only), payable strictly in advance on or before the 5th day of each calendar month via electronic fund transfer."
      },
      "SRC-03304": {
        id: "SRC-03304",
        page: 4,
        section_label: "Sec 3.3",
        bbox: [88, 204, 510, 252],
        text: "Any installment of rent received after the 10th calendar day of the due month shall attract a mandatory penal late charge of INR 500/- (Rupees Five Hundred only) per day of delay computed from the 6th day until realized clearance."
      },
      "SRC-03405": {
        id: "SRC-03405",
        page: 5,
        section_label: "Sec 3.4",
        bbox: [80, 210, 510, 260],
        text: "Should the Lessee continue in occupation of the demised premises post expiry of the eleven-month term without executing a fresh registered agreement at least 30 days prior, monthly rent shall automatically escalate by 10.0% (Ten percent) per month."
      },
      "SRC-04206": {
        id: "SRC-04206",
        page: 6,
        section_label: "Sec 4.2",
        bbox: [60, 130, 515, 195],
        text: "The interest-free refundable security deposit of INR 3,50,000/- shall be refunded by the Lessor via bank wire within thirty (30) days from the date of peaceful physical handover of vacant possession and keys, subject to lawful deductions."
      },
      "SRC-04507": {
        id: "SRC-04507",
        page: 7,
        section_label: "Sec 4.5",
        bbox: [110, 580, 490, 620],
        text: "At the time of vacating, the Lessor is unconditionally entitled to deduct a flat sum of INR 25,000/- (Rupees Twenty-Five Thousand only) from the security deposit towards professional painting and mechanized restoration, irrespective of tenure duration or normal wear and tear."
      },
      "SRC-05108": {
        id: "SRC-05108",
        page: 8,
        section_label: "Sec 5.1",
        bbox: [45, 150, 520, 210],
        text: "In addition to rent, the Lessee shall pay monthly society maintenance charges of INR 7,500/- directly to the Palm Meadows Owners Association (PMOA) account on or before the 10th of every month."
      },
      "SRC-05209": {
        id: "SRC-05209",
        page: 9,
        section_label: "Sec 5.2",
        bbox: [105, 410, 510, 445],
        text: "The Lessee shall obtain and deliver an official BESCOM electricity final zero-dues clearance certificate and NOC within seven (7) days of lease termination; pending which the Lessor may retain an interim contingency hold of INR 15,000/-."
      },
      "SRC-07113": {
        id: "SRC-07113",
        page: 13,
        section_label: "Sec 7.1",
        bbox: [80, 310, 510, 390],
        text: "Subject to Clause 7.2, either party may terminate this lease after completion of the lock-in period by issuing sixty (60) calendar days prior written notice. Notice must be served exclusively by Indian Registered Post A.D. Email, WhatsApp, and courier intimations are expressly non-binding."
      },
      "SRC-07214": {
        id: "SRC-07214",
        page: 14,
        section_label: "Sec 7.2",
        bbox: [120, 450, 520, 490],
        text: "The initial six (6) months from the Commencement Date shall constitute a mandatory lock-in period. In the event the Lessee vacates prior to completion of 180 days, the Lessee shall pay a liquidated damages fee of INR 50,000/- and the Lessor retains the right to withhold the entirety of the Security Deposit until a replacement tenant is secured."
      },
      "SRC-08416": {
        id: "SRC-08416",
        page: 16,
        section_label: "Sec 8.4",
        bbox: [65, 230, 525, 285],
        text: "The Lessee shall ensure certified biannual preventive maintenance servicing of all six (6) installed Daikin split air conditioning units and retain authorized OEM service receipts. Failure to produce invoices upon inspection attracts an HVAC replacement charge."
      },
      "SRC-09118": {
        id: "SRC-09118",
        page: 18,
        section_label: "Sec 9.1",
        bbox: [100, 150, 500, 195],
        text: "The Lessor and authorized representatives/brokers shall have the right to enter and inspect the premises or conduct prospective buyer showings at reasonable daytime hours upon providing twenty-four (24) hours advance digital or telephonic intimation."
      }
    },

    financial_terms: [
      {
        id: "FT-01",
        source_id: "SRC-03104",
        label: "Base Monthly Rent",
        amount: 85000,
        currency: "INR",
        frequency: "monthly",
        trigger: "Due 5th of each calendar month in advance",
        evidence: "INR 85,000/- (Rupees Eighty-Five Thousand only), payable strictly in advance on or before the 5th day of each calendar month",
        confidence: 1.0,
        type: "recurring_commitment"
      },
      {
        id: "FT-02",
        source_id: "SRC-05108",
        label: "Society Maintenance Charges",
        amount: 7500,
        currency: "INR",
        frequency: "monthly",
        trigger: "Payable directly to Palm Meadows Owners Association by 10th",
        evidence: "monthly society maintenance charges of INR 7,500/- directly to the Palm Meadows Owners Association (PMOA)",
        confidence: 1.0,
        type: "recurring_commitment"
      },
      {
        id: "FT-03",
        source_id: "SRC-04206",
        label: "Refundable Security Deposit",
        amount: 350000,
        currency: "INR",
        frequency: "one_time",
        trigger: "Paid upon execution; refundable within 30 days post keys handover",
        evidence: "refundable security deposit of INR 3,50,000/- shall be refunded by the Lessor via bank wire within thirty (30) days",
        confidence: 1.0,
        type: "upfront_capital"
      },
      {
        id: "FT-04",
        source_id: "SRC-03104",
        label: "Advance First Month Rent",
        amount: 85000,
        currency: "INR",
        frequency: "one_time",
        trigger: "Execution of agreement before possession",
        evidence: "payable strictly in advance on or before the 5th day",
        confidence: 1.0,
        type: "upfront_capital"
      },
      {
        id: "FT-05",
        source_id: "SRC-07214",
        label: "Early Termination Liquidated Damages",
        amount: 50000,
        currency: "INR",
        frequency: "other",
        trigger: "Vacating during initial 6-month (180-day) lock-in period",
        evidence: "liquidated damages fee of INR 50,000/- and the Lessor retains the right to withhold the entirety of the Security Deposit",
        confidence: 1.0,
        type: "latent_liability"
      },
      {
        id: "FT-06",
        source_id: "SRC-04507",
        label: "Standard Painting & Deep Clean Deduction",
        amount: 25000,
        currency: "INR",
        frequency: "one_time",
        trigger: "Automatically deducted from deposit at exit regardless of condition",
        evidence: "flat sum of INR 25,000/- (Rupees Twenty-Five Thousand only) from the security deposit towards professional painting",
        confidence: 1.0,
        type: "latent_liability"
      },
      {
        id: "FT-07",
        source_id: "SRC-03304",
        label: "Daily Late Rent Charge",
        amount: 500,
        currency: "INR",
        frequency: "other",
        trigger: "Charged per day of delay for payments made after the 10th",
        evidence: "penal late charge of INR 500/- (Rupees Five Hundred only) per day of delay computed from the 6th day",
        confidence: 1.0,
        type: "contingent_penalty"
      },
      {
        id: "FT-08",
        source_id: "SRC-05209",
        label: "BESCOM Contingency Hold",
        amount: 15000,
        currency: "INR",
        frequency: "other",
        trigger: "Retained if final zero-dues power bill not furnished in 7 days",
        evidence: "interim contingency hold of INR 15,000/-",
        confidence: 1.0,
        type: "contingent_penalty"
      }
    ],

    deadlines: [
      {
        id: "DL-01",
        source_id: "SRC-02303",
        date: "2026-10-15",
        relative_label: "Day 0 (Commencement)",
        event: "Move-in Inventory Dispute Cutoff",
        consequence: "Failure to dispute inventory in 48 hours legally deems fixtures and woodwork in pristine condition.",
        action: "Conduct thorough photo walkthrough and submit written defects list before Oct 17, 2026 (48 hours).",
        category: "payment",
        attention_tier: "high",
        confidence: 1.0
      },
      {
        id: "DL-02",
        source_id: "SRC-03304",
        date: "Recurring (5th - 10th)",
        relative_label: "5th of each month",
        event: "Monthly Rent Grace Cutoff",
        consequence: "Accrues daily penalty of ₹500/day retroactive to 6th if payment not cleared by 23:59 IST on 10th.",
        action: "Set automated recurring bank mandate for 3rd of each month.",
        category: "payment",
        attention_tier: "medium",
        confidence: 1.0
      },
      {
        id: "DL-03",
        source_id: "SRC-07214",
        date: "2027-04-14",
        relative_label: "Day 180 (Month 6)",
        event: "6-Month Mandatory Lock-in Expiry",
        consequence: "Early termination fee liability of ₹50,000 drops off permanently after 23:59 IST.",
        action: "Tenancy enters flexible notice term; normal 60-day notice becomes permissible.",
        category: "critical",
        attention_tier: "high",
        confidence: 1.0
      },
      {
        id: "DL-04",
        source_id: "SRC-07113",
        date: "2027-07-16",
        relative_label: "Day 275 (60d before end)",
        event: "60-Day Termination Notice Window",
        consequence: "Late notice forfeits 1 full month rent equivalent (₹85,000) automatically deducted from deposit.",
        action: "Dispatch formal written letter strictly via Indian Post Registered A.D. with tracking.",
        category: "notice",
        attention_tier: "high",
        confidence: 1.0
      },
      {
        id: "DL-05",
        source_id: "SRC-03405",
        date: "2027-08-15",
        relative_label: "Day 305 (30d before end)",
        event: "Renewal Agreement Execution Cutoff",
        consequence: "Holdover triggers automatic 10% rent escalation (₹93,500/mo) if new agreement isn't registered.",
        action: "Conclude renewal negotiation and execute secondary deed with sub-registrar.",
        category: "notice",
        attention_tier: "medium",
        confidence: 1.0
      },
      {
        id: "DL-06",
        source_id: "SRC-04206",
        date: "2027-09-14",
        relative_label: "Day 335 (Term Expiry)",
        event: "Lease Expiry & Joint Handover Inspection",
        consequence: "30-day statutory window starts for security deposit refund (₹3,25,000 net).",
        action: "Handover keys, deliver BESCOM NOC, sign exit handover certificate.",
        category: "critical",
        attention_tier: "medium",
        confidence: 1.0
      }
    ],

    findings: [
      {
        id: "F-01",
        source_id: "SRC-07214",
        category: "Financial Penalty",
        title: "Early Termination Penalty & Lock-in Clause",
        severity_tier: "high",
        explanation: "Vacating prior to completion of the 6-month lock-in obligates tenant to pay a fixed ₹50,000 liquidation penalty in addition to potential deposit retention until re-let.",
        matters: "You are legally committing to a mandatory 6-month minimum occupancy. If your job relocates or you must leave for unforeseen reasons during these first 180 days, you will forfeit ₹50,000 cash and potentially wait months to recover your deposit while the landlord looks for a replacement tenant.",
        bullets: [
          "Immediate monetary forfeiture of ₹50,000 upon early vacation.",
          "Deposit refund timeline becomes contingent on third-party tenant acquisition.",
          "Notice period cannot offset or substitute for the liquidated cash fee."
        ],
        evidence: "The initial six (6) months from the Commencement Date shall constitute a mandatory lock-in period. In the event the Lessee vacates prior to completion of 180 days, the Lessee shall pay a liquidated damages fee of INR 50,000/-",
        ambiguity_detected: false,
        ambiguity_note: "No ambiguity detected in calculation trigger or monetary assignment.",
        confidence: 1.0,
        validation_status: "PASSED"
      },
      {
        id: "F-02",
        source_id: "SRC-03405",
        category: "Renewal & Rent Escalation",
        title: "Automatic 10% Escalation on Holdover / Renewal",
        severity_tier: "high",
        explanation: "If the lease continues past 11 months on verbal agreement or without formal sub-registrar renewal execution, baseline rent automatically jumps by 10% (₹93,500/mo).",
        matters: "If you do not proactively notify or sign your extension at least 30 days before lease expiration, your monthly rent automatically rises by ₹8,500/month without further negotiation.",
        bullets: [
          "Escalation activates by default without bilateral affirmative agreement.",
          "30-day pre-renewal deadline must be strictly diarized.",
          "Increases baseline liability immediately upon holdover."
        ],
        evidence: "without executing a fresh registered agreement at least 30 days prior, monthly rent shall automatically escalate by 10.0% (Ten percent) per month.",
        ambiguity_detected: true,
        ambiguity_note: "⚠ The contract does not clearly specify which party bears registration stamp duty charges for the secondary term renewal deed.",
        confidence: 0.95,
        validation_status: "PASSED"
      },
      {
        id: "F-03",
        source_id: "SRC-07113",
        category: "Notice & Procedure",
        title: "60-Day Prior Written Notice by Registered Post Only",
        severity_tier: "medium",
        explanation: "Either party may terminate after lock-in by providing 60 full calendar days notice strictly via physical Indian Post Registered A.D. Electronic intimations are non-binding.",
        matters: "Sending an email or messaging your landlord will not legally count as notice. If you give notice via WhatsApp, the landlord could legally claim no notice was received and charge additional months of rent.",
        bullets: [
          "Physical post tracking receipt required as legal proof of service.",
          "Digital communications explicitly disclaimed.",
          "Notice time counts only upon actual physical postal delivery date."
        ],
        evidence: "Notice must be served exclusively by Indian Registered Post A.D. Email, WhatsApp, and courier intimations are expressly non-binding.",
        ambiguity_detected: true,
        ambiguity_note: "⚠ The contract does not clearly specify transit delivery grace periods for postal delays.",
        confidence: 0.98,
        validation_status: "PASSED"
      },
      {
        id: "F-04",
        source_id: "SRC-04507",
        category: "Deductions & Maintenance",
        title: "Mandatory Standard Painting Deduction (₹25,000)",
        severity_tier: "medium",
        explanation: "Landlord holds right to deduct a flat sum of ₹25,000 from security deposit for repainting and deep clean irrespective of actual wear and tear standards.",
        matters: "Even if you maintain the walls immaculately or have them professionally repainted before handing over the keys, ₹25,000 will be permanently withheld from your deposit.",
        bullets: [
          "Fixed financial deduction not tied to real wear-and-tear damages.",
          "Cannot be disputed with move-out photographic inspection logs."
        ],
        evidence: "flat sum of INR 25,000/- (Rupees Twenty-Five Thousand only) from the security deposit towards professional painting and mechanized restoration, irrespective of tenure duration or normal wear and tear.",
        ambiguity_detected: false,
        ambiguity_note: "Deduction trigger is unambiguous and non-contingent.",
        confidence: 1.0,
        validation_status: "PASSED"
      },
      {
        id: "F-05",
        source_id: "SRC-09118",
        category: "Inspection & Entry Rights",
        title: "24-Hour Right of Entry for Prospective Showings",
        severity_tier: "medium",
        explanation: "Landlord and brokers reserve the right to enter and show premises to prospective buyers/tenants upon giving 24 hours telephonic or digital notice.",
        matters: "The landlord or brokers may request entry multiple times weekly if the property is being listed for sale or subsequent re-lease, disrupting privacy.",
        bullets: [
          "Verbal/telephonic notification allows disputed notice records.",
          "No stated limit on frequency or specific daytime window limits."
        ],
        evidence: "right to enter and inspect the premises or conduct prospective buyer showings at reasonable daytime hours upon providing twenty-four (24) hours advance digital or telephonic intimation.",
        ambiguity_detected: true,
        ambiguity_note: "⚠ The contract does not clearly specify daytime entry boundaries or reasonable showing frequency.",
        confidence: 0.94,
        validation_status: "PASSED"
      },
      {
        id: "F-06",
        source_id: "SRC-03304",
        category: "Late Payment Interest",
        title: "Late Fee of ₹500/day after 10th of Month",
        severity_tier: "low",
        explanation: "Daily penal charge of ₹500 automatically accrued for payments cleared post 23:59 IST on the 10th calendar day, calculated retroactively from the 6th.",
        matters: "Standard commercial late payment structure. You have a 10-day window to pay each month before the daily ₹500 fee begins accruing retroactively.",
        bullets: [
          "10-day grace period provided.",
          "Daily late fee ₹500 activates automatically on day 11."
        ],
        evidence: "penal late charge of INR 500/- (Rupees Five Hundred only) per day of delay computed from the 6th day until realized clearance.",
        ambiguity_detected: false,
        ambiguity_note: "Clear temporal cut-off and fixed daily calculation rate.",
        confidence: 1.0,
        validation_status: "PASSED"
      },
      {
        id: "F-07",
        source_id: "SRC-05209",
        category: "Utility Transfer & Metering",
        title: "Electricity NOC & Clearance Receipt within 7 Days",
        severity_tier: "low",
        explanation: "Tenant must provide final zero-dues electricity board (BESCOM) clearance certificate before remaining deposit disbursement; failure permits ₹15k hold.",
        matters: "Standard procedural requirement. Keep your final electricity payment receipts to ensure your final settlement is not delayed by the ₹15,000 contingency hold.",
        bullets: [
          "7-day timeline to submit final power utility zero-dues bill.",
          "Contingency hold of ₹15,000 released upon presentation."
        ],
        evidence: "deliver an official BESCOM electricity final zero-dues clearance certificate and NOC within seven (7) days of lease termination; pending which the Lessor may retain an interim contingency hold of INR 15,000/-.",
        ambiguity_detected: false,
        ambiguity_note: "Exact documentation requirements and timeline are stated clearly.",
        confidence: 1.0,
        validation_status: "PASSED"
      }
    ],

    clauses: [
      {
        id: "CLS-01",
        section: "1.1",
        title: "Parties & Definitions",
        page: 1,
        bbox: [50, 100, 520, 220],
        type: "definitions",
        summary: "Identifies Lessor (Brigade Horizon Estates) and Lessees (Arjun & Priya Sharma)."
      },
      {
        id: "CLS-02",
        section: "1.2",
        title: "Demised Premises Description",
        page: 2,
        bbox: [48, 110, 540, 165],
        type: "demise",
        summary: "Villa 42 Palm Meadows (4,250 sq.ft) restricted strictly to private residential usage."
      },
      {
        id: "CLS-03",
        section: "2.1",
        title: "Tenure & Term Duration",
        page: 2,
        bbox: [40, 210, 530, 275],
        type: "tenure",
        summary: "11-month term from 15 Oct 2026 to 14 Sep 2027."
      },
      {
        id: "CLS-04",
        section: "2.3",
        title: "Move-in Inspection & Inventory Protocol",
        page: 3,
        bbox: [42, 118, 498, 180],
        type: "inventory",
        summary: "48-hour defect notification cutoff for fixtures, woodwork, and HVAC."
      },
      {
        id: "CLS-05",
        section: "3.1",
        title: "Monthly Rent Amount & Due Date",
        page: 4,
        bbox: [50, 95, 520, 155],
        type: "rent",
        summary: "₹85,000/month due on or before 5th of each calendar month."
      },
      {
        id: "CLS-06",
        section: "3.3",
        title: "Late Payment Penal Interest",
        page: 4,
        bbox: [88, 204, 510, 252],
        type: "penalty",
        summary: "Grace till 10th; ₹500/day penal fee retroactive to 6th thereafter."
      },
      {
        id: "CLS-07",
        section: "3.4",
        title: "Rent Escalation & Holdover Terms",
        page: 5,
        bbox: [80, 210, 510, 260],
        type: "escalation",
        summary: "Automatic 10% rent escalation if secondary lease is not executed 30 days prior."
      },
      {
        id: "CLS-08",
        section: "4.1",
        title: "Interest-Free Security Deposit Quantum",
        page: 6,
        bbox: [55, 90, 510, 140],
        type: "deposit",
        summary: "₹3,50,000 interest-free refundable deposit paid prior to possession."
      },
      {
        id: "CLS-09",
        section: "4.2",
        title: "Deposit Refund Timeline & Conditions",
        page: 6,
        bbox: [60, 130, 515, 195],
        type: "deposit_refund",
        summary: "Refundable within 30 days of vacant key handover subject to lawful deductions."
      },
      {
        id: "CLS-10",
        section: "4.5",
        title: "Painting & Refurbishment Deduction",
        page: 7,
        bbox: [110, 580, 490, 620],
        type: "deduction",
        summary: "Mandatory flat ₹25,000 deduction from deposit for turnover painting."
      },
      {
        id: "CLS-11",
        section: "5.1",
        title: "Society Maintenance Direct Debit",
        page: 8,
        bbox: [45, 150, 520, 210],
        type: "maintenance",
        summary: "₹7,500/mo payable directly to Palm Meadows Owners Association by 10th."
      },
      {
        id: "CLS-12",
        section: "5.2",
        title: "Utilities & Electricity Clearance",
        page: 9,
        bbox: [105, 410, 510, 445],
        type: "utilities",
        summary: "BESCOM zero-dues receipt required in 7 days; ₹15,000 contingency hold authorized."
      },
      {
        id: "CLS-13",
        section: "7.1",
        title: "Termination Notice Formalities",
        page: 13,
        bbox: [80, 310, 510, 390],
        type: "notice",
        summary: "60-day prior notice required strictly via Indian Post Registered A.D."
      },
      {
        id: "CLS-14",
        section: "7.2",
        title: "Mandatory Lock-in & Early Termination Penalty",
        page: 14,
        bbox: [120, 450, 520, 490],
        type: "lock_in",
        summary: "6-month compulsory lock-in; ₹50,000 liquidated fee plus deposit withholding upon break."
      },
      {
        id: "CLS-15",
        section: "8.4",
        title: "HVAC & Electrical Maintenance Obligation",
        page: 16,
        bbox: [65, 230, 525, 285],
        type: "obligation",
        summary: "Tenant must perform certified biannual AC servicing and retain OEM receipts."
      },
      {
        id: "CLS-16",
        section: "9.1",
        title: "Landlord Inspection & Broker Showings",
        page: 18,
        bbox: [100, 150, 500, 195],
        type: "access",
        summary: "24-hour advance digital/telephonic notice for inspections or showings."
      }
    ]
  },

  // Second sample contract for upload demo switching
  "doc-koramangala-2026": {
    metadata: {
      id: "doc-koramangala-2026",
      filename: "Corporate Apartment Lease — Koramangala 4th Block.pdf",
      title: "Corporate Residential Lease Agreement (Flat 302, Prestige Oasis)",
      parties: [
        {
          role: "Lessor",
          name: "Suresh & Meenakshi Narayanan",
          rep: "Individual Landlords",
          reg: "N/A",
          jurisdiction: "Bengaluru, Karnataka"
        },
        {
          role: "Lessee",
          name: "Zenith Cognitive Systems Pvt Ltd (Emp: Tanmay Sen)",
          type: "Corporate Tenancy",
          kyc_status: "Verified (CIN & GSTIN)"
        }
      ],
      effective_date: "2026-11-01",
      expiration_date: "2027-10-31",
      tenure_months: 12,
      page_count: 16,
      sha256: "3f9801ec2912440b8a1c97ef012019488172901237c81a941bca90829b2d87e0",
      status: "COMPLETED",
      engine_version: "v2.4-GROUNDED",
      pydantic_validation: "Pass (Strict v2.8)",
      traceability_rate: 100
    },
    sources: {
      "SRC-KM-01": {
        id: "SRC-KM-01",
        page: 3,
        section_label: "Sec 3.1",
        bbox: [60, 100, 520, 150],
        text: "Monthly rental shall be INR 62,000/- inclusive of society maintenance charges."
      },
      "SRC-KM-02": {
        id: "SRC-KM-02",
        page: 5,
        section_label: "Sec 4.1",
        bbox: [70, 120, 510, 170],
        text: "Security deposit shall be INR 3,00,000/- refundable within 15 working days post move-out."
      },
      "SRC-KM-03": {
        id: "SRC-KM-03",
        page: 11,
        section_label: "Sec 8.2",
        bbox: [110, 320, 500, 390],
        text: "No pets permitted under any circumstances; breach triggers automatic forfeiture of deposit."
      }
    },
    financial_terms: [
      {
        id: "FT-KM-01",
        source_id: "SRC-KM-01",
        label: "Base Monthly Rent (Maintenance Incl.)",
        amount: 62000,
        currency: "INR",
        frequency: "monthly",
        trigger: "Due on 1st of month",
        evidence: "Monthly rental shall be INR 62,000/- inclusive of society maintenance charges.",
        confidence: 1.0,
        type: "recurring_commitment"
      },
      {
        id: "FT-KM-02",
        source_id: "SRC-KM-02",
        label: "Security Deposit",
        amount: 300000,
        currency: "INR",
        frequency: "one_time",
        trigger: "Refundable in 15 days",
        evidence: "Security deposit shall be INR 3,00,000/- refundable within 15 working days",
        confidence: 1.0,
        type: "upfront_capital"
      }
    ],
    deadlines: [
      {
        id: "DL-KM-01",
        source_id: "SRC-KM-02",
        date: "2026-11-01",
        relative_label: "Day 0",
        event: "Possession & Deposit Clearance",
        consequence: "Keys handed over upon RTGS reflection.",
        action: "Verify electronic NEFT acknowledgment.",
        category: "payment",
        attention_tier: "high",
        confidence: 1.0
      }
    ],
    findings: [
      {
        id: "F-KM-01",
        source_id: "SRC-KM-03",
        category: "Covenant Breach",
        title: "Strict No-Pets Covenant with Deposit Forfeiture",
        severity_tier: "high",
        explanation: "Harsh penalty clause providing for full security deposit forfeiture (₹3,00,000) if any domestic pet is kept on premises.",
        matters: "If you have a pet or plan to adopt, this lease poses an immediate ₹3,00,000 forfeiture risk.",
        bullets: ["Unilateral complete deposit forfeiture.", "No remediation notice window."],
        evidence: "No pets permitted under any circumstances; breach triggers automatic forfeiture of deposit.",
        ambiguity_detected: false,
        ambiguity_note: "Clause is unambiguous.",
        confidence: 1.0,
        validation_status: "PASSED"
      }
    ],
    clauses: [
      {
        id: "CLS-KM-01",
        section: "3.1",
        title: "Rent and Consideration",
        page: 3,
        bbox: [60, 100, 520, 150],
        type: "rent",
        summary: "₹62,000 per month inclusive of maintenance."
      },
      {
        id: "CLS-KM-02",
        section: "4.1",
        title: "Deposit Terms",
        page: 5,
        bbox: [70, 120, 510, 170],
        type: "deposit",
        summary: "₹3,00,000 refundable within 15 days."
      },
      {
        id: "CLS-KM-03",
        section: "8.2",
        title: "Restrictions and Prohibitions",
        page: 11,
        bbox: [110, 320, 500, 390],
        type: "restrictions",
        summary: "Total pet prohibition under penalty of deposit loss."
      }
    ]
  }
};
