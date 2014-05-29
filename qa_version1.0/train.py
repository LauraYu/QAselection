#!/usr/bin/env python
import sys, getopt
import numpy as np
import scipy.optimize as op

from log_reg import *
#from util import *
from preprocessing import *


embed_size = 50
# These three functions are helpers for the BFGS optimiser
last_func=0
iterations=0
def function(M, qa_dict, judgement_dict, r, b): 
  global last_func
  last_func = objective(qa_dict, judgement_dict,M, b) + log_prior(M, r, b)
  return last_func

def function_grad(M, qa_dict, judgement_dict, r, b): 
  return grad(qa_dict, judgement_dict,M, b)+prior_grad(M, r) 

def report(M):
  global last_func
  global iterations
  if not (iterations % 10):
    print '   iteration', iterations, ': cross entropy=', last_func
  iterations += 1


def get_QA_model(question_dict, answer_dict, \
    word_to_embeddings):
  qa_dict = collections.defaultdict(list)
  
  for qID, question in question_dict.iteritems():
    qa_list = []
    q_vec = np.zeros(embed_size, 'f')   
    n = 0
    for word in question:
      # delete '/n' in the last word of the sentence
      if n == len(question)-1:
        word = word[:-1]
      if word not in word_to_embeddings:
        word = "*UNKNOWN*"
      w_vec = np.array(word_to_embeddings[word])
      q_vec = q_vec + w_vec
      n += 1
    '''  
    print qID, ' answers.length = ', len(answer_dict[qID])
    print 'judgement.length = ', len(judgement_dict[qID])  
    '''  
    
    for answer in answer_dict[qID]:
      a_vec = np.zeros(embed_size, 'f')
      n = 0
      for word in answer:
        # delete '/n' in the last word of the sentence
        if n == len(answer)-1:
          word = word[:-1]
        if word not in word_to_embeddings:
          word = "*UNKNOWN*"
        
        w_vec = np.array(word_to_embeddings[word])
        a_vec += w_vec
        n += 1
      qa_list.append((q_vec, a_vec))
    qa_dict[qID] = qa_list  
    #print len(qa_list)  
  return qa_dict

'''
def getScore(qa_dict, M):
  ranked_probs_dict = collections.defaultdict(list)
  for qID, qa_list in qa_dict.iteriterms():
    probs_list = []
    i = 0
    for q, a in qa_list:
      temp = np.dot(q, M)
      z = np.dot(temp, a)
      prob = np.exp(log_sigmoid(z))
      probs_list.append((prob, i))
      i += 1
    ranked_probs_dict[qID] = [index for prob, index in sorted(probs_list, key=itemgetter(0))]
  return MAP(ranked_probs_dict, judgement_dict),\
         MRR(ranked_probs_dict, judgement_dict)
'''

def getScore(qa_dict, M):
  probs_dict = collections.defaultdict(list) 
  for qID, qa_list in qa_dict.iteritems():
    for q, a in qa_list:
      temp = np.dot(q, M)
      z = np.dot(temp, a)
      prob = np.exp(log_sigmoid(z))
      probs_dict[qID].append(prob)
  return probs_dict

