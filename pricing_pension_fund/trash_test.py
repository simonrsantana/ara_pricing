'''
LAUNCHING CODE TO EXECUTE THE STATIC PENSIONS EXAMPLE (multiple number of competitors)

In this code we will load all the parameters for the simulation example, and pass them onto the 
class that contains all the important methods for the computations.
'''

# Import the relevant packages
import numpy as np
import pandas as pd

from static_several_comp import *


# Import the parameters to run the simulation
from params_static_multiple_comps import simulation_params



# Load the class, passing all the parameters
dec = static_retirement_decision(simulation_params)

print(dec.n_comp)

optim_h, exp_ut, ut, probs = dec.estimate_h()

print(exp_ut)