#!/bin/bash
# A29: mesh and solve one case. Usage: ./run.sh <case-dir>
set -e
source /usr/share/openfoam/etc/bashrc
c="$1"
cd "$(dirname "$0")/$c"
rm -rf processor* [1-9]* 0.* log.* constant/polyMesh
blockMesh                    > log.blockMesh 2>&1
snappyHexMesh -overwrite     > log.snappy    2>&1
checkMesh                    > log.checkMesh 2>&1 || true
decomposePar                 > log.decompose 2>&1
mpirun --allow-run-as-root -np 4 simpleFoam -parallel > log.simpleFoam 2>&1
reconstructPar -latestTime   > log.reconstruct 2>&1
simpleFoam -postProcess -func wallShearStress -latestTime > log.wss 2>&1 || true
echo "$c done: $(grep -c '^' log.simpleFoam) lines"
