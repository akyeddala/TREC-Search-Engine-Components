'''

The purpose of this project is to explore tokenization, stop word removal, and stemming within a few real documents, and to investigate term statistics as related to Heaps' and possibly Zipf's Laws. 



# 1.1 tokenize_space()

This tokenizer will break the input line into a list of whitespace-separated tokens. If there are multiple whitespace characters in a row 
(multiple spaces, a space and a tab, a space and a line break, etc.) they are treated as a single token break: e.g., "a<space><space>b" is 
two tokens ("a" and "b") rather than three ("a", <empty>, "b"). No other changes are made to the tokens beyond separating them. 

So, for example, the start of this paragraph would result in the following 16 tokens (for the sake of space, listed across the line separated by ⍟):

    This ⍟ tokenizer ⍟ will ⍟ break ⍟ the ⍟ file ⍟ into ⍟ a ⍟ list ⍟ of ⍟ whitespace-separated ⍟ tokens.

Note that punctuation is included with a token based on where the whitespace is and tokens are produced without changing their case.


'''

def tokenize_space(input_str: str) -> list[str]:
    """
    Tokenize sentence into whitespace-separated tokens. For
    example, input_str = "2024 Fall Search Engine", the function
    should return ["2024", "Fall", "Search", "Engine"].

    Args:
        input_str: the sentence/phrase that we want to tokenize.

    Returns: 
        an array of whitespace-separated tokens.
    """

    toks = input_str.split();
    return toks

'''

# 1.2 tokenize_4grams()

This is another straightforward tokenizer using n-grams of n=4 (4-grams) as tokens. Unlike the one above, this one treats spaces as part of the token. Every four characters is a token, regardless of whether the characters are whitespace, punctuation, or alphanumeric characters. 
The one exception to that is that any white-space type character (newline or tab), including multiple in a row (multiple spaces, a space and a tab, a space and a line break, etc.), is treated as if it were a single space. 
E.g., "a<space><space>bc" is a single token ("a<space>bc") rather than the token "a<space><space>b" and so on. Similarly, "a<space><newline><tab>bcef" should generate "a<space>bc" and "bcef".

It turns out that in most applications, we need to use "overlapping" n-grams. So each token starts two characters after the previous one. Using the same notation as before, the sequence:

    An  iced coffee \t
    is very nice
    
would generate the following sequence of tokens (using the same notation as above, with ⍟ showing where tokens break). Spaces are replaced with underscores so they are easier to see:

    An_i ⍟ _ice ⍟ ced_ ⍟ d_co ⍟ coff ⍟ ffee ⍟ ee_i ⍟ _is_ ⍟ s_ve ⍟ very ⍟ ry_n ⍟ _nic ⍟ ice

For the final token, we do not include the 1-, 2-gram that ends that final token. And if the number of characters in the file is not a multiple of four, we stop with the final 3-gram (like what we have in the example with ice but not also e).

In special cases, if the string is too short to create even one 4-gram, you should return the original token instead.

'''

def tokenize_4grams(input_str: str) -> list[str]:
    """
    Tokenize sentence into 4char tokens with shifting windows. For example,
    input_str = "An\ticed coffee \t\nis very nice", the function should return
    ['An i', ' ice', 'ced ', 'd co', 'coff', 'ffee', 'ee i', ' is ', 's ve', 'very', 'ry n', ' nic', 'ice'].

    Args:
        input_str: the sentence/phrase that we want to tokenize.

    Returns: an array of 4-grams tokens.
    """

    #If string too short to create even one 4-gram
    if len(input_str) < 4:
      return [input_str]

    tmp = ' '.join(input_str.split())
    if input_str[0] == ' ':
      tmp = ' ' + tmp
    if input_str[-1] == ' ':
      tmp = tmp + ' '

    if tmp == ' ' or tmp == '  ':
      return [' ']
    elif len(tmp) < 4:
      return [tmp]

    toks = []
    for i in range(0, len(tmp)-2, 2):
      if i == len(tmp) - 3:
        toks.append(tmp[i: i+3])
      else:
        toks.append(tmp[i: i+4])

    return toks

