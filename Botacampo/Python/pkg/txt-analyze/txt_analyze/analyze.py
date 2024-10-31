def word_frequency(text: str) -> dict[str:int]:
    """Counts the frequency of every word in the given string.

    Args:
        text (str): String to be counted.

    Returns:
        {str: int}: A dictionary containg the word and the amount of times the key is repeated.
    """
    frequency = {}
    for word in text:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


def sentence_count(text: str) -> int:
    """Counts the amount of sentences in a given string.

    Args:
        text (str): String to be counted.

    Returns:
        int: Amount of senteces.
    """
    sentences = text.split(".")
    return len([s for s in sentences if s.strip() != ""])


def most_common_words(text: str, limit: int = 5) -> list[tuple[str, int]]:
    """Returns the most common words in a given string.

    Args:
        text (str): String to have the words counted.
        limit (int, optional): Limits the amount of words that is returned. Defaults to 5.

    Returns:
        list[tuple[str, int]]: _description_
    """
    frequency = word_frequency(text)
    sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq[:limit]
