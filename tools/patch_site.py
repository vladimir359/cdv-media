#!/usr/bin/env python3
"""Adapta public/site (index.html, main.js, styles.css) de Cloudinary a img.ciudaddelvalle.com."""
import re, sys, os
site = sys.argv[1]
MEDIA = 'https://img.ciudaddelvalle.com'

# ---------------- main.js ----------------
p = os.path.join(site, 'assets/js/main.js'); s = open(p).read(); orig = s
old_block = s[s.index('/* ---------- Cloudinary ---------- */'):s.index('/* ---------- Datos ---------- */')]
new_block = '''/* ---------- Medios · img.ciudaddelvalle.com (GitHub Pages, repo cdv-media) ----------
   Las imágenes se sirven ya convertidas (AVIF + WebP) en varias anchuras y el navegador
   elige la mejor con srcset. IMG_W (anchuras disponibles por imagen) la genera
   tools/update_imgw.py del repo cdv-media; no editar a mano. */
const MEDIA = 'https://img.ciudaddelvalle.com';
const IMG_W = {}; // @generated-imgw
const SIZES_FULL = '100vw';
const SIZES_CARD = '(max-width: 720px) 78vw, 400px';
const SIZES_CELL = '(max-width: 720px) 50vw, 25vw';
const srcset = (slug, ext) => IMG_W[slug].map(w => `${MEDIA}/img/${slug}-${w}.${ext} ${w}w`).join(', ');
function pic(slug, { alt = '', cls = '', attrs = '', sizes = SIZES_FULL, lazy = true } = {}) {
  const ws = IMG_W[slug];
  if (!ws) return `<img class="${cls}" ${attrs} loading="${lazy ? 'lazy' : 'eager'}" src="${MEDIA}/img/${slug}-1280.webp" alt="${alt}">`;
  const mid = ws[Math.min(1, ws.length - 1)];
  return `<picture>
      <source type="image/avif" srcset="${srcset(slug, 'avif')}" sizes="${sizes}">
      <img class="${cls}" ${attrs} loading="${lazy ? 'lazy' : 'eager'}" decoding="async" src="${MEDIA}/img/${slug}-${mid}.webp" srcset="${srcset(slug, 'webp')}" sizes="${sizes}" alt="${alt}">
    </picture>`;
}
const vid    = (slug, q = '720') => `${MEDIA}/video/${slug}-${q}.mp4`;
const poster = (slug)            => `${MEDIA}/video/${slug}-poster.webp`;

'''
s = s.replace(old_block, new_block)

# datos: ids de Cloudinary -> slugs
s = re.sub(r"video:'v\d+/cdv-modelos/(\w+)\.mp4'", r"video:'\1'", s)
SLUGS = {
  'v1778710043/casaclub-div_esgf1o.png': 'casa-club',
  'v1778690482/piscina_50_ltqi2p.png': 'piscina',
  'v1778710156/gym_50_ix7ql5.png': 'gimnasio',
  'v1778710898/Z_Yoga_fmrhze.png': 'yoga',
  'v1778688369/cdv-cancha-sintetica_zhl1na.png': 'cancha-sintetica',
  'v1778689128/circuito-atletico_washx2.png': 'circuito-atletico',
  'v1778688369/cdv-juegos-infantiles_gcenwh.png': 'juegos-infantiles',
  'v1778688983/cdv-parque-de-mascotas-3_tipznx.png': 'parque-mascotas',
  'v1778706406/azotea-atardecer_i0ki5p.png': 'azotea-atardecer',
  'v1774562228/web_carrusel_2_bsxxnr.png': 'carrusel-2',
  'v1774564768/IMG_0475_tpougd.png': 'img-0475',
  'v1774562230/web_carrusel_5_dv1dj4.png': 'carrusel-5',
  'v1774562227/ChatGPT_Image_20_mar_2026_01_34_25_p.m._v3vjol.png': 'mananas-luz',
  'v1778687635/cdv-parque-de-mascotas_t1lbuy.png': 'parque-mascotas-2',
  'v1774565390/DJI_20250514093524_0297_D_leyc6t.png': 'valle-novarum',
  'v1780953870/barani_myp2te.png': 'valle-barani',
  'v1780953775/DJI_20250627095734_0318_D_jcmxd5.jpg': 'plaza-diagonal',
  'v1780937412/CIIP_mink_3_-_Photo_llz4hr.jpg': 'valle-castilla',
}
for old, new in SLUGS.items():
    assert old in s, old
    s = s.replace(f"'{old}'", f"'{new}'")

