def extract_what_question_and_potential_answers_from_text_via_regex_and_spacy(text: str) -> list:
    import re
    import spacy
    
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        import os
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    
    def generate_term_variations(term_text: str) -> set:
        doc = nlp(term_text.lower())
        action_token = None
        target_tokens = []
        action_roots = {"install", "setup", "config", "build", "deploy", "run"}
        
        for token in doc:
            is_action = any(root in token.text or root in token.lemma_ for root in action_roots)
            if is_action and not action_token:
                action_token = token
            elif token.text != "of" and not token.is_punct:
                target_tokens.append(token.text)
                
        target = " ".join(target_tokens).strip()
        
        if not action_token and len(doc) > 0:
            action_token = doc[0]
            target = " ".join([t.text for t in doc[1:] if t.text != "of" and not t.is_punct]).strip()
    
        variations = set()
        if action_token:
            lemma = action_token.lemma_
            base_forms = [lemma, f"{lemma}ing", f"{lemma}ation", f"{lemma}ation of"]
            if lemma == "setup":
                base_forms = ["setup", "setting up", "set up"]
            elif lemma == "config":
                base_forms = ["config", "configuring", "configuration", "configuration of"]
                
            for form in base_forms:
                if target:
                    variations.add(f"{form} {target}".strip())
                    variations.add(f"{target} {form}".strip())
                else:
                    variations.add(form)
        
        variations.add(term_text.lower())
        return {v.strip() for v in variations if v}

    # --- SCHRITT 1: DEINE ORIGINALEN REGEXES ---
    pattern1 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    pattern2 = rf"(?:if\s+)?(?:\w+\s+)*what\s+(?:is|are|am|was|were|can|could|will|would)\s+(?:the|all|some|all the|some of the|you|we|they|I)\s+(?:necessities|pre-?requirements|requirements|needs|essentials|must have|must)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    pattern3 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:the|you|we|I|they)\s+(?:one|most advanced|only|top|highest|only one|best)\s+(?:need|necessity|requirement|pre-?requirement|essential|essentials|must have|must|must do)\s+(?:to|for|of)\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    pattern_installation = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were)|\s?´\s?s)\s+(?:the\s+)?(?:installation|setup|config|configuration)\s+(?:of|for)\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    qpattern = rf"(?:{pattern1}|{pattern2}|{pattern3}|{pattern_installation})"
    
    results = []
    
    # Text in Sätze splitten
    doc_all = nlp(text)
    all_sentences = [sent.text.strip() for sent in doc_all.sents if sent.text.strip()]

    for question in re.findall(qpattern, text, re.IGNORECASE):
        # Term-Extraktion
        term_match = re.search(
            r"what\s+(?:is|are|am|was|were|can|could|will|would|\w+\s+)*(?:necessary\s+to|required\s+to|needed\s+to|essential\s+to|installation\s+of|setup\s+of|configuration\s+of|requirements\s+of)\s+(?P<term>[^?,\n]+)", 
            question, 
            re.IGNORECASE
        )
        
        if not term_match:
            term_match = re.search(r"(?:to|of|for)\s+(?P<term>[^?,\n]+)", question, re.IGNORECASE)
            
        if not term_match:
            continue
            
        term = term_match.group("term").strip()
        term = re.sub(r"\s*,\s*if.*$", "", term, flags=re.IGNORECASE).strip()
        
        # --- SCHRITT 2: Repräsentationen generieren ---
        term_variations = generate_term_variations(term)
        
        # --- SCHRITT 3: Alle Sätze mit einer Format-Variation finden ---
        potential_sentences = []
        for sent in all_sentences:
            # FIX: Wir prüfen nur, ob der Satz exakt mit der Frage identisch ist, 
            # statt Substrings fälschlicherweise auszuschließen.
            if sent.lower() == question.strip().lower():
                continue
            if any(var in sent.lower() for var in term_variations):
                potential_sentences.append(sent)
                
        # --- SCHRITT 4: Antwort-Validierung ---
        final_answers = []
        answer_indicators = re.compile(r"\b(is|are|means|would mean|requires|needed|allows|essential)\b", re.IGNORECASE)
        
        for pot_sent in potential_sentences:
            if answer_indicators.search(pot_sent):
                final_answers.append(pot_sent)
                
        print("QUESTION:", question.strip())
        print("VALID ANSWERS:", final_answers)
        print("-" * 50)
        
        results.append({
            "question": question.strip(),
            "term": term,
            "answers": final_answers
        })
        
    return results

#example usage :
#extract_what_question_and_potential_answers_from_text_via_regex_and_spacy('\nWhat is installing an X?\nX is a software, so installation of X is to copy files.\ninstallation of X is to copy files.\nInstalling X requires strength in mind and body.\n')
# not accurate