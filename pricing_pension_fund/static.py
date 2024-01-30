'''

ESTE CÓDIGO CONTIENE LA PARTE PRINCIPAL DEL PROBLEMA ESTÁTICO DE PENSIONES PARA EL CASO ESTÁTICO

Como se hace para otros problemas, lo resolvemos definiendo una clase con las diferentes métodos 
establecidos en el texto principal y ejecutándolo conforme a lo que hemos descrito en el modelo. s

'''



# Import the packages needed
import numpy as np
import pandas as pd


"""
Class for the static retirment plans problem
"""

class static_retirement_decision:

    '''
    Initialize the class
    Args:
        params  :   Dictionary contanining all of the parameters for the simulation
    '''
    def __init__(self, params):

        ##########################
        # Bank 1 parameters (us) #
        ##########################

        self.h1_values = params["h1_values"]                    # Returns offered 
        self.z = params["z"]                                    # Bank 1 benefits
        self.x = params["x"]                                    # Client's capital (in 10K euros)
        self.lambda1 = params["lambda1"]                        # Percentage of penalty from the bonus
        self.T1 = params["T1"]                                  # Permanence required (yrs)
        self.probs1 = params["probs1"]                          # Probs of leaving early in bank 1
        self.bank_risk_aversion = params["bank_risk_aversion"]  # Bank 1 risk aversion
        self.money_max = params["money_max"]                    # Max. money possible for the client
        self.money_max_bank = params["money_max_bank"]          # Max. money possible for the bank
        self.money_min_bank = params["money_min_bank"]          # Min. money possible for the bank

        ##################################
        # Bank 2 parameters (competitor) #
        ##################################

        self.lambda2 = params["lambda2"]                        # Penalty for early leaving in bank 2
        self.T2 = params["T2"]                                  # Peramenence required in bank 2
        self.probs2 = params["probs2"]                          # Probs. of early leaving in bank 2
        self.h2_values = params["h2_values"]                    # Possible returns offered by bank 2
        self.h2_probs = params["h2_probs"]                      # Probs. of each possible return by bank 2

        #########################
        # Simulation parameters #
        #########################
        
        self.N = params["N"]                                    # Number of simulations
        self.rho_client_low = params["rho_client_low"]          # Lower bound for client's risk aversion
        self.rho_client_high = params["rho_client_high"]        # Upper bound for client's risk aversion
        

    """
    Create a method to estimate the probabiliy that the client accepts a given offer

    Input:
        self                :       previous information loadad in the model
        h                   :       bonus proposed to the client

    Output:
        estimated_prob      :       estimated probability of acceptance of the client if offer h is presented
    """

    def estimate_prob_acceptance(self, h):

        # Initialize the count to estimate the probability
        count = 0           # Count of how many times the client prefers our offer to the competitor's

        # Count how many times the client decides it is a tie between Bank 1
        # and Bank 2
        tie_count = 0

        # Initialize the lists of the client's utilities
        u1 = []
        u2 = []

        # Start the simulation, which will be run N times
        for i in range(self.N):

            # Sample the risk-aversion parameter
            # The rho sample is shared between bank 1 and 2 (same client)
            rho_sample = np.random.uniform(self.rho_client_low, self.rho_client_high) 

            # Sample a possible bonus for the competitor's bank, given by "h",
            # with probabilities "p"
            h2 = np.random.choice(self.h2_values, p = self.h2_probs)

            # Compute the utilities for the client of choosing the offer by
            # each bank
            ut1 = self.compute_utility(
                self.probs1,
                h,
                self.x,
                self.T1,
                rho_sample,
                self.money_max,
                self.lambda1)  # utility for the client if he chooses bank 1

            ut2 = self.compute_utility(
                self.probs2,
                h2,
                self.x,
                self.T2,
                rho_sample,
                self.money_max,
                self.lambda2)  # utility for the client if he chooses bank 2

            # Store the different utilities (*output disabled*)
            u1.append(ut1)
            u2.append(ut2)

            #ut2 = self.compute_utility(self.probs2, self.h2, self.x, self.T2, self.lambda2, rho_sample)

            # Update the count of the successful results to estimate the
            # probability
            if ut1 > ut2:
                count += 1

            if ut1 == ut2:  # Check in case there is a tie
                tie_count += 1

        # Obtain the estimated probability as the quotient of each count
        # divided by the total number of tries made (N)
        # estimated probability of acceptance of offer by Bank 1
        estimated_prob = count / self.N
        
        # estimated probability of tie between offer of Bank 1 and Bank 2
        tie_prob = tie_count / self.N

        # Output the estimated probability of acceptance
        return estimated_prob  # , tie_prob, u1, u2

    """
    Create a method to estimate the best possible h so that we maximize the Bank 1's utility

    Input:
        self                            :       Previous information loadad in the model

    Output:
        optimal_h_offer                 :       Optimal h offer
        exp_utilities                   :       Array of expected utilities for each given h ("product" of probs and utilities)
        utilities_array                 :       Array of utilities for the bank of each offer h
        probabilities                   :       Array of probabilities for each offer h

    """

    def estimate_h(self):

        # Create empty lists to contain the results for each important value
        exp_ut = []
        ut = []
        probs = []

        # Test the estimated utility for each h
        for h in self.h1_values:

            # Estimate the probability of acceptance given a h1 value
            prob_h1_tmp = self.estimate_prob_acceptance(h)
            probs.append(prob_h1_tmp)

            # Compute the utility for the bank given an offer of value h1 to
            # the client
            ut_bank = self.risk_averse_utility(
                (self.z - h) * self.x,
                self.bank_risk_aversion,
                self.money_max_bank,
                self.money_min_bank)
            ut.append(ut_bank)

            # Estimate the expected utility
            exp_ut.append(ut_bank * prob_h1_tmp)

            # Print the current state in the simulation once it is finished
            print("h1 " + str(h) + " finished")

        # Locate the optimal h between all available
        max_position = exp_ut.index(max(exp_ut))

        # Define the outputs
        optimal_h_offer = self.h1_values[max_position]
        exp_utilities = np.array(exp_ut)
        utilities_array = np.array(ut)
        probabilities = np.array(probs)

        return optimal_h_offer, exp_utilities, utilities_array, probabilities


