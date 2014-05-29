#!/usr/bin/env python
import sys, getopt
import numpy as np

def main():
  q = np.array([2,3])
  M = np.array([[1,2, 3],[4,5,6]])
  a = np.array([0.1, 0.2, 0.1])
  print 'q.shape = ', q.shape
  print 'M.shape = ', M.shape
  print 'a.shape = ', a.shape
  z = np.dot(q, M)
  L = np.dot(z,a)
  print  'z = ', z
  print 'L = ', L
  q = np.reshape(q, (-1,1))
  a = np.reshape(a, (-1,3))
  print 'after transpose a.shape = ', a.shape
  print 'after transpose q.shape = ', q.shape
  print 'qa = ', np.dot(q, a)
  M = np.ndarray.flatten(M)
  #M = M.T
  print 'after flatten M = ', M
  print 'after flatten M.shape = ', M.shape
  M = np.reshape(M, (-1, 3))
  print 'after reshape M = ', M
  print 'after reshape M.shape = ', M.shape

if __name__ == "__main__":
  sys.exit(main())
