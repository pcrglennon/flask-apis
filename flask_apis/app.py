from flask import Flask

from flask_apis.slack_text_utils.app import slack_text_utils_api

app = Flask(__name__)

app.register_blueprint(slack_text_utils_api, url_prefix='/slack-text-utils')

if __name__ == '__main__':
    app.run(debug=True)
