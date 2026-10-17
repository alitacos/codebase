def extract_what_question_and_potential_answers_from_text_via_regex_and_spacy(text:str)->list:
    import re
    import spacy
    
    # Lädt das englische Sprachmodell für die Wortstamm-Transformationen (Schritte 2-4)
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        import os
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    
    def generate_term_variations(term_text: str) -> set:
        """
        SCHRITT 2: Nimmt den extrahierten Term und generiert Repräsentationen.
        Wandelt z.B. "installation of pip" oder "install pip" in alle Formen um.
        """
        doc = nlp(term_text.lower())
        
        # Basis-Aktionen isolieren
        variations = {term_text.lower()}
        for token in doc:
            base = token.lemma_
            if "install" in token.text or "install" in base:
                variations.update(["install", "installing", "installation", "installation of"])
                
        # Das Zielobjekt (z. B. "pip" oder "x") herausfiltern
        target_words = [t.text for t in doc if t.pos_ in {"NOUN", "PROPN", "X"} and "install" not in t.text.lower()]
        target = target_words[0] if target_words else ""
        
        final_variations = set()
        for v in variations:
            if target:
                final_variations.add(f"{v} {target}".strip())
                final_variations.add(f"{target} {v}".strip())
            else:
                final_variations.add(v)
                
        return {v for v in final_variations if v}
    
    def extract_what_question_and_potential_answers_from_text_via_regex(text: str) -> list:
        # --- SCHRITT 1: DEINE ORIGINALEN REGEXES (Exakt wie von dir vorgegeben) ---
        pattern1 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
        pattern2 = rf"(?:if\s+)?(?:\w+\s+)*what\s+(?:is|are|am|was|were|can|could|will|would)\s+(?:the|all|some|all the|some of the|you|we|they|I)\s+(?:necessities|pre-?requirements|requirements|needs|essentials|must have|must)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
        pattern3 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:the|you|we|I|they)\s+(?:one|most advanced|only|top|highest|only one|best)\s+(?:necessity|requirement|pre-?requirement|need|essentials|must have|must|must do)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
        
        # Ergänzung für dein neues Beispiel: "What is installation of X?"
        pattern_installation = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were)|\s?´\s?s)\s+(?:the\s+)?(?:installation|setup|config|configuration)\s+(?:of|for)\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
        
        qpattern = rf"(?:{pattern1}|{pattern2}|{pattern3}|{pattern_installation})"
        
        results = []
        
        # Hilfs-Splitting für Sätze im Gesamttext für Schritt 3 & 4
        doc_all = nlp(text)
        all_sentences = [sent.text.strip() for sent in doc_all.sents]
    
        for question in re.findall(qpattern, text, re.IGNORECASE):
            # Extraktion des Terms aus deinen Mustern via Regex
            term_match = re.search(
                r"what(?:\s+(?:\w+))*\s+(?:to|of|for|by|via)\s+(?P<term>\w+(?:\s+\w+)*?)(?:\s*,?\s*if\b|\s*\?)", 
                question, 
                re.IGNORECASE
            )
            
            if not term_match:
                # Fallback-Extraktion, falls die Präpositionen variieren
                term_match = re.search(r"(?:to|of|for)\s+(?P<term>[^,?]+)", question, re.IGNORECASE)
                
            if not term_match:
                continue
                
            term = term_match.group("term").strip()
            
            # --- SCHRITT 2: Repräsentationen generieren (Verb <-> Nomen Transformation) ---
            term_variations = generate_term_variations(term)
            
            # --- SCHRITT 3: Sätze finden, die irgendeine Format-Variation enthalten ---
            potential_sentences = []
            for sent in all_sentences:
                if sent.lower() in question.lower() or question.lower() in sent.lower():
                    continue
                if any(var in sent.lower() for var in term_variations):
                    potential_sentences.append(sent)
                    
            # --- SCHRITT 4: Antwort-Validierung (Ausschluss von Smalltalk/unpassenden Sätzen) ---
            final_answers = []
            answer_indicators = re.compile(r"\b(is|are|means|would mean|requires|needed|allows|essential)\b", re.IGNORECASE)
            
            for pot_sent in potential_sentences:
                if answer_indicators.search(pot_sent):
                    final_answers.append(pot_sent)
                    
            print("QUESTION:", question.strip())
            print("EXTRACTED TERM:", term)
            print("VARIATIONS SEARCHED:", term_variations)
            print("VALID ANSWERS:", final_answers)
            print("-" * 50)
            
            results.append({
                "question": question.strip(),
                "term": term,
                "answers": final_answers
            })
            
        return results
# example usage :
# extract_what_question_and_potential_answers_from_text_via_regex_and_spacy('\nWhat is installation of X?\nX is a software, so installation of X is to copy files.\nInstalling X requires strength in mind and body.\nI like eating pizza.\n')
