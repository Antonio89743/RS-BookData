import os
import sys
import sqlite3
import subprocess
from pathlib import Path

default_db_path = "app/data/DB/"

dbs = [
    {
        "path": default_db_path + "authors.db",
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
            INSERT INTO authors (firstName, middleName, lastName, DOB, DOD) VALUES 
                ('George', 'R. R.', 'Martin', '1948-09-20', NULL),
                ('J. R. R.', NULL, 'Tolkien', '1892-01-03', '1973-09-02'),
                ('Agatha', NULL, 'Christie', '1890-09-15', '1977-01-12'),
                ('Timothy', NULL, 'Zahn', '1951-09-01', NULL),
                ('Michael', 'A.', 'Stackpole', '1957-11-27', NULL),
                ('Aaron ', NULL, 'Allston', '1960-12-08', '2014-02-27'),
                ('John', 'D.', 'Voelker', '1903-06-29', '1991-03-18'),
                ('Patrick ', NULL, 'Hamilton', '1904-03-17', '1962-09-23');
            INSERT INTO pseudonyms (author_id, pseudonym) VALUES
                (3, 'Mary Westmacott'),
                (6, 'Robert Traver');
            """
    },
    {
        "path": default_db_path + "publisher.db",
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
            INSERT INTO publisher (name, address, phoneNumber, dateFounded, website) VALUES
                ('Bantam Books', '1745 Broadway, New York, NY 10019', '212-782-9000', '1945-01-01', 'https://www.penguinrandomhouse.com/'),
                ('HarperCollins', '195 Broadway, New York, NY 10007', '212-207-7000', '1989-01-01', 'https://www.harpercollins.com/'),
                ('Penguin Books', '80 Strand, London WC2R 0RL, UK', '+44 20 7010 3000', '1935-01-01', 'https://www.penguin.co.uk/'),
                ('Hachette Book Group', '1290 Avenue of the Americas, New York, NY 10104', '212-364-1100', '2006-01-01', 'https://www.hachettebookgroup.com/'),
                ('Simon & Schuster', '1230 Avenue of the Americas, New York, NY 10020', '212-698-7000', '1924-01-01', 'https://www.simonandschuster.com/'),
                ('Macmillan Publishers', '120 Broadway, New York, NY 10271', '646-307-5151', '1843-01-01', 'https://us.macmillan.com/');
            """
    },
    {
        "path": default_db_path + "authorship.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS authorship (
                idWork INTEGER,
                idAuthor INTEGER,
                PRIMARY KEY (idWork, idAuthor)
                )
            """,
        "execute_message_insert_defaults": """
            INSERT INTO authorship (idWork, idAuthor) VALUES
                (1, 1),
                (2, 2),
                (3, 2),
                (4, 2),
                (5, 4),
                (6, 4),
                (7, 4),
                (8, 5),
                (9, 5),
                (10, 5),
                (11, 2),
                (12, 2),
                (13, 2),
                (14, 2),
                (15, 2),
                (16, 2);
            """
    },
    {
        "path": default_db_path + "languages.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS languages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT NOT NULL UNIQUE
                )
            """,
        "execute_message_insert_defaults": """
            INSERT INTO languages (language) VALUES
                ('English'),
                ('Spanish'),
                ('French'),
                ('German'),
                ('Chinese'),
                ('Japanese'),
                ('Croatian'),
                ('Italian'),
                ('Portuguese');
            """
    },
    {
        "path": default_db_path + "work_languages.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS work_languages (
                idLanguage INTEGER,
                idWork INTEGER,
                PRIMARY KEY (idLanguage, idWork)
                )
            """,
        "execute_message_insert_defaults": """
            INSERT INTO work_languages (idLanguage, idWork) VALUES
                (1, 1),
                (1, 2),
                (1, 3),
                (1, 4),
                (1, 5),
                (1, 6),
                (1, 7),
                (1, 8),
                (1, 9),
                (1, 10),
                (1, 11),
                (1, 12),
                (1, 13),
                (1, 14),
                (1, 15),
                (1, 16);
            """
    },
    {
        "path": default_db_path + "collection.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS collection (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
                );
            CREATE TABLE IF NOT EXISTS work_collection (
                idWork INTEGER,
                idCollection INTEGER,
                PRIMARY KEY (idWork, idCollection)
                )
            """,
        "execute_message_insert_defaults": """
            INSERT INTO collection (name) VALUES
                ('Star Wars'),
                ('Star Wars - Legends'),
                ('Star Wars - X-Wing Series'),
                ('The Lord of the Rings'),
                ('Middle-earth'),
                ('Game of Thrones');
            INSERT INTO work_collection (idWork, idCollection) VALUES
                (1, 6),
                (2, 4),
                (3, 4),
                (4, 4),
                (5, 1),
                (6, 1),
                (7, 1),
                (8, 3),
                (9, 3),
                (10, 3),
                (11, 5),
                (12, 5),
                (13, 5),
                (14, 5),
                (15, 5),
                (16, 5);
            """
    },
    {
        "path": default_db_path + "edition_languages.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS edition_languages (
                idEdition INTEGER,
                idLanguage INTEGER,
                PRIMARY KEY (idEdition, idLanguage)
                )
            """,
        "execute_message_insert_defaults": """
            INSERT INTO edition_languages (idEdition, idLanguage) VALUES
                (1, 1),
                (2, 1),
                (3, 1),
                (4, 1),
                (5, 1),
                (6, 1),
                (7, 1),
                (8, 1),
                (9, 1),
                (10, 1),
                (11, 1),
                (12, 1),
                (13, 1),
                (14, 1),
                (15, 1),
                (16, 1);
            """
    },
    {
        "path": default_db_path + "work.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS work (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                dateCompleted DATE,
                idOriginalLanguage INTEGER
                );
            CREATE TABLE IF NOT EXISTS genre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT NOT NULL UNIQUE
                ); 
            CREATE TABLE IF NOT EXISTS work_genre (
                idWork INTEGER,
                idGenre INTEGER,
                PRIMARY KEY (idWork, idGenre)
                )
            """,
        "execute_message_insert_defaults": """
            INSERT INTO work (title, dateCompleted, idOriginalLanguage) VALUES
                ("A Game of Thrones", '1996-08-06', 1),
                ("Anatomy of a Murder", NULL, 1),
                ("Rope", NULL, 1),
                ("The Witness for the Prosecution", NULL, 1),
                ("Heir to the Empire", NULL, 1),
                ("Dark Force Rising", NULL, 1),
                ("The Last Command", NULL, 1),
                ("X-Wing: Rogue Squadron", '1996', 1),
                ("X-Wing: Wedge's Gamble", '1997', 1),
                ("X-Wing: The Krytos Trap ", '1998', 1),
                ("The Hobbit", '1937-09-21', 1),
                ("The Fellowship of the Ring ", '1954-07-29', 1),
                ("The Two Towers", '1954-11-11', 1),
                ("The Return of the King ", '1955-03-20', 1),
                ("The Silmarillion", NULL, 1),
                ("The Children of Húrin", NULL, 1);
            INSERT INTO genre (genre) VALUES
                ('Fiction'),
                ('Non-Fiction'),
                ('Science Fiction'),
                ('Mystery'), 
                ('Romance'),
                ('Fantasy'),
                ('Biography'),
                ('History'),
                ('Horror'), 
                ('Crime'), 
                ('Thriller'),
                ('Adventure'),
                ('Drama'),
                ('Epic');
            INSERT INTO work_genre (idWork, idGenre) VALUES
                (1, 4),
                (1, 6),
                (1, 9),
                (1, 10),
                (2, 5),
                (2, 6),
                (3, 7),
                (2, 9),
                (3, 6),
                (4, 5),
                (4, 7),
                (5, 3),
                (5, 8),
                (6, 3),
                (6, 8),
                (7, 3),
                (7, 8),
                (8, 3),
                (8, 8),
                (9, 3),
                (9, 8),
                (10, 3),
                (10, 8),
                (11, 4),
                (11, 6),
                (11, 8),
                (12, 4),
                (12, 6),
                (12, 10),
                (13, 4),
                (13, 6),
                (13, 10),
                (14, 4),
                (14, 6),
                (14, 10),
                (15, 4),
                (15, 6),
                (15, 9),
                (16, 4),
                (16, 6);
            """
    },
    {
        "path": default_db_path + "edition.db",
        "execute_message_create": """
            CREATE TABLE IF NOT EXISTS edition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idWork INTEGER,
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
            INSERT INTO edition (idWork, publicationDate, publisherId, ISBN, formatId, idLanguage) VALUES
                -- A Game of Thrones (George R. R. Martin)
                (1, '1996-08-06', 1, '978-0553103540', 1, 1),
                (1, '1997-03-01', 1, '978-0553573404', 2, 1),
                (1, '2011-03-22', 2, '978-0007428540', 3, 1),
                -- Anatomy of a Murder (John D. Voelker)
                (2, '1958-01-01', 5, '9780312033569', 1, 1),
                (2, '1984-06-01', 3, '978-0140183070', 2, 1),
                -- Rope (Patrick Hamilton)
                (3, '1929-01-01', 6, '9780451526082', 1, 1),
                (3, '2001-05-01', 2, '978-0413771199', 2, 1),
                -- Witness for the Prosecution (Agatha Christie)
                (4, '1933-01-01', 4, '9780396074120', 1, 1),
                (4, '2016-09-06', 2, '978-0062693662', 3, 1),
                -- Heir to the Empire (Timothy Zahn)
                (5, '1991-05-01', 1, '978-0553296129', 1, 1),
                (5, '1992-06-01', 1, '978-0553568004', 2, 1),
                (5, '2011-09-06', 1, '978-0307796068', 3, 1),
                -- Dark Force Rising
                (6, '1992-06-01', 1, '978-0553296136', 1, 1),
                (6, '2011-09-06', 1, '978-0307796075', 3, 1),
                -- The Last Command
                (7, '1993-01-01', 1, '978-0553296143', 1, 1),
                (7, '2011-09-06', 1, '978-0307796082', 3, 1),
                -- X-Wing series (Stackpole)
                (8, '1996-01-01', 3, '978-0553568011', 1, 1),
                (8, '1997-02-01', 3, '978-0553568042', 2, 1),
                (9, '1997-01-01', 3, '978-0553568027', 1, 1),
                (10, '1998-01-01', 3, '978-0553568035', 1, 1),
                -- Tolkien works
                (11, '2012-09-18', 3, '978-0547928234', 3, 1),
                (12, '2012-09-18', 3, '978-0547928241', 3, 1),
                -- The Hobbit
                (11, '1937-09-21', 3, '9780618260300', 1, 1),
                (11, '1999-09-01', 3, '9780261102217', 2, 1),

                -- The Fellowship of the Ring
                (12, '1954-07-29', 3, '9780261102354', 2, 1),

                -- The Two Towers
                (13, '1954-11-11', 3, '9780261102361', 2, 1),

                -- The Return of the King
                (14, '1955-03-20', 3, '9780261102378', 2, 1),

                -- The Silmarillion
                (15, '1977-09-15', 3, '9780261102422', 2, 1),

                -- The Children of Húrin
                (16, '2007-04-17', 3, '9780618894642', 1, 1),
                (16, '2008-04-01', 3, '9780547086057', 2, 1);
            INSERT INTO edition_format (format) VALUES
                ('Hardcover'),
                ('Paperback'),
                ('Ebook'),
                ('Audiobook');
            """      
    }
]

def create_dbs(insert_defaults=True) -> None:
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
            conn = sqlite3.connect(db["path"])
            cursor = conn.cursor()
            cursor.executescript(db["execute_message_insert_defaults"])
            conn.commit()

    conn.close()

def install_dependencies() -> None:
    req_file = Path(__file__).parent / "requirements.txt"
    if req_file.exists():
        print(f"Installing dependencies from {req_file}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
        print("Dependencies installed successfully!")
    else:
        print("No requirements.txt found, skipping dependency installation.")

is_installing_dependencies: bool = True

if __name__ == "__main__":
    if is_installing_dependencies == False:
        install_dependencies()
    create_dbs()
