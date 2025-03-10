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




