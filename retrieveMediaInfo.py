import urllib.request
import sys

# Headers used for every API request
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

# NOTE: For the purposes of data storage, every piece of animated media (including movies and shorts) is stored as an "episode"

def getLongMediaTypeString(mediaType):
    if mediaType == 'EP': return 'episode'
    elif mediaType == 'M': return 'movie'

def getMediaInfo(episodeNum, mediaType):
    try:
        # Get wikitext of each episode
        url = 'https://bulbapedia.bulbagarden.net/w/api.php?action=parse&format=php&page=' + mediaType + str(episodeNum) + '&redirects=1&prop=wikitext'
        # There is one URL page that does not lead to the expected page, so I handled this one time error here:       
        if mediaType == 'EP' and episodeNum == 375:
            url = 'https://bulbapedia.bulbagarden.net/w/api.php?action=parse&format=php&page=AG101&redirects=1&prop=wikitext'
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        episodePageText = str(resp.read().decode('UTF-8'))
        

        # Page does not exist
        if episodePageText.startswith("a:1:{s:5:\"error\""):
            longMediaType = getLongMediaTypeString(mediaType)
            print("Error getting " + longMediaType + " number " + str(episodeNum) + ". Stopping the search for " + longMediaType + "s here.")
            return -1

        # Some media types do not have applicable data or have different wording to get information
        # TODO: There is probably a cleaner way of doing this
        if mediaType == 'M':
            episodeCode = mediaType + str(episodeNum)
            englishEpisodeTitle = getInfoFromEpisodePageText(episodePageText, "entitle")
            japaneseEpisodeTitle = getInfoFromEpisodePageText(episodePageText, "jatitle")
            japaneseEpisodeTitleTranslated = getInfoFromEpisodePageText(episodePageText, "rotitle")
            japaneseBroadcastDate = getInfoFromEpisodePageText(episodePageText, "jpprem")
            americanBroadcastDate = getInfoFromEpisodePageText(episodePageText, "usprem")
        else:
            episodeCode = getInfoFromEpisodePageText(episodePageText, "epcode")
            englishEpisodeTitle = getInfoFromEpisodePageText(episodePageText, "title_en")
            japaneseEpisodeTitle = getInfoFromEpisodePageText(episodePageText, "title_ja")
            japaneseEpisodeTitleTranslated = getInfoFromEpisodePageText(episodePageText, "title_ja_trans")
            japaneseBroadcastDate = getInfoFromEpisodePageText(episodePageText, "broadcast_jp")
            americanBroadcastDate = getInfoFromEpisodePageText(episodePageText, "broadcast_us")

        # Applicable to all
        id = mediaType + str(episodeNum)
        pokemonAppearances = getPokemonAppearancesFromEpisodePageText(episodePageText)

        return {
            "id": id,
            "type": "main_anime",
            "episodeNum": episodeNum,
            "episodeCode": episodeCode,          
            "englishEpisodeTitle": englishEpisodeTitle,
            "japaneseEpisodeTitle": japaneseEpisodeTitle,
            "japaneseEpisodeTitleTranslated": japaneseEpisodeTitleTranslated,
            "japaneseBroadcastDate": japaneseBroadcastDate,
            "americanBroadcastDate": americanBroadcastDate,
            "pokemonAppearances": pokemonAppearances,
            }

    except Exception as e:
        print(str(e))
        return -503


def getPokemonAppearancesFromEpisodePageText(episodePageText):
    pokemon = []
    pokemonSection = []
    if "===Pokémon===" in episodePageText:
        pokemonSection = episodePageText.split("===Pokémon===")[1].split("==")[0].splitlines()
    elif "=== Pokémon ===" in episodePageText:
        pokemonSection = episodePageText.split("=== Pokémon ===")[1].split("==")[0].splitlines()
    else:
        raise Exception('Pokémon section not found on page')

    for line in pokemonSection:
        if line.startswith("* {{p|"):
            pokemon.append(line.split("* {{p|")[1].split("}}")[0])

    # Remove duplicates before returning (such as multiple Pikachus in one episode)
    # return list(dict.fromkeys(pokemon))
    return pokemon

def getInfoFromEpisodePageText(episodePageText, string):
    try:
        info = episodePageText.split(string+"=")[1].split("|")[0]
        # Sometimes instead of actual info, the wikitext will contain a warning to not put bad information
        if "<!--" in info:
            return ''
    # Sometimes, info is not on the page. For example: no English titles for Japanese-only episodes.
    except Exception as e:
        return ''
    return info.strip()


def getEveryMainAnimeEpisodeInfo(episodeNum=1):
    pokemonEpisodesInfo = []
    while True:
        episodeInfo = getMediaInfo(episodeNum, 'EP')
        if episodeInfo == -1: break
        if episodeInfo == -503:
            print("An error occured while fetching episodes. Please try again.")
            exit()
        if episodeInfo != -1:
            pokemonEpisodesInfo.append(episodeInfo)
            print("Getting episode info from Bulbapedia API for Episode " + str(episodeNum))
            episodeNum = episodeNum + 1
        else:
            break
    return pokemonEpisodesInfo

def getEveryMovieInfo(movieNum=1):
    pokemonMoviesInfo = []
    while True:
        movieInfo = getMediaInfo(movieNum, 'M')
        if movieInfo == -1: break
        if movieInfo == -503:
            print("An error occured while fetching episodes. Please try again.")
            exit()
        if movieInfo != -1:
            pokemonMoviesInfo.append(movieInfo)
            print("Getting movie info from Bulbapedia API for Movie " + str(movieNum))
            movieNum = movieNum + 1
        else:
            break
    return pokemonMoviesInfo

def getAllMediaInfo(startingEpisodeNum=1):
    allMediaInfo = []
    # TODO: Side Stories, Origins, Generations, Twilight Wings, Mystery Dungeon, Animated trailers
    mediaTypes = ['EP', 'M']
    for mediaType in mediaTypes:
        longMediaType = getLongMediaTypeString(mediaType)

        # Get starting media num for iteration
        if mediaType == 'EP': mediaNum = startingEpisodeNum
        else: mediaNum = 1

        while True:
            mediaInfo = getMediaInfo(mediaNum, mediaType)
            if mediaInfo == -1: break
            if mediaInfo == -503:
                print("An error occured while fetching episodes. Please try again.")
                exit()
            if mediaInfo != -1:
                allMediaInfo.append(mediaInfo)
                print("Obtained info from Bulbapedia API for " + longMediaType.capitalize() + " " + str(mediaNum))
                mediaNum = mediaNum + 1
            else:
                break

    return allMediaInfo