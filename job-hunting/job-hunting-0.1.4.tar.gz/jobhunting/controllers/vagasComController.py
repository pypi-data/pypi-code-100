from time import sleep

from jobhunting.Models.vagasCom import VagasCom
from jobhunting.utils.output import output


def searchVagasCom(targetJob, login, password):
    vagas = VagasCom()
    try:
        vagas.login(login, password)
        vagas.insertJob(targetJob)
        vagas.searchOptions()
        vagas.selectJobs()
        vagas.subscribeJob()
        vagas.quitSearch()

    except Exception as error:
        output("Algum problema ocorreu e/ou as informações estão erradas!")
        vagas.quitSearch()

    except KeyboardInterrupt:
        output('Saindo, volte sempre!')
        vagas.quitSearch()
        
