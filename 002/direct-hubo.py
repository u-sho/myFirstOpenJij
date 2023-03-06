import openjij as oj

# HUBO (Higher Order Unconstraint Binary Optimization) Hamiltonian
# H = c + ∑_i h_i σ_i + ∑_{i<j} J_{ij} σ_i σ_j + ∑_{i<j<k} K_{ijk} σ_i σ_j σ_k + ・・・
# σ_i ∈ {-1, +1} called SPIN, or, σ_i ∈ {0, 1} called BINARY, and, i = 1, 2, ... , N
#
# inputs: c, h_i, J_{ij}, K_{ijk}, ...
# outputs: {arg min}_{σ_i} H

print('sample 1. direct HUBO solving')
print('  inputs')
polynomial = {(1,): -1, (1,2): -1, (1,2,3): 1}
print('    h_1:      ', polynomial[(1,)])
print('    J_{1,2}:  ', polynomial[(1,2)])
print('    K_{1,2,3}:', polynomial[(1,2,3)])

print('  outputs')
sampler = oj.SASampler()
response = sampler.sample_hubo(polynomial, 'SPIN')
print(response)


print('sample 2. direct HUBO solving with non integer key')
print('  inputs')
polynomial = {('q0',): 0, ('q0','q1'): 0, ('q0','q1','q2'): 1}
print('    h_1:      ', polynomial[('q0',)])
print('    J_{1,2}:  ', polynomial[('q0','q1')])
print('    K_{1,2,3}:', polynomial[('q0','q1','q2')])

print('  outputs')
sampler = oj.SASampler()
response = sampler.sample_hubo(polynomial, 'BINARY')
print(response)
