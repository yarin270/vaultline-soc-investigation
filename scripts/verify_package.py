"""Verify package structure and reported arithmetic; does not execute SPL."""
from pathlib import Path
from datetime import datetime
from urllib.parse import unquote
import hashlib, json, re

root = Path(__file__).resolve().parents[1]
errors = []
links = 0
for file in root.rglob('*.md'):
    text = file.read_text(encoding='utf-8')
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        path, _, anchor = unquote(target).partition('#')
        dest = (file.parent / path).resolve() if path else file.resolve()
        links += 1
        if not dest.is_relative_to(root.resolve()) or not dest.exists():
            errors.append(f'Broken or escaping link: {file.relative_to(root)} -> {target}')
        elif anchor:
            errors.append(f'Anchor requires explicit validation: {target}')
metrics = json.loads((root/'evidence/reported-metrics.json').read_text())
assert metrics['total_bytes'] == 270 * 43745037 + 8140
assert metrics['service_bytes_derived'] == 111 * 43745037
assert metrics['user_bytes_derived'] == 159 * 43745037 + 8140
assert metrics['service_bytes_derived'] + metrics['user_bytes_derived'] == metrics['total_bytes']
assert round(metrics['total_bytes']/1024**3, 2) == 11.00
assert round(metrics['total_bytes']/1000**3, 2) == 11.81
assert (datetime(2026,11,21,22,6)-datetime(2026,9,9,21)).total_seconds() == 73*86400+3960
assert (datetime(2026,9,9,21,40,1)-datetime(2026,9,9,21)).total_seconds() == 2401
presentation=(root/'docs/presentation.md').read_text(encoding='utf-8')
assert re.findall(r'^## Slide (\d{2}) ',presentation,re.M) == [f'{n:02d}' for n in range(1,27)]
for item in json.loads((root/'original-files/source-manifest.json').read_text()):
    content=(root/'original-files'/item['file']).read_bytes()
    assert len(content)==item['bytes']
    assert hashlib.sha256(content).hexdigest()==item['sha256']
assert len(list((root/'queries').glob('source-*.spl')))==7
assert len(list((root/'queries').glob('reviewed-*.spl')))==6
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {links} relative links; 26 ordered slides; 3 original hashes; 13 query files; reported arithmetic and time intervals.')
print('No raw logs examined and no SPL executed by this verifier.')
