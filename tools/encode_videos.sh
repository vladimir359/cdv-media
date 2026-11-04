#!/bin/zsh
S="/private/tmp/claude-501/-Users-vlad-Library-Mobile-Documents-com-apple-CloudDocs-Documents-Claude/807bc8e2-c499-49c9-a141-44a8106ff6f3/scratchpad"
FF="$S/tools/venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
V="/Users/vlad/Library/Mobile Documents/com~apple~CloudDocs/Documents/Proyectos/ciudad-del-valle/assets/vids"
OUT="$S/build/video"
for f in "$V"/*.mp4; do
  name=$(basename "$f" | sed -E 's/_pagina web\.mp4$//' | tr 'A-Z' 'a-z')
  echo "== $name  $(date '+%H:%M:%S')"
  "$FF" -y -hide_banner -loglevel error -i "$f" -an -vf "scale=1920:-2" -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -profile:v high -level 4.1 -movflags +faststart "$OUT/$name-1080.mp4"
  "$FF" -y -hide_banner -loglevel error -i "$f" -an -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -profile:v high -level 4.0 -movflags +faststart "$OUT/$name-720.mp4"
  "$FF" -y -hide_banner -loglevel error -ss 0 -i "$f" -frames:v 1 -vf "scale=1280:-2" -c:v libwebp -q:v 82 "$OUT/$name-poster.webp"
  "$FF" -y -hide_banner -loglevel error -ss 0 -i "$f" -frames:v 1 -vf "scale=1280:-2" -q:v 3 "$OUT/$name-poster.jpg"
  ls -l "$OUT/$name-"* | awk '{printf "   %6.1f MB  %s\n", $5/1048576, $9}'
done
echo "DONE $(date '+%H:%M:%S')"
