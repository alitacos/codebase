import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def generate_term_variations(term_text: str) -> set:
    """
    SCHRITT 2: Generiert flexible grammatikalische Repräsentationen für das Verb.
    Funktioniert generisch für Verben wie install, setup, config, build etc.
    """
    doc = nlp(term_text.lower())
    
    # 1. Identifiziere das Kern-Verb oder die Aktion (z.B. "installation", "installing")
    action_token = None
    target_tokens = []
    
    # Schlüsselwörter für technische Aktionen und deren typische Suffixe
    action_roots = {"install", "setup", "config", "build", "deploy", "run"}
    
    for token in doc:
        # Prüfe, ob das Wort mit einer unserer bekannten Wurzeln verwandt ist
        is_action = any(root in token.text or root in token.lemma_ for root in action_roots)
        if is_action and not action_token:
            action_token = token
        elif token.text != "of" and not token.is_punct:
            target_tokens.append(token.text)
            
    target = " ".join(target_tokens).strip()
    
    # Wenn kein explizites bekanntes Verb gefunden wurde, nimm das erste Wort als Aktion
    if not action_token and len(doc) > 0:
        action_token = doc[0]
        target = " ".join([t.text for t in doc[1:] if t.text != "of" and not t.is_punct]).strip()

    variations = set()
    if action_token:
        # Hole den Wortstamm (Lemma)
        lemma = action_token.lemma_
        
        # Generiere Standard-Formate basierend auf dem Wortstamm
        # Für unregelmäßige Formen wie "setup" bleibt das Lemma stabil
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
    
    # Füge den ursprünglichen Term zur Sicherheit immer hinzu
    variations.add(term_text.lower())
    return {v.strip() for v in variations if v}

def extract_what_question_and_potential_answers_from_text_via_regex_and_spacy(text: str) -> list:
    # --- SCHRITT 1: DEINE ORIGINALEN REGEXES (Absolut unverändert) ---
    pattern1 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    pattern2 = rf"(?:if\s+)?(?:\w+\s+)*what\s+(?:is|are|am|was|were|can|could|will|would)\s+(?:the|all|some|all the|some of the|you|we|they|I)\s+(?:necessities|pre-?requirements|requirements|needs|essentials|must have|must)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    pattern3 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:the|you|we|I|they)\s+(?:one|most advanced|only|top|highest|only one|best)\s+(?:necessity|requirement|pre-?requirement|need|essentials|must have|must|must do)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    # Ergänzung für Satzbau-Varianten wie "What is installation of X?"
    pattern_installation = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were)|\s?´\s?s)\s+(?:the\s+)?(?:installation|setup|config|configuration)\s+(?:of|for)\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    qpattern = rf"(?:{pattern1}|{pattern2}|{pattern3}|{pattern_installation})"
    
    results = []
    
    doc_all = nlp(text)
    all_sentences = [sent.text.strip() for sent in doc_all.sents]

    for question in re.findall(qpattern, text, re.IGNORECASE):
        # Präzise Term-Extraktion: Isoliere alles nach dem Trigger-Verb/Substantiv 
        # (z.B. nach "installation of", "necessary to") bis zum "?" oder "if"
        term_match = re.search(
            r"what\s+(?:is|are|am|was|were|can|could|will|would|\w+\s+)*(?:necessary\s+to|required\s+to|needed\s+to|essential\s+to|installation\s+of|setup\s+of|configuration\s+of|requirements\s+of)\s+(?P<term>[^?,\n]+)", 
            question, 
            re.IGNORECASE
        )
        
        if not term_match:
            # Flexiblerer Fallback, falls die Struktur kompakter ist
            term_match = re.search(r"(?:to|of|for)\s+(?P<term>[^?,\n]+)", question, re.IGNORECASE)
            
        if not term_match:
            continue
            
        term = term_match.group("term").strip()
        # Säubere eventuelle "if"-Reste aus dem Term, falls die Regex zu weit gegriffen hat
        term = re.sub(r"\s*,\s*if.*$", "", term, flags=re.IGNORECASE).strip()
        
        # --- SCHRITT 2: Repräsentationen generieren ---
        term_variations = generate_term_variations(term)
        
        # --- SCHRITT 3: Sätze finden, die irgendeine Format-Variation enthalten ---
        potential_sentences = []
        for sent in all_sentences:
            if sent.lower() in question.lower() or question.lower() in sent.lower():
                continue
            if any(var in sent.lower() for var in term_variations):
                potential_sentences.append(sent)
                
        # --- SCHRITT 4: Antwort-Validierung (Definitionen & Bedingungen filtern) ---
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

#example usage :
#extract_what_question_and_potential_answers_from_text_via_regex_and_spacy('\nWhat is installation of X?\nX is a software, so installation of X is to copy files.\nInstalling X requires strength in mind and body.\nI like eating pizza.\n')
