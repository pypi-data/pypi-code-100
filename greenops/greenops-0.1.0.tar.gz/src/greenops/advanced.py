"""
greenops
--------

Software to measure the footprints of deep learning models at training,
testing and evaluating to reduce energy consumption and carbon footprints.

Copyright rixel 2021
Distributed under the MIT License.
See accompanying file LICENSE.

File: submodule advanced
"""

from threading import Thread

from .measure import DEFAULT_STAGE_NAME, Measure


class ThreadMeasure(Measure):
    """
    Maintain measurement process with threading
    ===========================================
    """

    def create_stage(self, stage_name : str):
        """
        Create a new stage or re-initialize an existing stage
        =====================================================

        Parameters
        ----------
        stage_name : str
            Stage name to create or re-initialize.
        """

        Thread(target=super().create_stage, args=(stage_name, )).start()


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

        Thread(target=super().reset, args=(stage_name, )).start()


    def save_new_rows(self, stage_name : str = None):
        """
        Save new rows
        =============

        Parameters
        ----------
        stage_name : str
            Name of the stage to save new rows in.
        """

        Thread(target=super().save_new_rows, args=(stage_name, )).start()


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

        Thread(target=super().save_stats, args=(file_name, )).start()


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

        Thread(target=super().start, args=(stage_name, )).start()


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

        Thread(target=super().stop, args=(stage_name, )).start()


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

        Thread(target=super().update, args=(stage_name, )).start()
