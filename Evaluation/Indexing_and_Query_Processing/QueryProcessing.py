'''

We run a sequence of queries from a tsv file. The list of queries comprises lines with at least three fields separted by tabs (tsv) in the format:

  queryType  queryName  wordPhrase1  wordPhrase2  ...  wordPhraseN

where 
- wordPhrase is a phrase containing words that occur adjacently in an article in that given order, with each token being space separated (can be one word), which must be found using the inverted index. There will always be at least one wordPhrase and there is no limit to N.
- queryType indicates the type of query to process.
    Query types:
      - AND: a Boolean query that includes all of the wordPhrases listed
      - OR: a Boolean query that inlcudes any one of the wordPhrases listed
      - QL: a query likelihood algorithm with the wordPhrases as the query. Our version uses Dirichlet smoothing with μ=300.
      - BM25: the BM25 algorithm with the wordPhrases as the query. We use k_1=1.8, k2=5, b=0.75 in the algorithm.
      - TF: a calculation of the raw term frequence of wordPhrase for each story it appears in. Only one wordPhrase1 (one phrase or word) is inlcuded for a TF query. Rank of documents is determined by tf and documents that don't contain the phrase are not included in the trecrun output file.
      - DF: a calculation of the document frequency of each wordPhrase listed, even if it is a phrase. There will be N seperate lines for N wordPhrases. The output in trecrun file will show the wordPhrase as if it were a document and the DF as the score. Rank will be ignored and outputted as the index of the wordPhrase.
- queryName is a provided name for a specific query (e.g., "query1", "query7BM25", etc) The first column of every output line is the corresponding queryName.


The output will be in a TREC run format. For each query, it's ranked list is diplayed using exactly six columns per line, separated by white space. The format is:

  queryName skip storyID rank score username

where
- first column is the queryNmme from the input file.
- the second column is unused by convention and is always "skip".
- the third column is the value of the storyID JSON field of the particular ranked document. (For the DF query type, it should be the wordPhrase)
- the fourth column is the rank of the document retrieved. The highest rank is 1, and there are no ties (broken by storyID). (For the DF query type, it is ignored and should be the index of the wordPhrase since it must have a value for formatting purposes)
- the fifth column shows the score (floating point with 4 digits after the decimal) that generated the ranking. The score is is descending order. The score for a Boolean query is always 1.000 (no match means it is not included in output). The score for TF and DF is the corresponding value.
- the sixth column is the "run tag" and is a traditionally unique identifier for the user and the method used. Here, we use a username.

Notes:
- For QL, BM25, and TF, a story matches a ranked query if it contains at least one of the query terms (TF has only 1 term)
- If any QL, BM25, AND, OR, TF, DF query happens to retrieve zero documents (or DF is zero for a WordPhrase), there will be no lines in the output file for that query (no lines for the WordPhrase for DF). 
- If any TF query has 0 term frequency for some document, that document should be omitted from your output. Any term frequency greater than zero for any document should otherwise be printed out to the output file.
- If any wordPhrase in a DF query has 0 document frequency, there will be no line in the output file for that wordPhrase. 


'''

def tf(inverted_index, doc_id, term):
    """
      Calculate the number of times a term or phrase appears in a document

      Args:
          inverted_index: the inverted index data structure.
          doc_id: the document we want to calculate the term frequency for.
          term: the term or phrase we want to calculate the frequency for.

      Returns: an integer representing the number of times the term appears in doc_id.
    """

    term_frequency = 0

    wp = term.split()
    if len(wp) == 1:
      if term not in inverted_index:
        return 0
      elif inverted_index[term].hasDoc(doc_id):
        return inverted_index[term].getPosting(doc_id)[1]
      else:
        return 0
    else:
      wpLists = []
      for w in wp:
        if w not in inverted_index or not inverted_index[w].hasDoc(doc_id):
          return 0
        else:
          wpLists.append(inverted_index[w].getPosting(doc_id)[2])
      for pos in wpLists[0]:
        currPos = pos+1
        for i in range(1, len(wp)):
          if currPos not in wpLists[i]:
            break
          if i == len(wp)-1:
            term_frequency += 1
          else:
            currPos += 1

    return term_frequency



def df(inverted_index, wordPhrase):
    """
      Calculate the number of documents a term or phrase appears in
      NOTE that this sample only handles one wordPhrase at at time and so only returns
      a single number. This is primarily to highlight that it operates differently
      than the others that are ranking documents.

      Args:
          inverted_index: the inverted index data structure.
          wordPhrase: the term or phrase we want to calculate the frequency for.

      Returns: an integer representing the number of documents a term or phrase appears in.
    """

    doc_freq = 0

    wp = wordPhrase.split()
    if len(wp) == 1:
      if wordPhrase not in inverted_index:
        return 0
      return len(inverted_index[wordPhrase].getList())
    else:
      if wp[0] not in inverted_index:
        return 0
      check = [posting[0] for posting in inverted_index[wp[0]].getList()]
      for docID in check:
        if tf(inverted_index, docID, wordPhrase) > 0:
          doc_freq += 1


    return doc_freq



