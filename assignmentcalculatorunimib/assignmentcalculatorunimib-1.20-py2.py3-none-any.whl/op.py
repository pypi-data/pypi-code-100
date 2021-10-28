import numpy as np
import pymongo
from assignmentcalculatorunimib.calculator import somma, sottrazione

# creazione del client di mongo
# è presente un try catch in quanto se non trova mongo in localhost allora ciò significa
# che si trova sulla pipeline e perciò deve usare l'indirizzo mongodb

try:
    client = pymongo.MongoClient('localhost', 27017)
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError:
    client = pymongo.MongoClient('mongodb', 27017)

proc_svil = client['proc_svil']
assignment_1 = proc_svil['first']

# somma/sottrae i vettori e salva i valori su mongo
def scelta_operatore(operatore, array_1, array_2):
    if operatore == "somma":
        return True, save_to_mongo(somma(array_1, array_2))
    if operatore == "sottrazione":
        return True, save_to_mongo(sottrazione(array_1, array_2))
    return False, -1


def crea_array(value_1, value_2, value_3):
    return np.array([value_1, value_2, value_3])

# funzione che si occupa di salvare i valori su mongo
def save_to_mongo(array):
    assignment_1.insert_one({
        'element': array.tolist()
    })
    return array
