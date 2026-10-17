import re

def extract_what_question_and_potential_answers_from_text_via_regex(text: str) -> list:
    # pattern1: "What is necessary/needed to..."
    pattern1 = r"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+(?:to|for|of|by)\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    # pattern2: ERWEITERT um Singular "need", "requirement" und "of/for" (z.B. "the need of installing pip")
    pattern2 = r"(?:if\s+)?(?:\w+\s+)*what\s+(?:is|are|am|was|were|can|could|will|would)\s+(?:the|all|some|all the|some of the|you|we|they|I)\s+(?:need|needs|necessity|necessities|pre-?requirement|pre-?requirements|requirement|requirements|essential|essentials|must have|must)\s+(?:to|for|of)\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    # pattern3: "What is the one/best requirement to..."
    pattern3 = r"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:the|you|we|I|they)\s+(?:one|most advanced|only|top|highest|only one|best)\s+(?:need|necessity|requirement|pre-?requirement|essential|essentials|must have|must|must do)\s+(?:to|for|of)\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    qpattern = rf"(?:{pattern1}|{pattern2}|{pattern3})"
    results = []

    for question in re.findall(qpattern, text, re.IGNORECASE):
        # Das term_pattern muss flexibel genug sein, um alle oben genannten Strukturen für die Gruppe (?P<term>...) zu matchen
        term_pattern = ( r"(?:if\s+)?(?:\w+\s+)*what" r"(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)" r"\s+(?:the|all|some|all the|some of the|you|we|they|I)?\s*" r"(?:necessary|required|pre-?required|needed|essential|needful|need|needs|necessity|necessities|requirement|requirements)" r"\s+(?:to|from|of|by|via|for)\s+" r"?(?P<term>\w+(?:\s+\w+)*?)" r"(?:\s*,?\s*if\b|\s*\?)" )
        term_match = re.search(term_pattern, question, re.IGNORECASE)
        if not term_match:
            continue
            
        term = term_match.group("term").strip()
        remaining = text.replace(question, "", 1)
        
        answer_pattern = rf"(?:if\s+)?(?:\w+\s+)*(?<!\w){re.escape(term)}[^.!?;]*[.!?;]"
        answers = re.findall(answer_pattern, remaining, re.IGNORECASE)
        valid_answers = [i.strip() for i in answers if term.lower() in i.lower()]
        
        print("QUESTION:", question.strip())
        print("TERM:", term)
        print("ANSWERS:", valid_answers)
        print("-" * 40)
        
        results.append({"question": question, "term": term, "answers": valid_answers})
        
    return results

# Test mit deinem neuen Beispielsatz
#text_input = "What is the need of installing pip? Installing pip is highly recommended because it manages Python packages."
#text_input = "I am lonely. What is needed to install pip, if you want to go home ? What is lonely ? Do not know it ? Lovely is to be lonely some"
#text_input = "I am lonely. What are the requirements of pip installation, if you want to go home ? What is lonely ? Do not know it ? Lovely is to be lonely some"
#extract_what_question_and_potential_answers_from_text_via_regex(text_input)
##negative


#requires POS for verbs, verb_to_noun to identify the correct answers , else will not work for alternatives