def experiment(cmdline_args):
  # Process training files 
  word_file="./data/embeddings-scaled.EMBEDDING_SIZE=50.txt"
  QA_file="./data/answerSelectionExperiments/data/train-less-than-40.xml" 
  
  question_dict, answer_dict, judgement_dict, question_list = \
  read_QA_file(QA_file)
  word_to_embeddings = readWordFile(word_file)

  qa_dict = get_QA_model(question_dict, answer_dict, \
    word_to_embeddings)
  
  M = np.zeros((embed_size,embed_size))
  #print 'M.shape = ', M.shape
  
  if cmdline_args['bfgs']:
    # Use the quasi-Newton convex optimisation algorithm BFGS from Scipy. It's much more 
    # effective than gradient descent.
    # BFGS is an iterative algorithm which calls function(w) and function_grad(w) on each iteration 
    # to calculate the objective function and its gradient. The function report(w) is also called
    # to enable the progress of the optimisation to be reported to stdout. gtol is the gradient
    # tolerance, if the norm of the gradient doesn't change by at least this much between 
    # iterations the optimiser will terminate.
    print "Optimising with BFGS:"
    M = op.fmin_bfgs(function, M, args=(qa_dict,judgement_dict,cmdline_args["regularisation"], True), fprime=function_grad, \
                     callback=report, maxiter=cmdline_args["iterations"], \
                     gtol=cmdline_args["threshold"])
    M = np.reshape(M, (-1, embed_size))
  else: # otherwise use gradient descent
    print "Optimising with Gradient Descent:"
    for i in range(cmdline_args["iterations"]):
      M -= cmdline_args["eta"] * function_grad(M, qa_dict, judgement_dict, cmdline_args["regularisation"], False) 
      if not (i% 10):
        print '   iteration', i, ': cross entropy=', function(M, qa_dict, judgement_dict, cmdline_args["regularisation"], False)

  M_out = open("training_result.txt", 'w')
  print >>M_out, M
  M_out.close()
  print '\nFinal training cross entropy', objective(qa_dict, judgement_dict,M, False)
  

  # Use the learnt model to assign probabilities to each QA pair
  test_QA_file="./data/answerSelectionExperiments/data/dev-less-than-40.xml" 
  
  test_question_dict, test_answer_dict, test_judgement_dict, test_question_list = \
  read_QA_file(test_QA_file)

  test_qa_dict = get_QA_model(test_question_dict, test_answer_dict, \
    word_to_embeddings)
  probs_dict = getScore(test_qa_dict, M)

  # Generate output file
  out = open(cmdline_args['test-out'],'w')
  for i in range(0, len(test_question_list)):
    qID = test_question_list[i]
    answer_prob_list = probs_dict[qID]
    for j in range(0, len(answer_prob_list)):
        prob = answer_prob_list[j]
        print >>out, i+1, ' ' , 'Q0 ', j, ' 0 ', prob, ' standard'
  out.close()
  


  '''
  print 'Final heldout cross entropy', (objective(xdev, tdev, w))

  # Use the learnt model to assign probabilities to each training and development point
  probs = np.exp(log_sigmoid(np.dot(x, w)))
  dev_probs = np.exp(log_sigmoid(np.dot(xdev, w)))

  # AUC calculation
  print '\nTraining AUC', AUC(t,probs)
  print 'Heldout development AUC', AUC(tdev,dev_probs)

  # Use the learnt model to assign probabilities to each test point
  test_probs = np.exp(log_sigmoid(np.dot(xtest, w)))

  # label the test data using the learnt feature weights w
  out = open(cmdline_args['test-out'],'w')
  print >>out, "Id,solution"
  for i,p in enumerate(test_probs):
    print >>out,'%d,%f' % (i+1,p)
  out.close()
  '''
 
    
   
    
   
     
      
    

def main(argv=None):
  experiment_args = {}
  experiment_args["iterations"] = 30
  experiment_args["eta"] = 1e-8
  experiment_args["regularisation"] = 10
  experiment_args["threshold"] = 1e1
  experiment_args["bfgs"] = False
  experiment_args["test-out"] = "result.txt"

  # Example command line argument processing.
  # You can add any arguments you see fit. 
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "hi:n:r:t:bo:", 
                                 ["help",
                                  "iterations=",
                                  "eta=",
                                  "threshold=",
                                  "test-out=",
                                  "bfgs",
                                  "regularisation-parameter="])
    except getopt.error, msg:
      raise Usage(msg)

    # process options
    for option, argument in opts:
      if option in ("-h", "--help"):
        print __doc__
        sys.exit(0)
      if option in ("-i", "--iterations"):
        experiment_args["iterations"] =int(argument)
      if option in ("-n", "--eta"):
        experiment_args["eta"] = float(argument)
      if option in ("-t", "--threshold"):
        experiment_args["threshold"] = float(argument)
      if option in ("-r", "--regularisation-parameter"):
        experiment_args["regularisation"] = float(argument)
      if option in ("-o", "--test-out"):
        experiment_args["test-out"] = argument
      if option in ("-b", "--bfgs"):
        experiment_args["bfgs"] = True

  except Usage, err:
    print "Error parsing command line arguments:"
    print >>sys.stderr, "  %s" % err.msg
    print __doc__
    return 2
  
 
  # run our experiment function
  experiment(experiment_args)




if __name__ == "__main__":
  main()
