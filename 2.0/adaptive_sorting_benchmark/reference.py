"""
Adaptive Sorting Benchmark - Reference Solution

This is a baseline solution that demonstrates adaptive sorting strategy.
It detects input patterns and selects appropriate sorting algorithms.
"""


def sort_adaptive(arr: list[int]) -> list[int]:
    """
    Adaptive sorting algorithm that analyzes input patterns
    and selects optimal strategy.

    Strategy:
    1. Detect if already sorted or reverse sorted
    2. Check for high duplicate density
    3. Measure partial sorting (inversions)
    4. Select appropriate algorithm based on pattern

    Args:
        arr: List of integers to sort

    Returns:
        Sorted list in ascending order
    """
    if len(arr) <= 1:
        return arr.copy()

    n = len(arr)

    # Pattern detection
    is_sorted = _check_sorted(arr)
    if is_sorted:
        return arr.copy()

    is_reverse = _check_reverse_sorted(arr)
    if is_reverse:
        return arr[::-1]

    # Check duplicate density
    unique_ratio = len(set(arr)) / len(arr)
    if unique_ratio < 0.1:  # High duplicates
        return _counting_sort_wrapper(arr)

    # Check if partially sorted (few inversions)
    inversion_ratio = _estimate_inversions(arr)
    if inversion_ratio < 0.2:  # Mostly sorted
        return _insertion_sort(arr.copy())

    # Default: use Python's Timsort (already adaptive)
    return sorted(arr)


def _check_sorted(arr: list[int]) -> bool:
    """Check if array is already sorted."""
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def _check_reverse_sorted(arr: list[int]) -> bool:
    """Check if array is reverse sorted."""
    for i in range(len(arr) - 1):
        if arr[i] < arr[i + 1]:
            return False
    return True


def _estimate_inversions(arr: list[int], sample_size: int = 100) -> float:
    """
    Estimate the ratio of inversions (out-of-order pairs).
    Uses sampling for large arrays to keep detection fast.
    """
    n = len(arr)
    if n < sample_size:
        inversions = sum(1 for i in range(n) for j in range(i + 1, n) if arr[i] > arr[j])
        total_pairs = n * (n - 1) // 2
        return inversions / total_pairs if total_pairs > 0 else 0

    # Sample for large arrays
    import random
    sample = random.sample(range(n), min(sample_size, n))
    sample.sort()

    inversions = 0
    for i in range(len(sample)):
        for j in range(i + 1, len(sample)):
            if arr[sample[i]] > arr[sample[j]]:
                inversions += 1

    total_pairs = len(sample) * (len(sample) - 1) // 2
    return inversions / total_pairs if total_pairs > 0 else 0


def _insertion_sort(arr: list[int]) -> list[int]:
    """
    Insertion sort - efficient for nearly sorted arrays.
    O(n) best case, O(n²) worst case.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def _counting_sort_wrapper(arr: list[int]) -> list[int]:
    """
    Counting sort wrapper - efficient for arrays with many duplicates.
    O(n + k) where k is the range of values.
    """
    if not arr:
        return []

    min_val = min(arr)
    max_val = max(arr)
    range_size = max_val - min_val + 1

    # Only use counting sort if range is reasonable
    if range_size > len(arr) * 10:
        return sorted(arr)

    # Counting sort
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1

    result = []
    for i, cnt in enumerate(count):
        result.extend([i + min_val] * cnt)

    return result


if __name__ == "__main__":
    # Test cases
    test_cases = [
        # Already sorted
        ([1, 2, 3, 4, 5], "sorted"),
        # Reverse sorted
        ([5, 4, 3, 2, 1], "reverse"),
        # Random
        ([3, 1, 4, 1, 5, 9, 2, 6], "random"),
        # Many duplicates
        ([1, 1, 2, 2, 2, 3, 3, 3, 3], "duplicates"),
        # Partially sorted
        ([1, 2, 3, 5, 4, 6, 7, 9, 8], "partial"),
    ]

    print("Testing adaptive sorting...")
    for arr, pattern in test_cases:
        result = sort_adaptive(arr)
        expected = sorted(arr)
        status = "[PASS]" if result == expected else "[FAIL]"
        print(f"{status} {pattern:12s}: {arr[:5]}... -> {result[:5]}...")

    print("\nAll tests passed!" if all(
        sort_adaptive(arr) == sorted(arr) for arr, _ in test_cases
    ) else "\nSome tests failed!")
