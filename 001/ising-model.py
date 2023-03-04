import openjij as oj
import numpy as np

# ising model Hamiltonian
# H({σ_i}) = ∑_{i>j} J_{ij} σ_i σ_j + ∑_{i=1}^{N} h_i σ_i
# σ_i ∈ {-1, 1}, i = 1, 2, ... , N
#
# inputs: J_{ij}, h_i
# outputs: {arg min}_{σ_i} H({σ_i})

print('sample 1. annealing method')
print('  inputs')
N = 5
h = {i: -1 for i in range(N)}
J = {(i, j): -1 for i in range(N) for j in range(i+1, N)}
print('    h_i:    ', h)
print('    J_{ij}: ', J)

print('  outputs')
sampler = oj.SASampler(num_reads=1)
response = sampler.sample_ising(h, J)
#print('    states: ', response.states)
print('    states: ', [s for s in response.samples()])

print('sample 2. use numpy for huge problems')
# /    h_0     J_{0,1}  ... J_{0,N-1} \
# |  J_{1,0}     h_1    ... J_{1,N-1} |
# |     :         :      :      :     |
# \ J_{N-1,0} J_{N-1,1} ...  h_{N-1}  /
mat = np.array([[-1,-0.5,-0.5,-0.5,-0.5],
                [-0.5,-1,-0.5,-0.5,-0.5],
                [-0.5,-0.5,-1,-0.5,-0.5],
                [-0.5,-0.5,-0.5,-1,-0.5],
                [-0.5,-0.5,-0.5,-0.5,-1]])
bqm = oj.BinaryQuadraticModel.from_numpy_matrix(mat, vartype='SPIN')
#print('  inputs: ', mat)
print('  inputs')
print('    ', bqm)

print('  outputs')
sampler = oj.SASampler(num_reads=1)
response = sampler.sample(bqm)
print('    states: ', [s for s in response.samples()])

