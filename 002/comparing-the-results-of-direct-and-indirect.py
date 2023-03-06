import openjij as oj
import dimod
import random
import matplotlib.pyplot as plt

# `strength` is penalty of QUBO transformation
def plot_histgram_of_the_results_of_direct_and_indirect_HUBO_solving(polynomial, N, strength, num_reads):
    sampler = oj.SASampler()

    print('direct HUBO solving')
    response = sampler.sample_hubo(polynomial, 'SPIN', num_reads=num_reads)
    energy_hubo = response.energies
    max_energy_hubo = max(energy_hubo)
    min_energy_hubo = min(energy_hubo)
    avg_energy_hubo = sum(energy_hubo) / num_reads
    print('  max of energy:    ', max_energy_hubo)
    print('  min of energy:    ', min_energy_hubo)
    print('  average of energy:', avg_energy_hubo)


    print('indirect HUBO solving by QUBO transformation')
    bqm_dimod = dimod.make_quadratic(poly=polynomial, strength=strength, vartype='SPIN')

    # Convert mixture of strings and integers to integers only
    mapping = {}
    for i in range(1, N+1):
        mapping[i] = i
    count = N+1
    for v in bqm_dimod.variables:
        if type(v) == str:
            mapping[v] = count
            count += 1
    bqm_dimod.relabel_variables(mapping)

    # convert to OpenJij model
    bqm_oj = oj.BinaryQuadraticModel(dict(bqm_dimod.linear), dict(bqm_dimod.quadratic), bqm_dimod.offset, vartype="SPIN")

    response = sampler.sample(bqm_oj, num_reads=num_reads)

    # It is not garantied that `strength` is appropriate.
    energy_quad = []
    for i in range(num_reads):
        hubo_configuration = {j+1: response.record[i][0][j] for j in range(N)}
        energy_quad.append(dimod.BinaryPolynomial(polynomial, 'BINARY').energy(hubo_configuration))

    max_energy_quad = max(energy_quad)
    min_energy_quad = min(energy_quad)
    avg_energy_quad = sum(energy_quad) / num_reads
    print('  max of energy:    ', max_energy_quad)
    print('  min of energy:    ', min_energy_quad)
    print('  average of energy:', avg_energy_quad)


    # plot
    max_energies = max(max_energy_hubo, max_energy_quad)
    min_energies = min(min_energy_hubo, min_energy_quad)
    plt.hist(energy_hubo, label='HUBO', range=(min_energies, max_energies), bins=10, alpha=0.5)
    plt.hist(energy_quad, label='Through QUBO', range=(min_energies, max_energies), bins=10, alpha=0.5)
    plt.legend()
    plt.xlabel('Energy')
    plt.ylabel('Frequency')



print('sample 1. N=3')
num_reads = 100
N = 3
polynomial = {(1,): -1, (1,2): -1, (1,2,3): 1}
#strength = 5.0
strength = 1.0
plot_histgram_of_the_results_of_direct_and_indirect_HUBO_solving(polynomial, N, strength, num_reads)


print('sample 2. N=10')
N = 10
polynomial = {}
for i in range(1, N+1):
    for j in range(i+1, N+1):
        for k in range(j+1, N+1):
            polynomial[(i,j,k)] = random.uniform(-1, +1)
strength = 2
plot_histgram_of_the_results_of_direct_and_indirect_HUBO_solving(polynomial, N, strength, num_reads)
