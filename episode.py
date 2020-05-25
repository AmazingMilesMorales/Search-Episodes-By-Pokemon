import urllib.request

# Headers used for every API request
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

def getEpisodeInfo(episodeNum):
    print(episodeNum)
    try:
        # Get wikitext of each episode
        url = 'https://bulbapedia.bulbagarden.net/w/api.php?action=parse&format=php&page=EP' + str(episodeNum) + '&redirects=1&prop=wikitext'
        # There is one URL page that does not lead to the expected page, so I handled this one time error here:       
        if episodeNum == 375:
            url = 'https://bulbapedia.bulbagarden.net/w/api.php?action=parse&format=php&page=AG101&redirects=1&prop=wikitext'
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        episodePageText = str(resp.read().decode('UTF-8'))
        

        # Page does not exist
        if episodePageText.startswith("a:1:{s:5:\"error\""):
           return -1

        englishEpisodeTitle = getEnglishEpisodeTitleFromEpisodePageText(episodePageText)
        pokemonAppearances = getPokemonAppearancesFromEpisodePageText(episodePageText)

        return {
            "episodeNum": episodeNum,
            "englishEpisodeTitle": englishEpisodeTitle,
            "pokemonAppearances": pokemonAppearances,
            }

    except Exception as e:
        print(str(e))
        return -1

def getPokemonAppearancesFromEpisodePageText(episodePageText):
    pokemon = []
    pokemonSection = episodePageText.split("===Pokémon===")[1].split("==")[0].splitlines()
    for line in pokemonSection:
        if line.startswith("* {{p|"):
            pokemon.append(line.split("* {{p|")[1].split("}}")[0])

    # Remove duplicates before returning (such as multiple Pikachus in one episode)
    return list(dict.fromkeys(pokemon))

def getEnglishEpisodeTitleFromEpisodePageText(episodePageText):
    englishTitle = episodePageText.split("title_en=")[1].split("|")[0]
    return englishTitle.strip()


def getEveryEpisodeInfo():
    pokemonEpisodesInfo = []
    episodeNum = 1
    while True:
        episodeInfo = getEpisodeInfo(episodeNum)
        if(episodeInfo != -1):
            pokemonEpisodesInfo.append(episodeInfo)
            episodeNum = episodeNum + 1
        else:
            break
    return getEveryEpisodeInfo