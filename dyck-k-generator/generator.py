import random
import json
from typing import List, Dict
from checker import is_dyck_word
import constants as c

def _generate_balanced_string(order: int, length: int) -> str:
    """
    Generate a string of length `length` from the Dyck language of order `order`.

    Args:
        order (int): The order of the Dyck language.
        length (int): The length of the string to generate.

    Returns:
        str: A string of length `length` from the Dyck language of order `order`.
    """
    length = length if length % 2 == 0 else length + 1

    brackets = [(k, v) for k, v in list(c.BRACKETS.items())[:order]]

    half_length = length // 2

    first_half = last_half = ''

    for _ in range(half_length):
        bracket_pair = random.choice(brackets)
        first_half += bracket_pair[0]
        last_half += bracket_pair[1]

    first_half = list(first_half)
    random.shuffle(first_half)

    last_half = list(last_half)
    random.shuffle(last_half)

    balanced_string = first_half + last_half
    return ''.join(balanced_string)


def _generate_unbalanced_string(order: int, length: int) -> str:
    """
    Generate a string of length `length` that is not necessarily from the Dyck language of order `order`.
    
    Args:
        order (int): The order of the Dyck language.
        length (int): The length of the string to generate.

    Returns:
        str: A string of length `length` that is not necessarily from the Dyck language of order `order`.
    """

    brackets = [(k, v) for k, v in list(c.BRACKETS.items())[:order]]
    brackets = [bracket for pair in brackets for bracket in pair]

    return ''.join(random.choice(brackets) for _ in range(length))


def _generate_samples(n: int, k: int, max_length: int = 1024, balanced: float = 0.5) -> List[str]:
    """
    Generate a list of 'n' strings of length at most 'max_length' from the Dyck language of order 'k'.
    These strings may or may not be members of the Dyck language of order 'k'.
    
    The distribution of balanced and unbalanced strings is controlled by the 'balanced' parameter.
    A value of 1.0 will generate only balanced strings, a value of 0.0 will generate only unbalanced strings
    and a value of 0.5 will generate an equal number of balanced and unbalanced strings.
    
    Args:
        n (int): The number of strings to generate.
        k (int): The order of the Dyck language.
        max_length (int): The maximum length of the strings to generate.
        balanced (float): The proportion of balanced strings to generate.
        
    Returns:
        List[str]: A list of 'n' strings of length at most 'max_length' from the Dyck language of order 'k'."""
    
    balanced_strings = [_generate_balanced_string(k, random.randint(2, max_length)) for _ in range(int(n * balanced))]
    unbalanced_strings = [_generate_unbalanced_string(k, random.randint(2, max_length)) for _ in range(n - len(balanced_strings))]
    
    samples = balanced_strings + unbalanced_strings
    random.shuffle(samples)
    
    return samples
    

def generate_dataset(n: int, k: int, max_length: int = 1024, balanced: float = 0.5, path: str = None) -> List[Dict[str, bool]]|None:
    """
    Generate a list of 'n' strings of length at most 'max_length' from the Dyck language of order 'k'.
    These strings may or may not be members of the Dyck language of order 'k'.
    
    The distribution of balanced and unbalanced strings is controlled by the 'balanced' parameter.
    A value of 1.0 will generate only balanced strings, a value of 0.0 will generate only unbalanced strings
    and a value of 0.5 will generate an equal number of balanced and unbalanced strings.
    
    Args:
        n (int): The number of strings to generate.
        k (int): The order of the Dyck language.
        max_length (int): The maximum length of the strings to generate.
        balanced (float): The proportion of balanced strings to generate.
        path (str): The path to save the generated strings - if None, the list will be returned to a variable.
        
    Returns:
        List[Dict[str, bool]]|None: A list of dictionaries that contain {"string": str, "class": bool}, where string is the Dyck-k member string and class is its membership to the language.
    """
    
    strings = _generate_samples(n, k, max_length, balanced)
    dataset = [{'string': s, 'class': is_dyck_word(s, k)} for s in strings]

    if path:
        with open(path, 'w') as f:
            for sample in dataset:
                json_record = json.dumps(sample)
                f.write(json_record + '\n')
            print(f'Dataset saved to {path}')
    else:
        return dataset


