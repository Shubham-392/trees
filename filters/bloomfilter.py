"""
Remember: Every data structure have some trade-off's and we see it in programming very often
BloomFilter:
    - Probabilistic data structure that answers set membership queries.
    - False negative will never occur
    - False positive may occur sometime

    A bloomfilter needs to define:
        - Size of bitmap
        - number of hash functions to use

    To be optimal, the hash functions should be uniformly distributed and independent.
    Hash Functions:
        - The number of hash functions, k, must be a positive integer.
        - Putting this constraint aside, for a given m and n, the value of k that minimizes the false positive probability is

            k = (m/n) * ln(2) ; n: number of inserted elements

Note: Bloom filter API will only support two operations, and it is not possible to delete an element from the filter

Operations:
    - Insert(X): Use `k` hash functions to set bits in the filter to 1.
    - Lookup(X): Check whether the bits are 1 for each hash function.


Other Bloomfilters examples:
    1). Counting Bloom Filters
    2). Cuckoo Filter (CMU)
    3). Succinct Range Filter (CMU)

Tradeoffs:
    Bloom filter used to speed up answers in a key-value storage system.
    Values are stored on a disk which has slow access times. Bloom filter decisions are much faster.

    However some unnecessary disk accesses are made when the filter reports a positive (in order to weed out the false positives).
    Overall answer speed is better with the Bloom filter than without the Bloom filter.
    ` Use of a Bloom filter for this purpose, however, does increase memory usage.`
"""

import math
from typing import Any

import mmh3

HASH_FUNCS: list[object] = []


# Implementaion algorithms reference is taken from wikipedia
# source: https://en.wikipedia.org/wiki/Bloom_filter
class MinimalBloomFilter:
    def __init__(self, expected_elem: int, false_p: float = 0.000001):

        if expected_elem <= 0:
            raise ValueError("Expected number of elements must be positive integer.")
        if (0 < false_p < 1) and isinstance(false_p, float):
            self.false_p = false_p
        else:
            raise ValueError(
                "False positive probability(false_p) should be in float and between exclusive (0,1)"
            )
        self.expected_elem = (
            expected_elem  # n: number of expected element (upper bound estimation)
        )
        self._bitlen = math.ceil(
            (self.expected_elem * math.log(self.false_p))
            / math.log(1 / pow(2, math.log(2)))
        )
        # hash functions based on expected_elem and array length
        self._hash_count = max(
            1, (round((self._bitlen / self.expected_elem) * math.log(2)))
        )

        # bit array init
        self._bit_array = [0] * self._bitlen
        self._elem_counter = 0

    @property
    def get_m(self):
        return self._bitlen

    @property
    def get_k(self):
        return self._hash_count


    def insert(self, x: Any):
        # To add an element, feed it to each of the k hash functions to get k array positions.
        # Set the bits at all these positions to 1.
        # increase the count for inserted element i.e., self._elem_counter += 1
        if not self.lookup(x):
            for i in range(self._hash_count):
                self._bit_array[mmh3.hash(x, i) % self._bitlen] = True

            self._elem_counter += 1

    def lookup(self, x: Any):
        # To test whether an element is in the set,
        # feed it to each of the k hash functions to get k array positions.
        # If any of the bits at these positions is 0, the element is definitely not in the set;
        # if it were, then all the bits would have been set to 1 when it was inserted.
        #
        # If all are 1, then either the element is in the set,
        # or the bits have by chance been set to 1 during the insertion of other elements, resulting in a false positive.
        for i in range(self._hash_count):
            if not self._bit_array[mmh3.hash(x, i) % self._bitlen]:
                return False

        return True


    def __contains__(self, x:Any):
        return self.lookup(x)
