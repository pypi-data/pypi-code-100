import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.models.resource_list import TrajectoryList
from cognite.well_model.client.models.trajectory_rows import TrajectoryRows
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.client.utils._distance_unit import create_distance_unit
from cognite.well_model.client.utils._identifier_list import create_identifier, identifier_list
from cognite.well_model.client.utils.constants import DEFAULT_LIMIT
from cognite.well_model.client.utils.multi_request import cursor_multi_request
from cognite.well_model.models import (
    DistanceRange,
    DistanceUnit,
    Trajectory,
    TrajectoryData,
    TrajectoryDataRequest,
    TrajectoryFilter,
    TrajectoryFilterRequest,
    TrajectoryIngestion,
    TrajectoryIngestionItems,
    TrajectoryInterpolationRequest,
    TrajectoryInterpolationRequestItems,
    TrajectoryItems,
    TrueVerticalDepths,
)

logger = logging.getLogger(__name__)


class TrajectoriesAPI(BaseAPI):
    def __init__(self, client: APIClient):
        super().__init__(client)

        @extend_class(Trajectory)
        def data(
            this: Trajectory,
            measured_depth: Optional[DistanceRange] = None,
            true_vertical_depth: Optional[DistanceRange] = None,
        ):
            return self.list_data(
                sequence_external_id=this.source.sequence_external_id,
                measured_depth=measured_depth,
                true_vertical_depth=true_vertical_depth,
            )

    def list(
        self,
        wellbore_asset_external_ids: Optional[List[str]] = None,
        wellbore_matching_ids: Optional[List[str]] = None,
        limit: Optional[int] = DEFAULT_LIMIT,
    ) -> TrajectoryList:
        """List trajectories

        Args:
            wellbore_asset_external_ids (Optional[List[str]], optional)
            wellbore_matching_ids (Optional[List[str]], optional)
            limit (Optional[int], optional)

        Returns:
            TrajectoryList:
        """

        def request(cursor, limit):
            filter = TrajectoryFilterRequest(
                filter=TrajectoryFilter(
                    wellbore_ids=identifier_list(wellbore_asset_external_ids, wellbore_matching_ids),
                ),
                cursor=cursor,
                limit=limit,
            )

            path: str = self._get_path("/trajectories/list")
            response: Response = self.client.post(url_path=path, json=filter.json())
            trajectory_items: TrajectoryItems = TrajectoryItems.parse_raw(response.text)
            return trajectory_items

        items = cursor_multi_request(
            get_cursor=lambda x: x.next_cursor,
            get_items=lambda x: x.items,
            limit=limit,
            request=request,
        )
        return TrajectoryList(items)

    def list_data(
        self,
        sequence_external_id: str,
        measured_depth: Optional[DistanceRange] = None,
        true_vertical_depth: Optional[DistanceRange] = None,
    ) -> TrajectoryRows:
        """Get trajectory data

        Args:
            sequence_external_id (str): External id of a sequence ingested as a trajectory
            measured_depth (Optional[DistanceRange]): MD range
            true_vertical_depth (Optional[DistanceRange]): TVD range

        Returns:
            TrajectoryRows: Trajectory and iterator over rows
        """
        request = TrajectoryDataRequest(
            sequence_external_id=sequence_external_id,
            measured_depth=measured_depth,
            true_vertical_depth=true_vertical_depth,
        )
        path = self._get_path("/trajectories/data")
        response: Response = self.client.post(url_path=path, json=request.json())
        trajectory_data = TrajectoryData.parse_raw(response.text)
        return TrajectoryRows(trajectory_data)

    def interpolate(
        self,
        measured_depths: List[float],
        measured_depth_unit: str = "meter",
        true_vertical_depth_unit: str = "meter",
        *,
        wellbore_matching_id: Optional[str] = None,
        wellbore_asset_external_id: Optional[str] = None,
    ) -> List[float]:
        """Get the true vertical depth corresponding to a list of measured depths

        The interpolation uses the minimum curvature method between trajectory
        points.

        Args:
            measured_depths (List[float]): List of measured depths.
            measured_depth_unit (str, optional): Unit for the measured depths. Defaults to "meter".
            true_vertical_depth_unit (str, optional): Unit for the returned true vertical depths. Defaults to "meter".
            wellbore_matching_id (Optional[str], optional)
            wellbore_asset_external_id (Optional[str], optional)

        Returns:
            List[float]: A list of true vertical depths corresponding to the given measured depths.

        Examples:
            Interpolate measured depths
                >>> from cognite.well_model import CogniteWellsClient
                >>> wm = CogniteWellsClient()
                >>> wm.trajectories.interpolate(
                ...     wellbore_asset_external_id="VOLVE:13/10-F-11 T2",
                ...     measured_depths=[100.0, 150.0, 200.0, 250.0]
                ... )
                [45.1, 95.1, 145.1, 195.1]
        """
        identifier = create_identifier(
            external_id=wellbore_asset_external_id,
            matching_id=wellbore_matching_id,
        )
        tvd_unit = DistanceUnit(unit=create_distance_unit(true_vertical_depth_unit))
        md_unit = DistanceUnit(unit=create_distance_unit(measured_depth_unit))

        request = TrajectoryInterpolationRequestItems(
            items=[
                TrajectoryInterpolationRequest(
                    wellbore_id=identifier,
                    measured_depths=measured_depths,
                    measured_depth_unit=md_unit,
                    true_vertical_depth_unit=tvd_unit,
                )
            ]
        )
        path = self._get_path("/trajectories/interpolate")
        response = self.client.post(path, request.json())
        interps = response.json()["items"]
        assert len(interps) == 1
        interp = TrueVerticalDepths.parse_obj(interps[0])
        assert interp.true_vertical_depth_unit == tvd_unit
        tvds: List[float] = interp.true_vertical_depths
        return tvds

    def ingest(self, ingestions: List[TrajectoryIngestion]) -> TrajectoryList:
        """Ingest trajectories

        Args:
            ingestions (List[TrajectoryIngestion]): List of trajectory ingestion objects

        Returns:
            TrajectoryList:
        """
        path = self._get_path("/trajectories")
        json = TrajectoryIngestionItems(items=ingestions).json()
        response: Response = self.client.post(path, json)

        return TrajectoryList([Trajectory.parse_obj(x) for x in response.json()["items"]])
