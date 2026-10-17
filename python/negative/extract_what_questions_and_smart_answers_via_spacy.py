def extract_what_questions_and_smart_answers_via_spacy(text: str) -> list:
    import spacy
    
    # Lädt das englische Sprachmodell (muss einmalig via `pip install spacy` 
    # und `python -m spacy download en_core_web_sm` installiert werden)
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        import os
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    
    def get_significant_lemmas(text_segment):
        """Extrahiert die Grundformen (Lemmas) von Nomen, Verben und Adjektiven."""
        doc = nlp(text_segment.lower())
        # Wir filtern Stopwörter (the, of, to) aus, um nur die Kernbegriffe zu vergleichen
        return {token.lemma_ for token in doc if token.pos_ in {"NOUN", "VERB", "PROPN", "ADJ"} and not token.is_stop}

    doc = nlp(text)
    sentences = list(doc.sents)
    results = []
    
    # 1. Keywords definieren, die eine "Anforderungs-Frage" signalisieren
    trigger_keywords = {"need", "necessary", "requirement", "essential", "needed", "pre-requirement"}
    
    for i, sent in enumerate(sentences):
        sent_text = sent.text.strip()
        
        # Prüfen, ob es sich um eine "What"-Frage handelt, die nach Anforderungen sucht
        if sent_text.lower().startswith("what") and any(kw in sent_text.lower() for kw in trigger_keywords):
            
            # 2. Den "Term" (das Ziel) aus der Frage extrahieren
            # Wir suchen nach der Präposition (to, of, for), die auf das Schlüsselwort folgt
            term_text = ""
            prep_found = False
            term_tokens = []
            
            for token in sent:
                if token.text.lower() in {"to", "of", "for"}:
                    prep_found = True
                    continue
                if prep_found:
                    # Wir stoppen, falls ein Nebensatz (z. B. ", if you...") beginnt
                    if token.text == "," or token.text.lower() == "if" or token.is_punct:
                        break
                    term_tokens.append(token.text)
            
            term_text = " ".join(term_tokens).strip()
            if not term_text:
                continue
                
            # Kern-Lemmas des Terms extrahieren (z.B. {"pip", "installation"} -> {"pip", "install"})
            term_lemmas = get_significant_lemmas(term_text)
            
            # 3. Passende Antworten im restlichen Text suchen
            valid_answers = []
            for other_sent in sentences:
                # Die Frage selbst ausschließen
                if other_sent.text == sent.text:
                    continue
                    
                other_lemmas = get_significant_lemmas(other_sent.text)
                
                # Wenn alle Kernbegriffe der Frage (als Stammform) im Satz existieren: Match!
                if term_lemmas and term_lemmas.issubset(other_lemmas):
                    valid_answers.append(other_sent.text.strip())
            
            print("QUESTION:", sent_text)
            print("EXTRACTED TERM:", term_text)
            print("SMART ANSWERS:", valid_answers)
            print("-" * 40)
            
            results.append({
                "question": sent_text,
                "term": term_text,
                "answers": valid_answers
            })
            
    return results
# example usage :
# extract_what_questions_and_smart_answers_via_spacy("What are the requirements of pip installation, if you want to go home? You should install pip using python get-pip.py.")
