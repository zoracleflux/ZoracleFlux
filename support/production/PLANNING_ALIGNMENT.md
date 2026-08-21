# Planning alignment

This overlay implements the local portions of the release and planning
reports without rewriting the preserved candidate:

* `planning\security\security-hardening-plan.md`: offline defaults, redacted
  audit, least-privilege Compose shape, backup/restore and threat checks.
* `planning\security\dependency-cost-ledger.csv` and
  `planning\launchpm\dependency_ledger.csv`: free local tooling, exact
  observed versions, and deferred managed infrastructure.
* `planning\launchpm\launch_master_plan.md`: Gate B ownership and customer/legal
  handoffs represented in `GATE_B_REGISTER.csv`.
* `final-release-candidate\docs\SECURITY.md` and `FINAL_GAP_REGISTER.md`:
  AST-only boundary, no credentials, no hosted/certification/SLA claims.

The reports remain authoritative for product scope; this directory supplies
operator artifacts and evidence only.
