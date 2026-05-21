def boyer_moore_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0

    shift_table = {}
    pattern_length = len(pattern)

    for index in range(pattern_length - 1):
        shift_table[pattern[index]] = pattern_length - index - 1

    index = 0
    while index <= len(text) - pattern_length:
        pattern_index = pattern_length - 1

        while pattern_index >= 0 and pattern[pattern_index] == text[index + pattern_index]:
            pattern_index -= 1

        if pattern_index < 0:
            return index

        bad_character = text[index + pattern_length - 1]
        index += shift_table.get(bad_character, pattern_length)

    return -1


def build_prefix_table(pattern: str) -> list[int]:
    prefix_table = [0] * len(pattern)
    length = 0
    index = 1

    while index < len(pattern):
        if pattern[index] == pattern[length]:
            length += 1
            prefix_table[index] = length
            index += 1
        elif length:
            length = prefix_table[length - 1]
        else:
            prefix_table[index] = 0
            index += 1

    return prefix_table


def kmp_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0

    prefix_table = build_prefix_table(pattern)
    text_index = 0
    pattern_index = 0

    while text_index < len(text):
        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1

            if pattern_index == len(pattern):
                return text_index - pattern_index
        elif pattern_index:
            pattern_index = prefix_table[pattern_index - 1]
        else:
            text_index += 1

    return -1


def rabin_karp_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0

    pattern_length = len(pattern)

    if pattern_length > len(text):
        return -1

    base = 256
    modulus = 101
    pattern_hash = 0
    text_hash = 0
    high_order = 1

    for _ in range(pattern_length - 1):
        high_order = (high_order * base) % modulus

    for index in range(pattern_length):
        pattern_hash = (base * pattern_hash + ord(pattern[index])) % modulus
        text_hash = (base * text_hash + ord(text[index])) % modulus

    for index in range(len(text) - pattern_length + 1):
        if pattern_hash == text_hash:
            if text[index:index + pattern_length] == pattern:
                return index

        if index < len(text) - pattern_length:
            text_hash = (
                base * (text_hash - ord(text[index]) * high_order)
                + ord(text[index + pattern_length])
            ) % modulus

    return -1
