# ContractLens Workspace Directives

## 📋 Approved Plans Archive Protocol (MANDATORY)

**Rule:** Whenever a plan (e.g. implementation plan, architectural RFC, design doc, refactoring proposal) is approved by the user in this project:
1. **Target Archive Folder**: Ensure the directory `plans/` exists at the project root (`d:/Code/ContractLens/plans/`).
2. **Save the Approved Plan**: Immediately save or copy the approved plan markdown document directly into `plans/<plan_name>.md` (e.g. `plans/backend_implementation_plan.md` or `plans/YYYY-MM-DD_<plan_title>.md`).
3. **Update the Index**: Update `plans/README.md` to record the plan name, approval timestamp, summary, and relative file link in the approved plans table.
4. **Execution Invariant**: Never begin implementation or code modifications following plan approval without first ensuring the approved plan document is saved in `plans/`.

---

## ⚖️ Project Design Principles
- **Traceability > Intelligence > Visual Polish**: Every extracted amount, date, obligation, or finding must link to a valid source with page, section label, bounding box, and verbatim text.
- **Fail Loudly, Not Confidently**: Never silently infer or fabricate data. Drop ungrounded claims or mark them low-confidence.
