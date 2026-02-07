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

@router.get("/work/{work_id}/collections")
async def get_authors_collections(work_id: int):
    async with httpx.AsyncClient() as client:

        if work_id is None:
            raise HTTPException(status_code=404, detail=f"Author '{work_id}' not found")

        work_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.work_and_collection")
        resp = await client.get(f"http://127.0.0.1:{work_port}/collection/work_collection/rows?idWork={work_id}")
        resp.raise_for_status()
        work_collection_json = resp.json()
        collection_ids = list({row["idCollection"] for row in work_collection_json})
        
        if not collection_ids:
            return {"collections": []}
        
        resp = await client.get(f"http://127.0.0.1:{work_port}/collection/collection/rows?id={','.join(map(str, collection_ids))}")
        resp.raise_for_status()
        collections_json = resp.json()
        return {"collections": collections_json}

@router.get("/work/{work_id}/languagesPublished")
async def get_authors_collections(work_id: int):
    async with httpx.AsyncClient() as client:

        if work_id is None:
            raise HTTPException(status_code=404, detail=f"Author '{work_id}' not found")

        work_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.edition")
        resp = await client.get(f"http://127.0.0.1:{work_port}/edition/edition/rows?fields=idLanguage&idWork={work_id}")
        resp.raise_for_status()
        work_edition_json = resp.json()
        edition_ids = list({row["idLanguage"] for row in work_edition_json})
        
        work_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.languages")
        resp = await client.get(f"http://127.0.0.1:{work_port}/languages/languages/rows?fields=language&id={','.join(map(str, edition_ids))}")
        resp.raise_for_status()
        languages_json = resp.json()

        return {"languages": languages_json}

app.include_router(router)