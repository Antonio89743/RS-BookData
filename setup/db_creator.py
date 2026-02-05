import os
import sqlite3

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
                ('John', 'D.', 'Voelker', '1903-06-29', '1991-03-18'),
                ('Patrick ', NULL, 'Hamilton', '1904-03-17', '1962-09-23'),
                ('Aaron ', NULL, 'Allston', '1960-12-08', '2014-02-27');
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
                ("The Silmarillion", NULL, 1),
                ("The Children of Húrin", NULL, 1),
                ("The Return of the King ", '1955-03-20', 1);
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
                ('Thriller');
            INSERT INTO work_genre (idWork, idGenre) VALUES
                (1, 6),
                (11, 6),
                (12, 6),
                (13, 6),
                (14, 6),
                (15, 6),
                (16, 6);
            """
    },
    {
        "path": default_db_path + "edition.db",
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
            INSERT INTO edition (workId, publicationDate, publisherId, ISBN, formatId, idLanguage) VALUES
                (1, '1996-08-06', 1, '978-0553103540', 2, 1),
                (11, '1937-09-21', 3, '978-0547928227', 1, 1),
                (12, '1954-07-29', 3, '978-0547928210', 1, 1),
                (13, '1954-11-11', 3, '978-054  7928203', 1, 1),
                (14, NULL, 3, '978-0547928197', 1, 1),
                (15, NULL, 3, '978-0547928180', 1, 1),
                (16, '1955-03-20', 3, '978-0547928173', 1, 1);
            INSERT INTO edition_format (format) VALUES
                ('Hardcover'),
                ('Paperback'),
                ('Ebook'),
                ('Audiobook');
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
            conn = sqlite3.connect(db["path"])
            cursor = conn.cursor()
            cursor.executescript(db["execute_message_insert_defaults"])
            conn.commit()

    conn.close()

create_dbs()
