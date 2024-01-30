
# Import the relevant packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib

# Load the simulation parameters
from params_static_credit_comparison import simulation_params

font = {'size'   : 18}

matplotlib.rc('font', **font)

# Load the results for the sociodemographic covariate (credit score, 0 and 1)
results_0 = pd.read_csv("results/results_static_test_cs_0.csv")	# Case of a client with low score
results_1 = pd.read_csv("results/results_static_test_cs_1.csv")	# Case of a client with high score

# Obtain the benefits from each offer
z = simulation_params['z']
x = simulation_params['x'] * simulation_params['scale']

# Obtain the expected benefits for each offer
exp_benefits_low = x * (z - results_0['h']) * results_0['probs']
exp_benefits_high = x * (z - results_1['h']) * results_1['probs']

# -------- --------- -------- --------- -------- --------- -------- --------- -------- --------- 

# Plot the results, layer by layer
# We will overlay two plots, and thus we decompose the representation
fig, ax1 = plt.subplots(figsize=(14, 7.5))
ax2 = ax1.twinx()



# Plot the benefits (in euros) for each case
ax2.plot(results_0["h"], exp_benefits_low * 1e-3, color='green', marker='s', markeredgecolor='green', markerfacecolor='red', alpha = 0.8)
ax2.plot(results_1["h"], exp_benefits_high * 1e-3, color='green', marker='D', markeredgecolor='green', markerfacecolor='blue', alpha = 0.8)


ax1.plot(results_0["h"], results_0["exp_ut"], '--o', color = "red")
ax1.plot(results_1["h"], results_1["exp_ut"], '--o', color = "blue")

ax1.plot(results_0["h"], results_0["probs"], '--o', color = "red", alpha = 0.2)
ax1.plot(results_1["h"], results_1["probs"], '--o', color = "blue", alpha = 0.2)

# Find the maximum utility for each experiment and plot a line there (optimal h offer)
max_position_0 = float(results_0["h"][results_0["exp_ut"] == np.max(results_0["exp_ut"])])
ax1.vlines(max_position_0, 0, 1, linestyles=':', color = "red")

max_position_1 = float(results_1["h"][results_1["exp_ut"] == np.max(results_1["exp_ut"])])
ax1.vlines(max_position_1, 0, 1, linestyles=':', color = "blue")


plt.xlabel('h')
ax1.set_ylabel('')
ax2.set_ylabel('Benefits (K€)')

ax1.legend([ "Exp. utilities (L)", "Exp. utilities (H)", "Acceptance prob. (L)", "Acceptance prob. (H)", "Optimal h (L)", "Optimal h (H)"])
ax2.legend([ "Benefits (L)", "Benefits (H)"])
# plt.title("Comparison lient with high and low scores w.r.t. his covariates")


# Save the figure in a png
plt.savefig("figs/results_static_comparison_covariate.pdf")



