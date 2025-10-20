'''

Parses a collection of documents and creates an inverted index.

Tested using a dataset of stories from Scientific American issues from the 1800s. The data has been tokenized and stemmed but not stopped. Punctiation was stripped out and the Krovetz Stemmer was applied. 
Note that apostraphes are not removed and are instead used as word separators, so that "I've" tokenizes to "I" and "ve". That way, a phrase query "I ve" should find the word "I've". 
We will not use a stopword list in this case, allowing support for queries with conjuction words, e.g., "clumps and keys" in order.

Stories have the following format:

  { 
    "article" : "<article_number>",
    "storyID" : "<article_number>-<story_number>",
    "storynum" : "<story_number>",
    "url" : "<story_url>",
    "text" : "<story_text_after_processing_as_space_separated_tokens>"
  }


Documents are a list of JSON dictionary objects. For this project, we use an in-memory only index since we will not reuse it.

Inverted index is a dictionary of terms as keys and their corresponding posting list as values. It also contains four special key-value pairs to keep track of overall index data:
 - "xx_numDocs" : total number of docs in index
 - "xx_numUniqueTerms" : total number of unique terms in index
 - "xx_totalTF" : total term frequency in index
 - "xx_docLens" : a dictionary of docIDs as keys and the number of terms in that document as the value


'''

class PostingList:

  """
  A class defining a posting list data structure which will be the elements of the inverted index.
  
  Each unique term has a posting list, which contains the term, a list of postings, total term frequency across all documents, and a dictionary to look up postings by docID in the posting list. 
  A posting is a list containing the docID, the term frequency in that doc, and a list of positions of the term in that doc in order.
  A posting is initialized by passing the term to its constructor. It is updated by passing a docID and term position in that doc to its update method.
  
  """ 
  
  def __init__(self, term):
    self.term = term
    self.tf = 0
    self.pList = []
    self.docNumLookup = dict()

  def getDocNum(self, docID):
    return self.docNumLookup[docID]

  def getPosting(self, docID):
    return self.pList[self.getDocNum(docID)]

  def getList(self):
    return self.pList

  def getTF(self):
    return self.tf

  def hasDoc(self, docID):
    return docID in self.docNumLookup

  def getDocs(self):
    return list(self.docNumLookup.keys())

  def getNumDocs(self):
    return len(self.docNumLookup)


  def update(self, docID, pos):
    if docID not in self.docNumLookup:
      self.docNumLookup[docID] = len(self.pList)
      self.pList.append([docID, 1, [pos]])
    else:
      self.pList[self.getDocNum(docID)][2].append(pos)
      self.pList[self.getDocNum(docID)][1] += 1
    self.tf += 1

  def __repr__(self):
    return "[" + ', '.join(str(x) for x in self.pList) + "]"




def build_inverted_index(docs):
    """
      Build an inverted index from a collection of documents

      Args:
          file: the loaded sciam.json.gz file to parse

      Returns: an inverted index.
    """
    inverted_index = {}

    inverted_index["xx_numDocs"] = 0
    inverted_index["xx_numUniqueTerms"] = 0
    inverted_index["xx_totalTF"] = 0
    inverted_index["xx_docLens"] = dict()

    for doc in docs:
      terms = doc["text"].split()
      docLen = len(terms)
      docID = doc["storyID"]
      inverted_index["xx_numDocs"] += 1
      inverted_index["xx_docLens"][docID] = docLen
      for i in range (0, len(terms)):
        if terms[i] not in inverted_index:
          inverted_index[terms[i]] = PostingList(terms[i])
          inverted_index["xx_numUniqueTerms"] += 1
        inverted_index[terms[i]].update(docID, i+1)
        inverted_index["xx_totalTF"] += 1
    return inverted_index




'''

We use a debug function for the index once it is created to see information for each term in a list of terms we pass to function. 
It will first display the the number of documents in the collection, the number of unique terms across the collection, and the total number of term occurences across the collection.
Then, 
  If showTerms=False: it will display the number of documents it was found in, and the number of total occurences across the collection.
  If showTerms=True: it will instead display the posting list for each term with each posting separated by a space.

'''


def debug_inverted_index(inverted_index, terms, showTerms=True):
    """
      Print out debugging information for the index

      Args:
          inverted_index: the inverted index data structure.
          terms: an array of strings, representing the terms to debug
          showTerms: defaults to true, will print out inverted list instead of # of docs and occurrences for each term

      Returns: n/a
    """

    print(f"Total Index: {inverted_index['xx_numDocs']} docs, {inverted_index['xx_numUniqueTerms']} terms, {inverted_index['xx_totalTF']} occurrences \n")
    for term in terms:
      if term not in inverted_index:
        print("****" + term + " NOT FOUND ***** \n")
      else:
        print(f"{term} - {len(inverted_index[term].getList())} docs, {inverted_index[term].getTF()} occurrences")
        if showTerms:
          print(f"\t at: {inverted_index[term]}")


