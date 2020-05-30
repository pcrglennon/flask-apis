def cross_text(text: str, axis_index: int = 0) -> str:
    if not 0 <= axis_index < len(text):
        return

    uppercased_text = text.upper()
    vertical_axis_padding = ' ' * (axis_index * 2)
    string = ''

    # vertical axis (start)
    for c in uppercased_text[:axis_index]:
        string += f'{vertical_axis_padding}{c}\n'

    # horizontal axis
    string += ' '.join(c for c in uppercased_text)

    # vertical axis (end)
    for c in uppercased_text[(axis_index + 1):]:
        string += f'\n{vertical_axis_padding}{c}'

    return string
