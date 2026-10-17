import re

def extract_what_question_and_potential_answers_from_text_via_regex(text: str) -> list:
    data = {}
    
    pattern1 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+to\s+\w+(?:\s+\w+)*\s*\?"
    pattern2 = rf"(?:if\s+)?(?:\w+\s+)*what\s+(?:is|are|am|was|were|can|could|will|would)\s+(?:the|all|some|all the|some of the|you|we|they|I)\s+(?:necessities|pre-?requirements|requirements|needs|essentials|must have|must)\s+to\s+\w+(?:\s+\w+)*\s*\?"
    pattern3 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:the|you|we|I|they)\s+(?:one|most advanced|only|top|highest|only one|best)\s+(?:necessity|requirement|pre-?requirement|need|essentials|must have|must|must do)\s+to\s+\w+(?:\s+\w+)*\s*\?"
    
    qpattern = rf"(?:{pattern1}|{pattern2}|{pattern3})"
    
    # 1. Find questions
    qmatches = re.findall(qpattern, text, re.IGNORECASE)
    
    for question in qmatches:
    
        # 2. Extract everything after the question's "what ... [keyword]"
        term_match = re.search(
            rf'what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)'
            rf'\s+(?:necessary|required|pre-?required|needed|essential|needful)'
            rf'\s+(?P<term>to\s+\w+(?:\s+\w+)*)\s*\?',
            question,
            re.IGNORECASE
        )
    
        if not term_match:
            continue
    
        term = term_match.group('term').strip()
    
        # 3. Find sentences that START with {term}
        answer_pattern = rf'(?<!\w){re.escape(term)}[^.!?;]*[.!?;]'
    
        answers = re.findall(answer_pattern, text, re.IGNORECASE)
    
        
        data[term] = {}
        data[term[question] = answers
        return data
#extract_what_question_and_potential_answers_from_text_via_regex