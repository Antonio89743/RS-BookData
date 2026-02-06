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
import httpx
import sqlite3
import api.base_api
from pathlib import Path
from fastapi import FastAPI, APIRouter, HTTPException

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

@router.get("/authors/publisher/{publisher_name}")
async def get_authors_by_publisher(publisher_name: str):
    async with httpx.AsyncClient() as client:
 
        publisher_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.publisher")
        r = await client.get(f"http://127.0.0.1:{publisher_port}/publisher/publisher/rows")
        r.raise_for_status()
        publisher_json = r.json()
        
        publisher_id = None
        for publisher in publisher_json:
            if publisher_name.lower() in publisher["name"].lower():
                publisher_id = publisher["id"]
                break

        if publisher_id is None:
            raise HTTPException(status_code=404, detail=f"Publisher '{publisher_name}' not found")
        
        edition_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.edition")
        resp = await client.get(f"http://127.0.0.1:{edition_port}/edition/edition/rows?fields=workId&publisherId={publisher_id}")
        resp.raise_for_status()
        edition_json = resp.json()

        work_ids = []
        for edition in edition_json:
            work_ids.append(edition["workId"])

        authorship_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.authorship")
        resp = await client.get(f"http://127.0.0.1:{authorship_port}/authorship/authorship/rows?fields=idAuthor&idWork={','.join(map(str, work_ids))}")
        resp.raise_for_status()
        authorship_json = resp.json()

        authors_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.authors")
        resp = await client.get(f"http://127.0.0.1:{authors_port}/authors/authors/rows?id={','.join(map(str, [author['idAuthor'] for author in authorship_json]))}")
        resp.raise_for_status()
        authors_json = resp.json()
        return {"authors": authors_json}

@router.get("/authors/{author_id}/genres")
async def get_authors_by_publisher(author_id: int):
    async with httpx.AsyncClient() as client:

        if author_id is None:
            raise HTTPException(status_code=404, detail=f"Publisher '{author_id}' not found")

        authorship_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.authorship")
        resp = await client.get(f"http://127.0.0.1:{authorship_port}/authorship/authorship/rows?fields=idWork&idAuthor={author_id}")
        resp.raise_for_status()
        authorship_json = resp.json()

        work_ids = []
        for authorsip in authorship_json:
            work_ids.append(authorsip["idWork"])

        work_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.work_and_collection")
        resp = await client.get(f"http://127.0.0.1:{work_port}/work/work_genre/rows?fields=idGenre&idWork={','.join(map(str, work_ids))}")
        resp.raise_for_status()
        work_genre_json = resp.json()

        genre_ids = []
        for work_genre in work_genre_json:
            genre_ids.append(work_genre["idGenre"])

        resp = await client.get(f"http://127.0.0.1:{work_port}/work/genre/rows?fields=genre&id={','.join(map(str, genre_ids))}")
        resp.raise_for_status()
        work_genre_json = resp.json()

        return {
            "genres": list(
                sorted({item["genre"] for item in work_genre_json})
            )
        }



# fetch all works by author
# fetch if any of those works are in a collection


@router.get("/authors/{author_id}/collections")
async def get_authors_collections(author_id: int):
    async with httpx.AsyncClient() as client:

        if author_id is None:
            raise HTTPException(status_code=404, detail=f"Author '{author_id}' not found")

        authorship_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.authorship")
        resp = await client.get(f"http://127.0.0.1:{authorship_port}/authorship/authorship/rows?fields=idWork&idAuthor={author_id}")
        resp.raise_for_status()
        authorship_json = resp.json()

        work_ids = [row["idWork"] for row in authorship_json]
        if not work_ids:
            return {"collections": []}

        work_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.work_and_collection")
        resp = await client.get(f"http://127.0.0.1:{work_port}/collection/work_collection/rows?idWork={','.join(map(str, work_ids))}")
        resp.raise_for_status()
        work_collection_json = resp.json()
        collection_ids = list({row["idCollection"] for row in work_collection_json})  # unique IDs
        
        if not collection_ids:
            return {"collections": []}
        
        resp = await client.get(f"http://127.0.0.1:{work_port}/collection/collection/rows?id={','.join(map(str, collection_ids))}")
        resp.raise_for_status()
        collections_json = resp.json()
        return {"collections": collections_json}

@router.get("/authors/{author_id}/{collection_id}/works")
async def get_authors_by_publisher(author_id: int):
    async with httpx.AsyncClient() as client:

        return

app.include_router(router)
