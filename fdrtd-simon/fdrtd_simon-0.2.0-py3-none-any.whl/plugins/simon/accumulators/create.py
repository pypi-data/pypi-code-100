import fdrtd


def create(accumulator_name):

    if accumulator_name == 'BasicMinMax':
        from fdrtd.plugins.simon.accumulators.accumulator_basic_minimum_maximum import AccumulatorBasicMinimumMaximum
        return AccumulatorBasicMinimumMaximum

    if accumulator_name == 'BasicSum':
        from fdrtd.plugins.simon.accumulators.accumulator_basic_sum import AccumulatorBasicSum
        return AccumulatorBasicSum

    if accumulator_name == 'SetIntersection':
        from fdrtd.plugins.simon.accumulators.accumulator_set_intersection import AccumulatorSetIntersection
        return AccumulatorSetIntersection

    if accumulator_name == 'SetIntersectionSize':
        from fdrtd.plugins.simon.accumulators.accumulator_set_intersection_size import AccumulatorSetIntersectionSize
        return AccumulatorSetIntersectionSize

    if accumulator_name == 'StatisticsBivariate':
        from fdrtd.plugins.simon.accumulators.accumulator_statistics_bivariate import AccumulatorStatisticsBivariate
        return AccumulatorStatisticsBivariate

    if accumulator_name == 'StatisticsFrequency':
        from fdrtd.plugins.simon.accumulators.accumulator_statistics_frequency import AccumulatorStatisticsFrequency
        return AccumulatorStatisticsFrequency

    if accumulator_name == 'StatisticsUnivariate':
        from fdrtd.plugins.simon.accumulators.accumulator_statistics_univariate import AccumulatorStatisticsUnivariate
        return AccumulatorStatisticsUnivariate

    raise fdrtd.server.exceptions.NotAvailable(accumulator_name)
