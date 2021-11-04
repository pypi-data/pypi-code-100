import requests
import threading
import time

url = 'https://pokeapi.co/api/v2/'
endpointPokedex = 'pokedex/1/'
endpointGames = 'generation/'

pokemonList = [] #List to save pokemon names from the pokedex
gamesList = [] #List to save pokemon games names


########## FETCH DATA FUNCTION ##########

def fetchData(url, listName, option, waitTime): #Function parameters --> url: API url, listName: list to append the results, option: type of data to fetch, waitTime: time to wait
    response = requests.get(url).json() #Response from API

    if not response.get('error'): #If everything is correct calling the API
        time.sleep(waitTime) #Wait stablished time

        if not option: #If not option means user want to fetch pokemon name data
            for item in response.get('pokemon_entries'):
                listName.append(item.get('pokemon_species').get('name')) #Apped data to the list
            
            print('\nPokemon names fetched\n') #Alert Pokemon names are fetched

        else: #If option means user want to fetch the game names
            numberOfGenerations = requests.get(url).json().get('count') #Response from API about number of generations

            for generationNumber in range(1, numberOfGenerations + 1):
                games = requests.get(url + str(generationNumber)).json().get('version_groups') #Response from API about games

                for gameName in games:
                    gamesList.append(gameName.get('name')) #Apped data to the list

            print('\nPokemon games fetched\n') #Alert Pokemon games are fetched

    else: #If something goes wrong calling the API
        print('\n' + response.get('error') + ', please try again' + '\n') #Print the error message



########## REQUEST FOR POKEMON NAMES FUNCTION ##########

def pokemonNames():
    print('\nAsking for Pokemon List')
    waitTime = 10 #Set time to wait
    print('\nIt will be available in ' + str(waitTime) + ' seconds approximately')

    threadPokemon = threading.Thread(target=fetchData, args=(url + endpointPokedex, pokemonList, False, waitTime))  #Create a new thread with target fetchData funcion
                                                                                                                    #with arugments: API url with pokedex endpoint,
                                                                                                                    #pokemonList to apped the data, False to indicate
                                                                                                                    #the data to fetch, and waitTime
    threadPokemon.start() #Start thread


########## REQUEST FOR POKEMON GAMES NAMES FUNCTION ##########

def gameNames():
    print('\nAsking for Pokemon Games List')
    waitTime = 5 #Set time to wait
    print('\nIt will be available in ' + str(waitTime) + ' seconds approximately')

    threadGames = threading.Thread(target=fetchData, args=(url + endpointGames, gamesList, True, waitTime)) #Create a newthread with target fetchData funcion
                                                                                                            #with arugments: API url with games endpoint,
                                                                                                            #gamesList to apped the data, True to indicate
                                                                                                            #the data to fetch, and waitTime
    threadGames.start() #Start thread


########## CHECK REQUESTS LISTS FUNCTION ##########

def requestsList():
    print('\nPokemon names: ' + str(pokemonList)) #Print pokemonList
    print('\nPokemon games names: ' + str(gamesList)) #Print gamesList