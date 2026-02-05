# Aplikacija koja sadrži informacije o knjigama. Informacije mogu biti naziv knjige, izvorni jezik, autor knjige, izdavač, ISBN knjige, i slično.  
# Aplikacija se sastoji od nekoliko servera koji mogu međusobno komunicirati. 
# Na primjer, jedan server ima sve podatke o piscu, dok drugi server ima podatke o izdavačima. Moguće je da server o piscu zatraži od drugog 
# servera da vrati popis svih knjiga koje je napisao određeni pisac, a koje je izdao određeni izdavač.

# Ideas:
    # get a list of authors published under a specific publisher




# to do:
# enable communication between servers

# http://localhost:9000/authors/docs
# http://localhost:9000/edition/docs
# http://localhost:9000/authors/authors/authors/rows
# http://localhost:9000/authors/authors/authors/rows?firstName=John
# http://localhost:9000/authors/authors/authors/rows?firstName=John&lastName=Voelker

from fastapi.responses import RedirectResponse
import uvicorn
import importlib
from fastapi import FastAPI

PORT = 9000
DEFAULT_DB_PATH = "app/data/DB/"

SERVERS = [
    {
        "port": 8001,
        "api": "api.authors",
        "databases": [
            {
                "name": "authors",
                "db_path": DEFAULT_DB_PATH + "authors.db"
            }
        ]
    },
    {
        "port": 8002,
        "api": "api.authorship",
        "databases": [
            {
                "name": "authorship",
                "db_path": DEFAULT_DB_PATH + "authorship.db"
            }
        ]
    },
    {
        "port": 8003,
        "api": "api.edition",
        "databases": [
            {
                "name": "edition",
                "db_path": DEFAULT_DB_PATH + "edition.db"
            }
        ]
    },
    {
        "port": 8004,
        "api": "api.edition_languages",
        "databases": [
            {
                "name": "edition_languages",
                "db_path": DEFAULT_DB_PATH + "edition_languages.db"
            }
        ]
    },
    {
        "port": 8005,
        "api": "api.languages",
        "databases": [
            {
                "name": "languages",
                "db_path": DEFAULT_DB_PATH + "languages.db"
            }
        ]
    },
    {
        "port": 8006,
        "api": "api.publisher",
        "databases": [
            {
                "name": "publisher",
                "db_path": DEFAULT_DB_PATH + "publisher.db"
            }
        ]
    },
    {
        "port": 8007,
        "api": "api.work_and_collection",
        "databases": [
            {
                "name": "work",
                "db_path": DEFAULT_DB_PATH + "work.db"
            },
            {
                "name": "collection",
                "db_path": DEFAULT_DB_PATH + "collection.db"
            }
        ]
    },
    {
        "port": 8009,
        "api": "api.work_languages",
        "databases": [
            {
                "name": "work_languages",
                "db_path": DEFAULT_DB_PATH + "work_languages.db"
            }
        ]
    }
]

app = FastAPI(title="Book Gateway API")

@app.get("/servers", include_in_schema=True)
def root():
    tables = [server["api"].split(".")[-1] for server in SERVERS]
    return {"tables": tables}

if __name__ == "__main__":
    for server in SERVERS:
        module = importlib.import_module(server["api"])
        mount_path = "/" + server["api"].split(".")[-1]
        if hasattr(module, "app"):
            app.mount(mount_path, module.app)

    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")