REPL = [
  ('<img loading="lazy" src="${img(d.img, 1100)}" alt="${d.nombre}">',
   '${pic(d.img, { alt: d.nombre, sizes: SIZES_CARD })}'),
  ('<img loading="lazy" src="${img(a.img, 1100)}" alt="${a.nombre}">',
   '${pic(a.img, { alt: a.nombre, sizes: SIZES_CELL })}'),
  ('''`<img class="bene-img ${i === 0 ? 'active' : ''}" data-bene="${i}" loading="${i === 0 ? 'eager' : 'lazy'}" src="${img(id, 2400)}" alt="">`''',
   '''pic(id, { cls: `bene-img ${i === 0 ? 'active' : ''}`, attrs: `data-bene="${i}"`, lazy: i !== 0 })'''),
  ('''`<img class="life-img ${i === 0 ? 'active' : ''}" data-life="${i}" loading="${i === 0 ? 'eager' : 'lazy'}" src="${img(l.img, 2400)}" alt="${l.txt}">`''',
   '''pic(l.img, { cls: `life-img ${i === 0 ? 'active' : ''}`, attrs: `data-life="${i}"`, lazy: i !== 0, alt: l.txt })'''),
  ('v.src = vid(m.video); v.poster = poster(m.video);',
   "v.src = vid(m.video, window.innerWidth > 900 ? '1080' : '720'); v.poster = poster(m.video);"),
  ('<div class="lb-video"><video src="${vid(m.video)}" poster="${poster(m.video)}" autoplay muted loop playsinline></video></div>',
   '<div class="lb-video"><video src="${vid(m.video, \'1080\')}" poster="${poster(m.video)}" autoplay muted loop playsinline></video></div>'),
]
for old, new in REPL:
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)
assert 'cloudinary' not in s.lower() and '${img(' not in s
open(p, 'w').write(s); print('main.js: ok')

# ---------------- index.html ----------------
p = os.path.join(site, 'index.html'); s = open(p).read()
REPL = [
  ('<meta property="og:image" content="https://res.cloudinary.com/dnbydvjki/image/upload/f_auto,q_auto,w_1200/v1774287170/resized_web_hero_cdv_irft6r.png">',
   f'<meta property="og:image" content="{MEDIA}/img/og.jpg">'),
  ('<link rel="preconnect" href="https://res.cloudinary.com">',
   f'<link rel="preconnect" href="{MEDIA}" crossorigin>\n  <link rel="preconnect" href="{MEDIA}">'),
  ('<img src="https://res.cloudinary.com/dnbydvjki/image/upload/f_auto,q_auto:best,w_2600/v1774287170/resized_web_hero_cdv_irft6r.png" alt="Vista aérea de Ciudad del Valle en el Valle de Coris">',
   '<picture id="hero-pic" data-img="hero"><img src="" alt="Vista aérea de Ciudad del Valle en el Valle de Coris" fetchpriority="high" decoding="async"></picture>'),
  ('src="https://res.cloudinary.com/dnbydvjki/video/upload/f_auto,q_auto:good,vc_auto,w_1920/v1780937479/Topaz_Video_Upscaler_0001_gyek6y.mp4"',
   f'src="{MEDIA}/video/hero-1080.mp4"'),
  ('poster="https://res.cloudinary.com/dnbydvjki/video/upload/so_0,f_auto,q_auto:good,w_1920/v1780937479/Topaz_Video_Upscaler_0001_gyek6y.jpg"',
   f'poster="{MEDIA}/video/hero-poster.webp"'),
  ('assets/css/styles.css?v=41', 'assets/css/styles.css?v=42'),
  ('assets/js/main.js?v=41', 'assets/js/main.js?v=42'),
]
for old, new in REPL:
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)
assert 'cloudinary' not in s.lower()
open(p, 'w').write(s); print('index.html: ok')

# el hero se rellena desde main.js (necesita IMG_W): añadimos renderHero()
p = os.path.join(site, 'assets/js/main.js'); s = open(p).read()
s = s.replace('''/* ============================================================================
   RENDER
   ========================================================================== */
''', '''/* ============================================================================
   RENDER
   ========================================================================== */
function renderHero() {
  const ph = $('#hero-pic'); if (!ph) return;
  ph.outerHTML = pic('hero', { alt: 'Vista aérea de Ciudad del Valle en el Valle de Coris', lazy: false })
    .replace('<img ', '<img fetchpriority="high" ');
}
''')
s = s.replace("document.addEventListener('DOMContentLoaded', () => {\n  renderDesarrollos();",
              "document.addEventListener('DOMContentLoaded', () => {\n  renderHero();\n  renderDesarrollos();")
assert 'renderHero();' in s
open(p, 'w').write(s)

# ---------------- styles.css ----------------
p = os.path.join(site, 'assets/css/styles.css'); s = open(p).read()
old = '.bg img, .bg video { width: 100%; height: 100%; object-fit: cover; }'
assert s.count(old) == 1
s = s.replace(old, 'picture { display: contents; }   /* <picture> no afecta el layout: el <img> se comporta como hijo directo */\n' + old)
open(p, 'w').write(s); print('styles.css: ok')
