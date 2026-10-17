#positive
def extract_all_comment_spans_from_str_script_via_tokenize_with_line_index(code: str='')->list[tuple]:
    import tokenize
    from io import StringIO
    comments = []
    for tok in tokenize.generate_tokens(StringIO(code).readline):
        if tok.type == tokenize.COMMENT:
            comments.append((tok.start[0], tok.string))

    return comments
#extract_all_comments_of_script_via_tokenize_with_line_index("""was ist a, \ndef foo(a,/,  b: int, c='hello', *,l):\n\tpass""")#[out]:[] 
#extract_all_comments_of_script_via_tokenize_with_line_index("""#was ist a, \ndef foo(a,/,  b: int, c='hello', *,l):\n\tpass""")#[out]: [(1, '#was ist a, ')]
