import openjij as oj
import matplotlib.pyplot as plt
import random

# QUBO (Quadratic Unconstraited Binary Optimization) Hamiltonian
# H({q_i}) = ∑_{i≧j} Q_{ij} q_i q_j = ∑_{i>j} Q_{ij} q_i q_j + ∑_i Q_{ii} q_i
# q_i ∈ {0,1}
#
# inputs: Q_{ij}
# outputs: {arg min}_{q_i} H({q_i})

print('sample 1. QUBO')
print('  inputs')
Q = {(0,0): -1, (0,1): -1, (1,2): 1, (2,2): 1}
print('    Q_{ij}: ', Q)

print('  outputs')
sampler = oj.SASampler(num_reads=2)
response = sampler.sample_qubo(Q)
print('    states:   ', response.states)
print('    energies: ', response.energies)

print('sample 2. random QUBO')
#print('  inputs')
N = 50
Q = {(i, j): random.uniform(-1, 1) for i in range(N) for j in range(i+1, N)}
#print('    Q_{ij}: ', Q)

print('  outputs')
sampler = oj.SASampler()
response = sampler.sample_qubo(Q, num_reads=100)
#print('    states[:5]:   ', response.states[:5])
#print('    energies[:5]: ', response.energies[:5])
print('    min energy state occurrences: ', response.first.num_occurrences)
print('    min energy:        ', response.first.energy)
print('    min energy sample: ', response.first.sample)

plt.hist(response.energies, bins=15)
plt.xlabel('Energy')
plt.ylabel('Frequency')
plt.show()


