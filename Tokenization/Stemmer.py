'''

After tokenizing and removing stopwords, we stem each token using one of three options.

Note that while stemming operates only on tokens that are not stopped, many cases (URLs, numbers, and tokens that are already their stem) will not change.
Also note that if a token generated multiple tokens (the spaces or non-period punctuation rules), the stemmer must be applied to each of them.

Both types of stemming accept a list of strings and return a stemmed copy.



# 3.1 "Suffix s" stemming

stemmingtype=suffix_s. Removes the final character of a token if it is an "s", otherwise leaves it unchanged.

'''

def stemming_s(input_tokens: list[str]) -> list[str]:
    """
    Applying suffix-s stemming to the list of tokens.

    Args:
        input_tokens: the list of tokens that we want to perform stemming.

    Returns: an array of array of tokens in format,
        [
            sub_token_1_1,
            sub_token_1_2,
            ...
        ]

        For example, if the input is ["hi", "is", "this", "lass", "silly"] the output should be:
        [ "hi", "i", "thi", "las", "silly" ]
    """

    stemmed_toks = []
    for tok in input_tokens:
      if tok[-1] == 's':
        stemmed_toks.append(tok[:-1])
      else:
        stemmed_toks.append(tok)

    return stemmed_toks 



'''

3.2 Stemming with Porter Stemmer

stemming_type=porter. Applies the Porter stemmer ("the English stemmer" or "Porter2") with small changes.

For each token in turn, apply the rule of Step 1a that matches the longest suffix (if it matches any),
then apply the one rule of Step 1b that matches the longest suffix (if any) of the output of Step 1a,
then apply Step 1c to Step 1b's result if it fits. In each step, if no suffix matches, do nothing and then continue to the next step.

To simplify the algorithm, we redifine tokens to have a type of "structure" following the pattern [C] (VC)^m [V] where V is a sequence of one or more vowels (a, e, i, o, u), C is a sequence of one or more consonants (anything that is not a vowel, including punctuation), and m indicates how often the CV pattern repeats (if m = 0 then it does not occur at all).
Here are some examples:

  - agreed is VCVC which is (VC)^2 with the leading C and trailing V empty.
  - retrieval is CVCVCVC which is C(VC)^3 with the trailing V empty.
  - feed is CVC which is C(VC)^1 with the trailing V empty.
  - tree is CV which is C(VC)^0V or CV with nothing in the middle.


The steps of the stemmer are:


  Step 1a:
  
  - Replace sses by ss (e.g., stresses→stress) and do nothing else for Step 1a.
  - If the stem ends with ied or ies, then if the remaining stem is more than one character long, replace the ending by i, otherwise replace it by ie (e.g., ties→tie, cries→cri). In either case, do nothing else for Step 1a.
  - If the stem ends in us or ss do nothing (e.g., stress→stress), including doing nothing else for Step 1a
  - If the stem ends with s, then "if the preceding stem part contains a vowel not immediately before the s" then delete the trailing s (e.g., gaps→gap but gas→gas). And do nothing else for Step 1a. (Note that the "contains a vowel" bit is not helped by the m rule described above and needs another way to check for that.)
  
  Step 1b:
  
  - If the stem ends in eed or eedly then:
    - if it is in the part of the stem after the first non-vowel following a vowel (i.e., if m > 1 in the token that gets to 1b), replace it by ee (e.g., agreed→agree, feed→feed).
    - then go to step 1c
  - If the stem ends in ed, edly, ing, or ingly then:
    - if the preceding stem part does not contain a vowel, go to step 1c
    - if the preceding stem part does contain a vowel delete the ending and then also consider the following three possibilities with the resulting stem:
      - if the stem now ends in at, bl, or iz add e (e.g., fished → fish, pirating →pirate) and go to step 1c
      - if the stem now ends with a double letter that is one of bb, dd, ff, gg, mm, nn, pp, rr, or tt, remove the last letter (e.g., falling→fall, dripping→drip) and go to step 1c
      - if the stem is now short (defined as m = 1 for the stem after removing the suffix), add e (e.g., hoping→hope) and go to step 1c.
  
  Step 1c (added to original Porter2):
  
  - If the stem ends in y and the character before the y is neither a vowel nor the first letter of the word, replace the y with an i (e.g., cry→cri, bi→bi, bamby→bambi, bambi→bambi, say→say, why→whi)

  '''


def stemming_porter(input_tokens: list[str]) -> list[str]:
    """
    Applying stemming to the list of tokens.

    Args:
        input_tokens: the list of tokens that we want to perform stemming.

    Returns: an array of array of tokens in format,
        [
            sub_token_1_1,
            sub_token_1_2,
            ...
        ], or
        [
            "a.-2./c.",
            "2.",
            "c",
            "a2",
            "c"
        ].
    """

    vowels = "aeiou"
    stemmed_toks = []

    for token in input_tokens:
      tok = token

      #Step 1a:
      if tok.endswith("sses"):
        tok = tok[0:-2]
      elif tok.endswith("ied") or tok.endswith("ies"):
        if len(tok[0:-3]) > 1:
          tok = tok[0:-2]
        else:
          tok = tok[0:-1]
      elif tok.endswith("us") or tok.endswith("ss"):
        tok = tok
      elif tok.endswith("s"):
        if len(tok) > 2 and any(vowel.lower() in tok[:-2] for vowel in vowels):
          tok = tok[0:-1]


      #Step 1b:
      m = 0
      lastWasV = False
      for char in tok:
        if not lastWasV and char.lower() in vowels:
          lastWasV = True
        elif lastWasV and char.lower() not in vowels:
          m = m + 1
          lastWasV = False
        else:
          continue

      if tok.endswith("eed"):
        if m > 1:
          tok = tok[0:-1]
      elif tok.endswith("eedly"):
        if m > 1:
          tok = tok[0:-3]
      else:
        deleted = False


        if tok.endswith("ed"):
          if any(char.lower() in vowels for char in tok[0:-2]):
            tok = tok[0:-2]
            deleted = True
        elif tok.endswith("edly"):
          if any(char.lower() in vowels for char in tok[0:-4]):
            tok = tok[0:-4]
            deleted = True
        elif tok.endswith("ing"):
          if any(char.lower() in vowels for char in tok[0:-3]):
            tok = tok[0:-3]
            deleted = True
        elif tok.endswith("ingly"):
          if any(char.lower() in vowels for char in tok[0:-5]):
            tok = tok[0:-5]
            deleted = True

        if deleted:
          if tok.endswith("at") or tok.endswith("bl") or tok.endswith("iz"):
            tok = tok + "e"
          elif tok.endswith("bb") or tok.endswith("dd") or tok.endswith("ff") or tok.endswith("gg") or tok.endswith("mm") or tok.endswith("nn") or tok.endswith("pp") or tok.endswith("rr") or tok.endswith("tt"):
            tok = tok[0:-1]
          else:
            m = 0
            lastWasV = False
            for char in tok:
              if not lastWasV and char.lower() in vowels:
                lastWasV = True
              elif lastWasV and char.lower() not in vowels:
                m = m + 1
                lastWasV = False
              else:
                continue

            if m == 1:
              tok = tok + "e"


      #Step 1c:
      if tok.endswith("y") and len(tok) > 2 and tok[-2].lower() not in vowels:
        tok = tok[0:-1] + 'i'

      #Add to list
      stemmed_toks.append(tok)

    return stemmed_toks 































