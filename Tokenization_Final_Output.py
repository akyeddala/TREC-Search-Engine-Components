'''

# 4.1 Tokenization with or without stopping and stemming: tokenization()

tokenization() will tokenize a list of sentences given the option specified and return a list of processed token in the required format. 
Each element of the returned list (a tuple) will contain the original space-separated word and a list of token that are generated using the original space-separated word. 
So if fancy tokenization, normal stopping, and the Porter stemming are enabled, the sentences:

  sentence 1: "whitespace-Separated" ⍟ tokens ⍟ (as ⍟ in ⍟ P0).
  sentence 2: And, ⍟ a.-2./c. ⍟ also.

where "⍟" indicates whitespace sequences, would result in:

  "whitespace-Separated"  ---> 	"whitespace", "separate", "whitespaceseparate"
                  tokens  ---> 	"token"
                     (as  --->  []
                     in   --->  [] 	
                   P0).   --->  "p0"
                    And,  --->  []
                 a.-2./c  --->  "2.", "c", "a2"
                   also.  ---> "also"


Expectations:

  - The tokens must be listed in the order that the original tokens were encountered in the input file.
  - If an original token is removed (e.g., stopped) nothing will be printed for that token (e.g., the line for "(as", "in", and "And,").
  - If an original token is transformed into additional tokens (e.g., because of hyphens) all of the new tokens will be listed on the same line (e.g., the hyphenated word and the weird "a.-2./c." sequence).
  - If a token is stemmed, the stem will be displayed with the original token. Note that the hyphenated word is separated, made into three tokens, and each of them is stemmed.
  - Note that the process of tokenization with stopping and stemming can be executed as you read through the input file, though in this, we choose to read all the content in the file and then process it.

  '''

def tokenization(
    input_list_str: list[str],
    stopwords: list[str] = None,
    tokenizer_type: str = None,
    stemming_type: str = None
) -> list[tuple[str, list[str]]]:
    """
    Tokenize the input sentences and apply stopping and stemming procedure to the tokenized sentences.

    Args:
        input_list_str: the list of sentences that we read from the input file.
        stopwords: the list of stopwords that need to be removed from list of token (omit to skip stopping)
        tokenizer_type: (case-insensitive) the tokenizer method that we want to apply on the token list.
              Options are ["space", "4grams", "fancy"].
              Default and unrecognized value(s) are considered as "space".
        stemming_type: (case-insensitive) the stemming method that we want to apply on the token list.
              Options are [None, "suffix_s", "porter"].
              Default and unrecognized value(s) are considered as None.

    Returns: an array of processed tokens (tokenized then stopped then stemmed as indicated) in required format, i.e.,
        [
            ("\"whitespace-Separate\"", ["whitespace", "separate", "whitespaceseparate"]),
            ("Tokens", ["token"]),
            ...
        ].
    """
  
    tokenizer_method = tokenize_space
    tokenizer_per_token_func = lambda x: [x]
    if tokenizer_type.lower() == "4grams":
      tokenizer_method = tokenize_4grams
    elif tokenizer_type.lower() == "fancy":
      tokenizer_per_token_func = tokenize_fancy


    stemming_method = lambda x: x # a function that returns its argument
    if stemming_type.lower() == "porter":
      stemming_method = stemming_porter
    elif stemming_type.lower() == "suffix_s":
      stemming_method = stemming_s


    recorder = []
    for input_str in input_list_str:
        recorder.extend(
            [
                (
                    token,
                    stemming_method(
                        stopping(tokenizer_per_token_func(token), stopwords=stopwords)),
                )
                for token in tokenizer_method(input_str)
            ]
        )

    return recorder
