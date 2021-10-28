# Ladybug: A Plugin for Environmental Analysis (GPL)
# This file is part of Ladybug.
#
# Copyright (c) 2021, Ladybug Tools.
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Construct a Ladybug data collection from header and values.
-

    Args:
        _header:A Ladybug header object describing the metadata of the data collection.
        _values: A list of numerical values for the data collection.
        _interval_: Text to indicate the time interval of the data collection, which
            determines the type of collection that is output. (Default: hourly).
            _
            Choose from the following:
                - hourly
                - daily
                - monthly
                - monthly-per-hour
            _
            Note that the "hourly" input is also used to represent sub-hourly
            intervals (in this case, the timestep of the analysis period
            must not be 1).

    Returns:
        data: A Ladybug data collection object.
"""

ghenv.Component.Name = "LB Construct Data"
ghenv.Component.NickName = '+Data'
ghenv.Component.Message = '1.3.1'
ghenv.Component.Category = 'Ladybug'
ghenv.Component.SubCategory = '1 :: Analyze Data'
ghenv.Component.AdditionalHelpFromDocStrings = '1'

try:
    from ladybug.datacollection import HourlyContinuousCollection, DailyCollection, \
        MonthlyCollection, MonthlyPerHourCollection
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

try:
    from ladybug_rhino.grasshopper import all_required_inputs
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component):
    inter = _interval_.lower() if _interval_ is not None else 'hourly'
    if inter == 'hourly':
        data = HourlyContinuousCollection(_header, _values)
    elif inter == 'monthly':
        data = MonthlyCollection(
            _header, _values, _header.analysis_period.months_int)
    elif inter == 'daily':
        data = DailyCollection(
            _header, _values, _header.analysis_period.doys_int)
    elif inter == 'monthly-per-hour':
        data = MonthlyPerHourCollection(
            _header, _values, _header.analysis_period.months_per_hour)
    else:
        raise ValueError('{} is not a recongized interval.'.format(_interval_))
