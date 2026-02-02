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




