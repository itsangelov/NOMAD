"""Assemble a single-feature test payload for the Onshape test_feature tool.

A FeatureScript source (default NOMAD_P01.fs) minus its PRODUCTION FEATURES section, plus one harness
file (default NOMAD_P01.test.fs), so the payload defines exactly one feature (the harness).

Usage:  py CAD/tools/build_test_payload.py OUTPUT_PATH [HARNESS_FILE_NAME [SOURCE_FILE_NAME]]
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FS_DIR = ROOT / "CAD" / "featurescript"

source = sys.argv[3] if len(sys.argv) > 3 else "NOMAD_P01.fs"
prod = (FS_DIR / source).read_text(encoding="utf-8")
harness = (FS_DIR / (sys.argv[2] if len(sys.argv) > 2 else "NOMAD_P01.test.fs")).read_text(encoding="utf-8")
section = re.compile(r"// BEGIN PRODUCTION FEATURES.*?// END PRODUCTION FEATURES\n?", re.S)
if not section.search(prod):
    sys.exit(f"PRODUCTION FEATURES markers not found in {source}")
payload = section.sub("", prod).rstrip() + "\n\n" + harness
Path(sys.argv[1]).write_text(payload, encoding="utf-8", newline="\n")
print(f"wrote {sys.argv[1]} ({len(payload.splitlines())} lines)")
