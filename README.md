# cdv-media

Imágenes y videos del sitio **ciudaddelvalle.com**, servidos con GitHub Pages en `https://img.ciudaddelvalle.com`.

- `img/` — imágenes en AVIF y WebP, en varias anchuras (`nombre-ANCHO.avif|webp`). Nunca se escalan hacia arriba.
- `video/` — videos H.264 a 1080p y 720p (`nombre-1080.mp4`, `nombre-720.mp4`) y sus posters (`nombre-poster.webp|jpg`).
- `CNAME` — dominio personalizado de GitHub Pages. No borrar.

Los originales NO viven aquí (pesan demasiado); se conservan en iCloud (`Documents/CDV/sitio-web-originales`).
Para regenerar: `tools/build_images.py manifest.json img/` (ver carpeta `tools/`).
