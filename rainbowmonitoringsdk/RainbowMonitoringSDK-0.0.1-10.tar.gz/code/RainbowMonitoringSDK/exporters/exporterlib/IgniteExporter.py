"""
This module implements the ignite exporter for the storage layer

"""
import json
import logging
import os
import threading
import time

import requests
from RainbowMonitoringSDK.exporters.Exporter import Exporter


class IgniteExporter(Exporter):
    """
    With this class the agent requests other service(s) through socket connection
    """

    connection_timer = 5
    ignite_request_has_failed = True

    def __init__(self, hostname, port, metric_repr=None):
        self.hostname, self.port, self.metric_repr = hostname, port, metric_repr
        Exporter.__init__(self, "IgniteExporter")

    def update(self, data: dict):
        res = []
        for _, metrics in data.items():
            print(f"Metrics from {_} have {len(metrics)} datapoints")
            for metric_name, metric in metrics.items():
                metric_repr = self.__extract_metric_representation(metric)
                res.append(metric_repr)
        self.metric_repr = res
        self.send_data(res)

    def send_data(self, res):

        IgniteExporter.ignite_request_has_failed = True
        while IgniteExporter.ignite_request_has_failed:
            try:
                payload = {"monitoring": res}
                headers = {'Content-Type': 'text/plain'}
                response = requests.post("http://%s:%s/put" %
                                         (self.hostname, self.port), data=json.dumps(payload), headers=headers)
                logging.info("Ignite server returns %s with the following response: %s" %
                             (response.status_code, response.text))
                IgniteExporter.ignite_request_has_failed = False
            except:
                IgniteExporter.ignite_request_has_failed = True
                logging.error("Error at the API does not respond", exc_info=True)
                # wait for some seconds (< 5 min) to retry to search for ignite exporter
                logging.error("Waiting %s seconds to retry to search for Ignite Exporter" % IgniteExporter.connection_timer)
                time.sleep(IgniteExporter.connection_timer)
                # double the wait
                if IgniteExporter.connection_timer < 300:
                    IgniteExporter.connection_timer *= 2

    def __extract_metric_representation(self, metric):
        metric_repr = metric.to_dict()
        entity_id, entity_type = self.__extract_group_and_entity_from_name(metric.name)
        metric_repr["entityID"] = entity_id
        metric_repr["entityType"] = entity_type
        metric_repr["metricID"] = metric.name
        return metric_repr

    @staticmethod
    def __extract_group_and_entity_from_name(name):
        entity_type = 'FOG_NODE'
        entity_id = os.environ['NODE_ID']  # TODO Find a better way for that
        if '_CGROUP_' in name:
            entity_type = 'CONTAINER'
            index = name.find('_CGROUP_') + len('_CGROUP_')
            entity_id = name[index: index + 12]
        return entity_id, entity_type
