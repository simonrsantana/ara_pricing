# ARA for personalized pricing
This repository contains the code for the manuscript titled "Personalized pricing through Adversarial Risk Analysis". The code present allows to reproduce the experiments shown in the paper, both for the pricing in retail case and for the pension fund market.

## 1. Python and libraries versions 

`python >= 3.8.10`

`pandas == 1.2.2`

`numpy  == 1.19.5`

## 2. Pricing in retail

Here we consider the pricing in retailing problem for different scenarios. As detailed in the paper, we assume that the customer bases his decision solely based on price, excluding other variables. 
The model employed here is thus a streamlined version of the general template outlined in the paper.
This particular case allows us to delve into the specifics of modeling, numerical and algorithmic details within a relevant application of interest,
while also facilitating comparisons concerning knowledge assumptions.

In this case we have constructed the code around `pricing_in_retail/run.py`, which executes the code for the specifications detailed in `pricing_in_retail/Config/config.json`. The parameters there include, among others:
* `poly_degree`: Degree of the polinomial to approximate the CDF in the inverse transform sampling
* `n_samples`: Number of samples to extract in the inverse transform sampling
* `lower_lim`: Lower limit set for the prices for the supported pricer
* `upper_lim`: Upper limit set for the prices for the supported pricer
* `alpha_1` and `alpha_2`: Parameters for the Gamma prior over the customer's standard deviation
* `N`: Number of runs to estimate the probability of acceptance of a given offer
* `value_1`: Value of producing the item sold for the supported pricer
* `value_2`: Value of producing the item sold for the competitor 
* `init_price_1`: Initial price for the supported pricer
* `init_price_2`: Initial price for the competitor
* `price_step`: Step width to explore the allowed price range (from `lower_lim` to `upper_lim`)
 
To run the code, move to `pricing_in_retail` and execute `run.py`. The code will output the figure with the information from the run alongside the optimal price suggested by the model.

## 3. Pricing in for the pension fund market

The problem of finding the optimal return of a pension plan offered to a client with a certain capital and certain sociodemographic conditions is considered. The optimal return is the one that maximizes the bank's expected utility. For the expected utility calculation, a strategy is developed to estimate the probability that a given client with a certain capital will accept a particular return.

A class named `static_retirement_decision` for this problem is defined in `pricing_pension_fund/static.py`. 
To initialize it, the following attributes are passed in the dictionary `params` (which constructed in `pricing_pension_fund/params_static.py`):

* `h1_values` : possible returns to be offered
* `z`         : bank's percentual benefit 
* `x`         : client's capital (in 10K euros)
* `lambda1`   : percentage of penalty from the bonus in bank 1
* `T1`        : permanence required in bank 1 (yrs) 
* `probs1`    : probs of early leaving in bank 1
* `bank_risk_aversion` : bank 1 risk aversion
* `money_max`: max. money possible for the client
* `money_max_bank`: max. money possible for the bank
* `money_min_bank`: min. money possible for the bank
* `lambda2`: penalty for early leaving in bank 2
* `T2`: peramenence required in bank 2
* `probs2`: probs. of early leaving in bank 2
* `h2_values`: possible returns offered by bank 2
* `h2_probs`:  estimated probs. of each possible return offered by bank 2
* `N`: number of simulations
* `rho_client_low`: estimated lower bound for client's risk aversion
* `rho_client_high`:  estimated upper bound for client's risk aversion


The class has two main methods:

* `estimate_prob_acceptance(self, h)`: this method estimates the probability of the client accepting a return of h

* `estimate_h`: this method finds the return h that maximized the bank's expected utility


#### Several competitors case

For the several competitors case, a class named `static_retirement_decision` for this problem is 
defined in `pricing_pension_fund/static_several_comp.py`. To initialize it, almost the same attributes 
as before are passed in the dictionary `params` (which constructed in `pricing_pension_fund/params_static_multiple_comps.py`).
The only difference is that now, the parameters corresponding to the competitors are lists whose j-th elements corresponds to the
parameters of the j-th competitor. For example, `lambda2[j]` is the penalty for early leaving in bank j.

Operationally, the difference w.r.t. the previous case is found in the `estimate_prob_acceptance(self, h)` method. Now, for each simulation
we compute the client's random expected utility in every competitor and compare those with the supported bank.  
