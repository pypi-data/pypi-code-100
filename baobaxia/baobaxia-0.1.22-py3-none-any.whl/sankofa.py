from datetime import datetime
from typing import Optional

from .saberes import Mocambola, Saber, SaberesConfig, SaberesDataset

from datalad.api import Dataset, create
from datalad.config import ConfigManager

from pathlib import Path

from datetime import datetime

import glob, os, subprocess
import shutil

    
class SankofaInfo():
    """Context manager for setting commit info on datalad operations that use it."""

    def __init__(self, balaio, name=None, email=None, where='local'):
        self.config_manager = ConfigManager(balaio)
        self.email = email if email else 'exu@mocambos.net'
        self.name = name if name else 'exu'
        self.where = where

    def __enter__(self):
        self.config_manager.set('user.email', self.email, self.where)
        self.config_manager.set('user.name', self.name, self.where)

    def __exit__(self, exception_type, exception_value, traceback):
        self.config_manager.set('user.email', 'exu@mocambos.net', self.where)
        self.config_manager.set('user.name', 'exu', self.where)


class Sankofa():

    @staticmethod
    def _prepare_paths(saberes: [Saber], config: SaberesConfig):
        #print(repr(saberes))
        sankofa_data = {}
        balaios = {b.balaio for b in saberes if not b.balaio is None}
        for balaio in balaios:
            saberes_paths = []
            for saber in saberes:
                #print("Saber: ")
                #print(repr(saber))
                if saber.balaio == balaio:
                    if saber.mucua is None:
                        saberpath = saber.path 
                    else:
                        saberpath = saber.mucua / saber.path
                    saberes_paths.append(saberpath)
                    saberes_paths.append(saberpath / config.saber_file_ext)
                    for content_path in saber.content:
                        saberes_paths.append(saberpath / content_path)
            sankofa_data[balaio] = saberes_paths
        return sankofa_data
    
    @classmethod
    def create_balaio(cls, *, balaio: str, description: str,
                      config: SaberesConfig):
        balaio_path = Path(balaio)
        balaio_fullpath = config.data_path / balaio_path 
        dataset = create(path=balaio_fullpath,
                         force=True,
                         annex=True,
                         cfg_proc='text2git',
                         description=description)
        dataset.save()

    @classmethod
    def destroy_balaio(cls, balaio: str, config: SaberesConfig):
        shutil.rmtree(config.data_path / balaio)

    # Metodos para atualizar os dados da Mucua, rotas, ssh e territorios

    @classmethod
    def mucua_remote_add(cls, *, balaio_slug: str, mucua_slug: str, uri: str,
                         config: SaberesConfig):
        repopath = Path(config.data_path)
        balaiopath = repopath / balaio_slug

        cmd = 'git remote add ' + mucua_slug + ' ' + uri
        pipe = subprocess.Popen(cmd, shell=True, cwd=balaiopath)
        pipe.wait()

    @classmethod    
    def mucua_remote_get(cls, *, balaio_slug: str, config: SaberesConfig):
        repopath = Path(config.data_path)
        balaiopath = repopath / balaio_slug
        cmd = 'git remote -v'
        pipe = subprocess.Popen(cmd, shell=True, 
                                cwd=balaiopath, 
                                stdout=subprocess.PIPE)
        output, error = pipe.communicate()
        
        mucuas = []
        # Match repositories.
        if output:
            for line in output.splitlines():
                mucuas.append(line.split(None, 1)[1].split()[0].decode("utf-8"))
        return list(set(mucuas))

    @classmethod
    def mucua_remote_del(cls, *, balaio_slug: str, mucua_slug: str,
                            config: SaberesConfig):
        repopath = Path(config.data_path)
        balaiopath = repopath / balaio_slug
        cmd = 'git remote rm ' + mucua_slug 
        pipe = subprocess.Popen(cmd, shell=True, cwd=balaiopath)
        pipe.wait()
    
    @classmethod
    def mucua_group_add(cls, *, balaio_slug: str, mucua_slug: str,
                        group: str, config: SaberesConfig):
        repopath = Path(config.data_path)
        balaiopath = repopath / balaio_slug
        cmd = 'git annex group ' + mucua_slug + ' ' + group
        pipe = subprocess.Popen(cmd, shell=True, cwd=balaiopath,
                                stdout=subprocess.PIPE)
        output, error = pipe.communicate()

    @classmethod
    def mucua_group_del(cls, *, balaio_slug: str, mucua_slug: str,
                        group: str, config: SaberesConfig):
        repopath = Path(config.data_path)
        balaiopath = repopath / balaio_slug
        cmd = 'git annex ungroup ' + mucua_slug + ' ' + group
        pipe = subprocess.Popen(cmd, shell=True, cwd=balaiopath,
                                stdout=subprocess.PIPE)
        output, error = pipe.communicate()

    @classmethod
    def mucua_group_list(cls, *, balaio_slug: str, mucua_slug: str = None,
                         config: SaberesConfig):
        if mucua_slug == None:
            mucua_slug = config.mucua_slug

        repopath = Path(config.data_path)
        balaiopath = repopath / balaio_slug
        cmd = 'git annex group ' + mucua_slug
        pipe = subprocess.Popen(cmd, shell=True, cwd=balaiopath,
                                stdout=subprocess.PIPE)
        output, error = pipe.communicate()
        if output != '':
            return output.decode("utf-8").split()
        else:
            return []

    @classmethod
    def add(cls, *,
            saberes: [Saber], mocambola: Mocambola,
            config: SaberesConfig):

        sankofa_data = Sankofa._prepare_paths(saberes, config)

        for balaio, saberes_paths in sankofa_data.items():
            repopath = config.data_path
            balaiopath = repopath / balaio
            dataset = Dataset(balaiopath)
            
            with SankofaInfo(balaio=dataset,
                             name=mocambola.username,
                             email=mocambola.email):
                dataset.save(path=saberes_paths)
                
    @classmethod
    def remove(cls, *,
            saberes: [Saber], mocambola: Mocambola,
            config: SaberesConfig, local_only=False):
        """
        Remove os files associados aos saberes de forma permanente em todas
        as mucuas (se local_only=False (padrão)) ou apenas localmente (se
        local_only=True).

        """
        for saber in saberes:
            repopath = config.data_path
            balaiopath = repopath / saber.balaio
            dataset = Dataset(balaiopath)
            
            if saber.mucua is None:
                saber_path = Path(saber.path)
            else:
                saber_path = Path(saber.mucua) / saber.path
            saber_fullpath = balaiopath / saber_path

            with SankofaInfo(balaio=dataset,
                             name=mocambola.username,
                             email=mocambola.email):
                try:
                    if local_only:
                        dataset.drop(path=saber_path,
                            recursive=True,
                            check=False)
                    else:
                        dataset.remove(path=saber_path,
                            recursive=True,
                            check=False)
                except:
                    # Caso o arquivo não esteja no git (TODO especializar except)
                    if saber_fullpath.exists() and saber_fullpath.is_dir():
                        shutil.rmtree(saber_fullpath)
                    else:
                        print('Sankofa.remove (not found): '+str(saber_fullpath))

    @classmethod
    def sync(cls, *, balaio_slug: Optional[str] = None,
             mucua_slug: Optional[str] = None,
             config: SaberesConfig, **kwargs):
        """
        Sincroniza com outra mucua. 
        """
        
        repopath = config.data_path
        balaiopath = repopath / balaio_slug
        dataset = Dataset(balaiopath)
        
        with SankofaInfo(balaio=dataset):
            dataset.update(**kwargs)       
