# Python Performance Optimization

## Profiling Quick Start

```bash
# PyInstrument (statistical, readable output)
uv run pyinstrument script.py

# cProfile (detailed, built-in)
uv run python -m cProfile -s cumulative script.py

# Memory profiling
uv add --dev memray
uv run memray run script.py
uv run memray flamegraph memray-*.bin
```

## PyInstrument Usage

```python
from pyinstrument import Profiler

profiler = Profiler()
profiler.start()
result = my_function()
profiler.stop()
print(profiler.output_text(unicode=True, color=True))
```

## Memory Analysis

```python
import tracemalloc

tracemalloc.start()
# ... code ...
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics('lineno')[:10]:
    print(stat)
```

## Benchmarking (pytest-benchmark)

```python
def test_encode_benchmark(benchmark):
    result = benchmark(encode, 37.7749, -122.4194)
    assert len(result) == 12
```

```bash
uv run pytest tests/ --benchmark-only
uv run pytest tests/ --benchmark-compare
```

## Common Optimizations

```python
# Use set for membership (O(1) vs O(n))
valid = set(items)
if item in valid: ...

# Use deque for queue operations
from collections import deque
queue = deque()
queue.popleft()  # O(1) vs list.pop(0) O(n)

# Use generators for large data
def process(items):
    for item in items:
        yield transform(item)

# Cache expensive computations
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive(x):
    return compute(x)

# String building
result = "".join(str(x) for x in items)  # Not += in loop
```

## Algorithm Complexity

| Operation | list | set | dict |
|-----------|------|-----|------|
| Lookup | O(n) | O(1) | O(1) |
| Insert | O(1) | O(1) | O(1) |
| Delete | O(n) | O(1) | O(1) |

For detailed strategies, see:
- **[performance-profiling.md](performance-profiling.md)** - Advanced profiling techniques
- **[performance-benchmarks.md](performance-benchmarks.md)** - CI benchmark regression testing

## Optimization Checklist

```
Before Optimizing:
- [ ] Confirm there's a real problem
- [ ] Profile to find actual bottleneck
- [ ] Establish baseline measurements

Process:
- [ ] Algorithm improvements first
- [ ] Then data structures
- [ ] Then implementation details
- [ ] Measure after each change

After:
- [ ] Add benchmarks to prevent regression
- [ ] Verify correctness unchanged
- [ ] Document why optimization needed
```
