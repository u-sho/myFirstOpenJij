# 001 OpenJij introduction

https://openjij.github.io/OpenJij/tutorial/ja/001-openjij_introduction.html

## Sampler

```python3
sampler = oj.SASampler(num_reads=1)
```

The above sampler instance uses an algorithm called simulated annealing (SA).
Instead of `SASampler`, you can use `SQASampler` to use simulated _quantum_ annealing (SQA).

You can specify the number of times to solve the puzzle per interaction by putting an integer in `num_reads` argument.
When the value of `num_reads` is not specified, it will be set to default value `num_reads=1`.

## Response

`.sample_ising(h, J)` returns the response class having various properties like below.

- `.states`: `list[list[int]]`
	- The number of `num_reads` count solutions is stored.
- `.energies`: `list[float]`
	- The energies of each solution for the `num_reads` times are stored.
- `.indices`: `list[object]`
	- The solution is stored in `.states`, and the corresponding indices of each spin are stored in `.indices`.
- `.first.sample`: `dict`
	- The minimum energey state is stored.
- `.first.energy`: `float`
	- The minimum energey state is stored.

