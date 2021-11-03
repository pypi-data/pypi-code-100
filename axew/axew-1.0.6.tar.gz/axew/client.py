from typing import Dict

import aiohttp
import requests

from axew import (
    InvalidParams,
    Entry,
    BASE_URL,
    EntryNotFound,
    MAX_SIZE,
    ValidationError,
    Profile,
)


class AxewClient:
    def __init__(self):
        self.cache: Dict[str, Entry] = {}

    @staticmethod
    def create_entry(data: Dict) -> Entry:
        return Entry(
            name=data["name"],
            slug=data["slug"],
            code=data["code"],
            error=data["error"],
            language=data["language"],
            created_at=data["created_at"],
            description=data["description"],
            times_viewed=data["times_viewed"],
            absolute_url=data["absolute_url"],
            last_modified=data["last_modified"],
        )

    @staticmethod
    def create_profile(data: Dict) -> Profile:
        return Profile(
            user=data["user"],
            slug=data["slug"],
            entry_set=data["entry_set"],
            times_viewed=data["times_viewed"],
        )

    def create_paste(
        self,
        *,
        code: str = "",
        error: str = "",
        name: str = "",
        description: str = "",
    ) -> Entry:
        """Creates a new paste

        Parameters
        ----------
        code : str, optional
            The code portion of the paste
        error : str, optional
            The error portion of the paste
        name : str, optional
            What to name this entry
        description : str, optional
            A short description of this entry

        Returns
        -------
        Entry
            The created entry

        Raises
        ------
        InvalidParams
            Invalid provided arguments
        ValidationError
            The given arguments were too long
        """
        if not code and not error:
            raise InvalidParams

        if name and len(name) > MAX_SIZE["name"]:
            raise ValidationError(name, MAX_SIZE["name"])

        if description and len(description) > MAX_SIZE["description"]:
            raise ValidationError(description, MAX_SIZE["description"])

        if code and len(code) > MAX_SIZE["code"]:
            raise ValidationError(code, MAX_SIZE["code"])

        if error and len(error) > MAX_SIZE["error"]:
            raise ValidationError(error, MAX_SIZE["error"])

        data = {"code": code, "error": error, "name": name, "description": description}

        r = requests.post(f"{BASE_URL}/api/entry/create/", json=data)
        return_data = r.json()
        entry = self.create_entry(return_data)
        self.cache[entry.slug] = entry

        return entry

    def get_paste(self, slug: str) -> Entry:
        """Returns the given Entry for a slug

        Parameters
        ----------
        slug : str
            The slug for the entry you wish to fetch

        Returns
        -------
        Entry
            The entry for said slug

        Raises
        ------
        EntryNotFound
            Couldn't find an entry with that slug
        """
        if slug in self.cache:
            return self.cache[slug]

        r = requests.get(f"{BASE_URL}/api/entry/get/{slug}/")
        if r.status_code != 200:
            raise EntryNotFound

        return_data = r.json()
        entry: Entry = self.create_entry(return_data)
        return entry

    async def async_create_paste(
        self,
        *,
        code: str = "",
        error: str = "",
        name: str = "",
        description: str = "",
    ) -> Entry:
        """Creates a new paste asynchronously

        Parameters
        ----------
        code : str, optional
            The code portion of the paste
        error : str, optional
            The error portion of the paste
        name : str, optional
            What to name this entry
        description : str, optional
            A short description of this entry

        Returns
        -------
        Entry
            The created entry

        Raises
        ------
        InvalidParams
            Invalid provided arguments
        ValidationError
            The given arguments were too long
        """
        if not code and not error:
            raise InvalidParams

        if name and len(name) > MAX_SIZE["name"]:
            raise ValidationError(name, MAX_SIZE["name"])

        if description and len(description) > MAX_SIZE["description"]:
            raise ValidationError(description, MAX_SIZE["description"])

        if code and len(code) > MAX_SIZE["code"]:
            raise ValidationError(code, MAX_SIZE["code"])

        if error and len(error) > MAX_SIZE["error"]:
            raise ValidationError(error, MAX_SIZE["error"])

        data = {"code": code, "error": error, "name": name, "description": description}

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            async with session.post(
                f"{BASE_URL}/api/entry/create/", json=data
            ) as response:
                return_data = await response.json()
                entry = self.create_entry(return_data)
                self.cache[entry.slug] = entry

        return entry

    async def async_get_paste(self, slug: str) -> Entry:
        """Returns the given Entry for a slug asynchronously

        Parameters
        ----------
        slug : str
            The slug for the entry you wish to fetch

        Returns
        -------
        Entry
            The entry for said slug

        Raises
        ------
        EntryNotFound
            Couldn't find an entry with that slug
        """
        if slug in self.cache:
            return self.cache[slug]

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            async with session.get(f"{BASE_URL}/api/entry/get/{slug}/") as r:
                if r.status != 200:
                    raise EntryNotFound

                return_data = await r.json()
                entry: Entry = self.create_entry(return_data)
        return entry

    def get_profile(self, slug: str) -> Profile:
        """
        Gets a profile for the given slug

        Parameters
        ----------
        slug : str
            The slug for the profile to find
        """
        r = requests.get(f"{BASE_URL}/api/profile/get/{slug}/")
        if r.status_code != 200:
            raise EntryNotFound

        return_data = r.json()
        profile: Profile = self.create_profile(return_data)
        return profile
