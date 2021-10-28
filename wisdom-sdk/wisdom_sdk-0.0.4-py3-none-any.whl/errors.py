class AuthFailedError(Exception):
    """
    Exception - Raised when issues with subscription key.

    Attributes
    ----------
    msg : string, optional
        Message to be shown when the error is thrown.
    """

    def __init__(self, msg="Failed Authentication, Enter a Valid Subscription Key"):
        self.message = msg

    def __str__(self):
        return f'{self.message}'


class DeviceInitError(Exception):
    """
    Exception - Raised when issues with device.

    Attributes
    ----------
    msg : string, optional
        Message to be shown when the error is thrown.
    """

    def __init__(self, msg="Device not configured properly. Try resetting the device."):
        self.message = msg

    def __str__(self):
        return f'{self.message}'


class RequestError(Exception):
    """
    Exception - Raised when connection to Azure Services Failed.

    Attributes
    ----------
    msg : string, optional
        Message to be shown when the error is thrown.
    """

    def __init__(self,
                 msg="Something is wrong in the backend. Kindly raise a support ticket at https://support.nexstem.ai"):
        self.message = msg

    def __str__(self):
        return f'{self.message}'


class UnexpectedError(Exception):
    """
    Exception - Raised when something unexpected occured.

    Attributes
    ----------
    msg : string, optional
        Message to be shown when the error is thrown.
    """

    def __init__(self, msg="Uhhhohhh something is wrong. Kindly raise a support ticket at https://support.nexstem.ai"):
        self.message = msg

    def __str__(self):
        return f'{self.message}'


class ValidationError(Exception):
    """
    Exception - Raised when input is invalid.

    Attributes
    ----------
    msg : string, optional
        Message to be shown when the error is thrown.
    """

    def __init__(self, msg="Invalid Input."):
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class SerialConnectionError(Exception):
    """
    Exception - Raised when wrong or invalid COM port is selected.

    Attributes
    ----------
    msg : string, optional
        Message to be shown when the error is thrown.
    """

    def __init__(self, msg="Select the correct COM port."):
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class StreamingError(Exception):
    """
    Exception - Raised when device is not streaming data but server is turned on.

    Attributes
    ----------
    msg : string, optional
        Message to be shown when the error is thrown.
    """

    def __init__(self, msg="Device is not streaming. Check the device battery."):
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class ProvisionError(Exception):
    """
    Exception - Raised when Wifi Provisioning Fails

    Attributes
    ----------
    msg : string, optional
        Message to be shown when the error is thrown.
    """

    def __init__(self, msg="Wifi Provision Failed"):
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class FilterError(Exception):
    """
    Exception - Raised when Wifi Provisioning Fails

    Attributes
    ----------
    msg : string, optional
        Message to be shown when the error is thrown.
    """

    def __init__(self, msg="Filter creation failed"):
        """

        Returns
        -------
        object
        """
        self.message = msg

    def __str__(self):
        return f"{self.message}"
