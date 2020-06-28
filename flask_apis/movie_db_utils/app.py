import asyncio
import os

from flask import Blueprint, request
import httpx

movie_db_utils_api = Blueprint('movie_db_utils_api', __name__)

@movie_db_utils_api.route('/actors-crossover', methods=['GET'])
def actors_crossover():
    actor_id_strings = request.args.get('actor_ids', '').split(',')
    if len(actor_id_strings) < 2:
        return { 'message': '"actor_ids" param is required, must contain at least 2 comma-separated IDs' }, 422

    actor_ids = [int(id_string) for id_string in actor_id_strings]

    loop = asyncio.get_event_loop()
    all_actor_credits = loop.run_until_complete(fetch_all_actor_credits(actor_ids))

    movies_id_map = build_movies_id_map(all_actor_credits)

    crossover_movies = list(filter(lambda movie: len(movie['credits']) > 1, movies_id_map.values()))

    return {
        'actor_ids': actor_ids,
        'actor_credits': all_actor_credits,
        'crossover_movies': crossover_movies
    }

async def fetch_all_actor_credits(actor_ids: [int]):
    async with httpx.AsyncClient() as client:
        actor_credits = await asyncio.gather(*[fetch_actor_credits(client, actor_id) for actor_id in actor_ids])

        return actor_credits

async def fetch_actor_credits(client: httpx.AsyncClient, actor_id: int):
    tmdb_api_key = os.getenv('TMDB_API_KEY')

    response = await client.get(
        f'https://api.themoviedb.org/3/person/{actor_id}/movie_credits',
        params={ 'api_key': tmdb_api_key, 'language': 'en-US' }
    )

    cast_credits = response.json().get('cast')

    return { 'actor_id': actor_id, 'credits': cast_credits }

def build_movies_id_map(all_actor_credits: [dict]):
    movies_id_map = {}

    for credits_object in all_actor_credits:
        actor_id = credits_object['actor_id']
        actor_credits = credits_object['credits']

        for actor_credit in actor_credits:
            movie_id = actor_credit['id']
            movie = movies_id_map.get(movie_id)
            character, credit_id = map(actor_credit.get, ('character', 'credit_id'))

            if not movie:
                movie = build_movie_object(movie_id, actor_credit)

            movie['credits'].append({
                'actor_id': actor_id,
                'character': character,
                'credit_id': credit_id
            })
            movies_id_map[movie_id] = movie

    return movies_id_map

def build_movie_object(movie_id: int, actor_credit: dict):
    return {
        'id': movie_id,
        'title': actor_credit['title'],
        'release_date': actor_credit['release_date'],
        'poster_path': actor_credit['poster_path'],
        'credits': []
    }

# [
#     {
#         'id': 11,
#         'title': 'Star Wars',
#         'release_date': '1977-05-25',
#         'poster_path': '/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg',
#         'credits': [
#             {
#                 'actor_id': 2,
#                 'character': 'Luke Skywalker',
#                 'credit_id': '52fe420dc3a36847f8000441'
#             },
#             {
#                 'actor_id': 3,
#                 'character': 'Han Solo',
#                 'credit_id': '52fe420dc3a36847f8000445'
#             }
#         ]
#     }
# ]
