# Local validation record

Run date: `2026-08-21` (workstation local time); scope is the overlay under
`artifacts\zoracleflux\gatework\compliance`. This record is not a production
availability report or legal/certification evidence. Incremental cash spend:
`$0.00`.

## Versions

Command:

```text
py -3 --version
```

Literal output:

```text
Python 3.12.3
```

Command:

```text
git --version
```

Literal output:

```text
git version 2.53.0.windows.4
```

## Checks

Command:

```text
py -3 ..\gatework\compliance\tools\synthetic_uptime.py generate --out ..\gatework\compliance\evidence\synthetic-uptime.jsonl --samples 24
py -3 ..\gatework\compliance\tools\synthetic_uptime.py check --input ..\gatework\compliance\evidence\synthetic-uptime.jsonl --target 0.999
py -3 ..\gatework\compliance\tools\check_bundle.py
py -3 -m py_compile ..\gatework\compliance\tools\synthetic_uptime.py ..\gatework\compliance\tools\check_bundle.py
```

Literal output:

```text
GENERATED synthetic=true samples=24 path=..\gatework\compliance\evidence\synthetic-uptime.jsonl
PASS synthetic=true samples=24 available=24 availability=1.000000 target=0.999000 NON_PRODUCTION_EVIDENCE_ONLY
PASS files=20 controls=17 evidence_map=15 pathways=17 templates=10 synthetic=PASS no-network=true
```

The compile command is silent on success. `check_bundle.py` validates required
files, CSV control fields, draft markers, and a fresh generate/check round trip.
Generated Python cache directories were removed after the check.

Manifest command literal output:

```text
PASS manifest_entries=24
```

## Hashes

`HASHES.sha256` contains SHA-256 values for every bundle file except the two
evidence ledgers themselves. Hashes are reproducibility evidence, not signatures
or certification.
