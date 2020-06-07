import re

# TODO - make this a class?

def cross_text(text: str, axis_index: int = 0, ignore_colon_emojis: bool = True) -> str:
    if not 0 <= axis_index < len(text):
        return

    if ignore_colon_emojis:
        formatted_text = upper_ignore_colon_emojis(text)
    else:
        formatted_text = text.upper()
    vertical_axis_padding = ' ' * (axis_index * 2)
    string = ''

    # vertical axis (start)
    for c in formatted_text[:axis_index]:
        string += f'{vertical_axis_padding}{c}\n'

    # horizontal axis
    string += ' '.join(c for c in formatted_text)

    # vertical axis (end)
    for c in formatted_text[(axis_index + 1):]:
        string += f'\n{vertical_axis_padding}{c}'

    return string

def upper_ignore_colon_emojis(text):
    text_parts = re.split(r'(:[^:]+:)', text)
    text_parts = list(map(
        lambda string: string if re.match(r':[^:]+:', string) else string.upper(),
        text_parts
    ))
    return ''.join(text_parts)
