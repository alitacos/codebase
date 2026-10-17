import re

def extract_what_question_and_potential_answers_from_text_via_regex(text: str) -> list:
    
    pattern1 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:necessary|required|pre-?required|needed|essential|needful)\s+to\s+\w+(?:\s+\w+)*\s*\?"
    pattern2 = rf"(?:if\s+)?(?:\w+\s+)*what\s+(?:is|are|am|was|were|can|could|will|would)\s+(?:the|all|some|all the|some of the|you|we|they|I)\s+(?:necessities|pre-?requirements|requirements|needs|essentials|must have|must)\s+to\s+\w+(?:\s+\w+)*\s*\?"
    pattern3 = rf"(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)\s+(?:the|you|we|I|they)\s+(?:one|most advanced|only|top|highest|only one|best)\s+(?:necessity|requirement|pre-?requirement|need|essentials|must have|must|must do)\s+to\s+\w+(?:\s+\w+)*\s*\?"
    
    qpattern = rf"(?:{pattern1}|{pattern2}|{pattern3})"
    
    for question in re.findall(qpattern, text, re.IGNORECASE):
    
        # Extract: "to install pip"
        term_match = re.search(
            rf'(?:if\s+)?(?:\w+\s+)*what(?:\s+(?:is|are|am|was|were|can|could|will|would)|\s?´\s?s)'
            rf'\s+(?:necessary|required|pre-?required|needed|essential|needful)'
            rf'\s+(?P<term>to\s+\w+(?:\s+\w+)*)\s*\?',
            question,
            re.IGNORECASE
        )
    
        if not term_match:
            continue
    
        term = term_match.group('term').strip()
    
        # Remove the question itself before looking for answers.
        remaining = text.replace(question, '', 1)
    
        # Find a sentence that STARTS with "to install pip".
        answer_pattern = rf'(?:if\s+)?(?:\w+\s+)*(?<!\w){re.escape(term)}[^.!?;]*[.!?;]'
    
        answers = re.findall(answer_pattern, remaining, re.IGNORECASE)
    
        print("QUESTION:", question)
        print("TERM:", term)
        print("ANSWERS:", answers)
# Example usage :
#extract_what_question_and_potential_answers_from_text_via_regex("I am lonely. What is needed to install pip, if you want to go home ? What is lonely ? Do not know it ? Lovely is to be lonely some")
##negative