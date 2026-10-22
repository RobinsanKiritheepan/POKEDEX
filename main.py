from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from schemas.pokemon import Pokemon
from db.database import get_connection
from clients.pokeapi import get_pokemon_from_api


app = FastAPI()

@app.get("/health")
def read_health():
    return {"status": "ok"}


@app.get("/pokemons/{number}")
def read_pokemon(number: int):
    URL = f"https://pokeapi.co/api/v2/pokemon/{number}"
    appel_pokeAPI = requests.get(URL)
    if appel_pokeAPI.status_code == 200:
        data = appel_pokeAPI.json()
        return {
            "number": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
        }
    else:
        raise HTTPException(status_code=404, detail="Pokemon not found")


@app.get("/pokemons/{number}/scan" )
def scan_pokemon(number: int):
    try:
        data = get_pokemon_from_api(number)
    except requests.HTTPError:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO pokemon (
            number,
            name,
            name_fr,
            types,
            image_url,
            height,
            weight,
            evolves_from_number
        )VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (data["id"], data["name"], data["name"],data["name"], data["name"], data["height"], data["weight"], None))
  
    connection.commit()
    connection.close()
    return {"status": "scanned", "number": data["id"]}

    