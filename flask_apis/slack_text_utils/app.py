from flask import Blueprint, request

from .cross_text import cross_text as cross_text_transform

slack_text_utils_api = Blueprint('slack_text_utils_api', __name__)

@slack_text_utils_api.route('/cross-text', methods=['POST'])
def cross_text():
    text = request.form.get('text').strip()
    axis_index = 0

    # TODO - investigate how to fix formatting in Slack for different axes
    # axis_index = int(request.args.get('axis_index', 0))

    return {
        'response_type': 'in_channel',
        'text': cross_text_transform(text, axis_index=axis_index, ignore_colon_emojis=True)
    }

