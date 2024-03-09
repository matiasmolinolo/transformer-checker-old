import constants as c

def is_dyck_word(query: str, k: int) -> bool:
    """
    Check if a word is a member of the Dyck language of order k.

    @param query: The word to check.
    @param k: The order of the Dyck language.

    @return: True if the word is a member of the Dyck language of order k, False otherwise.
    """

    if len(query) % 2 != 0:
        return False
    
    bracket_types = {k: v for k, v in list(c.BRACKETS.items())[:k]}
    closing_brackets = {v: k for k, v in bracket_types.items()}

    stack = []

    for bracket in query:
        if bracket in bracket_types:
            stack.append(bracket)
        elif bracket in closing_brackets:
            if not stack or closing_brackets[bracket] != stack.pop():
                return False
            
    return not stack



    

    