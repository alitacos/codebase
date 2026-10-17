def extract_sentences_via_spacy_from_text(sentences, output_dir="output"):

    import spacy
    from pathlib import Path
    
    nlp = spacy.load("en_core_web_sm")
    
    ALLOWED_MODIFIER_POS = {
        "ADV",
        "ADJ",
        "PART",
    }
    
    # POS that can be ignored after the action.
    # This allows "{x}", punctuation, etc.
    TRAILING_POS = {
        "PUNCT",
        "NOUN",
        "PROPN",
    }
    
    
    def find_action(doc):
        """
        Find the action word according to the constructions
        we are interested in.
        """
    
        # ---------------------------------------------------------
        # 1. Find "to" and look forward for the action.
        #
        # to install
        # to never install
        # to never stealth install
        # ---------------------------------------------------------
    
        for i, token in enumerate(doc):
    
            if token.lower_ != "to":
                continue
    
            j = i + 1
    
            # Skip allowed modifiers
            while (
                j < len(doc)
                and doc[j].pos_ in ALLOWED_MODIFIER_POS
            ):
                j += 1
    
            if j < len(doc):
                action = doc[j]
    
                # We found the action after "to".
                if action.is_alpha:
                    return action
    
        # ---------------------------------------------------------
        # 2. "How to ..."
        #
        # This is already covered by "to", but keeping this
        # explicit makes the intention clear.
        # ---------------------------------------------------------
    
        if (
            len(doc) >= 2
            and doc[0].lower_ == "how"
            and doc[1].lower_ == "to"
        ):
            j = 2
    
            while (
                j < len(doc)
                and doc[j].pos_ in ALLOWED_MODIFIER_POS
            ):
                j += 1
    
            if j < len(doc) and doc[j].is_alpha:
                return doc[j]
    
        # ---------------------------------------------------------
        # 3. Command-like:
        #
        # remote install
        # not remote install
        #
        # Here spaCy calls "install" NOUN.
        # We treat the final alphabetic token as the action.
        # ---------------------------------------------------------
    
        alpha_tokens = [
            token for token in doc
            if token.is_alpha
        ]
    
        if alpha_tokens:
            last = alpha_tokens[-1]
    
            if last.pos_ in {"NOUN", "VERB", "PROPN"}:
                previous = doc[last.i - 1] if last.i > 0 else None
    
                if previous and previous.pos_ in ALLOWED_MODIFIER_POS:
                    return last
    
        return None
    


    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for text in sentences:

        doc = nlp(text)

        action = find_action(doc)

        if action is None:
            continue

        filename = output_dir / f"{action.lemma_}.txt"

        with filename.open("a", encoding="utf-8") as f:
            f.write(text.strip() + "\n")
