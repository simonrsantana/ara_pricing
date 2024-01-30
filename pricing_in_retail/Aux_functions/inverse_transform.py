
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform, gamma, norm

def inverse_transform_sampling(n_samples, lower_lim, upper_lim, value_1, init_price_1, poly_degree, p_val, prices_precision_step = 1000):
    
    # Extract values from the cdf function
    price_range = np.linspace(lower_lim, upper_lim, prices_precision_step)
    cdf_values = np.array([cdf(x, value_1, init_price_1, poly_degree, p_val) for x in price_range])

    # Sample from the uniform
    unif = np.random.uniform(size = n_samples)

    # Obtain the samples through ITS
    idx = [(np.abs(cdf_values - sample)).argmin() for sample in unif]

    return price_range[idx]


def cdf(x, value_1, init_price_1, poly_degree, p_val):
    probs = np.array([unnorm_pdf(x, value_1, init_price_1, poly_degree) for x in p_val])
    norm_const = sampling_norm_constant_q2_p1(probs)
    avail_p = p_val[p_val < (x + 0.001)]
    cum_probs = np.sum( np.array([norm_const * unnorm_pdf(y, value_1, init_price_1, poly_degree) for y in avail_p]) )
    return cum_probs

def unnorm_pdf(x, value_1, init_price_1, poly_degree):

    if ((value_1 < x) and (x <= init_price_1)):
        y = (x - value_1)**poly_degree
    else:
        y = 0

    return y



def sampling_norm_constant_q2_p1(probs_sampled):
    return (1/np.sum(probs_sampled))


