import os
import sqlite3

dbs = [
    {
        "path": "files/DB/authors.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName TEXT,
                middleName TEXT,
                lastName TEXT,
                DOB DATE,
                DOD DATE
                );
            CREATE TABLE IF NOT EXISTS pseudonyms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_id INTEGER,
                pseudonym TEXT,
                FOREIGN KEY (author_id) REFERENCES authors(id)
                )
            """,
        "execute_message_insert_defaults": """
            """
    },
    {
        "path": "files/DB/publisher.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS publisher (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                address TEXT,
                phoneNumber TEXT,
                dateFounded DATE,
                website TEXT
                )
            """,
        "execute_message_insert_defaults": """
            """
    },
    {
        "path": "files/DB/authorship.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS authorship (
                idAuthor INTEGER,
                idWork INTEGER,
                PRIMARY KEY (idAuthor, idWork)
                )
            """,
        "execute_message_insert_defaults": """
            """
    },
    {
        "path": "files/DB/languages.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS languages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT
                )
            """,
        "execute_message_insert_defaults": """
            """
    },
    {
        "path": "files/DB/work_languages.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS work_languages (
                idLanguage INTEGER,
                idWork INTEGER,
                PRIMARY KEY (idLanguage, idWork)
                )
            """,
        "execute_message_insert_defaults": """
            """
    },
    {
        "path": "files/DB/edition_languages.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS edition_languages (
                idLanguage INTEGER,
                idEdition INTEGER,
                PRIMARY KEY (idLanguage, idEdition)
                )
            """,
        "execute_message_insert_defaults": """
            """
    },
    {
        "path": "files/DB/work.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS work (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                dateCompleted DATE,
                idOriginalLanguage INTEGER
                );
            CREATE TABLE IF NOT EXISTS genre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT
                ); 
            CREATE TABLE IF NOT EXISTS work_genre (
                idGenre INTEGER,
                idWork INTEGER,
                PRIMARY KEY (idGenre, idWork)
                )
            """,
        "execute_message_insert_defaults": """
            INSERT INTO genre (genre) VALUES ('Fiction'), ('Non-Fiction'), ('Science Fiction'), ('Mystery'), ('Romance'), ('Fantasy'), ('Biography'), ('History'), ('Self-Help'), ('Horror')
            """
    },
    {
        "path": "files/DB/edition.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS edition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workId INTEGER,
                publicationDate DATE,
                publisherId INTEGER,
                ISBN TEXT,
                formatId INTEGER,
                idLanguage INTEGER,
                FOREIGN KEY (formatId) REFERENCES edition_format(id)
                );
            CREATE TABLE IF NOT EXISTS edition_format (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                format TEXT
                )
            """,
        "execute_message_insert_defaults": """
            INSERT INTO edition_format (format) VALUES ('Hardcover'), ('Paperback'), ('Ebook'), ('Audiobook')
            """      
    }
]

def create_dbs(insert_defaults=True):
    for db in dbs:
        db_dir = os.path.dirname(db["path"])
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        conn = sqlite3.connect(db["path"])
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = OFF;")
        cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%';
        """)
        tables = [row[0] for row in cursor.fetchall()]
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table};")
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.executescript(db["execute_message_create"])
        conn.commit()

    if insert_defaults:
        for db in dbs:
            if db["path"] == "files/DB/edition.db":
                conn = sqlite3.connect(db["path"])
                cursor = conn.cursor()
                cursor.executescript(db["execute_message_insert_defaults"])
                conn.commit()

    conn.close()

create_dbs()
