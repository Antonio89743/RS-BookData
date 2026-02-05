# Aplikacija koja sadrži informacije o knjigama. Informacije mogu biti naziv knjige, izvorni jezik, autor knjige, izdavač, ISBN knjige, i slično.  
# Aplikacija se sastoji od nekoliko servera koji mogu međusobno komunicirati. 
# Na primjer, jedan server ima sve podatke o piscu, dok drugi server ima podatke o izdavačima. Moguće je da server o piscu zatraži od drugog 
# servera da vrati popis svih knjiga koje je napisao određeni pisac, a koje je izdao određeni izdavač.

# Ideas:
    # get a list of authors published under a specific publisher




# to do:
# enable communication between servers

# http://localhost:8007/work/tables

import importlib
import multiprocessing

default_db_path = "app/data/DB/"

servers = [
    {
        "port": 8001,
        "api": "api.authors",
        "databases": [
            {
                "name": "authors",
                "db_path": default_db_path + "authors.db"
            }
        ]
    },
    {
        "port": 8002,
        "api": "api.authorship",
        "databases": [
            {
                "name": "authorship",
                "db_path": default_db_path + "authorship.db"
            }
        ]
    },
    {
        "port": 8003,
        "api": "api.edition",
        "databases": [
            {
                "name": "edition",
                "db_path": default_db_path + "edition.db"
            }
        ]
    },
    {
        "port": 8004,
        "api": "api.edition_languages",
        "databases": [
            {
                "name": "edition_languages",
                "db_path": default_db_path + "edition_languages.db"
            }
        ]
    },
    {
        "port": 8005,
        "api": "api.languages",
        "databases": [
            {
                "name": "languages",
                "db_path": default_db_path + "languages.db"
            }
        ]
    },
    {
        "port": 8006,
        "api": "api.publisher",
        "databases": [
            {
                "name": "publisher",
                "db_path": default_db_path + "publisher.db"
            }
        ]
    },
    {
        "port": 8007,
        "api": "api.work_and_collection",
        "databases": [
            {
                "name": "work",
                "db_path": default_db_path + "work.db"
            },
            {
                "name": "collection",
                "db_path": default_db_path + "collection.db"
            }
        ]
    },
    {
        "port": 8009,
        "api": "api.work_languages",
        "databases": [
            {
                "name": "work_languages",
                "db_path": default_db_path + "work_languages.db"
            }
        ]
    }
]

    # @app.get("/health")
    # def health():
    #     return {
    #         "status": "ok",
    #         "port": server_cfg["port"],
    #         "databases": list(connections.keys())
    #     }

    # @app.get("/{db_name}/tables")
    # def list_tables(db_name: str):
    #     if db_name not in connections:
    #         raise HTTPException(404, "Unknown database")

    #     cur = connections[db_name].cursor()
    #     cur.execute("""
    #         SELECT name FROM sqlite_master
    #         WHERE type='table' AND name NOT LIKE 'sqlite_%'
    #     """)
    #     return [row["name"] for row in cur.fetchall()]

    # @app.get("/{db_name}/query")
    # def query(db_name: str, sql: str):
    #     """
    #     Example:
    #     /edition/query?sql=SELECT * FROM edition_format
    #     """
    #     if db_name not in connections:
    #         raise HTTPException(404, "Unknown database")

    #     try:
    #         cur = connections[db_name].cursor()
    #         cur.execute(sql)
    #         rows = cur.fetchall()
    #         return [dict(row) for row in rows]
    #     except sqlite3.Error as e:
    #         raise HTTPException(400, str(e))

    # uvicorn.run(app, host="127.0.0.1", port=server_cfg["port"], log_level="info")

def start_server(server_cfg: dict):
    module = importlib.import_module(server_cfg["api"])
    module.run()

def main():
    processes = []
    for server in servers:
        p = multiprocessing.Process(
            target=start_server,
            args=(server,),
            name=f"server_{server['port']}"
        )
        p.start()
        processes.append(p)
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
