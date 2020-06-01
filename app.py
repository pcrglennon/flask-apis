from flask import Flask, request

from cross_text import cross_text as cross_text_transform

app = Flask(__name__)

@app.route('/slack/cross-text', methods=['POST'])
def slack_cross_text():
    text = request.form.get('text')
    axis_index = 0

    # TODO - investigate how to fix formatting in Slack for different axes
    # axis_index = int(request.args.get('axis_index', 0))

    return {
        'response_type': 'in_channel',
        'text': cross_text_transform(text, axis_index)
    }

if __name__ == '__main__':
    app.run(debug=True)
