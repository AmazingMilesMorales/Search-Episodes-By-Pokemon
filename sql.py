import sqlite3
import pickle 

# Local
import retrieveMediaInfo
import species

# Commands and Constants
CREATE_EPISODES_TABLE = """CREATE TABLE episodes (
            id string,
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

CREATE_EPISODES_SPECIES_TABLE = """CREATE TABLE episodesSpecies (
           episodeId integer,
           pokemonId integer
)"""

DATABASE = "pokemonanime.db"

DROP_EPISODES_TABLE = "DROP TABLE episodes"

DROP_SPECIES_TABLE = "DROP TABLE species"

DROP_EPISODES_SPECIES_TABLE = "DROP TABLE episodesSpecies"

CLEAR_EPISODES_TABLE_DATA = "DELETE FROM episodes"

CLEAR_SPECIES_TABLE_DATA = "DELETE FROM species"

CLEAR_EPISODES_SPECIES_TABLE_DATA = "DELETE FROM episodesSpecies"

def sendSqlStatement(command):
    connection = sqlite3.connect(DATABASE)
    db = connection.cursor()
    db.execute(command)
    connection.commit()
    return db.fetchall()

def escapedString(string):
    return string.translate(str.maketrans({"'":  r"''"}))

def stripSqlResult(string):
    return string.strip("(),[] ")

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
        print("Filling EpisodesTable for " + str(pokemonEpisode['id']))
        sqlStatement = ("INSERT INTO episodes VALUES ('" + 
            str(pokemonEpisode['id']) + "', '" +
            pokemonEpisode['type'] + "', " +
            str(pokemonEpisode['episodeNum']) + ", '" +
            pokemonEpisode['episodeCode'] + "', '" +
            escapedString(pokemonEpisode['englishEpisodeTitle']) + "', '" +
            escapedString(pokemonEpisode['japaneseEpisodeTitle']) + "', '" +
            escapedString(pokemonEpisode['japaneseEpisodeTitleTranslated']) + "', '" +
            pokemonEpisode['japaneseBroadcastDate'] + "', '" +
            pokemonEpisode['americanBroadcastDate'] + "')")
        db.execute(sqlStatement)
    connection.commit()
    connection.close()

def fillEpisodesSpeciesTable(pokemonEpisodeInfo):
    connection = sqlite3.connect(DATABASE)
    db = connection.cursor()

    for pokemonEpisode in pokemonEpisodeInfo:
        episodeId = str(pokemonEpisode['id'])
        print("Filling EpisodesSpeciesTable for " + episodeId)
        pokemonAppearances = pokemonEpisode['pokemonAppearances']
        for pokemon in pokemonAppearances:
            pokemonId = getPokemonIdByName(pokemon)
            sqlStatement = ("INSERT INTO episodesSpecies VALUES ('" + episodeId + "', " + pokemonId + ")")
            db.execute(sqlStatement)
    connection.commit()
    connection.close()

def getPokemonIdByName(pokemon):
    connection = sqlite3.connect(DATABASE)
    db = connection.cursor()    
    getPokemonId = "SELECT id FROM species WHERE name='" + escapedString(pokemon) + "'"
    db.execute(getPokemonId)
    connection.commit()
    return stripSqlResult(str(db.fetchall()))

def getMediaByPokemonId(pokemonId, pokemon):
    connection = sqlite3.connect(DATABASE)
    db = connection.cursor()

    # Get Episodes
    # TODO: Why are there duplicates in the first place? Investigate database. Use Incineroar as test case
    getEpisodes = "SELECT DISTINCT episodeId FROM episodesSpecies WHERE pokemonId='" + pokemonId + "'"
    db.execute(getEpisodes)
    connection.commit()

    episodeIds = db.fetchall()
    for episodeId in episodeIds:
        episodeIdString = stripSqlResult(episodeId[0])
        #episodeNum = stripSqlResult(str(sendSqlStatement("SELECT episodeNum FROM episodes WHERE id=" + episodeIdString + "")))
        episodeTitle = stripSqlResult(str(sendSqlStatement("SELECT englishEpisodeTitle FROM episodes WHERE id='" + episodeIdString + "'")))
        if episodeTitle == "''":
            episodeTitle = stripSqlResult(str(sendSqlStatement("SELECT japaneseEpisodeTitleTranslated FROM episodes WHERE id='" + episodeIdString + "'"))) + " (translated)"
        print(pokemon + " appears in " + episodeIdString + ": " + episodeTitle)
        connection.commit()
    connection.close()

    # TODO: Movies, Side Stories, Origins, Generations, Twilight Wings, Mystery Dungeon, Animated trailers

    print(pokemon + " has appeared in " + str(len(episodeIds)) + " pieces of media!")

def getMediaByPokemonName(pokemon):
    pokemonId = getPokemonIdByName(pokemon)
    getMediaByPokemonId(pokemonId, pokemon)


def dumpFile(file, listObject):
    with open(file, 'wb') as fp:
        pickle.dump(listObject, fp)

def readFile(file):
    with open(file, 'rb') as fp:
        return pickle.load(fp)

def createSpeciesTable():
    sendSqlStatement(DROP_SPECIES_TABLE)
    sendSqlStatement(CREATE_SPECIES_TABLE)
    pokemonSpeciesInfo = species.getEverySpeciesInfo()
    fillPokemonSpeciesTable(pokemonSpeciesInfo)

def createDatabase():
    # Create Species Table
    createSpeciesTable()

    # Create Episodes Table
    sendSqlStatement(DROP_EPISODES_TABLE)
    sendSqlStatement(CREATE_EPISODES_TABLE)
    pokemonMediaInfo = retrieveMediaInfo.getAllMediaInfo()
    # Since we are dealing with a 1115+ episodes of content, just in case
    # any errors happen, I'll dump the file for reuse/testing
    dumpFile("pokemonMediaInfo.p", pokemonMediaInfo)
    fillEpisodesTable(pokemonMediaInfo)

    # Create Species-Episodes Relationship Table
    sendSqlStatement(DROP_EPISODES_SPECIES_TABLE)
    sendSqlStatement(CREATE_EPISODES_SPECIES_TABLE)
    fillEpisodesSpeciesTable(pokemonMediaInfo)

def createDatabaseFromSavedFile(file="pokemonMediaInfo.p"):
    # Create Species Table
    createSpeciesTable()

    # Create Episodes Table
    sendSqlStatement(DROP_EPISODES_TABLE)
    sendSqlStatement(CREATE_EPISODES_TABLE)
    pokemonMediaInfo = readFile(file)
    fillEpisodesTable(pokemonMediaInfo)

    # Create Species-Episodes Relationship Table
    sendSqlStatement(DROP_EPISODES_SPECIES_TABLE)
    sendSqlStatement(CREATE_EPISODES_SPECIES_TABLE)
    fillEpisodesSpeciesTable(pokemonMediaInfo)

def updateDatabaseFromSavedFile(file="pokemonMediaInfo.p"):
    # Create Species Table
    createSpeciesTable()

    # Create Episodes Table
    sendSqlStatement(DROP_EPISODES_TABLE)
    sendSqlStatement(CREATE_EPISODES_TABLE)
    
    # Read file
    pokemonMediaInfo = readFile(file)

    # Add media to table
    # numOfEpisodesSoFar = len(pokemonEpisodesInfo) - 25; # the previous 25 episodes are also run again in case of updates to the episodes wiki page due to upcoming episodes
    # TODO: Above solution no longer works due to more media types being added. Figure out solution so that updating does not take forever in the future.
    #       Additionally, current solution ensures that episodes are always stored first.
    numOfEpisodesSoFar = 1199
    pokemonMediaInfo = pokemonMediaInfo[0:numOfEpisodesSoFar] # cut potentially outdated episode data
    newEpisodesInfo = retrieveMediaInfo.getAllMediaInfo(numOfEpisodesSoFar + 1) # Also gets every nonepisode media
    pokemonMediaInfo = pokemonMediaInfo + newEpisodesInfo

    # Save results to file and table
    dumpFile("pokemonMediaInfo.p", pokemonMediaInfo)
    fillEpisodesTable(pokemonMediaInfo)

    # Create Species-Episodes Relationship Table
    sendSqlStatement(DROP_EPISODES_SPECIES_TABLE)
    sendSqlStatement(CREATE_EPISODES_SPECIES_TABLE)
    fillEpisodesSpeciesTable(pokemonMediaInfo)