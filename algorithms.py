"""
Algorithms: Sorting and Searching
Demonstrates: Algorithm implementation, Big-O analysis, and performance comparison
"""
import timeit
from typing import List, Any


# ============================================================================
# SORTING ALGORITHMS
# ============================================================================

def bubble_sort(arr: List[float]) -> List[float]:
    """
    Bubble Sort Implementation
    Time Complexity: O(n²)
    Space Complexity: O(1)
    
    Simple but inefficient for large datasets.
    """
    arr = arr.copy()  # Don't modify original
    n = len(arr)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr


def merge_sort(arr: List[float]) -> List[float]:
    """
    Merge Sort Implementation
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Efficient divide-and-conquer algorithm.
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return _merge(left, right)


def _merge(left: List[float], right: List[float]) -> List[float]:
    """Helper function to merge two sorted arrays"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def benchmark_sorting(data: List[float], name: str = "data") -> dict:
    """
    Compare sorting algorithms and built-in methods
    
    Returns:
        dict: Execution times for each algorithm
    """
    results = {}
    
    # Custom implementations
    results["Bubble Sort"] = timeit.timeit(
        lambda: bubble_sort(data), number=1
    )
    results["Merge Sort"] = timeit.timeit(
        lambda: merge_sort(data), number=1
    )
    
    # Built-in methods
    results["Python sorted()"] = timeit.timeit(
        lambda: sorted(data), number=1
    )
    
    return results


# ============================================================================
# SEARCHING ALGORITHMS
# ============================================================================

def linear_search(arr: List[Any], target: Any) -> int:
    """
    Linear Search Implementation
    Time Complexity: O(n)
    
    Works on unsorted arrays. Checks each element sequentially.
    """
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1


def binary_search(arr: List[Any], target: Any) -> int:
    """
    Binary Search Implementation
    Time Complexity: O(log n)
    Prerequisites: Array must be sorted!
    
    Efficient for sorted arrays. Divides search space in half each iteration.
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def benchmark_searching(data: List[float], target: float) -> dict:
    """
    Compare searching algorithms and built-in methods
    
    Args:
        data: List of values to search in
        target: Value to find
    
    Returns:
        dict: Execution times and results
    """
    sorted_data = sorted(data)
    results = {}
    
    # Custom implementations
    results["Linear Search"] = timeit.timeit(
        lambda: linear_search(data, target), number=1000
    )
    results["Binary Search"] = timeit.timeit(
        lambda: binary_search(sorted_data, target), number=1000
    )
    
    # Built-in methods
    results["'in' operator"] = timeit.timeit(
        lambda: target in data, number=1000
    )
    
    return results
