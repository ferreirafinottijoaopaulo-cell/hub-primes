# hub-primes

Computational investigation of symmetric prime clusters up to 1e8

## What is this?

Investigation of HUBs: integers `n` where `n-2, n, n+2` form a symmetric cluster with special prime patterns.

We found:
- 8,675,746 HUBs up to 1e8
- Density: 8.6757% of even numbers are HUBs
- Only 15.9% of HUBs are prime HUBs

## Files

- `generator.py` - Segmented sieve generator (finds all HUBs up to 1e8)
- `audit.py` - Independent audit V1.1 (reproduces all counts)

## How to run

```bash
python generator.py
python audit.py
