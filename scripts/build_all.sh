#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:-${ROOT_DIR}/_site}"

SITES=(
  "DataStructuresAndAlgorithms"
  "ComputerNetworks"
  "ComputerOrganization"
  "OperatingSystems"
  "MonteCarlo"
  "NeuralNetwork"
  "ThermodynamicsStatisticalPhysics"
  "SolidStatePhysics"
  "QuantumInformation"
  "PhysicalNotes"
)

cd "$ROOT_DIR"
python scripts/normalize_formula_delimiters.py
python -m mkdocs build --strict --site-dir "$OUTPUT_DIR"

for site in "${SITES[@]}"; do
  echo "==> Building ${site}"
  (
    cd "$site"
    python -m mkdocs build \
      --strict \
      --site-dir "${OUTPUT_DIR}/${site}"
  )
done

echo "All notes built in ${OUTPUT_DIR}"
