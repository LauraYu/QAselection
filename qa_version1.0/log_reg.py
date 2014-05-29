import sys, getopt
import numpy as np
#from util import *

embed_size = 50

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
def objective(qa_dict, judgement_dict, M, b):
  if b:
    M = np.reshape(M, (-1, embed_size))
  L = 0
  for qID, qa in qa_dict.iteritems():
    n = 0
    for q, a in qa:
      '''
      print n,':'
      print 'q = ', q
      print 'q.shape = ', q.shape
      print 'a = ', a
      print 'a.shape = ', a.shape
      '''
      temp = np.dot(q, M)
      '''
      print 'temp = ', temp
      print 'temp.shape = ', temp.shape
      '''
      z = np.dot(temp, a)
      '''
      print 'z = ', z
      '''
      ls = log_sigmoid(z)
      lsc = log_sigmoid_complement(z)
      '''
      print 'ls = ', ls
      print 'lsc = ', lsc
      '''
      r = judgement_dict[qID][n]
      L += -r * ls - (1 - r) * lsc
      '''
      print 'added value = ', -r * ls - (1 - r) * lsc
      
      print 'r = ', r
      print 'L = ', L
      '''
      n += 1
  return L


# This is the log Gaussian prior 
def log_prior(M, alpha, b):
  '''
  print 'M = ', M
  print 'M.shape = ', M.shape
  print 'M.T = ', M.T
  print 'M.T.shape = ', M.T.shape
  print 'trace(M, M.T) = ', np.trace(np.dot(M, M.T))
  '''
  if b:
    M = np.reshape(M, (-1, embed_size))
  return -np.trace(np.dot(M, M.T)) * alpha / 2

# This function should calculate the gradient of the negative 
# conditional log probability of the data x given weights w
# and observed response variables y.
def grad(qa_dict, judgement_dict, M, b):
  if b:
    M = np.reshape(M, (-1, embed_size))
  L = 0
  for qID, qa in qa_dict.iteritems():
    n = 0
    for q, a in qa:
      '''
      print 'q = ', q
      print 'M.shape ', M.shape
      '''
      temp = np.dot(q, M)
      ''' 
      print n,':'
      print 'q = ', q
      print 'q.shape = ', q.shape
      print 'a = ', a
      print 'a.shape = ', a.shape
      '''
      
      z = np.dot(temp, a)
      '''
      print 'temp = ', temp
      print 'temp.shape = ', temp.shape
      '''
      r1 = np.exp(log_sigmoid(z))
      r2 = judgement_dict[qID][n]
      q = np.reshape(q, (-1, 1))
      a = np.reshape(a, (-1, a.shape[0]))
      '''
      print 'after reshaping, q = ', q
      print 'after reshaping, q.shape = ', q.shape
      print 'after reshaping, a = ', a
      print 'after reshaping, a.shape = ', a.shape
      '''
      m = np.dot(q, a)
      '''
      print 'm = ', m
      print 'm.shape = ', m.shape
      '''
      L += (r1 - r2)*m
      '''
      print 'L = ', L
      '''
      n += 1
  if b:    
    L = np.ndarray.flatten(L)
  return L

def grad_SGD(q, a, r, M):
  temp = np.dot(q, M)
  z = np.dot(temp, a)
  r1 = np.exp(log_sigmoid(z))
  r2 = judgement_dict[qID][n]
  q = np.reshape(q, (-1, 1))
  a = np.reshape(a, (-1, a.shape[0]))
  m = np.dot(q, a)
  return (r1 - r2)*m

# This is the derivative of the Gaussian prior
def prior_grad(M, alpha):
  return -alpha * M
  
def main():
  qa_dict = {}
  qa_dict[1] = [(np.array([2, 1, 2]), np.array([0.1, 0.2, 0.1])),\
                (np.array([2, 1, 2]), np.array([0.5, 0.1, 0.2]))]
  judgement_dict = {}
  judgement_dict[1] = [1, 0]
  
  M = np.array([[1, 2, 3],\
                [4, 5, 6],\
                [2, 3, 1]])
  print 'M = ', M
  M_ = np.zeros((3, 3))
  print 'M_ = ', M_
  
  alpha = 0.1
  
  print 'objective:'
  objective(qa_dict, judgement_dict, M, False)
  print 'log_prior:'
  log_prior(M, alpha, False)
  print 'grad:'
  grad(qa_dict, judgement_dict, M, False)
 
if __name__ == "__main__":
  sys.exit(main())
  
