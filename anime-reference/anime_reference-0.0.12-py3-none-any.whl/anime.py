from typing import Optional, List
import importlib
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).parent.resolve()}\\anime_objects\\")
try:
    from anime_reference.anime_objects.constants import titles_classes, titles_links
except:
    from anime_objects.constants import titles_classes, titles_links
import constants

def get_summary(title: str, name: str, movie = False) -> Optional[str]:
    """
    Description: Gets the summary of a given anime episode.

        Parameters:
        -----------
        title (str): anime title
        epsisode_name (str): anime episode name

        Returns:
        --------
        str: summary of anime episode
    """
    if movie:
        title_lower = title.lower()
        anime = anime_object(title_lower)
        try:
            return anime.movie_summary(name)
        except AttributeError:
            return None
    title_lower = title.lower()
    anime = anime_object(title_lower)
    try:
        return anime.episode_summary(name)
    except AttributeError:
        return None
    
def get_episodes(title: str) -> Optional[int]:
    """
    Description: Gets the number of episodes for a given anime title.

        Parameters:
        -----------
        title (str): anime title

        Returns:
        --------
        int: Number of episodes
    """
    title = title.lower()
    anime = anime_object(title)
    try:
        return anime.episode_names
    except AttributeError:
        return None

def get_movies(title: str) -> Optional[List[str]]:
    """
    Description: Gets all episode names of a given anime title.

        Parameters:
        -----------
        title (str): anime title

        Returns:
        --------
        List[str]: List of all anime movie names
    """
    title = title.lower()
    anime = anime_object(title)
    try:
        return anime.movie_names
    except AttributeError:
        return None

def get_anime_titles() -> Optional[List[str]]:
    """
    Description: Gets all anime titles currently supported.

        Parameters:
        -----------
        None
        
        Returns:
        --------
        List[str]: List of all anime titles currently supported
    """
    return titles

def anime_object(title: str):
    """
    Description: Converts the anime title into the correct
                 anime-reference anime object

        Parameters:
        -----------
        title (str): anime title
        
        Returns:
        --------
        Optional[]: List of all anime titles currently supported
    """
    if title in titles_classes.keys():
        try:
            import_statement = "anime_reference.anime_objects."+titles_classes[title]
        except:
            import_statement = "anime_objects."+titles_classes[title]
        module = importlib.import_module(import_statement)
        class_ = getattr(module, titles_classes[title])
        instance = class_(title)
        return instance
    else:
        print(f"Title {title} is not a valid title.")
        return None
    
if __name__ == "__main__":
    print(get_summary("naruto shippuden", 'Naruto and Hinata'))
    print(get_movies("naruto shippuden"))
