import sqlite3
import pickle 

# Local
import episode
import species

# Commands and Constants
CREATE_EPISODES_TABLE = """CREATE TABLE episodes (
            id integer,
            type text,
            episodeNum integer,
            episodeCode text,
            englishEpisodeTitle text,
            japaneseEpisodeTitle text,
            japaneseEpisodeTitleTranslated text,
            japaneseBroadcastDate text,
            americanBroadcastDate text
        )"""

CREATE_SPECIES_TABLE = """CREATE TABLE species (
            id integer,
            pkDexNum text,
            name text,
            primaryType text,
            secondaryType text,
            image text
        )"""

CREATE_EPISODES_SPECIES_TABLES = """CREATE TABLE episodesSpecies (
           episodeId integer,
           pokemonId integer
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

def escapedString(string):
    return string.translate(str.maketrans({"'":  r"''"}))


def fillPokemonSpeciesTable(pokemonSpeciesInfo):
    connection = sqlite3.connect(DATABASE)
    db = connection.cursor()

    for pokemon in pokemonSpeciesInfo:
        sqlStatement = ("INSERT INTO species VALUES (" + 
            str(pokemon['id']) + ", '" +
            pokemon['pkDexNum'] + "', '" +
            escapedString(pokemon['name']) + "', '" +
            pokemon['primaryType'] + "', '" +
            pokemon['secondaryType'] + "', '" +
            pokemon['image'] + "')")
        db.execute(sqlStatement)
    # db.execute("SELECT * FROM species")
    # print(db.fetchall())
    connection.commit()
    connection.close()

def fillEpisodesTable(pokemonEpisodeInfo):
    connection = sqlite3.connect(DATABASE)
    db = connection.cursor()

    for pokemonEpisode in pokemonEpisodeInfo:
        sqlStatement = ("INSERT INTO episodes VALUES (" + 
            str(pokemonEpisode['id']) + ", '" +
            pokemonEpisode['type'] + "', " +
            str(pokemonEpisode['episodeNum']) + ", '" +
            pokemonEpisode['episodeCode'] + "', '" +
            escapedString(pokemonEpisode['englishEpisodeTitle']) + "', '" +
            escapedString(pokemonEpisode['japaneseEpisodeTitle']) + "', '" +
            escapedString(pokemonEpisode['japaneseEpisodeTitleTranslated']) + "', '" +
            pokemonEpisode['japaneseBroadcastDate'] + "', '" +
            pokemonEpisode['americanBroadcastDate'] + "')")
        print(sqlStatement)
        db.execute(sqlStatement)
    connection.commit()
    connection.close()

def fillEpisodesSpeciesTable(pokemonEpisodeInfo):
    connection = sqlite3.connect(DATABASE)
    db = connection.cursor()

    for pokemonEpisode in pokemonEpisodeInfo:
        episodeId = pokemonEpisode['id']
        pokemonAppearances = pokemonEpisode['pokemonAppearances']
        for pokemon in pokemonAppearances:
            getPokemonId = "SELECT id FROM species WHERE name='" + escapedString(pokemon) + "'"
            db.execute(getPokemonId)
            connection.commit()
            pokemonId = int(str(db.fetchall().pop()).strip("(),"))
            sqlStatement = ("INSERT INTO episodesSpecies VALUES (" + str(episodeId) + ", " + str(pokemonId) + ")")
            db.execute(sqlStatement)
            print(sqlStatement)
    connection.commit()
    connection.close()
            

def dumpFile(file, listObject):
    with open(file, 'wb') as fp:
        pickle.dump(listObject, fp)

def readFile(file):
    with open(file, 'rb') as fp:
        return pickle.load(fp)

# sendSqlStatement(DROP_SPECIES_TABLE)
# sendSqlStatement(CREATE_SPECIES_TABLE)
# pokemonSpeciesInfo = species.getEverySpeciesInfo()
# fillPokemonSpeciesTable(pokemonSpeciesInfo)
# sendSqlStatement("SELECT name from species")

# sendSqlStatement(DROP_EPISODES_TABLE)
# sendSqlStatement(CREATE_EPISODES_TABLE)
# sendSqlStatement(CLEAR_EPISODES_TABLE_DATA)
# pokemonEpisodeInfo = episode.getEveryEpisodeInfo()
# Since we are dealing with a 1115+ episodes of content, for testing I'll export it so I don't
# have to call this over and over again
# dumpFile("pokemonEpisodeInfo.p", pokemonEpisodeInfo)
# print(savedPokemonEpisodeInfo)
# fillEpisodesTable(savedPokemonEpisodeInfo)
# sendSqlStatement("SELECT * from episodes WHERE episodeNum>= 10")

# sendSqlStatement(CREATE_EPISODES_SPECIES_TABLES)
savedPokemonEpisodeInfo = readFile("pokemonEpisodeInfo.p")
fillEpisodesSpeciesTable(savedPokemonEpisodeInfo)

# sendSqlStatement("SELECT id FROM species WHERE name='Pikachu'")