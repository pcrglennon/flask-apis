from flask_apis.slack_text_utils.cross_text import cross_text as cross_text_transform

def test_empty_string():
    assert cross_text_transform('') == ''

# ignore invalid axis_index, continue w/ axis_index of 0
def test_axis_index_too_high():
    assert cross_text_transform('abc', axis_index=10) == 'A B C\nB\nC'

# ignore invalid axis_index, continue w/ axis_index of 0
def test_axis_index_negative():
    assert cross_text_transform('abc', axis_index=-2) == 'A B C\nB\nC'

def test_simple_success():
    assert cross_text_transform('abc') == 'A B C\nB\nC'

def test_simple_success_axis_index():
    assert cross_text_transform('abc', axis_index=1) == '  A\nA B C\n  C'

def test_simple_success_truncated():
    assert cross_text_transform('abc', axis_max_length=2) == 'A B\nB\n\n_This message has been truncated, maximum message length is: 2_'

# preserve colon-form emoji strings
def test_colon_emoji_success():
    assert cross_text_transform('ab :smile: c') == 'A B :smile: C\nB\n:smile:\nC'
