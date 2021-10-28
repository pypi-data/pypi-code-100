import swcli.settings
import swcli.utils
from swcli.models import Film
from httpx import get


class GetFilm():
    def get_film_by_id(film_id):
        """
        Return a one or many movies on Star Wars trilogies by ID.
        """
        response = get(
            swcli.settings.BASE_URL +
            swcli.settings.FILMS +
            str(film_id))

        if response.status_code != 200:
            raise SystemExit('Resource does not exist!')

        json_data = response.json()

        film_response = {
            "title": json_data['title'],
            "episode": json_data['episode_id'],
            "director": json_data['director'],
            "producer": json_data['producer'],
            "release_date": json_data['release_date'],
            "species": swcli.utils.get_resources_dict(
                json_data['species'],
                'name'),
            "starships": swcli.utils.get_resources_dict(
                json_data['starships'],
                'name'),
            "vehicles": swcli.utils.get_resources_dict(
                json_data['vehicles'],
                'name'),
            "characters": swcli.utils.get_resources_dict(
                json_data['characters'],
                'name'),
            "planets": swcli.utils.get_resources_dict(
                json_data['planets'],
                'name'),
        }
        film = Film(**film_response)
        yield film.json(ensure_ascii=False, encoder='utf-8')

    def get_film_by_title(title):
        """
        Return a one or many movies on Star Wars trilogies by Title.
        """
        json_data = get(
            swcli.settings.BASE_URL +
            swcli.settings.FILMS +
            swcli.settings.SEARCH +
            title).json()

        if not json_data['results']:
            raise SystemExit('Resource does not exist!')

        for json_dict in json_data['results']:
            film_response = {
                "title": json_dict['title'],
                "episode": json_dict['episode_id'],
                "director": json_dict['director'],
                "producer": json_dict['producer'],
                "release_date": json_dict['release_date'],
                "species": swcli.utils.get_resources_dict(
                    json_dict['species'],
                    'name'),
                "starships": swcli.utils.get_resources_dict(
                    json_dict['starships'],
                    'name'),
                "vehicles": swcli.utils.get_resources_dict(
                    json_dict['vehicles'],
                    'name'),
                "characters": swcli.utils.get_resources_dict(
                    json_dict['characters'],
                    'name'),
                "planets": swcli.utils.get_resources_dict(
                    json_dict['planets'],
                    'name'),
            }

            film = Film(**film_response)
            yield film.json(ensure_ascii=False, encoder='utf-8')
