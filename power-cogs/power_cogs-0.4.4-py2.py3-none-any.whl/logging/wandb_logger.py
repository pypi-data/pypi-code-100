from typing import Dict, Optional, Union

import wandb
from loguru import logger

from power_cogs.logging.logger_utils import safe
from power_cogs.utils.utils import makedirs  # noqa


class WandbLogger:
    def __init__(
        self,
        job_type: Optional[str] = None,
        dir=None,
        config: Union[Dict, str, None] = None,
        project: Optional[str] = None,
        entity: Optional[str] = None,
        reinit: bool = None,
        tags=None,
        group: Optional[str] = None,
        name: Optional[str] = None,
        notes: Optional[str] = None,
        magic: Union[dict, str, bool] = None,
        config_exclude_keys=None,
        config_include_keys=None,
        anonymous: Optional[str] = None,
        mode: Optional[str] = None,
        allow_val_change: Optional[bool] = None,
        resume: Optional[Union[bool, str]] = None,
        force: Optional[bool] = None,
        tensorboard=None,
        sync_tensorboard=None,
        monitor_gym=None,
        save_code=None,
        id=None,
        settings=None,
    ):
        self.project = project
        self.config = config
        logger.info("Wandb Project: {}".format(self.project))
        wandb.init(
            job_type=job_type,
            dir=dir,
            config=config,
            project=project,
            entity=entity,
            reinit=reinit,
            tags=tags,
            group=group,
            name=name,
            notes=notes,
            magic=magic,
            config_exclude_keys=config_exclude_keys,
            config_include_keys=config_include_keys,
            anonymous=anonymous,
            mode=mode,
            allow_val_change=allow_val_change,
            resume=resume,
            force=force,
            tensorboard=tensorboard,
            sync_tensorboard=sync_tensorboard,
            monitor_gym=monitor_gym,
            save_code=save_code,
            id=id,
            settings=settings,
        )

    @safe
    def close(self):
        wandb.join()

    @safe
    def emit_metrics(self, output):
        metrics = output["metrics"]
        wandb.log(metrics)