def collection_frequency(inverted_index, term):
    """
      Calculate the number of times a term or phrase appears in the corpus

      Args:
          inverted_index: the inverted index data structure.
          term: the term or phrase we want to calculate the frequency for.

      Returns: an integer representing the number of times the term appears in the corpus.
    """

    collection_freq = 0

    wp = term.split()
    if len(wp) == 1:
      if term not in inverted_index:
        return 0
      return inverted_index[term].getTF()
    else:
      if wp[0] not in inverted_index:
        return 0
      check = [posting[0] for posting in inverted_index[wp[0]].getList()]
      for docID in check:
        collection_freq += tf(inverted_index, docID, term)

    return collection_freq


def findDocsForWP(inverted_index, wordPhrase):
    """
    Helper function for query functions. Returns list of docIDs that match AND query for a single wordPhrase.

    Args:
        inverted_index: the inverted index data structure.
        wordPhrase: a words or phrase to search for.
    """
  
    ret = []

    wp = wordPhrase.split()
    if len(wp) == 1:
      if wordPhrase not in inverted_index:
        return []
      return inverted_index[wordPhrase].getDocs()
    else:
      if wp[0] not in inverted_index:
        return []
      check = [posting[0] for posting in inverted_index[wp[0]].getList()]
      for docID in check:
        if tf(inverted_index, docID, wordPhrase) > 0:
          ret.append(docID)
    return ret



def intersect(inverted_index, wordPhrases):
    """
      Evaluate an AND boolean query over all wordPhrases in the query

      Args:
          inverted_index: the inverted index data structure.
          wordPhrases: a list of words or phrases to search for.

      Returns: a list of doc_ids
    """

    results = []

    checks = []
    for wordPhrase in wordPhrases:
      checks.append(findDocsForWP(inverted_index, wordPhrase))
    ret = set(checks[0])
    for i in range(1, len(checks)):
      ret = ret & set(checks[i])
    return list(ret)




def union(inverted_index, wordPhrases):
    """
      Evaluate an OR boolean query over all wordPhrases in the query

      Args:
          inverted_index: the inverted index data structure.
          wordPhrases: a list of words or phrases to search for.

      Returns: a list of doc_ids
    """

    results = set()

    for wp in wordPhrases:
      matches = findDocsForWP(inverted_index, wp)
      for doc in matches:
        results.add(doc)

    return list(results)




def query_likelihood(inverted_index, wordPhrases):
    """
      Evaluate a QL query over all wordPhrases

      Args:
          inverted_index: the inverted index data structure.
          wordPhrases: a list of words or phrases to search for.

      Returns: a set of tuples, where the first value is the doc_id, and the second is the score
    """
    ranking = []
    mu = 300  # Dirichlet smoothing parameter


    # do OR query to get list of docs
    # calculate score from textbook
      # qi is a query word, there are n query words
      # cqi is num times query word is in collection (collection freq)
    # sort all and take top 100 or all if less than 100

    docMatches = union(inverted_index, wordPhrases)
    colLen = inverted_index["xx_totalTF"]
    for doc in docMatches:
      logSum = 0
      docLen = inverted_index["xx_docLens"][doc]
      for wp in wordPhrases:
        fqi = tf(inverted_index, doc, wp)
        wpDocs = findDocsForWP(inverted_index, wp)
        cqi = 0
        for wpDoc in wpDocs:
          cqi += tf(inverted_index, wpDoc, wp)
        logVal = ((fqi + mu*(cqi/colLen)) / (docLen + mu))
        logSum += math.log(logVal)
      ranking.append((logSum, doc))

    ranking.sort(reverse=True)
    if len(ranking) >= 100:
      ranking = ranking[0:100]

    return ranking





