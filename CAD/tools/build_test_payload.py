"""Assemble a single-feature test payload for the Onshape test_feature tool.

NOMAD_P01.fs minus its PRODUCTION FEATURES section, plus NOMAD_P01.test.fs, so the
payload defines exactly one feature (the harness).

Usage:  py CAD/tools/build_test_payload.py OUTPUT_PATH
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FS_DIR = ROOT / "CAD" / "featurescript"

prod = (FS_DIR / "NOMAD_P01.fs").read_text(encoding="utf-8")
harness = (FS_DIR / "NOMAD_P01.test.fs").read_text(encoding="utf-8")
section = re.compile(r"// BEGIN PRODUCTION FEATURES.*?// END PRODUCTION FEATURES\n?", re.S)
if not section.search(prod):
    sys.exit("PRODUCTION FEATURES markers not found in NOMAD_P01.fs")
payload = section.sub("", prod).rstrip() + "\n\n" + harness
Path(sys.argv[1]).write_text(payload, encoding="utf-8", newline="\n")
print(f"wrote {sys.argv[1]} ({len(payload.splitlines())} lines)")
