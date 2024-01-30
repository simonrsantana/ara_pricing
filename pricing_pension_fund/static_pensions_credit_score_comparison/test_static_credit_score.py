
# Import the relevant packages
import numpy as np
import pandas as pd

from static_compare_credit_score import *
import sys

# Load a credit score from screen
cred_score = int(sys.argv[ 1 ])

# Import the parameters for the simulation
from params_static_credit_comparison import simulation_params

# Load the class
dec = static_retirement_decision(cred_score, simulation_params)

# Estimate the optimal h1 value, alongside the expected utility, the bank utility and 
# the probability that the client will stay in the bank
optim_h, exp_ut, ut, probs = dec.estimate_h()

avail_h = dec.h1_values							# Save the possible h for storing

# Write and save the results
results = pd.DataFrame({'h':avail_h, 'exp_ut':exp_ut, 'ut':ut, 'probs':probs})

print(results)

# Save the results in a file
results.to_csv("results/results_static_test_cs_" + str(cred_score) + ".csv")