##################
#                #
# Static methods #
#                #
##################

    """
    Function of the risk-averse-utility
    Input:
        x               :       Quantity of money subject to the utility
        rho             :       Risk aversion parameter
        money_max       :       Maximum amount of money attained in each case (to standardize the results)
        money_min       :       Minimum amount of money attained in each case (to standardize the results)

    Output:
        ut_norm         :       Estimated utility
    """

    @staticmethod
    def risk_averse_utility(x, rho, money_max, money_min=0):

        # Original estimate of the utility
        ut = (1 - np.exp(-rho * x))

        # Standardization of the utility
        ut_max = (1 - np.exp(-rho * money_max))
        ut_min = (1 - np.exp(-rho * money_min))

        ut_norm = (ut - ut_min) / (ut_max - ut_min)

        # Output the standardized utiltiy
        return ut_norm

    """
    Function for the estimated utility of the client given certain bank's parameters

    Input:
        probs           :       Probabilities of the client to leave at different times
        h               :       Proposed bonus offer
        x               :       Quantity of money subject to the utility
        T1              :       Required time of permanence inside the plan
        rho             :       Risk aversion parameter (for the client)
        lmb_coeff       :       Percetange of penalty on the bonus for early leaving
        money_max       :       Maximum amount of money attained in each case (to standardize the results)

    Output:
        estimated_ut    :       Estimated utility for the input setup
    """

    @staticmethod
    def compute_utility(probs, h, x, T1, rho, money_max, lmb_coeff):  # lmb

        # Bonus for the client for each year (total amount of money he would
        # have each year in an array of length equal to T1)
        bonus = (np.array([(1 + h)**i for i in range(1, T1 + 1)]) * x)  # - x (if we uncomment this, it's only the extra bonus)

        # Total penalty as a percentage of the bonus, in 10K euros
        lmb = (bonus - x) * lmb_coeff

        # Estimate the utility for the client in the first bank according to
        # the expression in the paper

        # First term in the summation
        ut1_first_term = (float(1 - np.sum(probs[["Probability"]])) *
                          static_retirement_decision.risk_averse_utility(bonus[-1], rho, money_max))

        # Second term in the summation
        ut1_sec_term = 0.0
        for j in range(probs.shape[0]):

            ut1_sec_term += (probs.loc[j, "Probability"] *
                             static_retirement_decision.risk_averse_utility((bonus[j] -
                                                                             lmb[j]), rho, money_max))

        estimated_ut = ut1_first_term + ut1_sec_term

        # Output the estimated utility for the setup given
        return estimated_ut
