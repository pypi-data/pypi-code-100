import requests

url = 'https://rickandmortyapi.com/api/'
endpointCharacter = 'character/'

characterList = [] #List to append character info


########## FETCH DATA FUNCTION ##########

def fetchData(url, listName): #Function parameters --> url: API url, listName: list to append the results
    print('Fetching data...\n') #Status control message

    response = requests.get(url).json() #Response from API

    if not response.get('error'): #If everything is correct calling the API
        if response.get('results'): #If 'results' exist means the response from the API is all character's list
            for item in response.get('results'):
                listName.append({ #Apped data to the list
                    'id': item.get('id'),
                    'name': item.get('name'),
                    'status': item.get('status'),
                    'species': item.get('species'),
                    'type': item.get('type'),
                    'gender': item.get('gender'),
                    'origin': item.get('origin').get('name'),
                    'location': item.get('location').get('name')
                })
            
            if response.get('info').get('next'): #As the API respond is paginated, if there is another page
                fetchData(response.get('info').get('next'), listName) #Call fetchData again with new function parameters --> new page url, and same list name to apped the data
        
        else: #If 'results' does not exist means the response from the API is a specific character info
            characterList.append({ #Apped data to the list
                'id': response.get('id'),
                'name': response.get('name'),
                'status': response.get('status'),
                'species': response.get('species'),
                'type': response.get('type'),
                'gender': response.get('gender'),
                'origin': response.get('origin').get('name'),
                'location': response.get('location').get('name')
            })

    else: #If something goes wrong vaalling the API
        print('\n' + response.get('error') + ', please try again' + '\n') #Print the error message


########## LIST ALL CHARACTERS FUNCTION ##########

def listAllCharacters():
    fetchData(url + endpointCharacter, characterList) #Call API fetchData with --> API url with characters endpoint, and characterList to apped the data
    
    return characterList


########## SHOW CHARACTER INFO FUNCTION ##########

def showCharacterInfo(id):
    fetchData(url + endpointCharacter + id, characterList) #Call API fetchData with --> API url with the character id, and characterList to apped the data

    return characterList