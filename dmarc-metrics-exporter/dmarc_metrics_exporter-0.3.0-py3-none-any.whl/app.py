import argparse
import asyncio
import json
from asyncio import CancelledError
from email.message import EmailMessage
from typing import Any, Callable, Sequence, Tuple

from dmarc_metrics_exporter.deserialization import (
    convert_to_events,
    get_aggregate_report_from_email,
)
from dmarc_metrics_exporter.dmarc_metrics import DmarcMetricsCollection
from dmarc_metrics_exporter.imap_queue import ConnectionConfig, ImapQueue, QueueFolders
from dmarc_metrics_exporter.metrics_persister import MetricsPersister
from dmarc_metrics_exporter.prometheus_exporter import PrometheusExporter


def main(argv: Sequence[str]):
    parser = argparse.ArgumentParser(
        description="Monitor an IMAP account for DMARC aggregate reports and "
        "provide a Prometheus endpoint for metrics derived from incoming "
        "reports."
    )
    parser.add_argument(
        "--configuration",
        type=argparse.FileType("r"),
        default="/etc/dmarc-metrics-exporter.json",
        help="Configuration file",
    )
    args = parser.parse_args(argv)

    configuration = json.load(args.configuration)
    args.configuration.close()
    app = App(
        prometheus_addr=(
            configuration.get("listen_addr", "127.0.0.1"),
            configuration.get("port", 9797),
        ),
        imap_queue=ImapQueue(
            connection=ConnectionConfig(**configuration["imap"]),
            folders=QueueFolders(**configuration.get("folders", {})),
            poll_interval_seconds=configuration.get("poll_interval_seconds", 60),
        ),
        metrics_persister=MetricsPersister(
            configuration.get(
                "metrics_db", "/var/lib/dmarc-metrics-exporter/metrics.db"
            )
        ),
    )

    asyncio.run(app.run())


class App:
    def __init__(
        self,
        *,
        prometheus_addr: Tuple[str, int],
        imap_queue: ImapQueue,
        metrics_persister: MetricsPersister,
        exporter_cls: Callable[[DmarcMetricsCollection], Any] = PrometheusExporter,
        autosave_interval_seconds: float = 60,
    ):
        self.prometheus_addr = prometheus_addr
        self.exporter = exporter_cls(DmarcMetricsCollection())
        self.imap_queue = imap_queue
        self.exporter_cls = exporter_cls
        self.metrics_persister = metrics_persister
        self.autosave_interval_seconds = autosave_interval_seconds

    async def run(self):
        self.exporter = self.exporter_cls(self.metrics_persister.load())
        try:
            self.imap_queue.consume(self.process_email)
            async with self.exporter.start_server(*self.prometheus_addr):
                while True:
                    await asyncio.sleep(self.autosave_interval_seconds or 60)
                    if self.autosave_interval_seconds:
                        self._save_metrics()
        except CancelledError:
            pass
        finally:
            self._save_metrics()
            await self.imap_queue.stop_consumer()

    def _save_metrics(self):
        with self.exporter.get_metrics() as metrics:
            self.metrics_persister.save(metrics)

    async def process_email(self, msg: EmailMessage):
        for report in get_aggregate_report_from_email(msg):
            for event in convert_to_events(report):
                with self.exporter.get_metrics() as metrics:
                    metrics.update(event)
