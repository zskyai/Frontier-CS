#!/bin/bash

# Local evaluation script for Adaptive Compression Benchmark
# This script allows you to test solutions before submitting to Harbor

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOLUTION_FILE="${1:-reference.py}"

echo "=========================================="
echo "Adaptive Compression Benchmark - Local Test"
echo "=========================================="
echo ""

# Check if solution file exists
if [ ! -f "$SOLUTION_FILE" ]; then
    echo "Error: Solution file '$SOLUTION_FILE' not found"
    echo "Usage: ./evaluate.sh <solution.py>"
    exit 1
fi

echo "Solution: $SOLUTION_FILE"
echo ""

# Step 1: Generate test cases
echo "[1/3] Generating test cases..."
python "$SCRIPT_DIR/evaluator.py" prepare
echo ""

# Step 2: Run reference solution test
echo "[2/3] Testing reference solution..."
python "$SCRIPT_DIR/reference.py"
echo ""

# Step 3: Evaluate solution
echo "[3/3] Evaluating solution..."
python "$SCRIPT_DIR/evaluator.py" "$SOLUTION_FILE"
echo ""

echo "=========================================="
echo "Evaluation complete!"
echo "=========================================="
