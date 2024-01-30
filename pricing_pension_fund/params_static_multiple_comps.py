
''' 
PARAMETER SETUP

Define here all the parameters for the simulation in the static pensions example.
These parameters are shared in the case with one and multiple opponents.
'''

import numpy as np
import pandas as pd


#####################################################################
# Define all the parameters of our simulation and the problem setup #
#####################################################################

# General parameters (client-related or simu)lation-related)

# Load the probs. assigned to the client leaving in each year of the plan
probs = pd.read_csv("data/permanence_probs", delim_whitespace=True)
x = 3                   # 30.000€, representing the client's capital in 10K euros (example)
scale = 10e4            # Scale of the "x" value
rho_client_low = 0.85   # Lower limit for the client's risk aversion coefficient
rho_client_high = 0.95  # Upper limit for the client's risk aversion coefficient

N = 10000              # Number of simulations conducted


##########################
# Bank 1 parameters (us) #
##########################

# Possible returns we want to consider offering to the client
h1_values = np.array([0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07])
z = 0.07            # Percentage earning by the bank (in total, taking into account that "h" comes from here)
lambda1 = 0.8       # Penalty as a percentage on the bonus for early leaving
T1 = 8         # Minimum required time for the client to stay, if the offer by Bank 1 is accepted (yrs)

probs1 = probs[probs.Bank == 1][["Year", "Probability"]] # Extract the probabilities that the client leaves if bank 1 is chosen 
bank_risk_aversion = 0.1   # Risk aversion parameter for the bank

money_max = x * (1 + h1_values[-1])**T1          # Maximum capital aquired by the client if he accepts bank 1's offer (for standarization)
money_max_bank = (z - h1_values[0]) * x          # Maximum money possibly attained by the bank in 1 period (client accepts the minimal offer)
money_min_bank = (z - h1_values[-1]) * x    # Minimum money possibly attained by the bank in 1 period (client accepts the maximum offer)

###################################
# Competitors parameters #
###################################

# Each parameter is a list with j-th entry corresponding to j-th competitor

lambda2 = [0.8, 0.8]       # Percetange of penalty on the bonus for early leaving
T2 = [8,8]                 # Minimum required time for the client to stay, if the offer by the competitor is accepted

# Extract the probabilities that the client leaves given that he chooses bank 2 (competitor)
probs2 = probs[probs.Bank == 2][["Year", "Probability"]].reset_index()  # Reset the indices
probs2 = probs2[["Year", "Probability"]]
probs2 = [probs2, probs2]


# For the case with multiple competitors we make sure our absolute best offer is higher than the rest (to cover all possibilities)
h2_values = np.array([0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065])
h2_probs = np.array([0.05, 0.1, 0.2, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05])

h2_values = [h2_values, h2_values]
h2_probs  = [h2_probs , h2_probs]


#################################


# Load all the parameters in a dictionary to pass them to the class
simulation_params = {'x' : x, 'rho_client_low' : rho_client_low, 'rho_client_high' : rho_client_high, 
    'scale' : scale, 'N' : N, 'h1_values' : h1_values, 'z' : z, 'lambda1' : lambda1, 'T1' : T1, 
    'probs1' : probs1, 'bank_risk_aversion' : bank_risk_aversion, 'money_max' : money_max, 
    'money_max_bank' : money_max_bank, 'money_min_bank' : money_min_bank, 
    'lambda2' : lambda2, 'T2' : T2, 'probs2' : probs2, 'h2_values' : h2_values, 'h2_probs' : h2_probs}
