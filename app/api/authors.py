from sqlite3 import Date


class Author():
    def __init__(self, firstName, middleName, lastName, dob, dod=None, pseudonyms=None):
        self.firstNaame = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.dob = dob
        self.dod = dod
        self.pseudonyms = pseudonyms if pseudonyms is not None else []

    firstNaame: str
    middleName: str
    lastName: str
    dob: Date
    dod: Date | None
    pseudonyms: list[str]

import os
import main
import sqlite3
import api.base_api
from pathlib import Path
from fastapi import FastAPI, APIRouter, HTTPException, Request

CURRENT_FILE = Path(__file__)
TARGET_API = CURRENT_FILE.stem
DEFAULT_DB_PATH = "app/data/DB/"

DB_NAMES = [TARGET_API]
db_paths = [db["db_path"] for server in main.SERVERS for db in server["databases"] if server["api"] == "api." + TARGET_API]

for path in db_paths:
    if not os.path.exists(path):
        raise RuntimeError(f"Database not found: {path}")

connections = {
    os.path.basename(path).split(".")[0]: sqlite3.connect(path, check_same_thread=False)
    for path in db_paths
}

for conn in connections.values():
    conn.row_factory = sqlite3.Row

router = APIRouter(prefix="", tags=[TARGET_API])
app = FastAPI(title=f"{TARGET_API} DB API")
api.base_api.main(app, connections)