def bm25(inverted_index, words):
    """
      Perform a bm25 query over all words in the query

      Args:
          inverted_index: the inverted index data structure.
          words: a list of words or phrases to search for.

      Returns: an array of tuples, where the first value is the doc_id, and the second is the score
    """
    results = []
    k1 = 1.8
    k2 = 5.0
    b = 0.75

    # ni = num of docs containing term i
    # N = num of docs in collection
    # fi = tf of term i in doc
    # qfi = tf of term i in query
    # K = k1((1-b) + b(dl/avdl))

    # score = sum of query term i in Q of: (log 1 / ((ni + 0.5) / (N - ni + 0.5))) * ((k1 + 1)fi / (K + fi)) * ((k2 + 1)qfi / (k2 + qfi))

    numDocs = inverted_index["xx_numDocs"]
    avdl = sum(inverted_index["xx_docLens"].values()) / numDocs

    nis = []
    for word in words:
      nis.append(df(inverted_index, word))
    docMatches = union(inverted_index, words)

    for doc in docMatches:
      scoreSum = 0
      dl = inverted_index["xx_docLens"][doc]
      for i in range(0, len(words)):
        ni = nis[i]
        fi = tf(inverted_index, doc, words[i])
        qfi = words.count(words[i])
        K = k1*((1-b) + b*(dl/avdl))
        scoreSum += (math.log(1 / ((ni + 0.5) / (numDocs - ni + 0.5))) * ((k1 + 1)*fi / (K + fi)) * ((k2 + 1)*qfi / (k2 + qfi)))
      results.append((scoreSum, doc))

    results.sort(key=lambda x: (-x[0], x[1]))
    if len(results) >= 100:
      results = results[0:100]

    return results



def run_queries(document_fpath, query_fpath, trecrun_file):
    """
      Create an inverted index, parse a query file, run them on the inverted index,
      and print out the results in trecrun format.

      Args:
          document_fpath: the name of a file containing the documents to index
          query_fpath: the name of the file containing queries to run
          trecrun_file: the name of the file that will be created to contain the
                        output of running the queries

      Returns: void
    """

    #inverted index creation
    docs = load_file(document_fpath, is_json=True)
    inv_ind = build_inverted_index(docs)

    #output file creation
    f = open(trecrun_file, "w")

    #parsing queries and outputting
    queries = load_file(query_fpath, gz_zip = False)
    #o = [qname, skip, docID, rank, score, username]
    outputFormat = "{: <20} {: <6} {: <25} {: <5} {: <15} {: <8}"
    for q in queries:

      if q[0] == 'tf':
        #q = [qtype, qname, wp1]
        matches = []
        possDocs = findDocsForWP(inv_ind, q[2])
        for d in possDocs:
          currTF = tf(inv_ind, d, q[2])
          matches.append((currTF, d))
        matches.sort(key=lambda x: (-x[0], x[1]))
        i = 0
        for tup in matches:
          i += 1
          printVal = [q[1], "skip", tup[1], i, f"{tup[0]:.4f}", "ayeddala"]
          # print(outputFormat.format(*printVal))
          f.write(outputFormat.format(*printVal) + "\n")

      elif q[0] == 'df':
        #q = [qtype, qname, wp1, ..., wpn]
        matches = []
        wps = q[2:]
        i = 0
        for wp in wps:
          i += 1
          currDF = df(inv_ind, wp)
          if currDF > 0:
            printVal = [q[1], "skip", wp.replace(" ", "_"), i, f"{currDF:.4f}", "ayeddala"]
            # print(outputFormat.format(*printVal))
            f.write(outputFormat.format(*printVal) + "\n")

      elif q[0] == 'and':
        #q = [qtype, qname, wp1, ..., wpn]
        matches = intersect(inv_ind, q[2:])
        matches.sort()
        i = 0
        for dID in matches:
          i += 1
          printVal = [q[1], "skip", dID, i, f"{1:.4f}", "ayeddala"]
          # print(outputFormat.format(*printVal))
          f.write(outputFormat.format(*printVal) + "\n")

      elif q[0] == 'or':
        #q = [qtype, qname, wp1, ..., wpn]
        matches = union(inv_ind, q[2:])
        matches.sort()
        i = 0
        for dID in matches:
          i += 1
          printVal = [q[1], "skip", dID, i, f"{1:.4f}", "ayeddala"]
          # print(outputFormat.format(*printVal))
          f.write(outputFormat.format(*printVal) + "\n")

      elif q[0] == 'ql':
        #q = [qtype, qname, wp1, ..., wpn]
        scores = query_likelihood(inv_ind, q[2:])
        i = 0
        for score, dID in scores:
          i += 1
          printVal = [q[1], "skip", dID, i, f"{score:.4f}", "ayeddala"]
          # print(outputFormat.format(*printVal))
          f.write(outputFormat.format(*printVal) + "\n")

      elif q[0] == 'bm25':
        #q = [qtype, qname, wp1, ..., wpn]
        scores = bm25(inv_ind, q[2:])
        i = 0
        for score, dID in scores:
          i += 1
          printVal = [q[1], "skip", dID, i, f"{score:.4f}", "ayeddala"]
          # print(outputFormat.format(*printVal))
          f.write(outputFormat.format(*printVal) + "\n")

      else:
        # print("SOMETHING IS WRONG OOPS")
        f.write("SOMETHING IS WRONG OOPS\n")

    f.close()
    return





































































