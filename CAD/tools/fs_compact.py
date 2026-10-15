"""Compact a FeatureScript source for the Onshape Feature Studio / test_feature payloads (standard library).

  py CAD/tools/fs_compact.py CAD/featurescript/NOMAD_V1_Visual.fs CAD/featurescript/NOMAD_V1_Visual.onshape.fs

Strips comments, blank lines and whitespace that is not significant (outside strings). Semantics are unchanged; the result
is what is pasted into Onshape (~30 % smaller, fewer transcription errors). The readable .fs stays the source."""
import sys

src = open(sys.argv[1], encoding='utf-8').read()
out_lines = []
for line in src.split('\n'):
    res = []
    i, n, ins = 0, len(line), False
    while i < n:
        ch = line[i]
        if ins:
            res.append(ch)
            if ch == '\\':
                res.append(line[i + 1]); i += 2; continue
            if ch == '"':
                ins = False
            i += 1; continue
        if ch == '"':
            ins = True; res.append(ch); i += 1; continue
        if line.startswith('//', i):
            break
        if ch in ' \t':
            j = i
            while j < n and line[j] in ' \t':
                j += 1
            prev = res[-1] if res else ''
            nxt = line[j] if j < n else ''
            if prev and nxt and (prev.isalnum() or prev == '_') and (nxt.isalnum() or nxt == '_'):
                res.append(' ')
            elif prev and nxt and prev in '+-*/=<>!&|~' and nxt in '+-*/=<>!&|~':
                res.append(' ')
            i = j; continue
        res.append(ch); i += 1
    out_lines.append(''.join(res))
out_lines = [ln for ln in out_lines if ln.strip()]
out = '\n'.join(out_lines) + '\n'
open(sys.argv[2], 'w', encoding='ascii', newline='\n').write(out)
print(len(src), '->', len(out), 'bytes;', len(out_lines), 'lines')