'''

# 1.3 tokenize_fancy()

This is a more complicated tokenizer that builds on the spaces tokenizer and adds additional rules to produce (more) consistent tokens when dealing with words with the same root, punctuation, casing, urls, etc.
These are the rules to be applied in order accordingly:


    1) Start with ONE space-separated token as in the spaces tokenizer above. (In reality, you'll do this for all of them. For simplicity we consider one at a time.)
    
    2) A token that is a URL of the form "https://…" or "http://…" should be recognized as a single token. If there is trailing punctuation, it is not part of the URL and that punctuation should be discarded. Note that "https://hithere.com+https://howdy.org" should be considered as one simple token 
    (since it starts with https). Also note that "446https://hithere.com" is not a URL because it does not start with the URL signal. Make sure to handle the cases of "HTTP" and "HTTPS" (etc.) as the start of a url is case-insensitive. No other changes to a URL token should happen – i.e., for a URL, 
    ignore the remaining rules below.
    
    3) Convert the tokens to lowercase.
    
    4) Treat numbers as a single token, including plus and/or minus signs, commas, and decimal points if they exist, so that "3,141.59" remains that string. A number can only be a sequence of numeric characters and those punctuation marks indicated but it must have at least one number character.
    You do not have to validate that the number is well formed (so "3+14..1,59" and "-1-5" would both still be number tokens). Do no other processing to number tokens.
    
    5) Apostrophes should be "squeezed out" so that it is as if they were never there. That means that a contraction such as "don't" would turn into "dont" and a name like "O'Brian" will become "obrian" (because it is was also lowercased in step 3).
    
    6) Any remaining punctuation other than periods and hyphens should be treated as a word separator (as if it were white space: note the sequence of whitespace rules from the spaces tokenizer), except recall that punctuation in a URL (step 2) or number (step 4) is not a word break. 
    So one token can generate multiple tokens: "3/11//23" will result in "3", "11", "23", and "3^rd" will result in "3", "rd", but "3.14/pi" will result in "3.14", "pi". If a new token is a number (as defined above), do not process it further. So in the example, "3.14" will not be treated as an abbreviation by step 8. You may prefer to do this recursively to handle these rules on sub-parts. So that "b.c.," (note the comma) would result in "b.c." (remember that periods are not word breaks) and an empty token. A recursive call on "b.c." will result in "bc" from abbreviation rule 8 and the empty token will be discarded.
    
    7)Hyphens (not treated as word separators) within a token should be processed in three steps: (1) remove the original token with its hyphen(s), (2) add new tokens with the hyphens treated as space separators (as in the spaces tokenizer), and then (3) add a new token with all hyphens squeezed out. So,
    
    "data-base" → "data", "base", "database" "mother-in-law" → "mother", "in", "law", "motherinlaw" "a.-b.-c." → "a.", "b.", "c.", "a.b.c."
    
    Note that as with the punctuation rule, the hyphen processing will result in additional tokens. Apply all tokenization rules to each of the tokens that are generated. So "1.-on-1." will generate "1.", "on", "1.", "1.on.1.". The occurrences of "1." will remain unchanged because they are numbers, 
    but "1.on.1." will be treated as an abbreviation and converted into "1on1". There are some edge cases that will cause odd things to happen (e.g., the token "1-https://Some.Url" will end up converting the embedded URL to lowercase which contractadicts rule 2), 
    but we won't stress about unusual subtokens caused by hyphens; we'll just accept and respect them for being what they are.
    
    8) Treat abbreviations as a single token. If a token is not a number or URL and the only punctuation it contains is periods, it is an abbreviation. Note that this includes a token that comprises nothing but periods, even if that is not intuitive. For an abbreviation, remove all periods. 
    So "i.b.m." converts to "ibm" and "Ph.D." and "Ph.D" both go to "phd" (because an abbreviation does not need to end with a period and because rule 3 converted it to lowercase). If the result of removing the periods is an empty string, then treat it as an empty token and do not report it out.


Here are some sample tokenizations that should happen:

    Token → token (lower case rule)
    She's → shes (apostrophe rule and lower case rule)
    Mother's-IN-Law → mothers, in, law, mothersinlaw (apostrophe, lowercase, hyphens)
    U.mass → umass (lowercase, abbreviation)
    go!!!!team → go team (non-period punctuation rule)
    USD$10.30 → usd 10.30 (non-period punctuation, case, number)
    USD$10,30 → usd 10 30 (not period punctuation, case)
    USD$10-30 → usd 10-30 (not-period punctuation, number (not hyphen!!))
    There will be interactions between rules, and that is OK. For example,
    
    "a.-2./c." → "a.-2.", "c." by non-period and non-hyphen punctuation rule
    → "a.", "2.", "a.2.", "c." by hyphen rule
    → "a", "2.", "a2", "c" after applying the abbreviation rule, noting that "2." is a number so retains its decimal point.

'''

