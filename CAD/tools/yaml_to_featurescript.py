"""Generate the FeatureScript parameter block from CAD/parameters/nomad.yaml (D-002).

Standard library only. nomad.yaml is written in a deliberately restricted YAML subset
(see the header of that file); this parser accepts exactly that subset and rejects
anything else with a line-numbered error, so it can never silently misread the file.

Usage:  py CAD/tools/yaml_to_featurescript.py [--check]
  default  rewrite the GENERATED PARAMS block in CAD/featurescript/NOMAD_P01.fs
  --check  exit 1 if the block is out of date (no write)
  --target FILE  write/check the block in CAD/featurescript/FILE instead (Round E: NOMAD_E_Prototype.fs)
  --validate-v1  validate and resolve the V1 master CAD/parameters/nomad.yaml (no FeatureScript is written)

Two parameter files (Virtual V1 sprint, 2026-10-06):
  YAML_PATH      CAD/parameters/nomad.yaml: the CURRENT Virtual V1 master (D-002). Read by CAD/tools/v1_integration.py.
  P01_YAML_PATH  CAD/parameters/history/nomad_P0.1_2026-10-02.yaml: the frozen P0.1 / Round C / Round E / Architecture A
                 parameter set. The P0.1 FeatureScript files (NOMAD_P01.fs, NOMAD_E_Prototype.fs = snapshots of Onshape
                 Feature Studios) and every P0.1 study script are generated from / read this snapshot, so they keep
                 reproducing exactly. It is history: never edit it.
"""

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
YAML_PATH = ROOT / "CAD" / "parameters" / "nomad.yaml"                                  # V1 master
P01_YAML_PATH = ROOT / "CAD" / "parameters" / "history" / "nomad_P0.1_2026-10-02.yaml"  # frozen P0.1 set
FS_PATH = ROOT / "CAD" / "featurescript" / "NOMAD_P01.fs"
SPEC_PATH = ROOT / "docs" / "mechanical-spec.md"
BEGIN = "// BEGIN GENERATED PARAMS"
END = "// END GENERATED PARAMS"

STATUSES = {"verified", "derived", "provisional", "TBD"}
UNITS = {"mm": "millimeter", "deg": "degree", "none": None}
FIELDS = {"value", "status", "source", "unit", "working", "formula",
          "reference", "intent", "limit", "note"}


class YamlSubsetError(Exception):
    pass


# ---------- restricted YAML parser ----------

class _Flow:
    """Recursive-descent parser for one inline flow value."""

    def __init__(self, text, lineno):
        self.s, self.i, self.lineno = text, 0, lineno

    def fail(self, msg):
        raise YamlSubsetError(f"line {self.lineno}: {msg} at col {self.i + 1}: {self.s!r}")

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] == " ":
            self.i += 1

    def peek(self):
        self.ws()
        return self.s[self.i] if self.i < len(self.s) else ""

    def parse_value(self):
        c = self.peek()
        if c == "{":
            return self.parse_map()
        if c == "[":
            return self.parse_list()
        if c == '"':
            return self.parse_string()
        return self.parse_scalar()

    def parse_map(self):
        self.i += 1
        out = {}
        if self.peek() == "}":
            self.i += 1
            return out
        while True:
            self.ws()
            m = re.compile(r"[A-Za-z_][A-Za-z0-9_]*").match(self.s, self.i)
            if not m:
                self.fail("expected key")
            key = m.group(0)
            self.i = m.end()
            if self.peek() != ":":
                self.fail("expected ':'")
            self.i += 1
            if key in out:
                self.fail(f"duplicate key {key!r}")
            out[key] = self.parse_value()
            c = self.peek()
            self.i += 1
            if c == "}":
                return out
            if c != ",":
                self.fail("expected ',' or '}'")

    def parse_list(self):
        self.i += 1
        out = []
        if self.peek() == "]":
            self.i += 1
            return out
        while True:
            out.append(self.parse_value())
            c = self.peek()
            self.i += 1
            if c == "]":
                return out
            if c != ",":
                self.fail("expected ',' or ']'")

    def parse_string(self):
        m = re.compile(r'"([^"\\]*)"').match(self.s, self.i)
        if not m:
            self.fail("bad string (escapes are not supported)")
        self.i = m.end()
        return m.group(1)

    def parse_scalar(self):
        m = re.compile(r"[^,\]\}\s]+").match(self.s, self.i)
        if not m:
            self.fail("expected value")
        self.i = m.end()
        return _scalar(m.group(0), self.lineno)


def _scalar(tok, lineno):
    if tok == "null":
        return None
    if tok == "true":
        return True
    if tok == "false":
        return False
    if re.fullmatch(r"-?\d+", tok):
        return int(tok)
    if re.fullmatch(r"-?\d+\.\d+", tok):
        return float(tok)
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", tok):
        return tok
    raise YamlSubsetError(f"line {lineno}: unsupported scalar {tok!r}")


