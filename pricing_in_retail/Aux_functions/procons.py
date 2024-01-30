import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform, gamma, norm 

def procons(p1, p2, alpha_1, alpha_2, N, sigma):
    PR = 0
    M = np.arange(1, N)
    for j in M:
        PR = PR + utils.prob_client_decision(p1, p2, sigma[j])
    return PR/(N-1)

