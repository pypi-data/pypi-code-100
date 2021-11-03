import typing as t

from .base import BaseAPI


class Sonarr(BaseAPI):
    """API wrapper for Sonarr."""

    # GET /series
    async def get_series(self) -> list[dict[str, t.Any]]:
        """Gets all series

        Returns:
            List of series
        """
        response = await self._client.get("/series")
        return response.json()

    # GET /series/{id}
    async def get_series_by_id(self, id_: int) -> dict[str, t.Any]:
        """Get a series by ID

        Args:
            id_: Series ID

        Returns:
            The series
        """
        response = await self._client.get(f"/series/{id_}")
        return response.json()

    # POST /series
    async def add_series(
        self,
        series: dict[str, t.Any],
        monitored: bool = True,
        search: bool = True,
        use_season_folders: bool = True,
        **kwargs: str | int,
    ) -> dict[str, t.Any]:
        """Add a series to sonarr

        Args:
            series: series data as obtained from other methods
            monitored: monitor show
            search: Search for missing episodes
        """

        series_json = {
            "tvdbID": series["tvdbId"],
            "title": series["title"],
            "rootFolderPath": self.root_folder,
            "qualityProfileId": self.quality_profile,
            "languageProfileId": 1,
            "monitored": monitored,
            "seasonFolder": use_season_folders,
            "addOptions": {
                "ignoreEpisodesWithFiles": False,
                "ignoreEpisodesWithoutFiles": False,
                "searchForMissingEpisodes": search,
            },
        }

        series_json.update(kwargs)

        response = await self._client.post("/series", json=series_json)  # type: ignore
        return response.json()

    # PUT /series
    async def update_series(self, series: dict[str, t.Any]) -> dict[str, t.Any]:
        """Update a series in the database.

        Args:
            series: The series to update.

        Returns:
            The updated series.
        """
        response = await self._client.put("/series", json=series)
        return response.json()

    # GET /series/lookup
    async def lookup_series(
        self, term: str, year: int | None = None
    ) -> list[dict[str, t.Any]]:
        """Search for a series to add to the database (Uses TVDB for search results)

        Args:
            term: Search for this series.
            year: Add this year to the search

        Returns:
            List of the search results
        """
        if year:
            term = f"{term} ({year})"
        response = await self._client.get("/series/lookup", params={"term": term})
        return response.json()

    # GET /series/lookup
    async def lookup_series_by_tvdb_id(self, id_: int) -> list[dict[str, t.Any]]:
        """Search for a series by its TVDB ID

        Args:
            id_: TVDB ID

        Returns:
            List of the search results
        """
        return await self.lookup_series(term=f"tvdb:{id_}")

    # POST /command
    async def _generic_command(self, name: str, **kwargs: t.Any) -> dict[str, t.Any]:
        """TODO: Needs docs"""
        response = await self._client.post(  # type: ignore
            "/command",
            json={"name": name, **{k: v for k, v in kwargs.items() if v is not None}},
        )
        return response.json()

    # POST /command, name=SeriesSearch
    async def search_series(self, id_: int) -> dict[str, t.Any]:
        """Search for a series.

        Args:
            id_: ID of the series to search for.
        """
        json_response = await self._generic_command("SeriesSearch", seriesId=id_)
        return json_response

    # POST /command, name=SeasonSearch
    async def search_season(self, id_: int, season: int) -> dict[str, t.Any]:
        """Search for a season of a series.

        Args:
            id_: ID of the series to search for.
            season: Season number to search for.
        """
        json_response = await self._generic_command(
            "SeasonSearch", seriesId=id_, seasonNumber=season
        )
        return json_response

    # POST /command, name=EpisodeSearch
    async def search_episodes(self, episodes: list[int]) -> dict[str, t.Any]:
        """Search for episodes.

        Args:
            episodes: Episode IDs to search for.
        """
        json_response = await self._generic_command("EpisodeSearch", episodeIds=episodes)
        return json_response

    # DELETE /episodefile/{id}
    async def delete_episode_file(self, id_: int) -> None:
        """Delete a episode file.

        Args:
            id_: ID of the episode file to delete.
        """
        await self._client.delete(f"/episodefile/{id_}")
