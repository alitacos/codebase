def extract_what_question_and_potential_answers_from_text_via_regex(text:str='')->list:
    import re
    pattern1 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+to\s+\w+(?:\s+\w+)*\s*\?"
    pattern2 = rf"(?:if\s+)?(?:\w+\s+)*what\s+(?:is|are|am|was|were|can|could|will|would)\s+(?:the|all|some|all the|some of the|you|we|they|I)\s+(?:necessities|pre-?requirements|requirements|needs|essentials|must have|must)\s+to\s+\w+(?:\s+\w+)*\s*\?"
    pattern3 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:the|you|we|I|they)\s+(?:one|most advanced|only|top|highest|only one|best)\s+(?:necessity|requirement|pre-?requirement|need|essentials|must have|must|must do)\s+to\s+\w+(?:\s+\w+)*\s*\?"
    qpattern = rf"(?:{pattern1}|{pattern2}|{pattern3})"
    qmatches = re.findall(qpattern, text, re.IGNORECASE)
    subpattern1 = rf'(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+'
    subpattern2 = rf'(?:if\s+)?(?:\w+\s+)*what\s+(?:is|are|am|was|were|can|could|will|would)\s+'
    subpattern3 = rf'(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:the|you|we|I|they)\s+'
    data = {}
    for qmatch in qmatches:
        data[qmatch] = []
        if re.fullmatch(pattern1, qmatch, re.IGNORECASE):
            m = re.match(subpattern1, qmatch, re.IGNORECASE)
        elif re.fullmatch(pattern2, qmatch, re.IGNORECASE):
            m = re.match(subpattern2, qmatch, re.IGNORECASE)
        elif re.fullmatch(pattern3, qmatch, re.IGNORECASE):
            m = re.match(subpattern3, qmatch, re.IGNORECASE)
        else:
            continue
    
        if m:
              
            data[qmatch]  = qmatch[m.end():].strip().rstrip('?').strip()
        print(match)

#extract_what_question_and_potential_answers_from_text_via_regex(text)
