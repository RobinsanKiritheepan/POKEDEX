from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from pydantic import BaseModel

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

    class Pokemon(BaseModel):
        number: int
        name: str
        name_fr: str
        types: list[str]
        image_url: str
        height: int
        weight: int
        evolves_from_number: int | None = None