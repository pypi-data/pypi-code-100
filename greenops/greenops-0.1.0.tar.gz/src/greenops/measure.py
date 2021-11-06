"""
greenops
--------

Software to measure the footprints of deep learning models at training,
testing and evaluating to reduce energy consumption and carbon footprints.

Copyright rixel 2021
Distributed under the MIT License.
See accompanying file LICENSE.

File: submodule measure
"""


from time import asctime, gmtime, localtime, strftime, time

from .context import Context
from .datamodel import DeviceData
from .exceptions import GreenOpsException
from .functions import extensionify_file, join_any, ws_to_kwh


DEFAULT_INCLUDE_DEVICE = True
DEFAULT_INCLUDE_HEADER = True
DEFAULT_INCLUDE_TIME = True
DEFAULT_INCLUDE_STAGE = True
DEFAULT_INSTANT_LOG = True
DEFAULT_STAGE_NAME = 'main'
TIME_FORMAT_GLOBAL = 'utc'
TIME_FORMAT_LOCAL = 'local'
TIME_FORMAT_TIMESTAMP = 'timestamp'


# pylint: disable=too-many-lines
#         Without docstrings this file is under 1000 lines.


class LogRow:
    """
    Represent a row of the log
    ==========================
    """

    def __init__(self, row_time : float, stage : str, device : str,
                 consumption : float, epoch : int, time_delta : float,
                 watch_values : list):
        """
        Initialize the object
        =====================

        Parameters
        ----------
        row_time : float
            Timestamp when the row was generated.
        stage : str
            Name of the stage where the row belongs to.
        device : str
            Name of the device of that was measured.
        consumption : float
            Consumption that was measured.
        epoch : int
            Number of the epoch.
        time_delta : float
            The measured time.
        watch_values : list
            Content of the watched values.

        See Also
        --------
            How watch work : Measure
        """

        # pylint: disable=too-many-arguments
        #         Number of argmunsts fits the requirements of this object.

        self.__consumption = consumption
        self.__device = device
        self.__epoch = epoch
        self.__row_time = row_time
        self.__stage = stage
        self.__time_delta = time_delta
        self.__watch_values = watch_values

    @property
    def consumption(self) -> float:
        """
        Get consumption
        ===============

        Returns
        -------
        float
            The measured consumption.
        """

        return self.__consumption


    @property
    def device(self) -> str:
        """
        Get device
        ==========

        Returns
        -------
        float
            The measured device.
        """

        return self.__device


    @staticmethod
    def device_consumption_from_context(device_str : str) -> tuple:
        """
        Calculate consumption from context
        ==================================

        Parameters
        ----------
        device_str : str
            Device name to search for.

        Returns
        -------
        tuple(str, float)
            Tuple of the name of the device and its base consumption.

        Raises
        ------
        ValueError
            When the data doesn't satisfy the needs to identify a device.
        """

        # pylint: disable=too-many-branches
        #         Wouldn't have sense to make more functions.

        Context.init()
        device = None
        consumption = None
        if device_str == 'cpu': # Support for torch.device
            device = 'cpu'
            consumption = Context.get_cpu()[0].consumption
        if device_str == 'gpu': # Support for lazy data scientists :)
            device = 'gpu:0'
            consumption = Context.get_gpu()[0].consumption
        else:
            device_parts = device_str.split(':')
            if len(device_parts) == 2:
                pos = None
                try:
                    pos = int(device_parts[1])
                except ValueError:
                    pass
                if pos is not None:
                    if device_parts[0] == 'cpu':
                        if pos < len(Context.get_cpu()):
                            device = device_str
                            consumption = Context.get_cpu()[pos].consumption
                    elif device_parts[0] == 'gpu':
                        if pos < len(Context.get_gpu()):
                            device = device_str
                            consumption = Context.get_gpu()[pos].consumption
            elif len(device_parts) == 1:
                for i, cpu in enumerate(Context.get_cpu()):
                    if cpu.long_name == device_str:
                        device = 'cpu:{}'.format(i)
                        consumption = cpu.consumption
                    elif cpu.short_name == device_str:
                        device = 'cpu:{}'.format(i)
                        consumption = cpu.consumption
                for i, gpu in enumerate(Context.get_gpu()):
                    if gpu.long_name == device_str:
                        device = 'cpu:{}'.format(i)
                        consumption = gpu.consumption
                    elif gpu.short_name == device_str:
                        device = 'gpu:{}'.format(i)
                        consumption = gpu.consumption
        if device is None or consumption is None:
            raise ValueError('greenops.measure.LogRow.' +
                  'device_consumption_from_context: Cannot identify device from'
                  + 'invalid data.')
        return device, consumption


    @staticmethod
    def device_from_parts(device_type : str, device_id : int) -> str:
        """
        Get device string from parts
        ============================

        Parameters
        ----------
        device_type : str
            The type of the device.
        device_id : int
            The ID of the device.

        Returns
        -------
        str
            Name of the device
        """

        return '{}:{}'.format(device_type, device_id)


    @property
    def epoch(self) -> int:
        """
        Get epoch number
        ================

        Returns
        -------
        int
            The epoch identifier of the measurement.
        """

        return self.__epoch


    @property
    def row_time(self) -> int:
        """
        Get measurement's time
        ======================

        Returns
        -------
        int
            The time of the measurement.
        """

        return self.__row_time


    @property
    def stage(self) -> str:
        """
        Get stage name
        ==============

        Returns
        -------
        str
            The identifier of the stage of the measurement.
        """

        return self.__stage


    @property
    def time_delta(self) -> float:
        """
        Get time delta
        ==============

        Returns
        -------
        float
            The measured time delta in seconds.
        """

        return self.__time_delta


    @property
    def watch_values(self) -> list:
        """
        Get watched values
        ==================

        Returns
        -------
        list[any]
            List of the content of the watched values at the time of the
            measurement.

        See Also
        --------
            How watch work : Measure
        """

        return self.__watch_values.copy()


