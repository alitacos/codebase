def extract_what_question_and_potential_answers_from_text_via_regex(text:str='')->list:
    import re
    
    
    pattern1 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    pattern2 = rf"(?:if\s+)?(?:\w+\s+)*what\s+(?:is|are|am|was|were|can|could|will|would)\s+(?:the|all|some|all the|some of the|you|we|they|I)\s+(?:necessities|pre-?requirements|requirements|needs|essentials|must have|must)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    pattern3 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:the|you|we|I|they)\s+(?:one|most advanced|only|top|highest|only one|best)\s+(?:necessity|requirement|pre-?requirement|need|essentials|must have|must|must do)\s+to\s+\w+(?:\s+\w+)*(?:\s*,?\s*if\s+\w+(?:\s+\w+)*)?\s*\?"
    
    qpattern = rf"(?:{pattern1}|{pattern2}|{pattern3})"
    
    for question in re.findall(qpattern, text, re.IGNORECASE):
    
        # Extract the actual term, stopping BEFORE the optional "if" clause.
        term_match = re.search( rf'(?:if\s+)?(?:\w+\s+)*what' rf'(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)' rf'\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+(?:to|from|of|by|via)\s+' rf'\s+(?P<term>\w+(?:\s+\w+)*?)' rf'(?:\s*,?\s*if\b|\s*\?)', question, re.IGNORECASE )
    
        if not term_match:
            continue
        term = term_match.group('term').strip()
        remaining = text.replace(question, '', 1)
        answer_pattern = rf'(?:if\s+)?(?:\w+\s+)*(?<!\w){re.escape(term)}[^.!?;]*[.!?;]'
        answers = re.findall(answer_pattern, remaining, re.IGNORECASE)
        print("QUESTION:", question)
        print("TERM:", term)
        print([i for i in answers if term in i])
# example usage :
#extract_what_question_and_potential_answers_from_text_via_regex('i am lonely. What is needed to install pip, if you want to go home ? What is lonely      ? Do not know it ? Lovely is to be lonely sometimes, but lovely is not lonely. lonely could potentialy be a noun . if x is y lonely is any distribution that is used ? I am lonely. If you want to install pip, go home. If you want to go home, to install pip yu have to by cli. But to install pip it is required to have a computer.')
