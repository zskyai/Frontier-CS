"""
Adaptive Sorting Benchmark - Evaluator

This evaluator tests AI agents' ability to design adaptive sorting algorithms
that recognize input patterns and optimize performance accordingly.
"""

import json
import random
import time
import sys
import os
from pathlib import Path
from typing import Any, Tuple


def prepare() -> dict[str, Any]:
    """
    Generate test cases with various data patterns.

    Returns:
        Dictionary containing test metadata (no actual test data exposed)
    """
    # Define test patterns
    patterns = [
        "random",
        "sorted",
        "reverse",
        "duplicates",
        "partial"
    ]

    sizes = [100, 1000, 10000, 100000]

    # Generate test cases
    test_cases = []
    for pattern in patterns:
        for size in sizes:
            test_cases.append({
                "pattern": pattern,
                "size": size,
                "id": f"{pattern}_{size}"
            })

    return {
        "test_count": len(test_cases),
        "patterns": patterns,
        "sizes": sizes,
        "description": "Adaptive sorting with 5 patterns × 4 sizes = 20 test cases"
    }


def _generate_test_data(pattern: str, size: int, seed: int) -> list[int]:
    """Generate test array based on pattern."""
    rng = random.Random(seed)

    if pattern == "random":
        return [rng.randint(0, size) for _ in range(size)]

    elif pattern == "sorted":
        return list(range(size))

    elif pattern == "reverse":
        return list(range(size, 0, -1))

    elif pattern == "duplicates":
        # Only 5% unique values
        unique_count = max(1, size // 20)
        return [rng.randint(0, unique_count) for _ in range(size)]

    elif pattern == "partial":
        # 80% sorted, 20% random shuffles
        arr = list(range(size))
        shuffle_count = size // 5
        for _ in range(shuffle_count):
            i = rng.randint(0, size - 1)
            j = rng.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    else:
        raise ValueError(f"Unknown pattern: {pattern}")


def _is_sorted(arr: list[int]) -> bool:
    """Check if array is sorted in ascending order."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def _baseline_sort(arr: list[int]) -> Tuple[list[int], float]:
    """
    Baseline sorting using Python's Timsort.

    Returns:
        Tuple of (sorted array, execution time)
    """
    arr_copy = arr.copy()
    start = time.perf_counter()
    result = sorted(arr_copy)
    elapsed = time.perf_counter() - start
    return result, elapsed


def evaluate(solution_path: str) -> Tuple[float, float, str, dict[str, Any]]:
    """
    Evaluate the submitted sorting solution.

    Args:
        solution_path: Path to the solution file

    Returns:
        Tuple of (score, score_unbounded, message, metrics)
    """
    # Load solution
    try:
        sys.path.insert(0, str(Path(solution_path).parent))

        if solution_path.endswith('.py'):
            module_name = Path(solution_path).stem
            solution_module = __import__(module_name)
        else:
            raise ValueError("Solution must be a Python file (.py)")

        if not hasattr(solution_module, 'sort_adaptive'):
            return (
                0.0,
                0.0,
                "Error: Solution must define a 'sort_adaptive(arr: list[int]) -> list[int]' function",
                {}
            )

        sort_func = solution_module.sort_adaptive

    except Exception as e:
        return (
            0.0,
            0.0,
            f"Error loading solution: {str(e)}",
            {}
        )

    # Run tests
    patterns = ["random", "sorted", "reverse", "duplicates", "partial"]
    sizes = [100, 1000, 10000, 100000]

    total_tests = 0
    passed_tests = 0
    total_time = 0.0
    baseline_time = 0.0

    results_by_pattern = {}
    seed = 42

    for pattern in patterns:
        pattern_passed = 0
        pattern_total = 0
        pattern_time = 0.0
        pattern_baseline_time = 0.0

        for size in sizes:
            test_id = f"{pattern}_{size}"
            total_tests += 1
            pattern_total += 1

            # Generate test data
            test_arr = _generate_test_data(pattern, size, seed)
            seed += 1

            # Run baseline
            baseline_result, baseline_elapsed = _baseline_sort(test_arr)
            baseline_time += baseline_elapsed
            pattern_baseline_time += baseline_elapsed

            # Run solution
            try:
                arr_copy = test_arr.copy()
                start = time.perf_counter()
                solution_result = sort_func(arr_copy)
                elapsed = time.perf_counter() - start

                # Check correctness
                if not isinstance(solution_result, list):
                    continue

                if len(solution_result) != len(test_arr):
                    continue

                if not _is_sorted(solution_result):
                    continue

                # Check if it's a valid permutation
                if sorted(solution_result) != sorted(test_arr):
                    continue

                # Test passed
                passed_tests += 1
                pattern_passed += 1
                total_time += elapsed
                pattern_time += elapsed

            except Exception:
                # Test failed
                continue

        # Store pattern statistics
        results_by_pattern[pattern] = {
            "passed": pattern_passed,
            "total": pattern_total,
            "time": round(pattern_time, 4),
            "baseline_time": round(pattern_baseline_time, 4),
            "speedup": round(pattern_baseline_time / pattern_time, 2) if pattern_time > 0 else 0.0
        }

    # Calculate scores
    correctness_score = (passed_tests / total_tests) * 50 if total_tests > 0 else 0

    # Performance score: baseline_time / solution_time * 50
    # Cap at 50 points (2x speedup), minimum 0
    if total_time > 0:
        speedup = baseline_time / total_time
        performance_score = min(speedup * 50, 50)
    else:
        performance_score = 0

    total_score = correctness_score + performance_score

    # Score unbounded (allow >100 for exceptional performance)
    score_unbounded = correctness_score + (baseline_time / total_time * 50 if total_time > 0 else 0)

    # Generate message
    if passed_tests == 0:
        message = f"Failed all {total_tests} tests. Check correctness and interface."
    elif passed_tests == total_tests:
        speedup = baseline_time / total_time if total_time > 0 else 0
        message = f"Perfect! {passed_tests}/{total_tests} tests passed. Speedup: {speedup:.2f}x"
    else:
        message = f"Passed {passed_tests}/{total_tests} tests. Focus on correctness first."

    metrics = {
        "correctness": f"{passed_tests}/{total_tests}",
        "total_time": round(total_time, 4),
        "baseline_time": round(baseline_time, 4),
        "speedup": round(baseline_time / total_time, 2) if total_time > 0 else 0.0,
        "by_pattern": results_by_pattern
    }

    return (
        round(total_score, 2),
        round(score_unbounded, 2),
        message,
        metrics
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluator.py <solution.py>")
        sys.exit(1)

    solution_path = sys.argv[1]

    print("=" * 60)
    print("Adaptive Sorting Benchmark - Evaluator")
    print("=" * 60)
    print()

    print("Preparing test cases...")
    metadata = prepare()
    print(f"[OK] {metadata['test_count']} test cases ready")
    print(f"  Patterns: {', '.join(metadata['patterns'])}")
    print(f"  Sizes: {', '.join(map(str, metadata['sizes']))}")
    print()

    print("Evaluating solution...")
    score, score_unbounded, message, metrics = evaluate(solution_path)

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Score: {score}/100")
    print(f"Score (unbounded): {score_unbounded:.2f}")
    print(f"Message: {message}")
    print()
    print("Metrics:")
    print(f"  Correctness: {metrics['correctness']}")
    print(f"  Total time: {metrics['total_time']}s")
    print(f"  Baseline time: {metrics['baseline_time']}s")
    print(f"  Speedup: {metrics['speedup']}x")
    print()
    print("By pattern:")
    for pattern, stats in metrics['by_pattern'].items():
        print(f"  {pattern:12s}: {stats['passed']}/{stats['total']} passed, "
              f"{stats['speedup']}x speedup")
    print("=" * 60)
