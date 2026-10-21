import sqlite3
from pathlib import Path

path_db = Path(__file__).parent.parent / "pokedex.db"

def get_connection():
    connection = sqlite3.connect(path_db)
    return connection