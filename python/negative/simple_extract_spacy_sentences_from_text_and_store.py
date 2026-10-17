def simple_extract_spacy_sentences_from_text_and_store(sentences, output_dir="output"):

    import spacy
    from pathlib import Path
    
    nlp = spacy.load("en_core_web_sm")
    
    ALLOWED_POS = {"ADV", "ADJ", "PART"}
    
    
    def find_action(doc):
        # First real VERB
        for token in doc:
            if token.pos_ == "VERB":
                return token
    
        # For short command-like phrases, use the last token.
        # spaCy often sees "install" in "remote install" as NOUN.
        if len(doc) <= 5:
            for token in reversed(doc):
                if token.is_alpha:
                    return token
    
        return None
    
    
    def is_match(doc, action):
        i = action.i
    
        # -----------------------------------------
        # How to ...
        # -----------------------------------------
        if len(doc) >= 2:
            if doc[0].lower_ == "how" and doc[1].lower_ == "to":
                return True
    
        # -----------------------------------------
        # to VERB
        # -----------------------------------------
        if i >= 1 and doc[i - 1].lower_ == "to":
            return True
    
        # -----------------------------------------
        # to WORD VERB
        # WORD must have an allowed POS
        # -----------------------------------------
        if i >= 2 and doc[i - 2].lower_ == "to":
            middle = doc[i - 1]
    
            if middle.pos_ in ALLOWED_POS:
                return True
    
        # -----------------------------------------
        # modifier VERB
        #
        # remote install
        # not remote install
        # -----------------------------------------
        if i >= 1:
            previous = doc[i - 1]
    
            if previous.pos_ in ALLOWED_POS:
                return True
    
        return False
    

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for text in sentences:
        doc = nlp(text)

        action = find_action(doc)

        if action is None:
            continue

        if not is_match(doc, action):
            continue

        filename = output_dir / f"{action.lemma_}.txt"

        with filename.open("a", encoding="utf-8") as f:
            f.write(text.strip() + "\n")
