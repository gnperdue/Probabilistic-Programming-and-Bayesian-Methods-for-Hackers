import numpy as np
import pymc3 as pm
import theano.tensor as tt

count_data = np.loadtxt('data/txtdata.csv')

with pm.Model() as model:
    alpha = 1.0 / count_data.mean()
    lambda_1 = pm.Exponential('lambda_1', alpha)
    lambda_2 = pm.Exponential('lambda_2', alpha)
    tau = pm.DiscreteUniform('tau', lower=0, upper=len(count_data)-1)
    idx = np.arange(len(count_data))
    lambda_ = pm.math.switch(tau >= idx, lambda_1, lambda_2)
    observation = pm.Poisson('obs', lambda_, observed=count_data)

with model:
    step = pm.Metropolis()
    trace = pm.sample(10000, tune=5000, step=step)

lambda_1_samples = trace['lambda_1']
lambda_2_samples = trace['lambda_2']
tau_samples = trace['tau']

print(lambda_1_samples)
print(lambda_2_samples)
print(tau_samples)
