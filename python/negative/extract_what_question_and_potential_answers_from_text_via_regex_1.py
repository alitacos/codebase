import re

def extract_what_question_and_potential_answers_from_text_via_regex(text: str) -> list:
    # Definition der einzelnen Muster (Regex-Strings müssen in Anführungszeichen stehen)
    pattern1 = r"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    pattern2 = r"(?:if\s+)?(?:\w+\s+)*what\s+(?:is|are|am|was|were|can|could|will|would)\s+(?:the|all|some|all the|some of the|you|we|they|I)\s+(?:necessities|pre-?requirements|requirements|needs|essentials|must have|must)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    pattern3 = r"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:the|you|we|I|they)\s+(?:one|most advanced|only|top|highest|only one|best)\s+(?:necessity|requirement|pre-?requirement|need|essentials|must have|must|must do)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    # Kombination der Muster mit ODER (|)
    qpattern = rf"(?:{pattern1}|{pattern2}|{pattern3})"
    
    results = []

    for question in re.findall(qpattern, text, re.IGNORECASE):
        # Dynamisches Suchmuster für den Begriff (Term) innerhalb der gefundenen Frage
        term_pattern = (
            r"(?:if\s+)?(?:\w+\s+)*what"
            r"(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)"
            r"\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+(?:to|from|of|by|via)\s+"
            r"(?P<term>\w+(?:\s+\w+)*?)"
            r"(?:\s*,?\s*if\b|\s*\?)"
        )
        
        term_match = re.search(term_pattern, question, re.IGNORECASE)
        if not term_match:
            continue
            
        term = term_match.group("term").strip()
        
        # Entfernt die Frage aus dem Text, um Antworten im Resttext zu suchen
        remaining = text.replace(question, "", 1)
        
        # Sucht Sätze, die den Begriff enthalten
        answer_pattern = rf"(?:if\s+)?(?:\w+\s+)*(?<!\w){re.escape(term)}[^.!?;]*[.!?;]"
        answers = re.findall(answer_pattern, remaining, re.IGNORECASE)
        
        # Filtert Antworten, die den Begriff exakt enthalten
        valid_answers = [i.strip() for i in answers if term.lower() in i.lower()]
        
        print("QUESTION:", question.strip())
        print("TERM:", term)
        print("ANSWERS:", valid_answers)
        print("-" * 40)
        
        results.append({"question": question, "term": term, "answers": valid_answers})
        
    return results

# Example usage :
#text_input = "I am lonely. What is needed to install pip, if you want to go home ? What is lonely ? Do not know it ? Lovely is to be lonely some"
#extract_what_question_and_potential_answers_from_text_via_regex(text_input)
