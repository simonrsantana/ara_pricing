import numpy as np
from scipy.stats import norm 
import json



def read_json(file):
    """
    Wrapper function to read json file into a python dictionary

    :param file: path to json file
    :return: content of json file (type: dict)
    """
    with open(file, 'r') as f: 
        data = json.load(f)
    return data

def prob_client_decision(price_1, price_2, sigma_2):
    """
    Obtain the probability that the client chooses a given offer

    Input:
        price_1
        price_2
        sigma_2
        
    Output:
        (gamma distribution sampled in value (x) with parameters alpha_1, alpha_2
    """

    # The default Normal distribution is already the standard N(0,1)
    return 1 - norm.cdf((price_1 - price_2) / sigma_2)

def sigma_2_client_decision(alpha_1, alpha_2, N):
    """
    Obtain a sample from the sigma^2 for the client decision

    Input:
        alpha_1
        alpha_2

    Output:
        (gamma distribution sampled in value (x) with parameters alpha_1, alpha_2
    """

    # Client's decision variance
    return np.random.gamma(alpha_1, alpha_2, N)

def unnorm_pdf(x, min_value, max_value, poly_degree):

    if ((min_value < x) and (x <= max_value)):
        y = (x - min_value)**poly_degree
    else:
        y = 0

    return y

def analytic_norm_constant_q2_p1(prices_probs, available_prices):
    return (1/np.trapz(y = available_prices, x = prices_probs)) # scipy.metrics area under curve (auc)