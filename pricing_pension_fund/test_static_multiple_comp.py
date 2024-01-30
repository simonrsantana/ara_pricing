'''
LAUNCHING CODE TO EXECUTE THE STATIC PENSIONS EXAMPLE (multiple number of competitors)

In this code we will load all the parameters for the simulation example, and pass them onto the 
class that contains all the important methods for the computations.
'''

# Import the relevant packages
import numpy as np
import pandas as pd

from static_several_comp import *

import time

# Import the parameters to run the simulation
from params_static import simulation_params

# Explore scenarios with different number of competitors  
n_comp_list = np.array([2, 5, 10])

# Load the class, passing all the parameters
dec = static_retirement_decision(simulation_params)
def_result = []

# Recursively explore each case 
for n_comp in n_comp_list:

    print("Processing n_comp:", n_comp)

    # Estimate the optimal h1 value, alongside the expected utility, the bank utility and 
    # the probability that the client will stay in the bank
    optim_h, exp_ut, ut, probs = dec.estimate_h(n_comp=n_comp)

    # Write and save the results
    results = pd.DataFrame({'n_comp': n_comp, 'h':simulation_params['h1_values'], 'exp_ut':exp_ut, 'ut':ut, 'probs':probs})

    results.to_csv("results/results_static_" + str(n_comp) + "comp_test.csv")

    def_result.append(results)


def_result = pd.concat(def_result)


# Save the results in a file
def_result.to_csv("results/results_static_several_comp_test.csv", index=False)

