import typing as t

from .base import BaseAPI


class Radarr(BaseAPI):
    """API wrapper for Radarr."""

    ## Movies

    # GET /movie
    async def get_movie(self, tmdb_id: int | None = None) -> list[dict[str, t.Any]]:
        """Gets all movies in the database or movie with a specific TMDB ID

        Args:
            tmdb_id: TMDB ID of movie

        Returns:
            List of movies in the database
        """
        if tmdb_id:
            params = {"tmdbId": tmdb_id}
        else:
            params = {}
        response = await self._client.get("/movie", params=params)
        return response.json()

    # POST /movie
    async def add_movie(
        self,
        movie: dict[str, t.Any],
        monitored: bool = True,
        search: bool = True,
        **kwargs: str | int,
    ) -> dict[str, t.Any]:
        """Adds a movie to the database

        Args:
            movie: movie data as obtained from other methods
            monitored: If the movie should be monitored.
            search: Search for the movie on adding.

        Returns:
            The added movie
        """
        movie_json = {
            "title": movie["title"],
            "year": movie["year"],
            "tmdbId": movie["tmdbId"],
            "images": movie["images"],
            "titleSlug": movie["titleSlug"],
            "monitored": monitored,
            "addOptions": {"searchForMovie": search},
            #
            "rootFolderPath": self.root_folder,
            "qualityProfileId": self.quality_profile,
        }

        movie_json.update(kwargs)

        response = await self._client.post("/movie", json=movie_json)  # type: ignore
        return response.json()

    # PUT /movie
    async def update_movie(
        self, movie: dict[str, t.Any], move_files: bool = False
    ) -> dict[str, t.Any]:
        """Updates a movie in the database

        Modify the fields on the movie dict and thenuse this method to
        update it in the database.

        Args:
            movie: movie data as obtained from other methods
            move_files: Move the files if the path is changed

        Returns:
            The updated movie
        """
        response = await self._client.put(  # type: ignore
            "/movie", json=movie, params={"moveFiles": move_files}
        )
        return response.json()

    # GET /movie/{id}
    async def get_movie_by_id(self, id_: int) -> dict[str, t.Any]:
        """Get a movie by database ID

        Returns a single movie.

        Args:
            id_: The database ID of the movie to get

        Returns:
            The movie data
        """
        response = await self._client.get(f"/movie/{id_}")
        return response.json()

    # DELETE /movie/{id}
    async def delete_movie_by_id(
        self, id_: int, import_exclusion: bool = False, delete_files: bool = False
    ) -> None:
        """Delete a single movie by database ID

        Args:
            id_: The database ID
            import_exclusion: Prevent movie from being added to Radarr by lists
            delete_files: Delete the movie files and movie folder
        """
        await self._client.delete(
            f"/movie/{id_}",
            params={
                "addImportExclusion": import_exclusion,
                "deleteFiles": delete_files,
            },
        )

    # GET /movie/lookup
    async def lookup_movie(
        self, term: str, year: int | None = None
    ) -> list[dict[str, t.Any]]:
        """Search for a movie to add to the database (Uses TMDB for search results)

        Args:
            term: Search for this movie.
            year: Add this year to the search

        Returns:
            List of the search results
        """
        if year:
            term = f"{term} ({year})"
        response = await self._client.get("/movie/lookup", params={"term": term})
        return response.json()

    # GET /movie/lookup
    async def lookup_movie_by_tmdb_id(self, id_: int) -> list[dict[str, t.Any]]:
        """Search for a movie by its TMDB ID

        Args:
            id_: TMDB ID

        Returns:
            List of the search results
        """
        return await self.lookup_movie(term=f"tmdb:{id_}")

    # GET /movie/lookup
    async def lookup_movie_by_imdb_id(self, id_: str) -> list[dict[str, t.Any]]:
        """Search for a movie by its IMDB ID

        Args:
            id_: IMDB ID

        Returns:
            List of the search results
        """
        return await self.lookup_movie(term=f"imdb:{id_}")

    # PUT /movie/editor
    async def update_movies(
        self,
        movie_ids: list[int],
        **kwargs: bool | str | int,
    ) -> list[dict[str, t.Any]]:
        """Update multiple movies at once

        Editor endpoint is used by the movie editor in Radarr.
        The Edit operation allows to edit properties of multiple movies at once.

        Args:
            movie_ids: The database IDs of the movies to update

        Keyword Args:
            monitored (bool): Monitor/Unmonitor movies
            qualityProfileId (int): Set quality profile
            minimumAvailability (str): Set minumumAvailability
            rootFolderPath (str): Set root folder
            tags (List[int]): Tags
            applyTags (str): applyTags
                One of add, remove, replace
            moveFiles (bool): Move files if rootFolderPath is changed.
        """
        response = await self._client.put(  # type: ignore
            "/movie/editor", json={"movieIds": movie_ids} | kwargs
        )
        return response.json()

    # DELETE /movie/editor
    async def delete_movies(
        self,
        movie_ids: list[int],
        import_exclusion: bool = False,
        delete_files: bool = False,
    ) -> None:
        """Delete multiple movies.

        Editor endpoint is used by the movie editor in Radarr.
        The Delete operation allows mass deletion of movies (and optionally files).

        Args:
            movie_ids: The database IDs of the movies to delete
            import_exclusion: Prevent movie from being added to Radarr by lists
            delete_files: Delete the movie files and movie folders
        """

        # Building a request manually since httpx follows the HTTP spec and
        # does not allow body in a delete request but radarr needs one.
        await self._client.request(  # type: ignore
            method="DELETE",
            url="/movie/editor",
            json={
                "movieIds": movie_ids,
                "deleteFiles": delete_files,
                "addImportExclusion": import_exclusion,
            },
        )

    # POST /movie/import
    async def import_movies(
        self, movies: list[dict[str, t.Any]]
    ) -> list[dict[str, t.Any]]:
        """Used to bulk import movies.

        The movie import endpoint is used by the bulk import view in Radarr UI.
        It allows movies to be bulk added to the Radarr database.

        Args:
            movies: The movies to import.
        """
        response = await self._client.post("/movie/import", json=movies)  # type: ignore
        return response.json()

    ## Moviefiles

    # GET /moviefile
    async def get_movie_files_by_movie_id(self, id_: int) -> list[dict[str, t.Any]]:
        """Get a list of movie files for a movie

        Args:
            id_: Databse ID of movie to get files for

        Returns:
            List of movie files for given movie ID
        """
        response = await self._client.get("/moviefile", params={"movieid": id_})
        return response.json()

    # GET /moviefile
    async def get_multiple_movie_files_by_ids(
        self, ids: t.Sequence[int]
    ) -> list[dict[str, t.Any]]:
        """Get multiple movie files by IDs

        Args:
            ids: Sequence of movie file IDs to get

        Returns:
            List of movie files
        """
        response = await self._client.get(
            "/moviefile",
            # Needs to be in format 2,3,4
            # Map ids to string and then join with ,
            params={"moviefileids": ",".join(map(str, ids))},
        )
        return response.json()

    # GET /moviefile/{id}
    async def get_moviefile_by_id(self, id_: int) -> dict[str, t.Any]:
        """Get a movie file by its database ID

        Args:
            id_: database ID of the moviefile

        Returns:
            The movie file
        """
        response = await self._client.get(f"/moviefile/{id}")
        return response.json()

    # DELETE /moviefile/{id}
    async def delete_movie_file(self, id_: int) -> None:
        """Delete a moviefile by its database ID

        Args:
            id_: The database ID if the moviefile.

        Returns:
            The JSON Response received
        """
        await self._client.delete(f"/moviefile/{id_}")
        return None

    ## History

    # GET /history
    async def get_history(
        self,
        page: int = 1,
        page_size: int = 20,
        sort_direction: str = "descending",
        sort_key: str = "date",
    ) -> dict[str, t.Any]:
        """Get history items.

        Args:
            page: Page of history to get. Defaults to 1.
            page_size: Results per page. Defaults to 20.
            sort_direction: Direction of sort. Defaults to "descending".
            sort_key: Field to sort by. Defaults to "date".

        Returns:
            Dict of stuff
                Key "records" has the history records.
                Key "totalRecords" has the number of total records.
        """
        response = await self._client.get(
            "/history",
            params={
                "page": page,
                "pageSize": page_size,
                "sortDirection": sort_direction,
                "sortKey": sort_key,
            },
        )
        return response.json()

    # GET /history/movie
    async def get_history_for_movie(
        self, id_: int, event_type: int | None = None
    ) -> list[dict[str, t.Any]]:
        # TODO: Elaborate on valid event_types.
        """Get the history for a movie

        Args:
            id_: The database ID of the movie.
            event_type: The type of event to filter. Defaults to None.

        Returns:
            List of history items.
        """
        params = {"movieId": id_}
        if event_type:
            params["eventType"] = event_type
        response = await self._client.get("/history/movie", params=params)
        return response.json()

    ## Blacklist

    # GET /blacklist
    async def get_blacklist(
        self,
        page: int = 1,
        page_size: int = 20,
        sort_direction: str = "descending",
        sort_key: str = "date",
    ) -> dict[str, t.Any]:
        """Get all blacklisted releases.

        Args:
            page: Page of blacklist to get. Defaults to 1.
            page_size: Results per page. Defaults to 20.
            sort_direction: Direction of sort. Defaults to "descending".
            sort_key: Field to sort by. Defaults to "date".

        Returns:
            Dict of stuff
                Key "records" has the blacklist records.
                Key "totalRecords" has the number of total records.
        """
        response = await self._client.get(
            "/blacklist",
            params={
                "page": page,
                "pageSize": page_size,
                "sortDirection": sort_direction,
                "sortKey": sort_key,
            },
        )
        return response.json()

    # DELETE /blacklist
    async def delete_blacklist(self, id_: int) -> None:
        """Delete a release from the blacklist

        Args:
            id_: database ID of the blacklist release
        """
        await self._client.delete("/blacklist", params={"id": id_})

    # GET /blacklist/movie
    async def get_blacklist_for_movie(self, id_: int) -> list[dict[str, t.Any]]:
        """Gets blacklisted releases for a movie

        Args:
            id_: database ID of the movie.

        Returns:
            List of blacklisted releases
        """
        response = await self._client.get("/blacklist/movie", params={"movieId": id_})
        return response.json()

    # DELETE /blacklist/bulk
    async def delete_blacklist_bulk(self, ids: list[int] | None) -> None:
        """Bulk delete blacklisted releases

        Args:
            ids: IDs of blacklisted releases to delete
        """
        # Building a request manually since httpx follows the HTTP spec and
        # does not allow body in a delete request but radarr needs one.
        await self._client.request(  # type: ignore
            method="DELETE", url="/blacklist/bulk", json={"ids": ids}
        )

    ## Queue

    # GET /queue
    async def get_queue(
        self,
        page: int = 1,
        page_size: int = 20,
        sort_direction: str = "ascending",
        sort_key: str = "timeLeft",
        include_unknown_movie_items: bool = True,
    ) -> list[dict[str, t.Any]]:
        """Get all items in the queue.

        Args:
            page: Page of queue to return. Defaults to 1.
            page_size: Results per page. Defaults to 20.
            sort_direction: Direction of sort. Defaults to "descending".
            sort_key: Field to sort by. Defaults to "date".
            include_unknown_movie_items: Include unknown movie items. Defaults to True.

        Returns:
            List of items in the queue.
        """
        response = await self._client.get(
            "/queue",
            params={
                "page": page,
                "pageSize": page_size,
                "sortDirection": sort_direction,
                "sortKey": sort_key,
                "includeUnknownMovieItems": include_unknown_movie_items,
            },
        )
        return response.json()

    # DELETE /queue/{id}
    async def delete_queue(
        self, id_: int, remove_from_client: bool = True, blacklist: bool = False
    ) -> None:
        """Delete a item from the queue by ID

        Args:
            id_: queue ID of the item.
            remove_from_client: Delete from client also. Defaults to True.
            blacklist: Add to blacklist. Defaults to False.
        """
        await self._client.delete(
            f"/queue/{id_}",
            params={"removeFromClient": remove_from_client, "blacklist": blacklist},
        )

    # DELETE /queue/bulk
    async def delete_queue_bulk(
        self, ids: list[int], remove_from_client: bool = True, blacklist: bool = False
    ) -> None:
        """Bulk delete from the queue by ID

        Args:
            ids: List of queue IDs to delete
            remove_from_client: Delete from client also. Defaults to True.
            blacklist: [description]. Defaults to False.
        """
        await self._client.request(  # type: ignore
            method="DELETE",
            url="/queue/bulk",
            params={"removeFromClient": remove_from_client, "blacklist": blacklist},
            json={"ids": ids},
        )

    # GET /queue/details
    async def get_queue_details(
        self, include_movie: bool = False
    ) -> list[dict[str, t.Any]]:
        """Get details of queue

        Args:
            include_movie: Include movie object if linked. Defaults to False.

        Returns:
            List of details of all items in queue
        """
        response = await self._client.get(
            "/queue/details", params={"includeMovie": include_movie}
        )
        return response.json()

    # GET /queue/status
    async def get_queue_status(self) -> dict[str, t.Any]:
        """Get status of queue

        Returns:
            Status of queue

        """
        response = await self._client.get("/queue/status")
        return response.json()

    # POST /queue/grab
    async def grab_queue_item(self, id_: int) -> None:
        """Grab item from queue

        Perform a Radarr "force grab" on a pending queue item by its ID.

        Args:
            id_: ID of item
        """
        await self._client.post(f"/queue/grab/{id_}")  # type: ignore

    ## Indexer

    # GET /indexer
    async def get_indexer(self) -> list[dict[str, t.Any]]:
        """Get all Indexers

        Returns:
            List of indexers
        """
        response = await self._client.get("/indexer")
        return response.json()

    # GET /indexer/{id}
    async def get_indexer_by_id(self, id_: int) -> dict[str, t.Any]:
        """Get a indexer by its ID.

        Args:
            id_: database ID of the indexer.

        Returns:
            The indexer.
        """
        response = await self._client.get(f"/indexer/{id_}")
        return response.json()

    # PUT /indexer/{id}
    async def update_indexer(
        self, id_: int, indexer: dict[str, t.Any]
    ) -> dict[str, t.Any]:
        """Updates an indexer in the database.

        Pass in a modified indexer obtained from other methods.

        Args:
            id: Database ID of the indexer.
            indexer: The modified indexer.

        Returns:
            The updated indexer.
        """
        response = await self._client.put(f"/indexer/{id_}", json=indexer)  # type: ignore
        return response.json()

    # DELETE /indexer/{id}
    async def delete_indexer(self, id_: int) -> None:
        """Delete a indexer.

        Args:
            id_: Database ID of the indexer to delete
        """
        await self._client.delete(f"/indexer/{id_}")

    ## Download Client

    # GET /downloadclient
    async def get_download_client(self) -> list[dict[str, t.Any]]:
        """Gets all download clients

        Returns:
            List of download clients

        """
        response = await self._client.get("/downloadclient")
        return response.json()

    # GET /downloadclient/{id}
    async def get_download_client_by_id(self, id_: int) -> dict[str, t.Any]:
        """Get a download client by ID

        Args:
            id_: Database ID of download client

        Returns:
            Download client
        """
        response = await self._client.get(f"/downloadclient/{id}")
        return response.json()

    # DELETE /downloadclient/{id}
    async def delete_download_client(self, id_: int) -> None:
        """Delete a download client by ID

        Args:
            id_: ID of the download client to delete
        """
        await self._client.delete(f"/downloadclient/{id_}")

    # PUT /downloadclient/{id}
    async def update_download_client(
        self, id_: int, download_client: dict[str, t.Any]
    ) -> dict[str, t.Any]:
        """Update a download client in the database

        Args:
            download_client: Modified download client data

        Returns:
            Updated download client
        """
        response = await self._client.put(  # type: ignore
            f"/downloadclient/{id_}", json=download_client
        )
        return response.json()

    ## Import lists

    # GET /importlist
    async def get_import_list(self) -> list[dict[str, t.Any]]:
        """Get all import lists

        Returns:
            List of import lists
        """
        response = await self._client.get("/importlist")
        return response.json()

    # GET /importlist/{id}
    async def get_import_list_by_id(self, id_: int) -> dict[str, t.Any]:
        """Get a import list by ID

        Args:
            id_: Database ID of the import list.

        Returns:
            The import list.
        """
        response = await self._client.get(f"/importlist/{id_}")
        return response.json()

    # PUT /importlist/{id}
    async def update_import_list(
        self, id_: int, import_list: dict[str, t.Any]
    ) -> dict[str, t.Any]:
        """Update a import list in the database

        Args:
            import_list: Modified import list data

        Returns:
            Updated import list
        """
        response = await self._client.put(  # type: ignore
            f"/importlist/{id_}", json=import_list
        )
        return response.json()

    # DELETE /importlist/{id}
    async def delete_import_list(self, id_: int) -> None:
        """Delete a import list by ID

        Args:
            id_: ID of the import list to delete
        """
        await self._client.delete(f"/importlist/{id_}")

    ## Notifications

    # GET /notification
    async def get_notification(self) -> list[dict[str, t.Any]]:
        """Gets all notifications

        Returns:
            List of notifications

        """
        response = await self._client.get("/notification")
        return response.json()

    # GET /notification/{id}
    async def get_notification_by_id(self, id_: int) -> dict[str, t.Any]:
        """Get a notification by ID

        Args:
            id_: Database ID of notification

        Returns:
            Notification
        """
        response = await self._client.get(f"/notification/{id}")
        return response.json()

    # DELETE /notification/{id}
    async def delete_notification(self, id_: int) -> None:
        """Delete a notification by ID

        Args:
            id_: ID of the notification to delete
        """
        await self._client.delete(f"/notification/{id_}")

    # PUT /notification/{id}
    async def update_notification(
        self, id_: int, notification: dict[str, t.Any]
    ) -> dict[str, t.Any]:
        """Update a notification in the database

        Args:
            notification: Modified notification data

        Returns:
            Updated notification
        """
        response = await self._client.put(  # type: ignore
            f"/notification/{id_}", json=notification
        )
        return response.json()

    ## Tags

    # GET /tag/detail/{id}
    async def get_tag_detail_by_id(self, id_: int) -> dict[str, t.Any]:
        """Returns the ID of all items with the specific tag

        Args:
            id_: Tag ID to get items with

        Returns:
            Dict of items.
        """
        response = await self._client.get(f"/tag/detail/{id_}")
        return response.json()

    # GET /tag/detail
    async def get_tag_details(self) -> list[dict[str, t.Any]]:
        """Returns a list of tag detail objects for all tags in the database.

        Returns:
            List of tag detail objects
        """
        response = await self._client.get("/tag.detail")
        return response.json()

    # GET /tag/{id}
    async def get_tag_by_id(self, id_: int) -> dict[str, t.Any]:
        """Return a given tag and its label by the database id.

        Args:
            id_: Tag ID

        Returns:
            Tag
        """
        response = await self._client.get(f"/tag/{id_}")
        return response.json()

    # DELETE /tag/{id}
    async def delete_tag(self, id_: int) -> None:
        """Delete a tag.

        Args:
            id_: Tag ID
        """
        await self._client.delete(f"/tag/{id_}")

    # PUT /tag/{id}
    async def update_tag(self, id_: int, tag: dict[str, t.Any]) -> dict[str, t.Any]:
        """Edit a Tag by its database id

        Args:
            id_: The tag ID to update.
            tag: The updated tag.

        Returns:
            The updated tag.
        """
        response = await self._client.put(f"/tag/{id_}", json=tag)  # type: ignore
        return response.json()

    # GET /tag
    async def get_tag(self) -> list[dict[str, t.Any]]:
        """Get all tags in the database.

        Returns:
            List of tags
        """
        response = await self._client.get("/tag")
        return response.json()

    # POST /tag
    async def create_tag(self, id_: int, label: str) -> dict[str, t.Any]:
        """Create a new tag.

        Create a new tag that can be assigned to a movie, list,
        delay profile, notification or restriction.

        Args:
            id_: ID of the tag to create.
            label: Label of the ta to create.

        Returns:
            The created tag.
        """
        response = await self._client.post("/tag", json={"id": id_, "label": label})  # type: ignore
        return response.json()

    ## Diskspace

    # GET /diskspace
    async def get_diskspace(self) -> list[dict[str, t.Any]]:
        """Query Radarr for disk usage information.

        Returns:
            Disk usage information.
        """
        response = await self._client.get("/diskspace")
        return response.json()

    ## Settings

    # GET /config/ui
    async def get_config_ui(self) -> dict[str, t.Any]:
        """Query Radarr for UI settings

        Returns:
            UI Settings
        """
        response = await self._client.get("/config/ui")
        return response.json()

    # PUT /config/ui
    async def update_config_ui(self, config: dict[str, t.Any]) -> dict[str, t.Any]:
        """Edit one or many UI settings and save to database.

        Args:
            config: UI config settings.

        Returns:
            Updated UI config settings.
        """
        response = await self._client.put("/config/ui", json=config)  # type: ignore
        return response.json()

    # GET /config/host
    async def get_config_host(self) -> dict[str, t.Any]:
        """Query Radarr for host settings

        Returns:
            host Settings
        """
        response = await self._client.get("/config/host")
        return response.json()

    # PUT /config/host
    async def update_config_host(self, config: dict[str, t.Any]) -> dict[str, t.Any]:
        """Edit one or many host settings and save to database.

        Args:
            config: host config settings.

        Returns:
            Updated host config settings.
        """
        response = await self._client.put("/config/host", json=config)  # type: ignore
        return response.json()

    # GET /config/naming
    async def get_config_naming(self) -> dict[str, t.Any]:
        """Query Radarr for naming settings

        Returns:
            naming Settings
        """
        response = await self._client.get("/config/naming")
        return response.json()

    # PUT /config/naming
    async def update_config_naming(self, config: dict[str, t.Any]) -> dict[str, t.Any]:
        """Edit one or many naming settings and save to database.

        Args:
            config: naming config settings.

        Returns:
            Updated naming config settings.
        """
        response = await self._client.put("/config/naming", json=config)  # type: ignore
        return response.json()

    ## Metadata

    # GET /metadata
    async def get_metadata(self) -> list[dict[str, t.Any]]:
        """Get all metadata consumer settings

        Returns:
            Metadata consumer settings
        """
        response = await self._client.get("/metadata")
        return response.json()

    ## System

    # GET /system/status
    async def get_system_status(self) -> dict[str, t.Any]:
        """Find out information such as OS, version, paths used, etc

        Returns:
            System status
        """
        response = await self._client.get("/system/status")
        return response.json()

    ## Health

    # GET /health
    async def get_health(self) -> dict[str, t.Any]:
        """Query radarr for health information

        Returns:
            Health
        """
        response = await self._client.get("/health")
        return response.json()

    ## Commands

    # POST /command
    async def _generic_command(self, name: str, **kwargs: t.Any) -> dict[str, t.Any]:
        """Pushes commands to Radarr using a key:value pair.

        ApplicationUpdate - Trigger an update of Radarr
        Backup - Trigger a backup routine
        CheckHealth - Trigger a system health check
        ClearBlocklist - Triggers the removal of all blocklisted movies
        CleanUpRecycleBin - Trigger a recycle bin cleanup check
        DeleteLogFiles - Triggers the removal of all Info/Debug/Trace log files
        DeleteUpdateLogFiles - Triggers the removal of all Update log files
        DownloadedMoviesScan - Triggers the scan of downloaded movies
        MissingMoviesSearch - Triggers a search of all missing movies
        RefreshMonitoredDownloads - Triggers the scan of monitored downloads
        RefreshMovie - Trigger a refresh / scan of library
            movieIds (List[int]) - Specify a list of ids (comma separated) for individual movies to refresh

        Not documented in API 👇👇

        MoviesSearch - Search for movies
            movieIds (List[int]) - List of movie IDs

        Args:
            name: Name of the commnad

        Keyword Args:
            If any commands have extra stuff.

        Returns:
            JSON Response
        """
        response = await self._client.post(  # type: ignore
            "/command",
            json={"name": name, **{k: v for k, v in kwargs.items() if v is not None}},
        )
        return response.json()

    # POST /command, name=ApplicationUpdate
    async def application_update_command(self) -> dict[str, t.Any]:
        """Trigger an update of Radarr"""
        json_response = await self._generic_command("ApplicationUpdate")
        return json_response

    # POST /command, name=Backup
    async def backup_command(self) -> dict[str, t.Any]:
        """Trigger a backup routine"""
        json_response = await self._generic_command("Backup")
        return json_response

    # POST /command, name=CheckHealth
    async def check_health_command(self) -> dict[str, t.Any]:
        """Trigger a system health check"""
        json_response = await self._generic_command("CheckHealth")
        return json_response

    # POST /command, name=ClearBlacklist
    async def clear_blacklist_command(self) -> dict[str, t.Any]:
        """Triggers the removal of all blocklisted movies"""
        json_response = await self._generic_command("ClearBlacklist")
        return json_response

    # POST /command, name=CleanUpRecycleBin
    async def clean_up_recycle_bin_command(self) -> dict[str, t.Any]:
        """Trigger a recycle bin cleanup check"""
        json_response = await self._generic_command("CleanUpRecycleBin")
        return json_response

    # POST /command, name=DeleteLogFiles
    async def delete_log_files_command(self) -> dict[str, t.Any]:
        """Triggers the removal of all Info/Debug/Trace log files"""
        json_response = await self._generic_command("DeleteLogFiles")
        return json_response

    # POST /command, name=DeleteUpdateLogFiles
    async def delete_update_log_files_command(self) -> dict[str, t.Any]:
        """Triggers the removal of all Update log files"""
        json_response = await self._generic_command("DeleteUpdateLogFiles")
        return json_response

    # POST /command, name=DownloadedMoviesScan
    async def downloaded_movies_scan_command(self) -> dict[str, t.Any]:
        """Triggers the scan of downloaded movies"""
        json_response = await self._generic_command("DownloadedMoviesScan")
        return json_response

    # POST /command, name=MissingMoviesSearch
    async def missing_movies_search_command(self) -> dict[str, t.Any]:
        """Triggers a search of all missing movies"""
        json_response = await self._generic_command("MissingMoviesSearch")
        return json_response

    # POST /command, name=RefreshMonitoredDownloads
    async def refresh_monitored_downloads_command(self) -> dict[str, t.Any]:
        """Triggers the scan of monitored downloads"""
        json_response = await self._generic_command("RefreshMonitoredDownloads")
        return json_response

    # POST /command, name=RefreshMovie
    async def refresh_movie_command(self, movie_ids: list[int]) -> dict[str, t.Any]:
        """Trigger a refresh / scan of library

        Args:
            movie_ids: Specify a list of ids (comma separated) for individual movies to refresh
        """
        json_response = await self._generic_command(
            "RefreshMovie", movieIds=",".join(map(str, movie_ids))
        )
        return json_response

    # POST /commnad, name=MoviesSearch
    async def search_movies(self, movie_ids: list[int]) -> dict[str, t.Any]:
        """Search for movies

        Args:
            movie_ids: List of movie IDs to search for
        """
        json_response = await self._generic_command("MoviesSearch", movieIds=movie_ids)
        return json_response

    # Update

    # GET /update
    async def get_update(self) -> list[dict[str, t.Any]]:
        """Will return a list of recent updates to Radarr

        Returns:
            Recent updates.
        """
        response = await self._client.get("/update")
        return response.json()

    # Quality Profile

    # GET /qualityprofile
    async def get_qualityprofile(self) -> list[dict[str, t.Any]]:
        """Get all quality profiles

        Returns:
            List of quality profiles.
        """
        response = await self._client.get("/qualityProfile")
        return response.json()

    # Calendar

    # GET /calendar
    async def get_calendar(
        self, start: str, end: str, unmonitored: bool = True
    ) -> list[dict[str, t.Any]]:
        """Get calendar events

        Args:
            start: Start date - ISO 8601 String
            end: End date - ISO 8601 String
            unmonitored: include unmonitored movies

        Returns:
            List of calendar events.
        """
        response = await self._client.get(
            "/calendar", params={"unmonitored": unmonitored, "start": start, "end": end}
        )
        return response.json()

    # Custom Filters

    # GET /customfilter
    async def get_custom_filter(self) -> list[dict[str, t.Any]]:
        """Query Radarr for custom filters

        Returns:
            List of custom filters
        """
        response = await self._client.get("/customfilter")
        return response.json()

    # Remote Path Mapping

    # GET /remotepathmapping
    async def get_remote_path_mapping(self) -> list[dict[str, t.Any]]:
        """Get a list of remote paths being mapped and used by Radarr.

        Returns:
            List of remote path mappings.
        """
        response = await self._client.get("/remotepathmapping")
        return response.json()

    # Root Folder

    # GET /rootfolder
    async def get_root_folder(self) -> list[dict[str, t.Any]]:
        """Query Radarr for root folder information.

        Returns:
            List of root folders.
        """
        response = await self._client.get("/rootfolder")
        return response.json()
