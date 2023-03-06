import openjij as oj

# HUBO (Higher order Unconstraint Binary Optimization) Hamiltonian
# H = c + ∑_i h_i σ_i + ∑_{i<j} J_{ij} σ_i σ_j + ∑_{i<j<k} K_{ijk} σ_i σ_j σ_k + ・・・
# σ_i ∈ {-1, +1} called SPIN, or, σ_i ∈ {0, 1} called BINARY, and, i = 1, 2, ... , N
#
# inputs: c, h_i, J_{ij}, K_{ijk}, ...
# outputs: {arg min}_{σ_i} H

import dimod

# Indirect HUBO solving by QUBO transformation
# 1. QUBO (Quadratic) Hamiltonian is written as follows:
#    H({q_i}) = ∑_{i≧j} Q_{ij} q_i q_j, q_i ∈ {0,1}
# 2. Convert higher-order terms of HUBO Hamiltonian to second or lower-order terms.
#    H = c + ∑_i h_i σ_i + ∑_{i<j} J_{ij} σ_i σ_j + O(σ_i σ_j σ_k)
# 3. map c, h_i, J_{ij} to Q_{ij}

# OpenJij cannot handle variables which are a mixture of integers and strings
# `mapping` between strings and integers
def generate_mapping(variables, N):
    mapping = {}

    # integer keys, no change
    for i in range(1, N+1):
        mapping[i] = i
    count = N+1

    # convert string keys to integers
    for v in variables:
        if type(v) == str:
            mapping[v] = count
            count += 1

    return mapping

print('sample 1. indirect HUBO solving by QUBO transformation')
print('  inputs')
N = 3
polynomial = {(1,): -1, (1,2): -1, (1,2,3): 1}
# `strength` is the penalty of QUBO transformation
bqm_dimod = dimod.make_quadratic(poly=polynomial, strength=5.0, vartype='SPIN')
#print('    0th-order term:', bqm_dimod.offset)
#print('    1st-order term:', bqm_dimod.linear)    # should transform to dict?
#print('    2nd-order term:', bqm_dimod.quadratic) # should transform to dict?

mapping = generate_mapping(bqm_dimod.variables, N)
bqm_dimod.relabel_variables(mapping)
print('    0th-order term:', bqm_dimod.offset)
print('    1st-order term:', bqm_dimod.linear)    # should transform to dict?
print('    2nd-order term:', bqm_dimod.quadratic) # should transform to dict?
print('      mapping term:', mapping)

bqm_oj = oj.BinaryQuadraticModel(dict(bqm_dimod.linear), dict(bqm_dimod.quadratic), bqm_dimod.offset, vartype='SPIN')

print('  outputs')
sampler = oj.SASampler()
response = sampler.sample(bqm_oj)
print(response)


print('sample 1-after. bake back to direct HUBO solution')
hubo_configuration = {i+1: response.record[0][0][i] for i in range(N)}
print('  Corresponding HUBO solution:', hubo_configuration)
print('  Energy of the corresponding HUBO solution:', dimod.BinaryPolynomial(polynomial, "SPIN").energy(hubo_configuration))

exact_solver = dimod.ExactPolySolver()
sampleset = exact_solver.sample_hising(h = {}, J = polynomial)
print('  Exact optimal solution:', sampleset.first.sample)
print('                energy:', sampleset.first.energy)
