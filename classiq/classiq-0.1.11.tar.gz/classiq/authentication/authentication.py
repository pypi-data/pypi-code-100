import asyncio
import warnings

from classiq import client
from classiq.authentication import device, password_manager
from classiq.exceptions import ClassiqAuthenticationError


def verify_token(overwrite: bool):
    # TODO: consider using refresh token rotation
    #  (https://auth0.com/docs/tokens/refresh-tokens/refresh-token-rotation)

    token_available = client.client().is_refresh_token_available()
    if not overwrite and token_available:
        raise ClassiqAuthenticationError(
            "Device is already registered.\nGenerating a new refresh token should only "
            "be done if the current refresh token is compromised.\nTo do so, set the "
            "overwrite parameter to true"
        )

    if overwrite and token_available:
        warnings.warn(
            "Overwriting an existing refresh token should only be done if "
            "it is compromised. Make sure this operation is necessary, "
            "and if not, remove the call to device registration."
        )


def register_device(overwrite: bool = False):
    verify_token(overwrite)

    access_token, refresh_token = asyncio.run(
        device.DeviceRegistrar.register(
            get_refresh_token=password_manager.is_password_manager_available()
        )
    )
    client.client().save_tokens(access_token=access_token, refresh_token=refresh_token)


async def register_device_async(overwrite: bool = False):
    """Async version of `register_device`"""
    verify_token(overwrite)

    access_token, refresh_token = await device.DeviceRegistrar.register(
        get_refresh_token=password_manager.is_password_manager_available()
    )
    client.client().save_tokens(access_token=access_token, refresh_token=refresh_token)
