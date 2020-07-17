import asyncio
import os

from flask import Blueprint, request
import httpx

movie_db_utils_api = Blueprint('movie_db_utils_api', __name__)

# Direct relay to the TMDB API /search/person endpoint, included here so that clients can utilize
# search without storing their own TMDB API token.
# This endpoint tacks on the API key, and forwards any incoming params (e.g. 'language', 'page')
@movie_db_utils_api.route('/tmdb-api-proxy/search/person', methods=['GET'])
def search_person():
    tmdb_api_key = os.getenv('TMDB_API_KEY')
    api_params = { 'api_key': tmdb_api_key, **request.values }

    response = httpx.get(
        f'https://api.themoviedb.org/3/search/person',
        params=api_params
    )

    return response.json()

@movie_db_utils_api.route('/actors-crossover', methods=['GET'])
def actors_crossover():
    actor_id_strings = request.args.get('actor_ids', '').split(',')
    if len(actor_id_strings) < 2:
        return { 'message': '"actor_ids" param is required, must contain at least 2 comma-separated IDs' }, 422

    actor_ids = [int(id_string) for id_string in actor_id_strings]

    loop = asyncio.get_event_loop()
    actors_data = loop.run_until_complete(fetch_actors_data(actor_ids))

    movies_id_map = build_movies_id_map(actors_data)

    crossover_movies = list(filter(lambda movie: len(movie['credits']) > 1, movies_id_map.values()))

    return {
        'crossover_movies': crossover_movies
    }

async def fetch_actors_data(actor_ids: [int]):
    async with httpx.AsyncClient() as client:
        actors_data = await asyncio.gather(*[fetch_actor_data(client, actor_id) for actor_id in actor_ids])

        return actors_data

async def fetch_actor_data(client: httpx.AsyncClient, actor_id: int):
    tmdb_api_key = os.getenv('TMDB_API_KEY')

    response = await client.get(
        f'https://api.themoviedb.org/3/person/{actor_id}?append_to_response=movie_credits',
        params={ 'api_key': tmdb_api_key, 'language': 'en-US' }
    )

    response_body = response.json()
    actor_name = response_body.get('name')
    cast_credits = response_body.get('movie_credits', {}).get('cast')

    return { 'id': actor_id, 'name': actor_name, 'cast_credits': cast_credits }

def build_movies_id_map(actors_data: [dict]):
    movies_id_map = {}

    for actor_object in actors_data:
        actor_id, actor_name, actor_credits = map(actor_object.get, ('id', 'name', 'cast_credits'))

        for credit_object in actor_credits:
            movie_id = credit_object['id']
            movie = movies_id_map.get(movie_id)
            character, credit_id = map(credit_object.get, ('character', 'credit_id'))

            if not movie:
                movie = build_movie_object(movie_id, credit_object)

            movie['credits'].append({
                'actor_id': actor_id,
                'actor_name': actor_name,
                'character': character,
                'credit_id': credit_id
            })
            movies_id_map[movie_id] = movie

    return movies_id_map

def build_movie_object(movie_id: int, credit_object: dict):
    return {
        'id': movie_id,
        'title': credit_object['title'],
        'release_date': credit_object['release_date'],
        'poster_path': credit_object['poster_path'],
        'credits': []
    }

# Example response for /actors-crossover:
#
# [
#     {
#         'id': 11,
#         'title': 'Star Wars',
#         'release_date': '1977-05-25',
#         'poster_path': '/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg',
#         'credits': [
#             {
#                 'actor_id': 2,
#                 'actor_name': 'Mark Hamill',
#                 'character': 'Luke Skywalker',
#                 'credit_id': '52fe420dc3a36847f8000441'
#             },
#             {
#                 'actor_id': 3,
#                 'actor_name': 'Harrison Ford',
#                 'character': 'Han Solo',
#                 'credit_id': '52fe420dc3a36847f8000445'
#             }
#         ]
#     }
# ]
