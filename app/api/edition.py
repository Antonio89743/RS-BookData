import os
import main
import httpx
import sqlite3
import api.base_api
from pathlib import Path
from fastapi import FastAPI, APIRouter, Response

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

@router.get("/edition/{edition_id}/cover")
async def get_edition_cover(edition_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as client:

        work_port = next(server["port"] for server in main.SERVERS if server["api"] == "api.edition")
        resp = await client.get(f"http://127.0.0.1:{work_port}/edition/edition/rows?fields=ISBN&id={edition_id}")
        resp.raise_for_status()
        work_edition_json = resp.json()

        edition_isbn = work_edition_json[0]["ISBN"]

        resp = await client.get(f"https://covers.openlibrary.org/b/isbn/{edition_isbn}-L.jpg")
        resp.raise_for_status()
        return Response(content=resp.content, media_type=resp.headers.get("content-type", "image/jpeg"))

app.include_router(router)