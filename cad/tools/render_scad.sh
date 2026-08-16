#!/usr/bin/env bash
# Render the OpenSCAD Gen5 model to PNG. Reproducible: same views every time.
#
# Needs a display. On a headless machine run it under xvfb-run, which is what the
# --headless flag does here.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SCAD="$ROOT/cad/scad/gen5.scad"
OUT="$ROOT/cad/renders/scad"
mkdir -p "$OUT"

RUN=(openscad)
if [ "${1:-}" = "--headless" ]; then
    RUN=(xvfb-run -a -s "-screen 0 1600x1200x24" openscad)
fi

# name|PART|camera (eye x,y,z, centre x,y,z)|size
VIEWS=(
  "mechanism_iso|mechanism|-900,-2600,1500,900,0,0|1600,1000"
  "mechanism_side|mechanism|900,-3200,120,900,0,120|1600,700"
  "mechanism_top|mechanism|900,0,3000,900,0,0|1600,700"
  "sled|sled|150,-900,520,400,0,0|1400,900"
  "magazine_cassette|magazine_cassette|-500,-900,650,320,0,150|1400,900"
  "interface_espa|interface_espa|-700,-500,380,0,0,0|1200,900"
  "enclosure|enclosure|-1100,-2900,1500,900,0,250|1600,1000"
)

for v in "${VIEWS[@]}"; do
    IFS='|' read -r name part cam size <<< "$v"
    printf '%-22s ' "$name"
    "${RUN[@]}" -D "PART=\"$part\"" --render --imgsize="$size" \
        --camera="$cam" --projection=perspective \
        -o "$OUT/$name.png" "$SCAD" >/dev/null 2>&1
    printf 'ok  %s bytes\n' "$(stat -c%s "$OUT/$name.png")"
done
echo "wrote $(ls "$OUT" | wc -l) renders to cad/renders/scad/"
