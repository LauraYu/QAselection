import numpy as np
from util import *

def sigmoid(z):
  return 1 / (1 + np.exp(-z))

def log_sigmoid(z):
  # n.b. -np.logaddexp(0,-z) calculates -log(1+exp(-z)) 
  # in log space without exponentiation to avoid overflow.
  # Try help(numpy.logaddexp) in the interpreter for
  # more information.
  return -np.logaddexp(0,-z)

def log_sigmoid_complement(z):
  return -np.logaddexp(0,z)

# This function should calculate the negative conditional 
# log probability of the data x given weights w and 
# observed response variables y.
def objective(x, y, w):
  z = np.dot(x, w)
  L = np.zeros(y.shape)
  ls = log_sigmoid(z)
  lsc = log_sigmoid_complement(z)
  for i in range (0, y.shape[0]):
    L[i] = -y[i] * ls[i] - (1 - y[i]) * lsc[i] 
  return L

# This is the log Gaussian prior 
def log_prior(w, alpha):
  return np.dot(w, w) / (2*alpha)

# This function should calculate the gradient of the negative 
# conditional log probability of the data x given weights w
# and observed response variables y.
def grad(x, y, w):
  z = np.dot(x, w)
  m = np.exp(log_sigmoid(z))
  r1 = np.dot(m.transpose(), x)
  r2 = np.dot(y.transpose(), x)
  r = r1 - r2
  r.shape = r.shape[0]
  return r
  

# This is the derivative of the Gaussian prior
def prior_grad(w, alpha):
  return (w/alpha)
