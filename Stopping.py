'''

# 2.1 stopping()

After tokenizing the input file, we may apply a stopword list. This function returns a version of the input tokens list with all stopwords omitted.

If stopwords=None, it will not apply any stopping to the list. The result of this choice means that the token list will be unchanged by the stopping step.

If stopwords=list[str], it will use the list of words (that was loaded from the stopwords.txt file for you) as stopwords.

Note that if an original token results in multiple tokens (spaces or non-period punctuation rules), the stopword list is applied to each of the resulting tokens.

Also note that something that does not look like a stopword in the original text could become one – consider "a-n" in the text that will turn into "a", "n", "an" by the hyphen rule that will result in having "a" and "an" removed (if they're in the stopword list), but the "n" will be retained.

'''

def stopping(input_tokens: list[str], stopwords: list[str] = None) -> list[str]:
    """
    Applying stopping to the list of tokens.

    Args:
        input_tokens: the list of tokens that we want to apply stopwords.
        stopwords: the list of stopwords that need to be removed from list of token.
            Default to None (an empty list), i.e., do not stop.

    Returns: an array of array of tokens in format,
        [
            sub_token_1_1,
            sub_token_1_2,
            ...
        ], or for example,
        [
            "a.-2./c.",
            "a",
            "2.",
            "c",
            "a2",
            "c"
        ].
    """

    if stopwords is None:
      return input_tokens

    toks = []
    for tok in input_tokens:
      if tok not in stopwords:
        toks.append(tok)

    return toks
