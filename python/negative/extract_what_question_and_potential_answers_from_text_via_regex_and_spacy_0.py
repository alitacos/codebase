def extract_what_question_and_potential_answers_from_text_via_regex_and_spacy(text:str)->list:
    import re
    import spacy
    
    # Lädt das englische Sprachmodell
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        import os
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    
    def generate_term_variations(term_text: str) -> set:
        """
        Schritt 2: Generiert verschiedene grammatikalische Repräsentationen des Terms.
        Deckt ab: "install", "installing", "installation", "installation of" etc.
        """
        doc = nlp(term_text.lower())
        words = [t.text for t in doc if not t.is_punct and t.text != "of"]
        
        # Extrahiere Kern-Lemmas, um die Basis-Aktion zu finden (z.B. "install")
        # Wir nutzen eine einfache Heuristik für Suffixe, um Nomen/Verben zu kreuzen
        variations = {term_text.lower(), " ".join(words)}
        
        for token in doc:
            if token.is_stop or token.is_punct:
                continue
                
            base = token.lemma_
            # Wenn das Wort auf -ation, -ing, oder ein Verb/Nomen ist, generiere Varianten
            if base.endswith("install") or "install" in token.text:
                # Füge die typischen Repräsentationen für technische Begriffe hinzu
                variations.update([
                    "install", 
                    "installing", 
                    "installation", 
                    "installation of"
                ])
                
        # Baue die Kombinationen mit den restlichen Argumenten (z.B. "X") wieder zusammen
        final_variations = set()
        # Finde das Zielobjekt (z.B. "pip" oder "x")
        target_words = [t.text for t in doc if t.pos_ in {"NOUN", "PROPN", "X"} and "install" not in t.text.lower()]
        target = target_words[0] if target_words else ""
        
        for v in variations:
            if target:
                final_variations.add(f"{v} {target}".strip())
                final_variations.add(f"{target} {v}".strip()) # z.B. "pip installation"
            else:
                final_variations.add(v)
                
        return {v for v in final_variations if v}
    
    def extract_what_questions_and_answers(text: str) -> list:
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        results = []
        
        for i, sent in enumerate(doc.sents):
            sent_text = sent.text.strip()
            sent_lower = sent_text.lower()
            
            # --- SCHRITT 1: Identifiziere "What"-Fragen (mit/ohne flexiblem "if") ---
            # Matcht: "What is...", "If you want..., what is...", "What is..., if you..."
            is_what_question = False
            if sent_lower.startswith("what") or ( "what" in sent_lower and "?" in sent_lower):
                # Prüfen, ob es relevante Trigger-Wörter enthält
                if any(kw in sent_lower for kw in {"is", "are", "need", "needed", "requirement", "installation"}):
                    is_what_question = True
                    
            if not is_what_question:
                continue
                
            # --- SCHRITT 2: Extrahiere den TERM und generiere Repräsentationen ---
            term_text = ""
            past_indicator = False
            
            # Heuristik zur Extraktion des Terms nach "is", "of", "to"
            for token in sent:
                if token.text.lower() in {"is", "are", "to", "of", "for"} and not past_indicator:
                    past_indicator = True
                    continue
                if past_indicator:
                    if token.text == "," or token.text.lower() == "if" or token.is_punct:
                        break
                    term_text += token.text + " "
            
            term_text = term_text.strip()
            if not term_text:
                # Fallback: Nutze die Substantive der Frage
                term_text = " ".join([t.text for t in sent if t.pos_ in {"NOUN", "PROPN", "X"} and t.text.lower() != "what"])
                
            if not term_text:
                continue
                
            # Generiere alle Repräsentationen (Schritt 2b)
            term_variations = generate_term_variations(term_text)
            
            # --- SCHRITT 3: Finde alle Sätze, die irgendeine Variation enthalten ---
            potential_sentences = []
            for other_sent in sentences:
                if other_sent == sent_text:
                    continue
                
                # Prüfe, ob eine der Term-Variationen als Substring im Satz vorkommt
                if any(var in other_sent.lower() for var in term_variations):
                    potential_sentences.append(other_sent)
                    
            # --- SCHRITT 4: Validiere, ob der Satz eine echte Antwort/Definition ist ---
            final_answers = []
            # Muster für typische Antwortstrukturen: "X is...", "X requires...", "X means..."
            answer_indicators = re.compile(r"\b(is|are|means|would mean|requires|needed for|allows to)\b", re.IGNORECASE)
            
            for pot_sent in potential_sentences:
                if answer_indicators.search(pot_sent):
                    final_answers.append(pot_sent)
                    
            results.append({
                "question": sent_text,
                "term": term_text,
                "variations_searched": list(term_variations),
                "answers": final_answers
            })
            
            # Konsolen-Ausgabe für das Debugging
            print(f"STEP 1 (Question): {sent_text}")
            print(f"STEP 2 (Term & Vars): {term_text} -> {term_variations}")
            print(f"STEP 3 & 4 (Filtered Answers): {final_answers}")
            print("-" * 60)
            
        return results

# example usage :
#extract_what_question_and_potential_answers_from_text_via_regex_and_spacy('\nWhat is installation of X?\nX is a software, so installation of X is to copy files.\nInstalling X requires strength in mind and body.\nI like eating pizza.\n')
