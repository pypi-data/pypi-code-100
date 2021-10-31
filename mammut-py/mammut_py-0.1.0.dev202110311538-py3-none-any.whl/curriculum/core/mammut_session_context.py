import dataclasses
import ray
import datetime
from typing import Optional
from mammut import config


@dataclasses.dataclass
class MammutSessionContext:
    """Data class to encapsulate the mammut curriculum context
    data across different processes.

    Currently, this class should encapsulate values that can be serialized
    out-of-the-box by Ray.


    TODO: there are details to work on. Right now is being used
        for main report registry actor handle propagation. But
        a good conceptual design is required.
    """

    package_id: str
    main_report_actor_handle: Optional[ray.actor.ActorHandle] = None
    session_id: str = str(datetime.datetime.now())
    mammut_id: int = 1
    ray_classroom_id: int = 0
    curriculum_save_folder: str = config.save_folder
    online_models_registry: Optional[ray.actor.ActorHandle] = None
