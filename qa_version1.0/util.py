#!/usr/bin/env python
import sys, numpy, getopt

# implementation of mean average precision
# the predicted ranking list is like this
# [2, 1, 3] which means the second sentence
# ranks in the highest position, etc.
def MAP (predict_rank_dict, judgement_dict):
  average_precisions = []
  for qID, predict_rank_list in predict_rank_dict.iteritems():
    total_r = 0
    precision = 0
    for i in range(0, len(predict_rank_list)):
      index = predict_rank_list[i]
      r = judgement_dict[qID][index][1]
      total_r += r
      precision += (r*total_r)/float(i+1)
    if total_r == 0:
      average_precisions.append(0)
    else:
      average_precisions.append(precision/total_r)
  return sum(average_precisions)/len(average_precisions)

# implementation of reciprocal rank
def MRR (predict_rank_dict, judgement_dict):
  rrs =[]
  for qID, predict_rank_list in predict_rank_dict.iteritems():
    # searching the index of the top ranked sentence
    index = 0
    for i in range(0, len(judgement_dict[qID])):
      rank = judgement_dict[qID][i]
      if rank == 0:
        index = i
        break
    for predict_rank in range(0, len(predict_rank_list)):
      if predict_rank_list[predict_rank] == index:
        rrs.append((1/float(predict_rank))
        break
  return sum(rrs)/len(rrs)

'''
def main():
'''  

if __name__ == "__main__":
  sys.exit(main())
