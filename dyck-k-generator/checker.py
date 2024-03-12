import click
import constants as c


@click.command()
@click.option("--query", "-q", type=str, help="The word to check.")
@click.option("--k", "-k", type=int, help="The order of the Dyck language.")
@click.option("--verbose", "-v", is_flag=True, help="Print the result of the check.")
def is_dyck_word(query: str, k: int, verbose: bool = False) -> bool|None:
    """
    Check if a word is a member of the Dyck language of order k.

    Args:
        query (str): The word to check.
        k (int): The order of the Dyck language.

    Returns:
        bool: True if the word is a member of the Dyck language of order k, False otherwise.
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
    if verbose:
        print(not stack)
    else:
        return not stack

if __name__ == "__main__":
    is_dyck_word()

    