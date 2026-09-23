"""
Reference solution for Adaptive Compression Benchmark

This baseline solution uses Python's zlib library (DEFLATE algorithm)
with default compression level. It provides a strong general-purpose
baseline that works reasonably well across different data types.
"""

import zlib


def compress(data: bytes) -> bytes:
    """
    Compress data using zlib (DEFLATE algorithm).

    Args:
        data: Raw bytes to compress

    Returns:
        Compressed bytes
    """
    return zlib.compress(data, level=6)


def decompress(compressed: bytes) -> bytes:
    """
    Decompress data compressed with zlib.

    Args:
        compressed: Compressed bytes

    Returns:
        Original decompressed bytes
    """
    return zlib.decompress(compressed)


if __name__ == "__main__":
    # Simple test
    test_data = b"Hello, World! " * 100
    compressed = compress(test_data)
    decompressed = decompress(compressed)

    print(f"Original size: {len(test_data)} bytes")
    print(f"Compressed size: {len(compressed)} bytes")
    print(f"Compression ratio: {len(test_data) / len(compressed):.2f}x")
    print(f"Correctness: {'PASS' if decompressed == test_data else 'FAIL'}")