def _strip_comment(line):
    in_str = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_str = not in_str
        elif ch == "#" and not in_str:
            return line[:i].rstrip()
    return line.rstrip()


def parse_restricted_yaml(text):
    doc, group = {}, None
    for n, raw in enumerate(text.splitlines(), 1):
        if "\t" in raw:
            raise YamlSubsetError(f"line {n}: tabs are not allowed")
        line = _strip_comment(raw)
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        m = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*):(.*)", line.strip())
        if not m:
            raise YamlSubsetError(f"line {n}: expected 'key: ...'")
        key, rest = m.group(1), m.group(2).strip()
        if indent == 0:
            if rest:
                raise YamlSubsetError(f"line {n}: top-level key must open a group")
            if key in doc:
                raise YamlSubsetError(f"line {n}: duplicate group {key!r}")
            group = doc[key] = {}
        elif indent == 2 and group is not None:
            if not rest:
                raise YamlSubsetError(f"line {n}: nested blocks are not supported")
            if key in group:
                raise YamlSubsetError(f"line {n}: duplicate key {key!r}")
            p = _Flow(rest, n)
            group[key] = p.parse_value()
            if p.peek():
                p.fail("trailing characters")
        else:
            raise YamlSubsetError(f"line {n}: unsupported indentation {indent}")
    return doc


# ---------- validation and resolution ----------

def flatten(doc):
    params = {}
    for gname, group in doc.items():
        if gname == "meta":
            continue
        for name, spec in group.items():
            if name in params:
                raise ValueError(f"{name}: defined in more than one group")
            params[name] = (gname, spec)
    return params


def validate(params):
    errors = []
    for name, (_, p) in params.items():
        if not isinstance(p, dict):
            errors.append(f"{name}: must be an inline map")
            continue
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", name):
            errors.append(f"{name}: name must be UPPER_SNAKE_CASE")
        unknown = set(p) - FIELDS
        if unknown:
            errors.append(f"{name}: unknown fields {sorted(unknown)}")
        if "value" not in p or "status" not in p:
            errors.append(f"{name}: 'value' and 'status' are required")
            continue
        if p["status"] not in STATUSES:
            errors.append(f"{name}: bad status {p['status']!r}")
        if (p["status"] == "TBD") != (p["value"] is None):
            errors.append(f"{name}: status TBD must pair with value null (and only then)")
        if p.get("unit", "mm") not in UNITS:
            errors.append(f"{name}: bad unit {p.get('unit')!r}")
        if "working" in p and not isinstance(p["working"], (int, float)):
            errors.append(f"{name}: 'working' must be a number")
        if "working" in p and "formula" in p:
            errors.append(f"{name}: use either 'working' or 'formula', not both")
        if p["value"] is not None and ("working" in p or "formula" in p):
            errors.append(f"{name}: has an authoritative value, so it must not carry working inputs")
    return errors


_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
}


def _eval_formula(expr, name, env):
    tree = ast.parse(expr, mode="eval")

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Name):
            return env(node.id)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            v = ev(node.operand)
            return -v if isinstance(node.op, ast.USub) else v
        if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
            return _BINOPS[type(node.op)](ev(node.left), ev(node.right))
        raise ValueError(f"{name}: formula uses unsupported syntax: {ast.dump(node)}")

    return ev(tree)


def resolve(params):
    """Return {name: (value, basis)}; basis in {'value', 'formula', 'working'}. Unresolved omitted."""
    out, stack = {}, []

    def get(name):
        if name in out:
            return out[name][0]
        if name not in params:
            raise ValueError(f"formula references unknown parameter {name!r}")
        if name in stack:
            raise ValueError(f"formula cycle: {' -> '.join(stack + [name])}")
        p = params[name][1]
        stack.append(name)
        try:
            if p["value"] is not None:
                out[name] = (p["value"], "value")
            elif "formula" in p:
                out[name] = (_eval_formula(p["formula"], name, get), "formula")
            elif "working" in p:
                out[name] = (p["working"], "working")
            else:
                raise LookupError(name)
        finally:
            stack.pop()
        return out[name][0]

    unresolved = []
    for name in params:
        try:
            get(name)
        except LookupError as e:
            if e.args[0] != name:
                raise ValueError(f"{name}: formula depends on unresolved parameter {e.args[0]}")
            unresolved.append(name)
    return out, unresolved


# ---------- FeatureScript emission ----------

def _num(x):
    s = f"{float(x):.6f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def _fs_value(v, unit):
    fs_unit = UNITS[unit]
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return f"{_num(v)} * {fs_unit}" if fs_unit else _num(v)
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, list):
        return "[" + ", ".join(_fs_value(e, unit) for e in v) + "]"
    if isinstance(v, dict):
        return "{ " + ", ".join(f'"{k}" : {_fs_value(e, unit)}' for k, e in v.items()) + " }"
    raise ValueError(f"cannot emit {v!r}")


