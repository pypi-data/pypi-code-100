from assignmentcalculatorunimib.op import crea_array, scelta_operatore
from flask import Flask

app = Flask(__name__)


@app.route('/calcolo/<op>/<array11>/<array12>/<array13>/<array21>/<array22>/<array23>')
def hello_world(op, array11, array12, array13, array21, array22, array23): #pylint: disable=too-many-arguments
    # abbiamo evitato il warning da parte di prospector sul numero di parametri massimo da dare a un metodo
    # questo in quanto Flask richiede di inserire tanti parametri quante le variabili della richiesta

    array_1 = crea_array(int(array11), int(array12), int(array13))
    array_2 = crea_array(int(array21), int(array22), int(array23))

    esito, risposta = scelta_operatore(op, array_1, array_2)

    if esito:
        return str(risposta)
    return "errore operatore"


def main():
    app.run(host="0.0.0.0") # nosec
    # comando inserito per evitare il warning da parte di bandit sull'host