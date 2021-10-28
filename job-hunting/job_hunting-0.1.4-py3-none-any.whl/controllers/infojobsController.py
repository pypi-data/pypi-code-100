from jobhunting.Models.Infojobs import Infojobs
from jobhunting.utils.output import output


def searchInfojob(jobTarget, login, password):
    """
    Infojobs automatic subscription job

    :jobTarget: target job to subsscribe
    :login: infojobs user to login
    :password: password to login
    """
    print('Iniciando...')
    jobs = Infojobs()

    try:
        jobs.login(login, password)
        jobs.searchList(jobTarget)
        jobs.searchOptions()
        jobs.getJob()
        jobs.quitSearch()

    except Exception as error:
        output("Algum problema ocorreu e/ou as inforamções estão erradas!")
        output(f"Erro {error}, contate o adminstrador do sistema")
        jobs.quitSearch()

    except KeyboardInterrupt:
        output('Saindo, volte sempre!')
        jobs.quitSearch()

