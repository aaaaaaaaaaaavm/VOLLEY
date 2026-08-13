#!/bin/bash
# Continue a converged case for N more iterations, writing often, so the force can be
# averaged over the last window rather than read off one iteration. A bluff-body wake is
# unsteady; a steady solver does not converge on it, it plateaus and oscillates, and a
# single-iteration force is a sample of that oscillation rather than an answer.
set -e
source /usr/share/openfoam/etc/bashrc
c="$1"; extra="${2:-400}"; every="${3:-40}"
cd "$(dirname "$0")/$c"
last=$(ls -d [0-9]* | sort -n | tail -1)
python3 - "$last" "$extra" "$every" <<'PY'
import re, sys
last, extra, every = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
s = open('system/controlDict').read()
s = re.sub(r'startFrom\s+\w+;', 'startFrom latestTime;', s)
s = re.sub(r'endTime\s+\d+;', f'endTime {last + extra};', s)
s = re.sub(r'writeInterval\s+\d+;', f'writeInterval {every};', s)
s = re.sub(r'purgeWrite\s+\d+;', 'purgeWrite 0;', s)
open('system/controlDict', 'w').write(s)
PY
rm -rf processor*
decomposePar -force > log.decompose2 2>&1
mpirun --allow-run-as-root -np 4 simpleFoam -parallel > log.simpleFoam2 2>&1
reconstructPar > log.reconstruct2 2>&1
echo "$c continued to $(ls -d [0-9]* | sort -n | tail -1)"
