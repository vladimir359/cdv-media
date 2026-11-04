#!/usr/bin/env python3
"""Escribe en main.js la lista de anchuras disponibles por imagen, leída del _manifest.json generado por build_images.py."""
import json, re, sys
man, js = sys.argv[1], sys.argv[2]
m = {r['slug']: r['widths'] for r in json.load(open(man)) if r.get('widths')}
line = 'const IMG_W = ' + json.dumps(m, separators=(',', ':')) + '; // @generated-imgw'
s = open(js).read()
s2, n = re.subn(r'const IMG_W = .*?; // @generated-imgw', line, s)
assert n == 1
open(js, 'w').write(s2); print('IMG_W:', ', '.join(f'{k}({v[0]})' for k, v in m.items()))
