"""Skaha Headless Session."""
from typing import Any, Optional

from attr import attrs

from skaha.client import SkahaClient
from skaha.exceptions import ParameterError
from skaha.utils import logs

log = logs.get_logger(__name__)


@attrs
class Session(SkahaClient):
    """Skaha Session Client."""

    def __attrs_post_init__(self):
        """Modify the attributes of the SkahaClient class."""
        self.server = self.server + "/session"

    def fetch(
        self,
        kind: Optional[str] = None,
        status: Optional[str] = None,
        view: Optional[str] = None,
    ) -> list:
        """List open sessions for the user.

        Args:
            kind (str, optional): Session kind. Defaults to None.
            status (str, optional): Session status. Defaults to None.
            view (str, optional): Session view level. Defaults to None.

        Raises:
            ParameterError: When `kind`, `status` or `view` are malformed.

        Returns:
            list: Sessions information.

        Examples:
            >>> from skaha.session import Session
                session = Session()
                session.fetch(kind="desktop")

        """
        params: dict = {}
        if kind:
            params["type"] = self.check(
                kind, ["desktop", "notebook", "carta", "headless"]
            )
        if status:
            params["status"] = self.check(
                status,
                [
                    "Pending",
                    "Running",
                    "Terminating",
                    "Succeeded",
                    "Error",
                ],
            )
        if view:
            params["view"] = self.check(view, ["all"])
        log.debug(params)
        response = self.get(url=self.server, params=params)
        return response.json()

    def check(self, parameter: Any, values: list) -> Any:
        """Check parameter.

        Args:
            parameter (str): Parameter to check.
            values (list): Valid values.

        Raises:
            ParameterError: When parameter is malformed.

        Returns:
            Any: Parameter.

        """
        try:
            assert parameter in values, f"invalid param: {parameter}"
            return parameter
        except AssertionError as e:
            raise ParameterError(e)

    def info(self, session_id: str) -> str:
        """Get session information.

        Args:
            session_id (str): Session ID.

        Returns:
            str: Session information.

        Examples:
            >>> session.info(session_id="hjko98yghj")

        """
        params = {"view": "event"}
        return self.get(url=self.server + "/" + session_id, params=params).text

    def logs(self, session_id: str) -> str:
        """Get session logs.

        Args:
            session_id (str): Session ID.

        Returns:
            str: Logs in text/plain format.

        Examples:
            >>> session.logs(session_id="hjko98yghj")

        """
        params = {"view": "logs"}
        return self.get(url=self.server + "/" + session_id, params=params).text

    def create(
        self,
        name: str,
        image: str,
        cores: int = 1,
        ram: int = 4,
        kind: Optional[str] = None,
        cmd: Optional[str] = None,
        args: Optional[str] = None,
        env: Optional[dict] = None,
    ) -> str:
        """Launch a new session.

        Args:
            name (str): The name for the session.
            image (str): The Image ID of the session.
                e.g. images.canfar.net/skaha/notebook-scipy:0.2
            cores (int, optional): Number of cores. Defaults to 1.
            ram (int, optional): Amount of RAM. Defaults to 4.
            kind (str, optional): Session kind for images not from harbor registries.
                Defaults to None.
            cmd (str, optional): Override the image entrypoint. Defaults to None.
            args (str, optional): Override the image CMD params. Defaults to None.
            env (dict, optional): Environment variables. Defaults to None.

        Raises:
            ParameterError: When a platform is malformed.

        Returns:
            str: Session ID.

        Examples:
            >>> session.create(
                    name="test",
                    image="images.canfar.net/skaha/terminal:0.1",
                    cores=2,
                    ram=8,
                    kind="headless",
                    cmd="env",
                    env={"TEST": "test"}
                )
            >>> "hjko98yghj"

        """
        data: dict = {"name": name, "image": image, "cores": cores, "ram": ram}
        params: dict = {}
        if kind:
            params["type"] = self.check(
                kind, ["desktop", "notebook", "carta", "headless"]
            )
        if cmd:
            self.check(kind, ["headless"])
            params["cmd"] = cmd
        if args:
            self.check(kind, ["headless"])
            params["args"] = args
        if env:
            self.check(kind, ["headless"])
            params["env"] = env
        log.info(params)
        return self.post(url=self.server, data=data, params=params).text.rstrip("\r\n")

    def destroy(self, session_id: str) -> bool:
        """Destroy a session.

        Args:
            session_id (str): Session ID.

        Returns:
            bool: True if the session was destroyed.

        Examples:
            >>> session.destroy(session_id="hjko98yghj")

        """
        response = self.delete(url=self.server + "/" + session_id)
        if response.status_code == 200:
            return True
        else:
            return False

    def app(self, session_id: str, image: str):
        """Attach a desktop-app to the session identified by sessionID.

        Args:
            session_id (str): Skaha session ID.
            image (str): The desktop-app to attach

        """
        raise NotImplementedError()
