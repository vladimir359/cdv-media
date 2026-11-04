#!/usr/bin/env python3
"""Genera versiones web (AVIF + WebP) en varias anchuras a partir de un manifiesto JSON.
Uso: build_images.py manifest.json outdir
manifest: [{"slug": "hero", "src": "/ruta/original.png", "kind": "wide|card|poster|og"}]
Nunca escala hacia arriba: solo genera las anchuras <= anchura del original (y la nativa si es menor que el peldaño mayor).
"""
import glob, json, os, sys, time
from PIL import Image, ImageOps

LADDERS = {
    "hero":   [3840, 2560, 1920, 1280, 800],   # 4K real solo para el hero
    "wide":   [2560, 1920, 1280, 800],         # fondos a pantalla completa
    "card":   [1600, 1100, 800, 500],
    "poster": [1280, 900, 600],
}
def quality(w):          # peldaños grandes, algo más comprimidos
    return (72, 50) if w >= 3000 else (80, 58)

def build(entry, outdir):
    slug, kind = entry["slug"], entry.get("kind", "wide")
    hits = sorted(glob.glob(entry["src"]))
    if not hits: raise FileNotFoundError("no encontrado: " + os.path.basename(entry["src"]))
    src = hits[0]
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w0, h0 = im.size
    out = {"slug": slug, "src": os.path.basename(src), "orig": [w0, h0], "widths": [], "files": []}
    if kind == "og":
        og = ImageOps.fit(im, (1200, 630), Image.LANCZOS)
        p = os.path.join(outdir, f"{slug}.jpg"); og.save(p, "JPEG", quality=85, optimize=True, progressive=True)
        out["files"].append((os.path.basename(p), os.path.getsize(p)))
        return out
    ladder = LADDERS[kind]
    widths = [w for w in ladder if w <= w0]
    if w0 < ladder[0] and w0 not in widths:
        widths = [w0] + widths          # la anchura nativa como peldaño superior
    for w in widths:
        h = round(h0 * w / w0)
        r = im if w == w0 else im.resize((w, h), Image.LANCZOS)
        wq, aq = quality(w)
        for ext, kw in (("webp", dict(quality=wq, method=6)),
                        ("avif", dict(quality=aq, speed=6))):
            p = os.path.join(outdir, f"{slug}-{w}.{ext}")
            r.save(p, ext.upper(), **kw)
            out["files"].append((os.path.basename(p), os.path.getsize(p)))
        out["widths"].append(w)
    return out

if __name__ == "__main__":
    manifest, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    results = []
    for e in json.load(open(manifest)):
        t = time.time()
        try:
            r = build(e, outdir); results.append(r)
            tot = sum(s for _, s in r["files"])
            print(f"{r['slug']:<22} {r['orig'][0]}x{r['orig'][1]:<6} widths={r['widths']}  {tot/1048576:5.1f} MB  {time.time()-t:4.0f}s")
        except Exception as ex:
            print(f"{e['slug']:<22} ERROR {ex}")
    json.dump(results, open(os.path.join(outdir, "_manifest.json"), "w"), indent=1)
