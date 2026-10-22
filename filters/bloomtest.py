import random
import string

from bloomfilter import MinimalBloomFilter

# create an instance of bloomfilter
bloom = MinimalBloomFilter(4000, false_p=1e-7)

print("------------------------- BloomFilter -----------------------------")
print("n: ", bloom.expected_elem)
print("m: ", bloom.get_m)
print("k: ", bloom.get_k)
print("p: ", bloom.false_p)


# 1. Test basic insertion and membership (Must have 0% False Negatives)
print("Testing basic insertions and membership...")
test_items = [f"item_{i}" for i in range(bloom.expected_elem)]

for item in test_items:
    bloom.insert(item)

for item in test_items:
    assert item in bloom, f"False Negative detected for item: {item}"
print("-> Success: All inserted items were found (0% False Negatives).")

# 2. Test False Positive Rate with non-inserted items
print("\nTesting false positive rate...")
num_tests = 100000
false_positives = 0

for _ in range(num_tests):
    # Generate random strings not in test_items
    random_item = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    if random_item not in test_items and random_item in bloom:
        false_positives += 1

empirical_fp = false_positives / num_tests
print(f"-> Tested {num_tests} non-existent items.")
print(f"-> False positives observed: {false_positives}")
print(f"-> Empirical False Positive Rate: {empirical_fp:.2e}")
print(f"-> Target False Positive Rate:     {bloom.false_p:.2e}")
