"""
Evaluator for Adaptive Compression Benchmark

This evaluator generates test cases across 6 data patterns and evaluates
compression solutions based on correctness and performance.
"""

import json
import os
import random
import string
import sys
import time
from pathlib import Path
from typing import Any


def prepare() -> None:
    """Generate test cases for the adaptive compression benchmark."""
    test_cases = []
    test_id = 1

    # Pattern 1: Text Data (4 cases)
    text_sizes = [10_000, 100_000, 1_000_000, 5_000_000]
    for size in text_sizes:
        data = generate_text_data(size)
        test_case = {
            "id": test_id,
            "pattern": "text",
            "size": size,
            "data_file": f"test_{test_id:03d}_text_{size}.bin"
        }
        save_test_data(test_case["data_file"], data)
        test_cases.append(test_case)
        test_id += 1

    # Pattern 2: Binary Data (4 cases)
    binary_sizes = [10_000, 100_000, 1_000_000, 5_000_000]
    for size in binary_sizes:
        data = generate_binary_data(size)
        test_case = {
            "id": test_id,
            "pattern": "binary",
            "size": size,
            "data_file": f"test_{test_id:03d}_binary_{size}.bin"
        }
        save_test_data(test_case["data_file"], data)
        test_cases.append(test_case)
        test_id += 1

    # Pattern 3: JSON Data (4 cases)
    json_sizes = [10_000, 100_000, 1_000_000, 5_000_000]
    for size in json_sizes:
        data = generate_json_data(size)
        test_case = {
            "id": test_id,
            "pattern": "json",
            "size": size,
            "data_file": f"test_{test_id:03d}_json_{size}.bin"
        }
        save_test_data(test_case["data_file"], data)
        test_cases.append(test_case)
        test_id += 1

    # Pattern 4: Repetitive Data (4 cases)
    repetitive_sizes = [10_000, 100_000, 1_000_000, 5_000_000]
    for size in repetitive_sizes:
        data = generate_repetitive_data(size)
        test_case = {
            "id": test_id,
            "pattern": "repetitive",
            "size": size,
            "data_file": f"test_{test_id:03d}_repetitive_{size}.bin"
        }
        save_test_data(test_case["data_file"], data)
        test_cases.append(test_case)
        test_id += 1

    # Pattern 5: Low-Entropy Data (4 cases)
    low_entropy_sizes = [10_000, 100_000, 1_000_000, 5_000_000]
    for size in low_entropy_sizes:
        data = generate_low_entropy_data(size)
        test_case = {
            "id": test_id,
            "pattern": "low_entropy",
            "size": size,
            "data_file": f"test_{test_id:03d}_low_entropy_{size}.bin"
        }
        save_test_data(test_case["data_file"], data)
        test_cases.append(test_case)
        test_id += 1

    # Pattern 6: High-Entropy Data (4 cases)
    high_entropy_sizes = [10_000, 100_000, 1_000_000, 5_000_000]
    for size in high_entropy_sizes:
        data = generate_high_entropy_data(size)
        test_case = {
            "id": test_id,
            "pattern": "high_entropy",
            "size": size,
            "data_file": f"test_{test_id:03d}_high_entropy_{size}.bin"
        }
        save_test_data(test_case["data_file"], data)
        test_cases.append(test_case)
        test_id += 1

    # Save test manifest
    manifest_path = Path("test_cases.json")
    with open(manifest_path, "w") as f:
        json.dump(test_cases, f, indent=2)

    print(f"Generated {len(test_cases)} test cases across 6 patterns")


def generate_text_data(size: int) -> bytes:
    """Generate realistic English text data."""
    # Common English words for realistic text
    words = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "algorithm", "data", "compression", "performance", "optimization", "benchmark",
        "solution", "test", "case", "pattern", "adaptive", "strategy", "efficiency"
    ]

    text_parts = []
    current_size = 0

    while current_size < size:
        # Generate sentences
        sentence_length = random.randint(5, 20)
        sentence = []
        for _ in range(sentence_length):
            word = random.choice(words)
            sentence.append(word)
        sentence_text = " ".join(sentence).capitalize() + ". "
        text_parts.append(sentence_text)
        current_size += len(sentence_text)

    text = "".join(text_parts)[:size]
    return text.encode('utf-8')