def tokenize_fancy(input_token: str) -> list[str]:
    """
    Tokenize ONE token into tokens using the fancy rules defined above.

    Args:
        input_token: the token that we want to tokenize.

    Returns: an array of array of tokens in format,
        [
            sub_token_1_1,
            sub_token_1_2,
            ...
        ], or
        [
            'c',
            'a',
            '2.',
            'a2'
        ].
    """

    toks = []

    #Step 2: URL
    if input_token.lower().startswith("https://") or input_token.lower().startswith("http://"):
      tok = input_token
      for i in range(len(input_token)-1, -1, -1):
        if input_token[i].lower() in string.ascii_lowercase + string.digits:
          tok = input_token[0:i+1]
          break
      return [tok]

    #Step 3: to lowercase
    tok = input_token.lower()

    #Step 4: number token check
    notNum = False
    hasNoNum = True
    validInNum = string.digits + "-+,."

    for char in tok:
      if hasNoNum and char in string.digits:
        hasNoNum = False
      if char not in validInNum:
        notNum = True
        break

    if not(notNum or hasNoNum):
      return [tok]

    #Step 5: remove apostrophes
    tok = tok.replace("'", "")

    #Step 6: process word separators
    word_seps = string.punctuation.replace(".", "").replace("-", "")
    for char in word_seps:
      tok = tok.replace(char, "*")
    toks = tok.split("*")

    if len(toks) > 1:
      new_toks = []
      for token in toks:
        if token != '':
          tmp = tokenize_fancy(token)
          new_toks = new_toks + tmp
      toks = new_toks

    #Step 7: process hyphens
    new_toks = []
    for i in range(0, len(toks)):
      if "-" in toks[i]:
        notNum = False
        hasNoNum = True
        validInNum = string.digits + "-+,."

        for char in toks[i]:
          if hasNoNum and char in string.digits:
            hasNoNum = False
          if char not in validInNum:
            notNum = True
            break

        if not(notNum or hasNoNum):
          new_toks.append(toks[i])
          continue

        else:
          tmp = toks[i].split("-") + [(toks[i].replace("-", ""))]
          ext_toks = []
          for token in tmp:
            if token != '':
              tmp_toks = tokenize_fancy(token)
              ext_toks.extend(tmp_toks)
          new_toks.extend(ext_toks)
      else:
        if toks[i] != '':
          new_toks.append(toks[i])

    toks = new_toks

    #Step 8: process abbreviations
    no_per = string.punctuation.replace(".", "")
    new_toks = []
    for token in toks:
      if token.lower().startswith("https://") or token.lower().startswith("http://"):
        new_toks.append(token)
        continue

      notNum = False
      hasNoNum = True
      validInNum = string.digits + "-+,."

      for char in token:
        if hasNoNum and char in string.digits:
          hasNoNum = False
        if char not in validInNum:
          notNum = True
          break

      if not(notNum or hasNoNum):
        new_toks.append(token)
        continue


      if "." in token and (char not in token for char in no_per):
        tmp = token.replace(".", "")
        if tmp != '':
          new_toks.append(tmp)
      else:
        new_toks.append(token)
    toks = new_toks

    return toks 





