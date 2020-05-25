import sqlite3

# Local
import episode
import species

# Commands and Constants
CREATE_EPISODES_TABLE = """CREATE TABLE episodes (
            episodeNumb integer,
            englishEpisodeTitle text,
            pokemonAppearances text
        )"""

CREATE_SPECIES_TABLE = """CREATE TABLE species (
            pokemonId integer,
            pkDexNum text,
            name text,
            primaryType text,
            secondaryType text,
            image text
        )"""

DATABASE = "pokemonanime.db"

DROP_EPISODES_TABLE = "DROP TABLE episodes"

DROP_SPECIES_TABLE = "DROP TABLE species"

CLEAR_EPISODES_TABLE_DATA = "DELETE FROM episodes"

CLEAR_SPECIES_TABLE_DATA = "DELETE FROM species"


def sendSqlStatement(command):
    connection = sqlite3.connect(DATABASE)
    db = connection.cursor()
    db.execute(command)
    print(db.fetchall())
    connection.commit()
    connection.close()

def fillPokemonSpeciesTable():
    pokemonSpeciesInfo = species.getEverySpeciesInfo()
    connection = sqlite3.connect(DATABASE)
    db = connection.cursor()

    for pokemon in pokemonSpeciesInfo:
        sqlStatement = ("INSERT INTO species VALUES (" + 
            str(pokemon['pokemonId']) + ", '" +
            pokemon['pkDexNum'] + "', '" +
            escapedString(pokemon['name']) + "', '" +
            pokemon['primaryType'] + "', '" +
            pokemon['secondaryType'] + "', '" +
            pokemon['image'] + "')")
        print(sqlStatement)
        db.execute(sqlStatement)
    # db.execute("SELECT * FROM species")
    # print(db.fetchall())
    connection.commit()
    connection.close()

def escapedString(string):
    return string.translate(str.maketrans({"'":  r"''"}))

# sendSqlStatement(CLEAR_SPECIES_TABLE_DATA)
# fillPokemonSpeciesTable()
# sendSqlStatement("SELECT name from species")
