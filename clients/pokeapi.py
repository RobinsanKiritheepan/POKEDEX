import requests


def get_pokemon_from_api(number: int):
    url = f"https://pokeapi.co/api/v2/pokemon/{number}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()