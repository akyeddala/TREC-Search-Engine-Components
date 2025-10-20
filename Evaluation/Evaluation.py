'''

For each input trecrun file, we report the calculated meausures in the output file following the format below:

  measure   queryid   score

If the trecrun file contains multiple queries, we calculate and report measures for each query. At the end of the output file, we include the sum of the numRel and relFound values, and the arithmetic mean of all other measures, averaged across all queries in the trecrun file. 
The final average across queries for RR and AP will be labeled MRR and MAP following convention. The query name for final average measures will be "all". Most measures are formatted to inlcude exactly 4 digits after the decimal. Counts are left as integers.

'''


def report_measures(outputFile: str, results) -> None:
  """
  Write all calculated measures into the output file.

  Args:
        outputFile: path in which the output file should be stored
        results: contains all calculated measures for all queries in the trecrun file
  """

  f = open(outputFile, "w")

  for query in results:
    qResults = results[query];
    for line in qResults:
      f.write(line + "\n")

  f.close()
  return



def eval(trecrunFile: str, qrelsFile: str, outputFile: str) -> None:
  """
  Calculate and report all the measures for each query in the trecrun file.

  Args:
        trecRunFile: path to where the trecrun file is stored
        qrelsFile: path to where the qrels file is stored
        outputFile: path in which the output file should be stored
  """

  queries = dict[str, QueryInfo]()
  read_trecrun(trecrunFile, queries)
  read_qrels(qrelsFile, queries)

  results = {}
  sums = {}
  sums["numRel"] = 0
  sums["relFound"] = 0
  sums["RR"] = 0
  sums["P@13"] = 0
  sums["R@13"] = 0
  sums["F1@13"] = 0
  sums["NDCG@23"] = 0
  sums["AP"] = 0
  sums["BPREF"] = 0
  sums["P@29R"] = 0
  sums["P@R"] = 0
  count = 0
  for query in queries:
    count += 1
    qInfo = queries[query]
    qRes = []

    nRel = numRel(qInfo)
    qRes.append(f"numRel {qInfo.query_id} {nRel}")
    sums["numRel"] += nRel

    rFound = relFound(qInfo)
    qRes.append(f"relFound {qInfo.query_id} {rFound}")
    sums["relFound"] += rFound

    rr = RR(qInfo)
    qRes.append(f"RR {qInfo.query_id} {'{:.4f}'.format(rr)}")
    sums["RR"] += rr

    P13 = P_13(qInfo)
    qRes.append(f"P@13 {qInfo.query_id} {'{:.4f}'.format(P13)}")
    sums["P@13"] += P13

    R13 = R_13(qInfo)
    qRes.append(f"R@13 {qInfo.query_id} {'{:.4f}'.format(R13)}")
    sums["R@13"] += R13

    F113 = F1_13(qInfo)
    qRes.append(f"F1@13 {qInfo.query_id} {'{:.4f}'.format(F113)}")
    sums["F1@13"] += F113

    NDCG23 = NDCG_23(qInfo)
    qRes.append(f"NDCG@23 {qInfo.query_id} {'{:.4f}'.format(NDCG23)}")
    sums["NDCG@23"] += NDCG23

    ap = AP(qInfo)
    qRes.append(f"AP {qInfo.query_id} {'{:.4f}'.format(ap)}")
    sums["AP"] += ap

    bpref = BPREF(qInfo)
    qRes.append(f"BPREF {qInfo.query_id} {'{:.4f}'.format(bpref)}")
    sums["BPREF"] += bpref

    p29r = P_29R(qInfo)
    qRes.append(f"P@29R {qInfo.query_id} {'{:.4f}'.format(p29r)}")
    sums["P@29R"] += p29r

    patr = PatR(qInfo)
    qRes.append(f"P@R {qInfo.query_id} {'{:.4f}'.format(patr)}")
    sums["P@R"] += patr

    results[query] = qRes;

  alls = []

  tmp = sums["numRel"]
  alls.append(f"numRel all {tmp}")

  tmp = sums["relFound"]
  alls.append(f"relFound all {tmp}")

  tmp = "{:.4f}".format(sums["RR"] / count)
  alls.append(f"MRR all {tmp}")

  tmp = "{:.4f}".format(sums["P@13"] / count)
  alls.append(f"P@13 all {tmp}")

  tmp = "{:.4f}".format(sums["R@13"] / count)
  alls.append(f"R@13 all {tmp}")

  tmp = "{:.4f}".format(sums["F1@13"] / count)
  alls.append(f"F1@13 all {tmp}")

  tmp = "{:.4f}".format(sums["NDCG@23"] / count)
  alls.append(f"NDCG@23 all {tmp}")

  tmp = "{:.4f}".format(sums["AP"] / count)
  alls.append(f"MAP all {tmp}")

  tmp = "{:.4f}".format(sums["BPREF"] / count)
  alls.append(f"BPREF all {tmp}")

  tmp = "{:.4f}".format(sums["P@29R"] / count)
  alls.append(f"P@29R all {tmp}")

  tmp = "{:.4f}".format(sums["P@R"] / count)
  alls.append(f"P@R all {tmp}")

  results["all"] = alls;

  report_measures(outputFile, results)

  return