class LogSettings:
    """
    Represent settings for logging
    ==============================
    """

    # pylint: disable=too-many-instance-attributes
    #         It could be transformed to functions but wouldn't have sense.

    def __init__(self, include_header : bool = DEFAULT_INCLUDE_HEADER,
                 include_time : bool = DEFAULT_INCLUDE_TIME,
                 time_format : str = TIME_FORMAT_TIMESTAMP,
                 include_stage : bool = DEFAULT_INCLUDE_STAGE,
                 include_device : bool = DEFAULT_INCLUDE_DEVICE,
                 watch_keys : list = None):
        """
        Initialize the object
        =====================

        Parameters
        ----------
        include_header : bool, optional (DEFAULT_INCLUDE_HEADER if omitted)
            Whether to inlude header into the log or not.
        include_time : bool, optional (DEFAULT_INCLUDE_TIME if omitted)
            Whether to inlude time into the log or not.
        time_format : bool, optional (TIME_FORMAT_TIMESTAMP if omitted)
            Format of time in the log.
        include_stage : bool, optional (DEFAULT_INCLUDE_STAGE if omitted)
            Whether to inlude stage name into the log or not.
        include_device : bool, optional (DEFAULT_INCLUDE_DEVICE if omitted)
            Whether to inlude device name into the log or not.
        watch_keys : list, optional (None if omitted)
            Name of variables to save into the log.

        See Also
        --------
            How watch work : Measure
        """

        # pylint: disable=too-many-arguments
        #         Number of parameters accords to number of attributes.

        self.__include_header = include_header
        self.__include_time = include_time
        self.__time_func = LogSettings.compile_time_function_(time_format)
        self.__time_format = time_format
        self.__include_stage = include_stage
        self.__include_device = include_device
        if watch_keys is None:
            self.__watch_keys = []
        else:
            self.__watch_keys = watch_keys
        self.__line_function = self.compile()
        self.__header = self.create_header()


    def compile(self) -> callable:
        """
        Compile row creator function
        ============================

        Returns
        -------
        callable
            The function that creates a log row which accords to the settings.

        See Also
        --------
            Function signature (interface) : self.line_as_list()
        """

        # pylint: disable=too-many-branches
        #         Developers of greenops agree with pylint but what to do.

        result = lambda r: r # It will be changed anyway
        if self.__include_time:
            if self.__include_stage:
                if self.__include_device:
                    if self.include_watch:
                        result = \
                        lambda r: [self.__time_func(r.row_time), r.stage,
                                   r.device, r.consumption, r.epoch,
                                   r.time_delta] + r.watch_values
                    else:
                        result = \
                        lambda r: [self.__time_func(r.row_time), r.stage,
                                   r.device, r.consumption, r.epoch,
                                   r.time_delta]
                else:
                    if self.include_watch:
                        result = \
                        lambda r: [self.__time_func(r.row_time), r.stage,
                                   r.consumption, r.epoch, r.time_delta
                                   ] + r.watch_values
                    else:
                        result = \
                        lambda r: [self.__time_func(r.row_time), r.stage,
                                   r.consumption, r.epoch, r.time_delta]
            else:
                if self.__include_device:
                    if self.include_watch:
                        result = \
                        lambda r: [self.__time_func(r.row_time), r.device,
                                   r.consumption, r.epoch, r.time_delta
                                   ] + r.watch_values
                    else:
                        result = \
                        lambda r: [self.__time_func(r.row_time), r.device,
                                   r.consumption, r.epoch, r.time_delta]
                else:
                    if self.include_watch:
                        result = \
                        lambda r: [self.__time_func(r.row_time), r.consumption,
                                   r.epoch, r.time_delta
                                   ] + r.watch_values
                    else:
                        result = \
                        lambda r: [self.__time_func(r.row_time), r.consumption,
                                   r.epoch, r.time_delta]
        else:
            if self.__include_stage:
                if self.__include_device:
                    if self.include_watch:
                        result = \
                        lambda r: [r.stage, r.device, r.consumption, r.epoch,
                                   r.time_delta] + r.watch_values
                    else:
                        result = \
                        lambda r: [r.stage, r.device, r.consumption, r.epoch,
                                   r.time_delta]
                else:
                    if self.include_watch:
                        result = \
                        lambda r: [r.stage, r.consumption, r.epoch, r.time_delta
                                   ] + r.watch_values
                    else:
                        result = \
                        lambda r: [r.stage, r.consumption, r.epoch,
                                   r.time_delta]
            else:
                if self.__include_device:
                    if self.include_watch:
                        result = \
                        lambda r: [r.device, r.consumption, r.epoch,
                                   r.time_delta] + r.watch_values
                    else:
                        result = \
                        lambda r: [r.device, r.consumption, r.epoch,
                                   r.time_delta]
                else:
                    if self.include_watch:
                        result = \
                        lambda r: [r.consumption, r.epoch, r.time_delta
                                   ] + r.watch_values
                    else:
                        result = \
                        lambda r: [r.consumption, r.epoch, r.time_delta]
        return result


    def create_header(self) -> list:
        """
        Create the header
        =================

        Returns
        -------
        list
            List of header names that matches settings.
        """

        # pylint: disable=too-many-branches
        #         Developers of greenops agree with pylint but what to do.

        result = [] # It will be changed anyway
        if self.__include_time:
            if self.__include_stage:
                if self.__include_device:
                    if self.include_watch:
                        result = ['time', 'stage', 'device', 'consumption',
                                  'epoch', 'time_delta'
                                  ] + self.__watch_keys
                    else:
                        result = ['time', 'stage', 'device', 'consumption',
                                  'epoch', 'time_delta']
                else:
                    if self.include_watch:
                        result = ['time', 'stage', 'consumption', 'epoch',
                                  'time_delta'] + self.__watch_keys
                    else:
                        result = ['time', 'stage','consumption', 'epoch',
                                  'time_delta']
            else:
                if self.__include_device:
                    if self.include_watch:
                        result = ['time', 'device','consumption', 'epoch',
                                  'time_delta'] + self.__watch_keys
                    else:
                        result = ['time', 'device', 'consumption', 'epoch',
                                  'time_delta']
                else:
                    if self.include_watch:
                        result = ['time', 'consumption', 'epoch', 'time_delta'
                                  ] + self.__watch_keys
                    else:
                        result = ['time', 'consumption', 'epoch', 'time_delta']
        else:
            if self.__include_stage:
                if self.__include_device:
                    if self.include_watch:
                        result = ['stage', 'device', 'consumption', 'epoch',
                                  'time_delta'] + self.__watch_keys
                    else:
                        result = ['stage', 'device', 'consumption', 'epoch',
                                  'time_delta']
                else:
                    if self.include_watch:
                        result = ['stage', 'consumption', 'epoch', 'time_delta'
                                  ] + self.__watch_keys
                    else:
                        result = ['stage', 'consumption', 'epoch', 'time_delta']
            else:
                if self.__include_device:
                    if self.include_watch:
                        result = ['device', 'consumption', 'epoch', 'time_delta'
                                  ] + self.__watch_keys
                    else:
                        result = ['device', 'consumption', 'epoch',
                                  'time_delta']
                else:
                    if self.include_watch:
                        result = ['consumption', 'epoch', 'time_delta'
                                   ] + self.__watch_keys
                    else:
                        result = ['consumption', 'epoch', 'time_delta']
        return result


    @property
    def header_as_list(self) -> list:
        """
        Get header fields as list
        =========================

        Returns
        -------
        list
            List of header names that matches settings.
        """

        return self.__header.copy()


    @property
    def include_device(self) -> bool:
        """
        Get device inclusion state
        ==========================

        Returns
        -------
        bool
            True if device name should be included, False if not.
        """

        return self.__include_device


    @property
    def include_header(self) -> bool:
        """
        Get header inclusion state
        ==========================

        Returns
        -------
        bool
            True if header should be included, False if not.
        """

        return self.__include_header


    @property
    def include_stage(self) -> bool:
        """
        Get stage identifier's inclusion state
        ======================================

        Returns
        -------
        bool
            True if stage name should be included, False if not.
        """

        return self.__include_stage


    @property
    def include_time(self) -> bool:
        """
        Get time inclusion state
        ========================

        Returns
        -------
        bool
            True if time should be included, False if not.
        """

        return self.__include_time


    @property
    def include_watch(self) -> bool:
        """
        Get inclusion state of the watched values
        =========================================

        Returns
        -------
        bool
            True if watched values should be included, False if not.

        See Also
        --------
            How watch work : Measure
        """

        return len(self.__watch_keys) == 0


    def line_as_list(self, row : LogRow) -> list:
        """
        Transform a log row to a list
        =============================

        Parameters
        ----------
        row : LogRow
            Row to Transform.

        Returns
        -------
        list
            List that mathces log settings.
        """

        return self.__line_function(row)


    @property
    def time_format(self) -> str:
        """
        Get time format
        ===============

        Returns
        -------
        str
            Format string to convert time.
        """

        return self.__time_format


    @property
    def watch_keys(self) -> list:
        """
        Get watched keys
        ================

        Returns
        -------
        list
            List of watched keys.

        See Also
        --------
            How watch work : Measure
        """

        return self.__watch_keys.copy()


    @staticmethod
    def compile_time_function_(time_format : str) -> callable:
        """
        Compile time conversion function
        ================================

        Parameters
        ----------
        time_format : str
            Format string that specifies time conversion.

        Returns
        -------
        callable
            A function that accords to the format string.

        Notes
        -----
        I.
            This function doesn't raise error in case of an invalid string
            since it has a default case, converting time to second precision
            timestamp.
        II.
            Custom time formats can based on local or global time as well. To
            access local time use 'local:custom_time_format', to access global
            (UTC, GMT) time, use 'global:custom_time_format'.
        III.
            To make custom time format please consult Python's official
            documentiation about time.strftime() at:
            https://docs.python.org/3/library/time.html#time.strftime
        """

        result = lambda t: int(round(t)) # Default and ultimate fallback
        if time_format == TIME_FORMAT_GLOBAL:
            result = lambda t: asctime(gmtime(t))
        elif time_format == TIME_FORMAT_LOCAL:
            result = lambda t: strftime('%x %X', localtime())
        elif time_format.startswith('global:'):
            time_str = time_format.replace('global:', '')
            result = lambda t: strftime(time_str, gmtime())
        elif time_format.startswith('local:'):
            time_str = time_format.replace('local:', '')
            result = lambda t: strftime(time_str, localtime())
        return result


