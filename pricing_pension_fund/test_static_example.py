'''
LAUNCHING CODE TO EXECUTE THE STATIC PENSIONS EXAMPLE (1 competitor)

In this code we will load all the parameters for the simulation example, and pass them onto the 
class that contains all the important methods for the computations.
'''

# Import the relevant packages
import numpy as np
import pandas as pd

from static import *

# Import the parameters for the simulation
from params_static import simulation_params

# Load the class
dec = static_retirement_decision(simulation_params)

# Estimate the optimal h1 value, alongside the expected utility, the bank utility and 
# the probability that the client will stay in the bank
optim_h, exp_ut, ut, probs = dec.estimate_h()

# Write and save the results
results = pd.DataFrame({'h':simulation_params['h1_values'], 'exp_ut':exp_ut, 'ut':ut, 'probs':probs})

print(results)  # On-screen


# Save the results in a file
results.to_csv("results/results_static_test.csv")

