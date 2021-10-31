__version__ = '0.0.1'

#################################################
# Imports #######################################
#################################################

import pandas as pd
from re import finditer
from io import StringIO
from contextlib import suppress
from typing import Dict, List, Tuple
from requests_html import HTMLSession, HTMLResponse

#################################################
# Class #########################################
#################################################

class Exporter:

    #############################################
    # Dunder ####################################
    #############################################

    def __init__(self) -> None:
        self.session = HTMLSession()
        self.doi_url = 'https://doi.org/'
        self.who_url = 'https://search.bvsalud.org/'+\
            'global-literature-on-novel-coronavirus-2019-ncov/'  # https://search.bvsalud.org/global-literature-on-novel-coronavirus-2019-ncov/?q=entry_date%3A%28%5B20210913+TO+20220101%5D%29

    #############################################
    # Requests ##################################
    #############################################

    def req(self,
            **kwargs) -> HTMLResponse:
        
        return self.session.get(
            self.who_url,
            params=self.gen_params(**kwargs))

    #############################################
    # Getters ###################################
    #############################################

    def get_content(self,
            **kwargs) -> str:
        
        return self.req(
            **kwargs).content.decode('utf-8')

    #############################################

    def get_df(self,
            date_interval: Tuple[int, int],
            count: int = -1) -> pd.DataFrame:
        
        return pd.concat([
            self.format_table(
                self.get_content(
                    output='csv',
                    count=count,
                    q=self.gen_q_date(*interval))
            ) for interval in self.calc_date_intervals(
                date_interval)]
        ).reset_index(drop=True)

    #############################################
    # Formatters ################################
    #############################################
    
    def format_table(self,
            content: str) -> pd.DataFrame:
        
        rows = content.split('\n\"')
        print(self.format_row(rows[1]))
        return pd.read_csv(StringIO('\n'.join(
            [','.join([col.strip()
                for col in rows[0].split(',')])] + \
            [self.format_row(row)
                for row in rows[1:]])))

    #############################################

    def format_row(self,
            row: str) -> pd.DataFrame:
        
        row = '\"' + row.strip()
        begin_pos, end_pos = self.find_abstract_pos(row)
        return ','.join([f'\"{col}\"'.strip()
            for col in (
                self.format_first_cols(row, begin_pos) + \
                self.format_abstract(row, begin_pos, end_pos) + \
                row[end_pos:].split(',')[:5])])

    #############################################

    def format_first_cols(self,
            row: str,
            begin_pos: int) -> List[str]:
        
        first_cols = [col.replace('\"', '\'')
            for col in row[0:begin_pos-2].split('\",\"')]
        first_cols[0] = first_cols[0][1:] if (
            first_cols[0][0] == "'") else first_cols[0]
        first_cols[-1] = first_cols[-1][:-2] if (
            first_cols[-1][-1] == "'") else first_cols[-1]
        return first_cols

    #############################################

    def format_abstract(self,
            row: str,
            begin_pos: int,
            end_pos: int) -> List[str]:
        
        abstract = [
            row[begin_pos:end_pos-2].replace('\"', '\'')]
        abstract[0] = "" if (
            abstract[0] == "") else (
                abstract[0][1:] if (
                    abstract[0][0] == "'") else abstract[0])
        return abstract

    #############################################

    def find_abstract_pos(self,
            row: str) -> Tuple[int, int]:
        
        with suppress(IndexError):
            return (
                [m for m in finditer(
                    r'","', row)][11].span()[1],
                [m for m in finditer(
                    r'.",[0-9]', row)][0].span()[1]-1)

    #############################################
    # Calculators ###############################
    #############################################     

    def calc_date_intervals(self,
            date_interval) -> Tuple[int, int]:
        
        return [date_interval]

    #############################################
    # Generators ################################
    #############################################

    def gen_params(self,
            **kwargs) -> Dict[str, str]:
        
        return kwargs
    
    #############################################

    def gen_q_date(self,
            from_date: int,
            to_date: int) -> str:
        
        return f'entry_date:([{from_date} TO {to_date}])'
    
    #############################################
    # Helpers ###################################
    #############################################

    def help(self,
            how: str = '') -> None:
        
        {
            '': self.help_basic,
            'params': self.help_params,
        }[how]()
    
    #############################################

    def help_basic(self) -> None:
        print('Infos:')

    #############################################

    def help_params(self) -> None:
        print(f"output -> possible values: 'site', 'csv', 'ris', 'citation'")
        # 'output': ['site', 'csv', 'ris', 'citation'][1],
        # 'count': -1,
        # 'q': f'entry_date:([{from_date} TO {to_date}])'}
