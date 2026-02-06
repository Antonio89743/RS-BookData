from fastapi import HTTPException, Request

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

        all_columns = [col["name"] if isinstance(col, dict) else col[1] for col in columns_info]

        conn.row_factory = lambda cursor, row: dict(zip([c[0] for c in cursor.description], row))
        cursor = conn.cursor()

        query_params = dict(request.query_params)
        fields = query_params.pop("fields", None)

        if fields:
            selected_columns = [col.strip() for col in fields.split(",")]
            invalid_cols = [col for col in selected_columns if col not in all_columns]
            if invalid_cols:
                raise HTTPException(status_code=400, detail=f"Invalid column(s) requested: {invalid_cols}")
        else:
            selected_columns = all_columns

        where_clauses = []
        params = []

        for k, v in query_params.items():
            if k not in all_columns:
                raise HTTPException(status_code=400, detail=f"Invalid column: {k}")

            values = []
            for part in v.split(","):
                if part.strip():
                    values.append(part.strip())

            if not values:
                continue

            if all(x.isdigit() for x in values):
                placeholders = ", ".join("?" for _ in values)
                where_clauses.append(f"{k} IN ({placeholders})")
                params.extend([int(x) for x in values])
            else:
                like_clauses = [f"{k} LIKE ?" for _ in values]
                where_clauses.append("(" + " OR ".join(like_clauses) + ")")
                params.extend([f"%{x}%" for x in values])

        query = f"SELECT {', '.join(selected_columns)} FROM {table_name}"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
