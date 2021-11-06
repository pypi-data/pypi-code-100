"""
greenops
--------

Software to measure the footprints of deep learning models at training,
testing and evaluating to reduce energy consumption and carbon footprints.

Copyright rixel 2021
Distributed under the MIT License.
See accompanying file LICENSE.

File: submodule torchmeasure
"""


from time import time

import torch

from .context import Context, DEFAULT_CPU_WATTS
from .measure import DEFAULT_INSTANT_LOG, LogRow, LogSettings, Measure


DEFAULT_CURRENT_STAGE = 'torch_main'


class TorchMeasure(Measure):
    """
    Maintain measurement process intagrated to a PyTorch model
    ==========================================================
    """


    def __init__(self, torch_model : torch.nn.Module,
                 output_file_name : str = None, watch : dict = None,
                 device_data : any = None, csv_delimiter : str = '\t',
                 log_settings : LogSettings = None,
                 instant_log : bool = DEFAULT_INSTANT_LOG,
                 current_stage : str = DEFAULT_CURRENT_STAGE):
        """
        Initialize the object
        =====================

        Parameters
        ----------
        torch_model : torch.nn.Module
            PyTorch or Fast.AI model to cooperate with.
        output_file_name : str, optional (None if omitted)
            Name of the file to output log to. If omitted,
            'greenops_timestamp.csv' is used in the current directory.
        watch : dict, optional (None if omitted)
            Dict of variables to watch.
        device_data : DeviceData | str, optional (None if omitted)
            Device data to use to measure.
        csv_delimiter : str, optional ('\t' if omitted)
            Delimiter of the csv file. Tab is used if omitted.
        log_settings : LogSettings, optional (None if omitted)
            Settings of the logging process. If omitted default settings are
            used.
        instant_log : bool, optional (DEFAULT_INSTANT_LOG if omitted)
            Whether to log instantly or not.

        Notes
        -----
        I.
            If you create a watch dict, you have to collect variables that are
            passed as reference instead of passed as a value. To achieve this
            please keep in mind Python's argument passing model. You can
            consult Python's official documentation abot the data models at:
            https://docs.python.org/3/reference/datamodel.html or a guide
            about passing references as arguments here:
            https://realpython.com/python-pass-by-reference/
        II.
            Tab (\t) is a quite common CSV delimiter, therefore greenops uses
            it, however the original name of CSV refers to 'comma separated
            values'. Some locales uses colon to split the number's whole and
            decimal parts while on the other hand some services, like Google
            Drive for example doesn't handle other CSV seprator than colon.

        See Also
        --------
            Create a custom log setting : LogSettings class
        """

        # pylint: disable=too-many-arguments
        #         Number of argmunsts fits the requirements of this object.

        super().__init__(output_file_name, watch, device_data, csv_delimiter,
                         log_settings, instant_log)

        self.change_model(torch_model)
        self.__current_stage = current_stage
        self.__last_device = None


    def change_model(self, torch_model : torch.nn.Module):
        """
        Change the model
        ================

        Parameters
        ----------
        torch_model : torch.nn.Module
            The new PyTorch or Fast.AI model to cooperate with.
        """

        self.__torch_model = torch_model
        self.__torch_model.register_forward_hook(self.__update_hook_forward)
        self.__torch_model.register_backward_hook(self.__update_hook_backward)
        self.__last_device = None


    @property
    def current_stage(self) -> str:
        """
        Get current stage
        =================

        Returns
        -------
        str
            The name of the current stage.
        """

        return self.__current_stage


    @current_stage.setter
    def current_stage(self, new_stage : str):
        """
        Set current stage
        =================

        Parameters
        -------
        new_stage : str
            The name of the new stage.
        """

        self.__current_stage = new_stage


    def __perform_update(self, device : torch.device, now : float,
                         prefix : str = '', suffix : str = ''):
        """
        Perform update
        ==============

        Parameters
        ----------
        device : torch.device
            Device to log to.
        now : float
            Timestamp to use.
        prefix : str, optional (empty string if omitted)
            Prefix set by the caller function to distinguish inner stages.
        suffix : str, optional (empty string if omitted)
            Suffix set by the caller function to distinguish inner stages.
        """

        # pylint: disable=no-member
        #         In fact torch has a member called device.

        stage_name = prefix + self.__current_stage + suffix
        device_index = 0
        d_name = 'unknown_torch'
        d_consumption = DEFAULT_CPU_WATTS
        try:
            device_index = int(device.index)
        except (TypeError, ValueError):
            pass
        if device.type == 'cuda':
            d_name = Context.get_gpu()[device_index].short_name
            d_consumption = Context.get_gpu()[device_index].consumption
        elif device.type == 'cpu':
            d_name = Context.get_cpu()[device_index].short_name
            d_consumption = Context.get_cpu()[device_index].consumption
        if not super().stage_exists(stage_name):
            super().create_stage(stage_name)
        if super()._get_last_update(stage_name) > 0:
            time_delta = now - super()._get_last_update(stage_name)
            super()._add_data_row(LogRow(now, stage_name, d_name,
                            d_consumption, super()._get_epoch(stage_name),
                            time_delta, super()._get_watch_values()))
        super()._increase_epoch(stage_name, 1)
        super()._set_last_update(stage_name, now)


    def __update_hook_backward(self, model : torch.nn.Module, inputs : tuple,
                               outputs : tuple):
        """
        Backward hook
        =============

        Parameters
        ----------
        model : torch.nn.Module
            The model.
        input : tuple
            The input tensors.
        output : tuple
            The output tensors.

        Notes
        -----
            This function meets the requirements of PytTorch. Please consult:
            https://pytorch.org/tutorials/beginner/former_torchies/nnft_tutorial.html
        """

        # pylint: disable=unused-argument
        #         Arguments are required due to compatibility.

        now = time()
        if self.__last_device is not None:
            self.__perform_update(self.__last_device, now, suffix='_backward')


    def __update_hook_forward(self, model : torch.nn.Module,
                              inputs : torch.Tensor, outputs : torch.Tensor):
        """
        Forward hook
        ============

        Parameters
        ----------
        model : torch.nn.Module
            The model.
        input : torch.Tensor
            The input tensors.
        output : torch.Tensor
            The output tensors.

        Notes
        -----
            This function meets the requirements of PytTorch. Please consult:
            https://pytorch.org/docs/stable/generated/torch.nn.modules.module.register_module_forward_hook.html
        """

        # pylint: disable=unused-argument
        #         Arguments are required due to compatibility.

        now = time()
        if isinstance(outputs, torch.Tensor):
            self.__last_device = outputs.device
            self.__perform_update(outputs.device, now, suffix='_forward')
