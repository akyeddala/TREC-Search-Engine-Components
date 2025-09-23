'''

We implement the following effectiveness measures used for evaluation on any trecrun files. If the file contains multiple queries (as most do), we calculate measures for each query, and then also produce the arithmetic mean of each evaluation measure across all queries in the trecrun file. 

Note that these numbers are produced for every query that occurs in the trecrun file. There will probably be queries listed in the qrels file that are not in the trecrun file, which will be ignored.

The measures are as follows:

  - numRel is the total number of relevant documents (relevance score above zero) that are listed in the qrels file for this query.
  - relFound is the count of those relevant documents that also appear in the ranked list of documents.
  - RR (Reciprocal Rank); if relFound is zero, then report “0” for this measure.
  - P@13 (Precision @ 13)
  - R@13 (Recall @ 13); if numRel is zero, then report "0" for this measure.
  - F1@13; if either precision or recall is zero, then report "0" for this measure.
  - AP (Average Precision); if numRel is zero, report "0".
  - nDCG@23 (there are multi-value relevance judgments in the data – 0,1,2 – though some queries only have 0/1 judgments). If numRel is zero, then report 0 for nDCG. Note: in calculating nDCG, the "ideal" DCG cannot be calculated using just the retrieved documents for a given query. 
  - BPREF. If numRel is zero, report "0". Use the formula (1/R) * Σ_(d_r) * (1 - (N_(d_r) / R)).
  - P@29R is precision when recall is 29 percent (note that this is percent recall and not rank 29); if numRel is zero, report "0". This requires that we interpolate to figure out the precision -- it is the maximum precision at any recall value R′ where R′ ≥ R.
  - P@R where R is the number of relevant documents for this query; if numRel is zero, report "0".

'''

def numRel(query: QueryInfo) -> int:
  """
  Calculate total number of relevant documents that are listed in the qrels file for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: number of relevant documents in the corpus for this query
  """

  return len(query.qrelRelDocs);



def relFound(query: QueryInfo) -> int:
  """
  Calculate the number of relevant documents retrieved in the ranked list for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: number of relevant documents retrieved in the ranked list for this query
  """

  count = 0;
  for trecLine in query.trecLines:
    if trecLine.doc_id in query.qrelRelDocs:
      count += 1

  return count;



def RR(query: QueryInfo) -> float:
  """
  Calculate the reciprocal rank for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: single number representing the reciprocal rank score of this query
  """

  if relFound(query) == 0:
    return 0

  for trecLine in query.trecLines:
    if trecLine.doc_id in query.qrelRelDocs:
      return 1/trecLine.rank

  return 0



def P_13(query: QueryInfo) -> float:
  """
  Calculate Precision at 13 for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: single number representing the P@13 score of this query
  """

  sum = 0
  trecLines = query.trecLines;
  qrelRelDocs = query.qrelRelDocs;
  for i in range(0,13):
    if len(trecLines) > i and trecLines[i].doc_id in query.qrelRelDocs:
      sum += 1


  return sum/13



def R_13(query: QueryInfo) -> float:
  """
  Calculate Recall at 13 for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: single number representing the R@13 score of this query
  """

  nRel = numRel(query)
  if nRel == 0:
    return 0

  sum = 0
  trecLines = query.trecLines;
  qrelRelDocs = query.qrelRelDocs;
  for i in range(0,13):
    if len(trecLines) > i and trecLines[i].doc_id in query.qrelRelDocs:
      sum += 1

  return sum / nRel



def F1_13(query: QueryInfo) -> float:
  """
  Calculate F1 score at 13 for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: single number representing the F1@13 score of this query
  """

  p = P_13(query)
  r = R_13(query)

  if p == 0 or r == 0:
    return 0

  return (2 * r * p) / (r + p)



def AP(query: QueryInfo) -> float:
  """
  Calculate Average Precision for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: single number representing the average precision score of this query
  """

  if numRel(query) == 0:
    return 0

  count = 0
  total = 0
  sum = 0

  for trecLine in query.trecLines:
    total += 1
    if trecLine.doc_id in query.qrelRelDocs:
      count += 1
      sum += count/total

  if count == 0:
    return 0

  return sum / numRel(query)



def NDCG_23(query: QueryInfo) -> float:
  """
  Calculate nDCG at 23 for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: single number representing the nDCG at 23 score of this query
  """

  if numRel(query) == 0:
    return 0

  trecLines = query.trecLines
  qrelRelDocs = query.qrelRelDocs
  qrelRelDocsRels = query.qrelRelDocsRels

  og = []
  ideal = []
  for i in range(0, 23):
    if len(trecLines) > i and trecLines[i].doc_id in qrelRelDocs:
      ind = qrelRelDocs.index(trecLines[i].doc_id)
      og.append(qrelRelDocsRels[ind])
    else:
      og.append(0)

  ideal = qrelRelDocsRels.copy()
  ideal.sort(reverse=True)
  if len(ideal) < 23:
    ideal.extend([0]*(23 - len(ideal)))
  elif len(ideal) > 23:
    ideal = ideal[:23]

  dcg = og[0]
  idcg = ideal[0]
  for i in range(1, 23):
    dcg += og[i] / math.log(i+1, 2)
    idcg += ideal[i] / math.log(i+1, 2)

  return dcg/idcg




def BPREF(query: QueryInfo) -> float:
  """
  Calculate BPREF for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: single number representing the BPREF score of this query
  """
  
  if numRel(query) == 0:
    return 0

  r = numRel(query)
  sum = 0
  nonRelCount = 0

  for trecLine in query.trecLines:
    if trecLine.doc_id not in query.qrelRelDocs:
      nonRelCount += 1
    else:
      ndr = nonRelCount if nonRelCount < r else r
      sum += 1 - ndr/r

  return sum / r




def P_29R(query: QueryInfo) -> float:
  """
  (Extra Credit) Calculate Precision at 29% recall for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: single number representing the Precision at 29% recall score of this query
  """

  nRel = numRel(query)
  if nRel == 0:
    return 0

  sum = 0
  trecLines = query.trecLines;
  qrelRelDocs = query.qrelRelDocs;
  ind29 = -1
  for i in range(0, len(trecLines)):
    if trecLines[i].doc_id in query.qrelRelDocs:
      sum += 1
    recall = sum / nRel
    if recall >= 0.29:
      ind29 = i
      break

  if ind29 == -1:
    return 0

  maxPrec = sum / (i+1)
  for j in range(i+1, len(trecLines)):
    if trecLines[j].doc_id in query.qrelRelDocs:
      sum += 1
    prec = sum / (j+1)
    if prec > maxPrec:
      maxPrec = prec

  return maxPrec



def PatR(query: QueryInfo) -> float:
  """
  (Extra Credit) Calculate Precision at the number of relevant documents for the given query.

  Args:
        query: input query holding the qrels and ranked list information

  Returns: single number representing the Precision at R score of this query
  """

  nRel = numRel(query)
  if nRel == 0:
    return 0

  sum = 0
  trecLines = query.trecLines;
  qrelRelDocs = query.qrelRelDocs;
  for i in range(0, nRel):
    if trecLines[i].doc_id in query.qrelRelDocs:
      sum += 1

  return sum / nRel