def generate_binary_data(size: int) -> bytes:
    """Generate random binary data."""
    return os.urandom(size)


def generate_json_data(size: int) -> bytes:
    """Generate structured JSON data."""
    records = []
    record_id = 1

    # Estimate records needed (rough average ~100 bytes per record)
    estimated_records = max(size // 100, 100)

    for _ in range(estimated_records):
        record = {
            "id": record_id,
            "name": f"user_{record_id}",
            "email": f"user{record_id}@example.com",
            "age": random.randint(18, 80),
            "score": round(random.uniform(0, 100), 2),
            "active": random.choice([True, False]),
            "tags": [f"tag{i}" for i in range(random.randint(1, 5))]
        }
        records.append(record)
        record_id += 1

    json_text = json.dumps(records, indent=2)[:size]
    return json_text.encode('utf-8')


def generate_repetitive_data(size: int) -> bytes:
    """Generate highly repetitive data."""
    # Create a pattern and repeat it
    pattern = b"ABCDEFGH" * 16  # 128-byte pattern
    repetitions = (size // len(pattern)) + 1
    data = pattern * repetitions
    return data[:size]


def generate_low_entropy_data(size: int) -> bytes:
    """Generate data with limited unique values."""
    # Only use 15 different byte values
    alphabet = bytes(range(15))
    return bytes(random.choices(alphabet, k=size))


def generate_high_entropy_data(size: int) -> bytes:
    """Generate high-entropy data (near-random)."""
    # Use crypto-quality random data
    return os.urandom(size)


def save_test_data(filename: str, data: bytes) -> None:
    """Save test data to file."""
    test_data_dir = Path("test_data")
    test_data_dir.mkdir(exist_ok=True)

    file_path = test_data_dir / filename
    with open(file_path, "wb") as f:
        f.write(data)


def evaluate(solution_path: str) -> tuple[float, float, str, dict[str, Any]]:
    """
    Evaluate a compression solution.

    Args:
        solution_path: Path to the solution file

    Returns:
        Tuple of (score, score_unbounded, message, metrics)
    """
    # Load test cases
    manifest_path = Path("test_cases.json")
    if not manifest_path.exists():
        return (0.0, 0.0, "Test cases not generated. Run prepare() first.", {})

    with open(manifest_path) as f:
        test_cases = json.load(f)

    # Import solution
    sys.path.insert(0, str(Path(solution_path).parent))
    try:
        solution_module = __import__(Path(solution_path).stem)
        compress = solution_module.compress
        decompress = solution_module.decompress
    except Exception as e:
        return (0.0, 0.0, f"Failed to import solution: {e}", {})

    # Import reference solution for baseline
    try:
        import reference
        reference_compress = reference.compress
    except Exception as e:
        return (0.0, 0.0, f"Failed to import reference solution: {e}", {})

    # Run evaluation
    results = []
    total_correct = 0
    total_cases = len(test_cases)

    for test_case in test_cases:
        result = run_test_case(
            test_case,
            compress,
            decompress,
            reference_compress
        )
        results.append(result)
        if result["correct"]:
            total_correct += 1

    # Calculate scores
    correctness_score = (total_correct / total_cases) * 50.0

    # Calculate performance score (only for correct solutions)
    if total_correct > 0:
        avg_ratio_multiplier = sum(r["ratio_multiplier"] for r in results if r["correct"]) / total_correct
        avg_speed_multiplier = sum(r["speed_multiplier"] for r in results if r["correct"]) / total_correct

        ratio_score = min(30.0 * avg_ratio_multiplier, 30.0)
        speed_score = min(20.0 * avg_speed_multiplier, 40.0)  # Capped at 2x

        performance_score = (ratio_score + speed_score) / 50.0
    else:
        performance_score = 0.0
        avg_ratio_multiplier = 0.0
        avg_speed_multiplier = 0.0

    final_score = correctness_score + (correctness_score * performance_score)

    # Unbounded score (no caps)
    if total_correct > 0:
        unbounded_performance = (30.0 * avg_ratio_multiplier + 20.0 * avg_speed_multiplier) / 50.0
        score_unbounded = correctness_score + (correctness_score * unbounded_performance)
    else:
        score_unbounded = 0.0

    # Generate message
    message = f"Correctness: {total_correct}/{total_cases} tests passed. "
    if total_correct > 0:
        message += f"Compression: {avg_ratio_multiplier:.2f}x baseline. "
        message += f"Speed: {avg_speed_multiplier:.2f}x baseline."
    else:
        message += "No correct solutions to evaluate performance."

    # Detailed metrics
    metrics = {
        "total_cases": total_cases,
        "correct_cases": total_correct,
        "correctness_score": correctness_score,
        "performance_score": performance_score * 50.0,
        "avg_compression_ratio_multiplier": avg_ratio_multiplier,
        "avg_speed_multiplier": avg_speed_multiplier,
        "test_results": results
    }

    return (final_score, score_unbounded, message, metrics)


def run_test_case(
    test_case: dict,
    compress_func,
    decompress_func,
    reference_compress_func
) -> dict[str, Any]:
    """Run a single test case."""
    test_data_dir = Path("test_data")
    data_file = test_data_dir / test_case["data_file"]

    # Load test data
    with open(data_file, "rb") as f:
        original_data = f.read()

    # Test solution
    try:
        # Compress
        start_time = time.perf_counter()
        compressed = compress_func(original_data)
        compress_time = time.perf_counter() - start_time

        # Decompress
        start_time = time.perf_counter()
        decompressed = decompress_func(compressed)
        decompress_time = time.perf_counter() - start_time

        # Check correctness
        correct = (decompressed == original_data)

        if not correct:
            return {
                "test_id": test_case["id"],
                "pattern": test_case["pattern"],
                "size": test_case["size"],
                "correct": False,
                "error": "Decompressed data does not match original",
                "ratio_multiplier": 0.0,
                "speed_multiplier": 0.0
            }

        # Calculate metrics
        original_size = len(original_data)
        compressed_size = len(compressed)
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 0.0
        total_time = compress_time + decompress_time

        # Get baseline metrics
        baseline_start = time.perf_counter()
        baseline_compressed = reference_compress_func(original_data)
        baseline_time = time.perf_counter() - baseline_start
        baseline_ratio = original_size / len(baseline_compressed)

        # Calculate multipliers
        ratio_multiplier = compression_ratio / baseline_ratio if baseline_ratio > 0 else 1.0
        speed_multiplier = baseline_time / total_time if total_time > 0 else 1.0

        return {
            "test_id": test_case["id"],
            "pattern": test_case["pattern"],
            "size": test_case["size"],
            "correct": True,
            "compressed_size": compressed_size,
            "compression_ratio": compression_ratio,
            "time_ms": total_time * 1000,
            "baseline_ratio": baseline_ratio,
            "baseline_time_ms": baseline_time * 1000,
            "ratio_multiplier": ratio_multiplier,
            "speed_multiplier": speed_multiplier
        }

    except Exception as e:
        return {
            "test_id": test_case["id"],
            "pattern": test_case["pattern"],
            "size": test_case["size"],
            "correct": False,
            "error": str(e),
            "ratio_multiplier": 0.0,
            "speed_multiplier": 0.0
        }


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prepare":
        prepare()
    elif len(sys.argv) > 1:
        solution_path = sys.argv[1]
        score, score_unbounded, message, metrics = evaluate(solution_path)
        print(f"Score: {score:.2f}/100")
        print(f"Score (unbounded): {score_unbounded:.2f}")
        print(f"Message: {message}")
        print(f"\nDetailed Metrics:")
        print(json.dumps(metrics, indent=2))
    else:
        print("Usage:")
        print("  python evaluator.py prepare          # Generate test cases")
        print("  python evaluator.py <solution.py>    # Evaluate solution")