class Measure:
    """
    Maintain measurement process
    ============================
    """

    # pylint: disable=too-many-instance-attributes
    #         It could be transformed to functions but wouldn't have sense.

    def __init__(self, output_file_name : str = None, watch : dict = None,
                 device_data : any = None, csv_delimiter : str = '\t',
                 log_settings : LogSettings = None,
                 instant_log : bool = DEFAULT_INSTANT_LOG):
        """
        Initialize the object
        =====================

        Parameters
        ----------
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
            consult Python's official documentation about the data models at:
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
        #         Number of parameters accords to number of attributes.

        if output_file_name is None:
            self.__output_file_name = 'greenops_{}.csv'.format(int(time()))
        else:
            self.__output_file_name = extensionify_file(output_file_name, 'csv')
        if watch is None:
            self.__watch = {}
        else:
            self.__watch = watch
        self.__device_data = None
        if isinstance(device_data, DeviceData):
            self.__device_data = device_data
        elif isinstance(device_data, str):
            device, consumption = LogRow.device_consumption_from_context(
                                                                    device_data)
            self.__device_data = DeviceData(device, device, consumption)
        Context.init()
        if self.__device_data is None: # Default and ultimate fallback
            self.__device_data = Context.get_cpu()[0]
        self.__csv_delimiter = csv_delimiter
        if log_settings is None:
            self.__log_settings = LogSettings(watch_keys=list(
                                                        self.__watch.keys()))
        else:
            self.__log_settings = log_settings
        self.__instant_log = instant_log
        self.reset()


    def create_stage(self, stage_name : str):
        """
        Create a new stage or re-Initialize an existing stage
        =====================================================

        Parameters
        ----------
        stage_name : str
            Stage name to create or re-Initialize.
        """

        self.__data[stage_name] = []
        self.__data_pointers[stage_name] = 0
        self.__epochs[stage_name] = 0
        self.__last_starts[stage_name] = 0
        self.__last_updates[stage_name] = 0


    @property
    def csv_delimiter(self) -> str:
        """
        Get CSV delimiter
        =================

        Returns
        -------
        str
            The CSV delimiter.
        """

        return self.__csv_delimiter


    @property
    def instant_log(self) -> bool:
        """
        Get instant log state
        =====================

        Returns
        -------
        bool
            True if instant logging is turned on, False if not.
        """

        return self.__instant_log


    @property
    def log_settings(self) -> LogSettings:
        """
        Get log settings
        ================

        Returns
        -------
        LogSettings
            The log settings object.
        """

        return self.__log_settings


    @property
    def output_file_name(self) -> str:
        """
        Get output file name
        ====================

        Returns
        -------
        str
            The name of the log output file.
        """

        return self.__output_file_name


    def reset(self, stage_name : str = None):
        """
        Reset the object or reset a stage
        =================================

        Parameters
        ----------
        stage_name : str, optional (None if omitted)
            If stage_name is given, resets the stage. If it is omitted the whole
            object get resetted. It means, all stages will be deleted.
        """

        if stage_name is None:
            self.__data = {}
            self.__data_pointers = {}
            self.__epochs = {}
            self.__first_row = True
            self.__last_starts = {}
            self.__last_updates = {}
        else:
            self.create_stage(stage_name)


    def save_new_rows(self, stage_name : str):
        """
        Save new rows
        =============

        Parameters
        ----------
        stage_name : str
            Name of the stage to save new rows in.
        """

        # pylint: disable=attribute-defined-outside-init
        #         In fact __first_row is set in reset() which is called in
        #         __init__().

        with open(self.__output_file_name, 'a', encoding='utf8') as outstream:
            if self.__first_row:
                self.__first_row = False
                if self.__log_settings.include_header:
                    outstream.write('{}\n'.format(join_any(self.__csv_delimiter,
                                        self.__log_settings.header_as_list)))
            while self.__data_pointers[stage_name] <\
                                                len(self.__data[stage_name]):
                outstream.write('{}\n'.format(join_any(self.__csv_delimiter,
                        self.__log_settings.line_as_list(self.__data[stage_name]
                        [self.__data_pointers[stage_name]]))))
                self.__data_pointers[stage_name] += 1


    def save_stats(self, file_name : str = None):
        """
        Save logs
        =========

        Parameters
        ----------
        file_name : str, optional (None if omitted)
            File to save logs to. If omitted, the name of the output file is
            used.
        """

        if file_name is None:
            the_file = self.__output_file_name
        else:
            the_file = extensionify_file(file_name, 'csv')
        with open(the_file, 'w', encoding='utf8') as outstream:
            if self.__log_settings.include_header:
                outstream.write('{}\n'.format(join_any(self.__csv_delimiter,
                                        self.__log_settings.header_as_list)))
            for stage_data in self.__data.values():
                for row in stage_data:
                    outstream.write('{}\n'.format(join_any(self.__csv_delimiter,
                                        self.__log_settings.line_as_list(row))))


    def stage_exists(self, stage_name : str) -> bool:
        """
        Get whether a stage exists
        ==========================

        Parameters
        ----------
        stage_name : str
            Name of the stage to search for.

        Returns
        -------
        bool
            True if the stage exists, False if not.
        """

        return all([stage_name in self.__data.keys(),
                    stage_name in self.__data_pointers.keys(),
                    stage_name in self.__last_updates.keys(),
                    stage_name in self.__last_starts.keys(),
                    stage_name in self.__epochs.keys()])


    def start(self, stage_name : str = DEFAULT_STAGE_NAME):
        """
        Start a measure
        ===============

        Parameters
        ----------
        stage_name : str, optional (DEFAULT_STAGE_NAME if omitted)
            Name of the stage to start.

        See Also
        --------
            Stop started measure    : self.stop()
            Loop style measure      : self.update()

        Notes
        -----
            If the given stage not yet exists, this function attempts to create
            it.
        """

        if not self.stage_exists(stage_name):
            self.create_stage(stage_name)
        self.__last_starts[stage_name] = time()


    @property
    def stats_summary(self) -> str:
        """
        Get a shallow summary of all measure
        ====================================

        Returns
        -------
        str
            Summary in human readable form.

        Notes
        -----
            You can get much more detailed data from the created log file(s).
        """

        Context.init()
        total_times = 0.0
        total_consumption = 0.0
        total_cost = 0.0
        stage_times = {}
        stage_consumptions = {}
        for stage, stage_data in self.__data.items():
            stage_times[stage] = 0.0
            stage_consumptions[stage] = 0.0
            for row in stage_data:
                total_times += row.time_delta
                stage_times[stage] += row.time_delta
                consumption = row.time_delta * row.consumption
                stage_consumptions[stage] += consumption

        result = 'greenops.measure.Measure stats summary:\n\nStages:\n'
        for stage, stage_time in stage_times.items():
            kwh = ws_to_kwh(stage_consumptions[stage])
            total_consumption += kwh
            usd = Context.get_power_price().price * kwh
            total_cost += usd
            result += ' --- Stage "{}" lasted {:.4f} seconds and '.format(
                      stage, stage_time
                      ) + 'consumed {:.2f} kWh. Cost: {:.2f} USD\n'.format(kwh,
                      usd)
        result += '\n\nTotal time: {:.4f} seconds\nTotal consumption '.format(
                  total_times) + '{:.2f} kWh\nTotal cost {:.2f} '.format(
                  total_consumption, total_cost) + 'USD\n\n{}\n\n{}'.format(
                  Context.get_power_price(), Context.get_power_sources())
        return result


    def stop(self, stage_name : str = DEFAULT_STAGE_NAME):
        """
        Stop a measure
        ==============

        Parameters
        ----------
        stage_name : str, optional (DEFAULT_STAGE_NAME if omitted)
            Name of the stage to stop.

        Raises
        ------
        GreenOpsException
            If the measure in the given stage is not started yet.

        See Also
        --------
            Start a measure     : self.start()
            Loop style measure  : self.update()
        """

        # pylint: disable=raise-missing-from
        #         The real source of the error is nat that important.

        now = time()
        try:
            time_delta = now - self.__last_starts[stage_name]
        except KeyError:
            raise GreenOpsException('greenops.measure.Measure.stop(): Cannot ' +
                                    'stop a non-running epoch period.')
        if self.__last_starts[stage_name] == 0:
            raise GreenOpsException('greenops.measure.Measure.stop(): Cannot ' +
                                    'stop a non-running epoch period.')
        self._add_data_row(LogRow(now, stage_name,
                                  self.__device_data.short_name,
                                  self.__device_data.consumption,
                                  self.__epochs[stage_name], time_delta,
                                  list(self.__watch.values())))
        self.__epochs[stage_name] += 1


    def update(self, stage_name : str = DEFAULT_STAGE_NAME):
        """
        Update a stage measured with loop
        =================================

        Parameters
        ----------
        stage_name : str, optional (DEFAULT_STAGE_NAME if omitted)
            Name of the stage to measure as a loop.

        See Also
        --------
            Start a duration style measure  : self.start()
            Stop a duration style measure   : self.stop()

        Notes
        -----
            If the given stage not yet exists, this function attempts to create
            it.
        """

        now = time()
        if not self.stage_exists(stage_name):
            self.create_stage(stage_name)
        if self.__last_updates[stage_name] > 0:
            time_delta = now - self.__last_updates[stage_name]
            self._add_data_row(LogRow(now, stage_name,
                                      self.__device_data.short_name,
                                      self.__device_data.consumption,
                                      self.__epochs[stage_name], time_delta,
                                      list(self.__watch.values())))
        self.__epochs[stage_name] += 1
        self.__last_updates[stage_name] = now


    @property
    def watch_keys(self) -> list:
        """
        Get names of watched variables
        ==============================

        Returns
        -------
        list
            List of keys of the watched variables.
        """

        return list(self.__watch.keys())


    def _add_data_row(self, row : LogRow):
        """
        Add data row to the log
        =======================

        Parameters
        ----------
        row : LogRow
            Data row to add to the log.

        Notes
        -----
        I.
            According to Python's naming conventions this is a private function,
            please don't call it directly even if you can.
        II.
            Outside call can lead to KeyError.
        """

        self.__data[row.stage].append(row)
        if self.__instant_log:
            self.save_new_rows(row.stage)


    def _get_last_update(self, stage_name : str) -> float:
        """
        Get timestamp of the last update of the stage
        =============================================

        Parameters
        ----------
        stage_name : str
            Name of the stage to get.

        Returns
        -------
        float
            Timestamp of the last update.

        Notes
        -----
        I.
            According to Python's naming conventions this is a private function,
            please don't call it directly even if you can.
        II.
            Outside call can lead to KeyError.
        """

        return self.__last_updates[stage_name]


    def _get_epoch(self, stage_name : str) -> int:
        """
        Get epoch ID
        ============

        Parameters
        ----------
        stage_name : str
            Name of the stage to get.

        Returns
        -------
        int
            The number of the actual epoch.

        Notes
        -----
        I.
            According to Python's naming conventions this is a private function,
            please don't call it directly even if you can.
        II.
            Outside call can lead to KeyError.
        """

        return self.__epochs[stage_name]


    def _get_watch_values(self) -> list:
        """
        Get the content of the watched values
        =====================================

        Returns
        -------
        list
            List of the content of the watched values.

        Notes
        -----
            According to Python's naming conventions this is a private function,
            please don't call it directly even if you can.
        """

        return list(self.__watch.values())


    def _increase_epoch(self, stage_name : str, value : int):
        """
        Increase epoch ID
        =================

        Parameters
        ----------
        stage_name : str
            Name of the stage to increase epoch in.
        value : int
            Value to increase the epoch ID with.

        Notes
        -----
        I.
            According to Python's naming conventions this is a private function,
            please don't call it directly even if you can.
        II.
            Outside call can lead to KeyError.
        """

        self.__epochs[stage_name] += value


    def _set_last_update(self, stage_name : str, new_value : float):
        """
        Set last update
        ===============

        Parameters
        ----------
        stage_name : str
            Name of the stage to get.
        new_value : float
            Timestamp of the update.

        Notes
        -----
            According to Python's naming conventions this is a private function,
            please don't call it directly even if you can.
        """

        self.__last_updates[stage_name] = new_value


    def __str__(self) -> str:
        """
        Information about the object
        ============================

        Returns
        -------
        str
            Human readable description of the object.

        See Also
        --------
            Returned content : self.summary
        """

        return self.stats_summary
