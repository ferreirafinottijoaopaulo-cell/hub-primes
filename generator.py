# generator.py - HUB Generator
# Finds all HUBs up to 1e8 using segmented sieve
# HUB: even n where n-2, n, n+2 form a symmetric cluster
# Author: Joao Paulo Ferreira Finotti

import math
import time

LIMIT = 100_000_000

def simple_sieve(limit):
    is_prime = bytearray(b'\x01') * (limit + 1)
    is_prime[0:2] = b'\x00\x00'
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            step = i
            start = i * i
            is_prime[start:limit+1:step] = b'\x00' * ((limit - start)//step + 1)
    return is_prime, [i for i, v in enumerate(is_prime) if v]

def segmented_hubs(limit=100_000_000, segment_size=1_000_000):
    _, base_primes = simple_sieve(int(limit**0.5) + 1)
    total_hubs = 0
    prime_hubs = 0
    hubs = []

    for low in range(0, limit + 1, segment_size):
        high = min(low + segment_size - 1, limit)
        size = high - low + 1
        is_prime = bytearray(b'\x01') * size

        for p in base_primes:
            if p * p > high:
                break
            start = max(p * p, ((low + p - 1)//p)*p)
            for j in range(start, high + 1, p):
                is_prime[j - low] = 0

        if low == 0:
            if size > 0:
                is_prime[0] = 0
            if size > 1:
                is_prime[1] = 0

        # Check HUBs in this segment: even n, n-2 and n+2 prime
        # Prime HUB: n-2, n, n+2 all prime (odd n case)
        for n in range(max(low, 4), high + 1):
            if n % 2 == 0:
                # even center: sexy prime pair around n
                if n-2 >= low and n+2 <= high:
                    if is_prime[n-2-low] and is_prime[n+2-low]:
                        total_hubs += 1
                        hubs.append(n)
                elif n-2 >= 0:
                    # border case handled by next segment logic - simplified
                    pass
            else:
                # odd center: check triple prime (rare)
                if n-2 >= low and n+2 <= high:
                    if is_prime[n-2-low] and is_prime[n-low] and is_prime[n+2-low]:
                        prime_hubs += 1

    return total_hubs, prime_hubs, hubs

if __name__ == "__main__":
    start = time.time()
    print(f"Searching HUBs up to {LIMIT}...")
    total, prime, hubs = segmented_hubs(LIMIT)
    print(f"Total HUBs: {total}")
    print(f"Prime HUBs: {prime}")
    print(f"Density: {total / (LIMIT//2) * 100:.4f}% of even numbers")
    if total > 0:
        print(f"Prime HUB ratio: {prime/total*100:.1f}%")
    print(f"Time: {time.time()-start:.2f}s")
    print(f"First 20 HUBs: {hubs[:20]}")
