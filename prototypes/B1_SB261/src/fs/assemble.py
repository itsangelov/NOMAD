import sys, re
HDR = 'FeatureScript 3083;\nimport(path : "onshape/std/common.fs", version : "3083.0");\n\n'
def strip(src):
    out = []
    for line in src.splitlines():
        s = line.strip()
        if s.startswith("//") or not s:
            continue
        out.append(s)
    return "\n".join(out)
common = open("b1_common.fs", encoding="utf-8").read()
for name in sys.argv[1:]:
    body = open(name + ".fs", encoding="utf-8").read()
    payload = HDR + strip(common) + "\n" + strip(body) + "\n"
    open(name + ".payload.fs", "w", encoding="utf-8").write(payload)
    print(name, len(payload), "chars")
