import numpy as np
import matplotlib.pyplot as plt
import openjij as oj
import jijmodeling as jm
from jijmodeling.transpiler.pyqubo import to_pyqubo

# TSP (Traveling Salesman Problem) objective function
# D = ∑_{t∈[0,N)} ∑_{i∈[0,N)} ∑_{j∈[0,N)} d_{i,j} x_{t,i} x_{t+1,j}
#
# inputs:
#   d_{i,j}: distance between city `i` and city `j`
#   x_{t,i}: binary that is visiting city `i` at time `t`
#            s.t. for all `i`, ∑_{t∈[0,N)} x_{t,i} = 1 (onehot constraint)
#             and for all `t`, ∑_{i∈[0,N)} x_{t,i} = 1 (onehot constraint)
# outputs:
#   min D: D is the total distance traveled


# create math model of TSP
dist = jm.Placeholder("dist", dim=2)
N = jm.Placeholder("N")
x = jm.Binary("x", shape=(N, N))
i = jm.Element("i", (0,N))
j = jm.Element("j", (0,N))
t = jm.Element("t", (0,N))

problem = jm.Problem("TSP")
obj = jm.Sum([t, i, j], dist[i, j] * x[t, i] * x[(t + 1) % N, j])
problem += obj

# constraint 1. onehot for location
problem += jm.Constraint(
                "onehot_location",
                x[:, i] == 1, # syntax suger of `jm.Sum(t, x[t,i])`
                forall=i,
            )
# constraint 2. onehot for time
problem += jm.Constraint(
                "onehot_time",
                x[t, :] == 1, # syntax suger of `jm.Sum(i, x[t,i])`
                forall=t,
            )

#problem   # check created mathematical model. for notebook


print('sample 1. 5 cities TSP')
N = 5
# random located cities
np.random.seed(3)
x_pos = np.random.rand(N)
y_pos = np.random.rand(N)
print('  inputs:')
print('    N     :', N)
print('    cities:', {(i): [x_pos[i], y_pos[i]] for i in range(N)})

#plt.plot(x_pos, y_pos, 'o')
#plt.xlim(0, 1)
#plt.ylim(0, 1)

# calculate distances
XX, XX_T = np.meshgrid(x_pos, x_pos) # matrixes
YY, YY_T = np.meshgrid(y_pos, y_pos) # matrixes
distance = np.sqrt((XX - XX_T)**2 + (YY - YY_T)**2)

# QUBO transformation
instance_data = {'N': N, 'dist': distance}
model, cache = to_pyqubo(problem,instance_data,{})
multipliers = {"onehot_location":1.0,"onehot_time":1.0}
Q, offset = model.compile().to_qubo(feed_dict = multipliers)

# optimization
sampler = oj.SASampler()
response = sampler.sample_qubo(Q=Q)
result = cache.decode(response)
#print('  outputs:', result)
print('  outputs:')
print('    does violate constraint?:         ', result.evaluation.constraint_violations)
print('    minimized total distance traveled:', result.evaluation.objective[0])

sparse_index, value, _ = result.record.solution['x'][0]
time_indices, city_indices = zip(*sorted(zip(*sparse_index)))
print('    traveled cities sort by time:     ', city_indices)

plt.plot(x_pos, y_pos, 'o',markersize=12)
plt.xlim(0, 1)
plt.ylim(0, 1)
for i, city_index in enumerate(city_indices[:-1]):
    next_city_index = city_indices[i+1]
    plt.plot([x_pos[city_index],x_pos[next_city_index ]],[y_pos[city_index],y_pos[next_city_index ]],c = "blue")
plt.plot([x_pos[city_indices[-1]],x_pos[city_indices[0]]],[y_pos[city_indices[-1]],y_pos[city_indices[0]]],c = "blue")

