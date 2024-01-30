
# Import the relevant packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import the parameters from the model 
from params_static import simulation_params

# Extract the percentage of benefits by the bank for this simulation
z = simulation_params['z']
x = simulation_params['x'] * simulation_params['scale']

# Read the results and plot them
results = pd.read_csv("results/results_static_test_extra.csv")

# Obtain the expected benefits for each offer
exp_benefits = x * (z - results['h']) * results['probs']

print(exp_benefits[results["exp_ut"] == np.max(results["exp_ut"])])

# import pdb; pdb.set_trace()

# We will overlay two plots, and thus we decompose the representation
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()


# Plot the results, layer by layer
ax1.plot(results["h"], results["probs"], '--o')
# plt.plot(results["h"], results["ut"], '--o') # , color = "g")
ax1.plot(results["h"], results["exp_ut"], '--o', color = "r")

# Find the maximum utility and plot a green line there (optimal h offer)
max_position = float(results["h"][results["exp_ut"] == np.max(results["exp_ut"])])
ax1.vlines(max_position, 0, 1, linestyles=':', color = "g")


ax2.plot(results["h"], exp_benefits * 1e-3, '--o',color = "forestgreen")


plt.xlabel('h')
ax1.set_ylabel('')
ax2.set_ylabel('Benefits obtained (K€)')

# ax1.legend([ "Probabilities", "Exp_utilities", "Optimal h"])
# ax2.legend([" Benefits"])
plt.title("Static case, client with 30K€")

# Save the figure in a png
plt.savefig("figs/test_results_static_1comp_extra.pdf") # , dpi = 1000)


