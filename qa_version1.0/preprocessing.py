#!/usr/bin/env python
import sys, getopt, collections
import numpy as np
import scipy.optimize as op
import scipy.stats as stats
import string
from math import log


def read_QA_file(QA_file):
  question_dict = collections.defaultdict(list)
  answer_dict = collections.defaultdict(list)
  judgement_dict = collections.defaultdict(list)
  
  question_list = []
  
  n = 0
  qID = 0
  label = ''
  
  for line in open(QA_file):
    
    if '<QApairs' in line:
      qID = float(line[13:-3])
      question_list.append(qID)
    elif line == '<question>\n' or line == '<positive>\n' or line == '<negative>\n':
      n = 0
      label = line
    elif n == 1:
      if label == '<question>\n':
        question_dict[qID] = line.split('\t')
      elif label == '<positive>\n':
        answer_dict[qID].append(line.split('\t'))
        judgement_dict[qID].append(1)
      elif label == '<negative>\n':
        answer_dict[qID].append(line.split('\t'))
        judgement_dict[qID].append(0)
    n += 1
  
  return question_dict, answer_dict, judgement_dict, question_list


'''
def readQuestionFile(question_file):
  question_dict = collections.defaultdict(lambda: collections.defaultdict(list))
  n = 0
  q_index = 0
  for line in open(question_file):
    words = line.split('\t')
    if words[0][0] == '<' and str.isdigit(words[0][1]):
      q_index = int(words[0][1:-2])
      n = 0
    if n == 1:
      question_dict[q_index] = words
    n = n + 1
    
  return question_dict
  
def readAnswerFile(answer_file):
  answer_dict = collections.defaultdict(lambda: collections.defaultdict(list))
  answer_list = []
  a_index = 0
  n = 0
  for line in open(answer_file):
    words = line.split('\t')
    if words[0][0] == '<' and str.isdigit(words[0][1]):
      a_index = int(words[0][1:-2])
      n = 0
      answer_list = []
    elif words[0] == '\n':
      n = 0
    elif words[0][0] == '<' and words[0][1] == '/':
      answer_dict[a_index] = answer_list
    elif n == 1:
      answer_list.append(words)
    n = n + 1
  
  return answer_dict
  
def readJudgementFile(judgement_file):
  judgement_dict = collections.defaultdict(list)
  judgement_list = []
  for line in open(judgement_file):
    nums = line.split()
    q = int(nums[0])
    rank = int(nums[2])
    relv = int(nums[3])
    judgement_dict[q].append((rank,relv))
  return judgement_dict
'''  
def readWordFile(word_file):
  word_to_embedding = {}
  for line in open(word_file):
    sp = string.split(line)
    word_to_embedding[sp[0]] = [float(v) for v in sp[1:]]
  '''
  vec = np.array(word_to_embedding['the'])
  print vec.shape
  '''   
  return word_to_embedding
 

def main ():
  read_QA_file("./data/answerSelectionExperiments/data/dev-less-than-40.xml")

if __name__ == "__main__":
  main()