def emit(params, resolved, unresolved):
    lines = [BEGIN,
             "// Generated from CAD/parameters/nomad.yaml by CAD/tools/yaml_to_featurescript.py.",
             "// DO NOT EDIT. The YAML is the source of truth (D-002).",
             "// Labels: VALUE = authoritative value (with its status); WORKING / FORMULA = P0.1",
             "// working input for a TBD parameter: provisional, not an engineering value."]
    group = None
    for name, (gname, p) in params.items():
        if name not in resolved:
            continue
        if gname != group:
            group = gname
            lines.append(f"// --- {gname} ---")
        v, basis = resolved[name]
        unit = p.get("unit", "mm")
        if basis == "value":
            label = f"VALUE ({p['status']})"
        elif basis == "formula":
            label = f"WORKING via FORMULA {p['formula']} = {_num(v)} (status TBD)"
        else:
            label = "WORKING (status TBD)"
        lines.append(f"export const {name} = {_fs_value(v, unit)}; // {label}")
    basis_map = ", ".join(f'"{n}" : "{resolved[n][1]}"' for n in params if n in resolved)
    lines.append(f"export const NOMAD_PARAM_BASIS = {{ {basis_map} }};")
    lines.append("export const NOMAD_UNRESOLVED = [" + ", ".join(f'"{n}"' for n in unresolved) + "];")
    lines.append(END)
    return "\n".join(lines)


def splice(fs_text, block):
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    if not pattern.search(fs_text):
        raise ValueError(f"{FS_PATH.name}: markers {BEGIN!r} / {END!r} not found")
    return pattern.sub(lambda _: block, fs_text, count=1)


def validate_v1():
    """Validate and resolve the V1 master; print the resolution summary. Returns an exit code."""
    params = flatten(parse_restricted_yaml(YAML_PATH.read_text(encoding="utf-8")))
    errors = validate(params)
    if errors:
        print("V1 VALIDATION FAILED: " + "; ".join(errors))
        return 1
    resolved, unresolved = resolve(params)
    counts = {"value": 0, "formula": 0, "working": 0}
    for _, basis in resolved.values():
        counts[basis] += 1
    status = {}
    for _, p in params.values():
        status[p["status"]] = status.get(p["status"], 0) + 1
    print(f"V1 master {YAML_PATH.relative_to(ROOT)}: {len(params)} parameters, valid")
    print(f"  status: " + ", ".join(f"{k} {v}" for k, v in sorted(status.items())))
    print(f"  resolved by value {counts['value']}, formula {counts['formula']}, working {counts['working']}; "
          f"unresolved (TBD, no working input): {', '.join(unresolved) or 'none'}")
    for name in params:
        if name in resolved and resolved[name][1] == "formula":
            print(f"  {name} = {_num(resolved[name][0])}  ({params[name][1]['formula']})")
    spec = SPEC_PATH.read_text(encoding="utf-8")
    missing = [n for n in params if n not in spec]
    if missing:
        print(f"  NOT in {SPEC_PATH.name}: {', '.join(missing)}")
        return 1
    print(f"  every parameter is mentioned in {SPEC_PATH.name}")
    return 0


def main(argv):
    if "--validate-v1" in argv:
        return validate_v1()
    fs_path = FS_PATH
    if "--target" in argv:                     # Round E: the same block in another FeatureScript file
        fs_path = FS_PATH.parent / argv[argv.index("--target") + 1]
    doc = parse_restricted_yaml(P01_YAML_PATH.read_text(encoding="utf-8"))   # P0.1 FeatureScript files: frozen set
    params = flatten(doc)
    errors = validate(params)
    if errors:
        print("VALIDATION FAILED:\n  " + "\n  ".join(errors))
        return 1
    resolved, unresolved = resolve(params)
    block = emit(params, resolved, unresolved)

    counts = {"value": 0, "formula": 0, "working": 0}
    for _, basis in resolved.values():
        counts[basis] += 1
    print(f"parsed {len(params)} parameters from {P01_YAML_PATH.relative_to(ROOT)}")
    print(f"  authoritative value: {counts['value']}   working via formula: {counts['formula']}"
          f"   working: {counts['working']}   unresolved: {len(unresolved)}")
    for name in params:
        if name in resolved and resolved[name][1] == "formula":
            print(f"  {name} = {_num(resolved[name][0])}  ({params[name][1]['formula']})")

    spec = SPEC_PATH.read_text(encoding="utf-8")
    missing = [n for n in params if n not in spec]
    if missing:
        print(f"  WARNING: not mentioned in {SPEC_PATH.name}: {', '.join(missing)}")

    current = fs_path.read_text(encoding="utf-8")
    updated = splice(current, block)
    if "--check" in argv:
        if updated != current:
            print(f"{fs_path.name}: GENERATED PARAMS block is OUT OF DATE")
            return 1
        print(f"{fs_path.name}: GENERATED PARAMS block is up to date")
        return 0
    if updated != current:
        fs_path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"wrote {fs_path.relative_to(ROOT)}")
    else:
        print(f"{fs_path.name}: no change")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (YamlSubsetError, ValueError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)
