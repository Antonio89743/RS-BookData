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
import sqlite3
import uvicorn
from fastapi import FastAPI, HTTPException

DB_PATH = "app/data/DB/authors.db"
PORT = 8001


def run():
    if not os.path.exists(DB_PATH):
        raise RuntimeError(f"Database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row

    app = FastAPI(title="Authors DB")

    @app.get("/{db_name}/tables")
    def list_tables(db_name: str):
        if db_name != "authors":
            raise HTTPException(status_code=404, detail="Database not found")

        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row["name"] for row in cursor.fetchall()]
        return {"tables": tables}

    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")
