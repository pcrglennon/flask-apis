from flask import Flask, abort, jsonify, request

from cross_text import cross_text as cross_text_transform

app = Flask(__name__)

@app.route('/cross-text', methods=['POST'])
def cross_text():
    text = request.args.get('text')
    axis_index = int(request.args.get('axis_index', 0))
    if text == None:
        error_response = jsonify({ 'message': '"text" parameter is required' } )
        error_response.status_code = 422
        return error_response

    return {
        'cross_text': cross_text_transform(text, axis_index)
    }

if __name__ == '__main__':
    app.run(debug=True)
