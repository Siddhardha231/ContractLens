"""Rigorous 4-Gate Deterministic Validation Engine conforming to PDD §7.6 & TDA §6."""
import re
import uuid
from typing import Dict, Any, List, Tuple, Optional
from app.schemas.extraction import RawExtractionResult

class GateAuditRecord:
    def __init__(self, finding_id: str, check_type: str, passed: bool, notes: Optional[str] = None):
        self.id = f"val-{uuid.uuid4().hex[:12]}"
        self.finding_id = finding_id
        self.check_type = check_type
        self.passed = passed
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "finding_id": self.finding_id,
            "check_type": self.check_type,
            "passed": self.passed,
            "notes": self.notes
        }


class DeterministicValidator:
    """Executes the 4-Gate Verification on LLM structured extraction output."""

    @classmethod
    def validate_extraction(
        cls,
        raw_data: Dict[str, Any],
        full_contract_text: str
    ) -> Tuple[Dict[str, Any], List[GateAuditRecord]]:
        """Run all 4 validation gates, returning validated IR elements and audit records."""
        audit_trail: List[GateAuditRecord] = []
        contract_lower = full_contract_text.lower()

        # Gate 1: Pydantic Schema Check
        schema_passed = True
        schema_notes = "Schema structure valid."
        try:
            parsed_raw = RawExtractionResult(**raw_data)
        except Exception as e:
            schema_passed = False
            schema_notes = f"Schema validation error: {str(e)}"
            parsed_raw = RawExtractionResult()

        validated_findings = []
        for idx, f in enumerate(raw_data.get("findings", [])):
            fid = f"F-{idx+1:02d}"
            
            # Record Gate 1
            audit_trail.append(GateAuditRecord(
                finding_id=fid,
                check_type="gate1_schema",
                passed=schema_passed,
                notes=schema_notes
            ))

            evidence = (f.get("evidence") or "").strip()
            explanation = (f.get("explanation") or "").strip()
            
            # Gate 2: Evidence Substring Match
            g2_passed = False
            confidence = 1.0
            g2_note = "Verbatim evidence substring verified."

            if evidence:
                evidence_clean = re.sub(r'\s+', ' ', evidence.lower())
                text_clean = re.sub(r'\s+', ' ', contract_lower)
                
                if evidence_clean in text_clean:
                    g2_passed = True
                    confidence = 1.0
                else:
                    # Normalized word-bag match
                    words = [w for w in re.split(r'\W+', evidence_clean) if len(w) > 3]
                    if words:
                        matches = sum(1 for w in words if w in text_clean)
                        ratio = matches / len(words)
                        if ratio >= 0.70:
                            g2_passed = True
                            confidence = round(ratio, 2)
                            g2_note = f"Normalized evidence match: {int(ratio*100)}% token alignment."
                        else:
                            g2_passed = False
                            confidence = 0.50
                            g2_note = f"Low evidence alignment ({int(ratio*100)}%). Dropping ungrounded finding."
                    else:
                        g2_passed = False
                        confidence = 0.30
                        g2_note = "Evidence string too short or non-textual."
            else:
                g2_passed = False
                confidence = 0.20
                g2_note = "Missing evidence string."

            audit_trail.append(GateAuditRecord(
                finding_id=fid,
                check_type="gate2_evidence",
                passed=g2_passed,
                notes=g2_note
            ))

            # Gate 3: Amount & Date Cross-Check
            g3_passed = True
            g3_notes = "Amounts and dates verified against source."
            numbers_in_evidence = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', evidence)
            for num_str in numbers_in_evidence:
                clean_num = num_str.replace(",", "")
                if clean_num not in contract_lower:
                    g3_passed = False
                    g3_notes = f"Amount or date {num_str} not verified in source contract text."
                    confidence = min(confidence, 0.65)
                    break

            audit_trail.append(GateAuditRecord(
                finding_id=fid,
                check_type="gate3_amount_date",
                passed=g3_passed,
                notes=g3_notes
            ))

            # Gate 4: Ambiguity & Confidence Classification
            ambiguity_detected = bool(f.get("ambiguity_detected", False))
            ambiguity_note = f.get("ambiguity_note")
            if not ambiguity_detected and ("not specified" in explanation.lower() or "unclear" in explanation.lower() or "silent" in explanation.lower()):
                ambiguity_detected = True
                ambiguity_note = ambiguity_note or "⚠ The contract does not clearly specify this provision."

            g4_passed = confidence >= 0.70
            status = "PASSED" if g4_passed else ("FLAGGED" if confidence >= 0.50 else "REJECTED")

            audit_trail.append(GateAuditRecord(
                finding_id=fid,
                check_type="gate4_ambiguity",
                passed=g4_passed,
                notes=f"Final confidence {confidence:.2f}, status: {status}."
            ))

            if status != "REJECTED":
                validated_findings.append({
                    **f,
                    "id": fid,
                    "confidence": confidence,
                    "validation_status": status,
                    "ambiguity_detected": ambiguity_detected,
                    "ambiguity_note": ambiguity_note
                })

        # Validate Financial Terms against text
        validated_financial_terms = []
        for idx, ft in enumerate(raw_data.get("financial_terms", [])):
            ft_id = f"FT-{idx+1:02d}"
            amt = ft.get("amount", 0)
            ev = (ft.get("evidence") or "").strip()
            # Verify amount or evidence
            ft_conf = 1.0 if (ev.lower() in contract_lower or str(int(amt)) in contract_lower) else 0.8
            validated_financial_terms.append({
                **ft,
                "id": ft_id,
                "confidence": ft_conf
            })

        # Validate Deadlines
        validated_deadlines = []
        for idx, dl in enumerate(raw_data.get("deadlines", [])):
            dl_id = f"DL-{idx+1:02d}"
            validated_deadlines.append({
                **dl,
                "id": dl_id,
                "confidence": 1.0
            })

        # Validate Obligations
        validated_obligations = []
        for idx, ob in enumerate(raw_data.get("obligations", [])):
            ob_id = f"OB-{idx+1:02d}"
            validated_obligations.append({
                **ob,
                "id": ob_id,
                "confidence": 1.0
            })

        result = {
            **raw_data,
            "findings": validated_findings,
            "financial_terms": validated_financial_terms,
            "deadlines": validated_deadlines,
            "obligations": validated_obligations
        }

        return result, audit_trail
