'''

Load data from trec datasets (qrels: relevance of queries to documents; and trecrun: system runs to evaluate) into a data structure for ease of use and efficiency


A trecrun file contains the actual system runs that you are going to evaluate. It is a text file with six space-separated columns on every line (note that for obvious reasons, no column can contain spaces):

  The first column is the query name (aka query id)
  The second column is unused and should always contain "skip" (for historical reasons)
  The third column is a document identifier (“docid”)
  The fourth column is the rank of that document for that query in this run
  The fifth column is the score from the retrieval model.
  The sixth column is some text to describe the run itself, normally the same for every line in the file.


The qrels file contains judgment information: given a query and a document, is the document relevant to the query? It is another space-separated text file:

  The first column is the query name/id (corresponding to the query name/id in the trecrun files)
  The second column is unused (it is present for historical reasons; you won't need to do anything with it except be sure you read it to get to the remaining columns)
  The third column is a document identifier (“docid”)
  The fourth column is a number representing the relevance of the document, either 0 for non-relevant, or positive for relevant.


Note that for many of the query-docid pairs in the trecrun file, there is a corresponding pair in the qrels file, which is used to evaluate how well the retrieval model did for that query. 
However, large numbers of query-docid pairs will be unjudged, so they will not appear in the qrels file. In this case, we assume that the query-docid pair is non-relevant (i.e., has a relevance score of zero).


# 1.1 Creating a data structure

'''



class QueryInfo:
  """
  QueryInfo class: store the trecrun and qrels data of each query
  """


  def __init__(self, query_id):
    self.query_id = query_id
    self.trecLines = [];
    self.qrelLines = [];
    self.trecDocs = [];
    self.qrelRelDocs = [];
    self.qrelRelDocsRels = [];

  def addTrecLine(self, trecLine):
    temp = TrecLine(trecLine)
    self.trecLines.append(temp)
    self.trecDocs.append(temp.doc_id)


  def addQrelLine(self, qrelLine):
    temp = QrelLine(qrelLine)
    self.qrelLines.append(temp)
    if temp.relevance > 0:
      self.qrelRelDocs.append(temp.doc_id)
      self.qrelRelDocsRels.append(temp.relevance)

class TrecLine:
  def __init__(self, trecLine):
    temp = trecLine.split(' ');
    self.query_id = temp[0];
    self.doc_id = temp[2];
    self.rank = int(temp[3]);
    self.score = temp[4];
    self.text = temp[5];

class QrelLine:
  def __init__(self, qrelLine):
    temp = qrelLine.split(' ');
    self.query_id = temp[0];
    self.doc_id = temp[2];
    self.relevance = int(temp[3]);



queries = dict[str, QueryInfo]() # dictionary to store query_id/QueryInfo mappings



'''

# 1.2 Parsing trecruns

'''


def read_trecrun(trecRunFile: str, queriesDict: dict[str, QueryInfo]) -> None:
  """
  Read the trecrun file data and store the ranking lists for each query in a corresponding QueryInfo object.

  Args:
        trecRunFile: path to where the trecrun file is stored
        queriesDict: dictionary to store QueryInfos, mapping each query's id to its corresponding QueryInfo object
  """


  trecFile = open(trecRunFile, 'r')
  for trecLine in trecFile:
    tl = TrecLine(trecLine)
    if tl.query_id not in queriesDict:
      queriesDict[tl.query_id] = QueryInfo(tl.query_id)
    queriesDict[tl.query_id].addTrecLine(trecLine)

  trecFile.close()


'''

# 1.3 Parsing qrels Add the qrels data to the data structure as well


'''


def read_qrels(qrelsFile: str, queriesDict: dict[str, QueryInfo]) -> None:
  """
  Read the qrels file data and store the relevance judgements for each query in a corresponding QueryInfo object.

  Args:
        qrelsFile: path to where the qrels file is stored
        queriesDict: dictionary to store QueryInfos, mapping each query's id to its corresponding QueryInfo object
  """


  qrelFile = open(qrelsFile, 'r')
  for qrelLine in qrelFile:
    ql = QrelLine(qrelLine)
    if ql.query_id not in queriesDict:
      continue
    else:
      queriesDict[ql.query_id].addQrelLine(qrelLine)

  qrelFile.close()























