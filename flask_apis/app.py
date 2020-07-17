from flask import Flask
from flask_cors import CORS

from flask_apis.slack_text_utils.app import slack_text_utils_api
from flask_apis.movie_db_utils.app import movie_db_utils_api

app = Flask(__name__)

CORS(app, resources={
    r'/movie-db-utils/*': {
        'origins': '*'
    }
})

app.register_blueprint(slack_text_utils_api, url_prefix='/slack-text-utils')
app.register_blueprint(movie_db_utils_api, url_prefix='/movie-db-utils')

if __name__ == '__main__':
    app.run(debug=True)
