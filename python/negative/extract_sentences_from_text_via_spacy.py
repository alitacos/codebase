def extract_sentences_from_text_via_spacy(sentences, output_dir="output"):

    import spacy
    from pathlib import Path
    
    nlp = spacy.load("en_core_web_sm")
    
    # Words that are allowed between "to" and the target verb.
    # We use POS, not the actual word.
    ALLOWED_POS = {
        "ADV",
        "ADJ",
        "PART",
    }
    
    
    def find_matching_verbs(doc):
        matches = []
    
        for token in doc:
    
            # We are interested in verbs
            if token.pos_ != "VERB":
                continue
    
            i = token.i
    
            # --------------------------------------------------
            # 1. How to VERB
            # --------------------------------------------------
            if (
                i >= 2
                and doc[0].lower_ == "how"
                and doc[1].lower_ == "to"
            ):
                matches.append(token)
                continue
    
            # --------------------------------------------------
            # 2. to VERB
            #
            # The steps to install
            # requirements to install
            # --------------------------------------------------
            if i >= 1 and doc[i - 1].lower_ == "to":
                matches.append(token)
                continue
    
            # --------------------------------------------------
            # 3. to WORD VERB
            #
            # to never install
            # to always install
            # to quickly install
            #
            # Exactly one token between "to" and VERB.
            # --------------------------------------------------
            if i >= 2:
                previous = doc[i - 1]
                before_previous = doc[i - 2]
    
                if (
                    before_previous.lower_ == "to"
                    and previous.pos_ in ALLOWED_POS
                ):
                    matches.append(token)
                    continue
    
            # --------------------------------------------------
            # 4. Modifier + VERB
            #
            # remote install
            # not remote install
            #
            # This handles cases where there is no "to".
            # --------------------------------------------------
            if i >= 1:
                previous = doc[i - 1]
    
                if previous.pos_ in ALLOWED_POS:
                    matches.append(token)
                    continue
    
        return matches
    

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for text in sentences:
        doc = nlp(text)
    
        print("\n", text)
        for t in doc:
            print(t.text, repr(t.pos_), repr(t.lemma_))

    for text in sentences:
        doc = nlp(text)

        matches = find_matching_verbs(doc)

        for verb in matches:
            filename = output_dir / f"{verb.lemma_}.txt"

            with filename.open("a", encoding="utf-8") as f:
                f.write(text.strip() + "\n")
