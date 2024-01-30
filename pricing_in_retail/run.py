import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import uniform, gamma, norm 
from Aux_functions import pricing
from Aux_functions import procons # ,
from Aux_functions import generate_p2 # , procons
# from Config import config 
from Utils import utils
from Aux_functions.inverse_transform import inverse_transform_sampling

# Read the configuration file
config = utils.read_json("config.json")

# Run the codes
def run_pricing(config):
    #Define params from config
    lower_lim = config["lower_lim"]
    upper_lim = config["upper_lim"]
    poly_degree = config["poly_degree"]
    n_steps = config["n_steps"]
    n_samples = config["n_samples"]
    price_step = config["price_step"]
    p_val = np.arange(lower_lim, upper_lim, price_step)
    alpha_1 = config["alpha_1"]
    alpha_2 = 1/config["alpha_2"]
    N = config["N"]
    value_1 = config["value_1"]
    value_2= config["value_2"]
    init_price_1 = config["init_price_1"]
    init_price_2 = config["init_price_2"]
    
    # Sigma samples 
    sigma = list(utils.sigma_2_client_decision(alpha_1, alpha_2, N))
    # sigma = np.ones(10)*0.1
    
    #Generate p1 samples for retailer 2 
    p1_samples = inverse_transform_sampling(n_samples, lower_lim, upper_lim, value_2, init_price_2, poly_degree, p_val)

    #Paint the samples
    probs = np.array([utils.unnorm_pdf(x, value_1, init_price_1, poly_degree) for x in p_val])
    
    #Generate p2 samples
    # p2_samples = generate_p2.generate_p2(p1_samples, alpha_1, alpha_2, N, value_2, init_price_2, price_step, sigma)
    p2_samples = np.ones(100)*30

    #Fix final price for p1
    prices_r1 = np.arange(value_1, upper_lim, price_step)

    final_price, prob, list_probs, util = pricing.pricing(p2_samples, prices_r1, alpha_1, alpha_2, p_val, N, value_1, sigma)
    
    return prices_r1, p1_samples, p2_samples, final_price, prob, list_probs, util, sigma
    
a, b, c, d, e, f, g, h = run_pricing(config)


# Generate the plots

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Price set (€)')
ax1.set_ylabel('Estimated probabilities') # , color=color)
ax1.plot(a, f, color=color)
ax1.tick_params(axis='y') # , labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax2.set_ylabel('Utilities') # , color=color)  # we already handled the x-label with ax1
ax2.plot(a, g, color=color)
ax2.tick_params(axis='y') #, labelcolor=color)
max_index = np.argmax(g)
ax2.axvline(a[max_index], color = 'green', linestyle = ':')

print("Best price: " + str(a[max_index]))
print("Prob: " + str(f[max_index]))


fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.show()


plt.savefig("results_pricing_tmp.pdf")
