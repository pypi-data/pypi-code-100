from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional, Dict, List, Tuple
try:
    from anime_reference.anime_objects.constants import *
    from anime_reference.anime_objects.utils import clean_str_list, format_episode_links, clean_text
except:
    from constants import *
    from utils import clean_str_list, format_episode_links
    
class Anime:
    """
    A class to represent a Naruto anime title.
    ...

    Attributes
    ----------
    title : str
        title of the anime

    Methods
    -------
    _check_title():
        Checks if the title is valid.

    _check_episode_name(episode_name):
        Checks if the episode name is valid

    _get_link():
        Gets the link of episodes associated with the anime title

    dataframe():
        Gets a lsit of dataframesassociated w/ movies and episodes of anime

    episode_names():
        Gets a list of episode names

    movie_names():
        Gets a list of movie names
    """    
    def __init__(self, title):
        self.title = title
        self._check_title()
        return None

    def _check_title(self) -> None:
        if self.title not in titles_links.keys():
            print(f"Anime \"{self.title}\" is not a valid anime title.")
            # TODO: Add a helper function that asks "Did you mean (title)?"
            return None
    
    @property    
    def get_link(self) -> str:
        return titles_links[self.title] # link for the all epsiodes, movies of the different naruto titles

    @property
    def dataframe(self) -> List[pd.DataFrame]:
        link = self.get_link
        try:
            return pd.read_html(link)
        except:
            return None
        
    @property
    def episode_names(self) -> List[str]:
        try:
            return clean_str_list(list(self.dataframe[0].iloc[:,1]))
        except:
            return None
    @property
    def movie_names(self) -> List[str]:
        try:
            return clean_str_list(list(self.dataframe[1].iloc[:,1]))
        except:
            return None

if __name__ == "__main__":
    x = Anime("naruto")
    print(x.episode_names)
