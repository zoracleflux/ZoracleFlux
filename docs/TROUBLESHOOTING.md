# Troubleshooting

* `ModuleNotFoundError`: activate the virtual environment and install the wheel
  or source package from this directory.
* `unknown relation tag`: replace the tag with one listed in
  `zoracleflux\relations.py`; unknown metadata is intentionally rejected.
* `not-executed`: external source analysis is static by design. Use a reviewed
  adapter or add a trusted fixture rather than bypassing the boundary.
* nonzero `check`: inspect JSON `relations` for the first failed case and
  review the declaration before changing code.
