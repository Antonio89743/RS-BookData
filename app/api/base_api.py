import os
import sqlite3
from fastapi import FastAPI, APIRouter, HTTPException, Request

def main(app, connections):
    @app.get("/dbs")
    def list_dbs():
        return {"dbs": list(connections.keys())}

    @app.get("/{db_name}/tables")
    def list_tables(db_name: str):
        if db_name not in connections:
            raise HTTPException(status_code=404, detail="Database not found")

        cursor = connections[db_name].execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        tables = [row["name"] for row in cursor.fetchall()]
        return {"tables": tables}

    @app.get("/{db_name}/{table_name}/rows")
    def get_rows(db_name: str, table_name: str, request: Request):
        if db_name not in connections:
            raise HTTPException(status_code=404, detail="Database not found")

        conn = connections[db_name]
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        if not columns_info:
            raise HTTPException(status_code=404, detail="Table not found")

        columns = [col[1] for col in columns_info]

        filters = dict(request.query_params)
        where_clauses = []
        params = []

        for k, v in filters.items():
            if k not in columns:
                raise HTTPException(status_code=400, detail=f"Invalid column: {k}")

            if v.lower() == "null":
                where_clauses.append(f"{k} IS NULL")
            else:
                where_clauses.append(f"{k} = ?")
                params.append(v)

        query = f"SELECT * FROM {table_name}"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]