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
    actor_credits = loop.run_until_complete(fetch_all_actor_credits(actor_ids))

    return {
        'actor_ids': actor_ids,
        'actor_credits': actor_credits
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

    return { 'actor_id': actor_id, 'credits': response.json() }
