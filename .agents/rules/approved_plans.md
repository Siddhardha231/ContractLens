# Approved Plans Archive Protocol

Whenever a plan (implementation plan, architectural RFC, design doc, refactoring plan) is approved by the user in this project:

1. **Target Archive Folder**: Ensure the directory `plans/` exists at the project root (`d:/Code/ContractLens/plans/`).
2. **Save the Approved Plan**: Immediately save or copy the approved plan markdown document directly into `plans/<plan_name>.md`.
3. **Update the Index**: Update `plans/README.md` with an entry recording the plan name, approval date, and description.
4. **Execution Invariant**: Do not proceed to code execution or modifications without first ensuring the approved plan document is archived in `plans/`.
