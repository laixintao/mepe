import logging
import requests
from . import exceptions
import prometheus_client
from prometheus_client.parser import text_string_to_metric_families
from typing import List

logger = logging.getLogger(__name__)


def fetch_metrics_url(url) -> List["prometheus_client.metrics_core.Metric"]:
    resp = requests.get(url)

    if resp.status_code != 200:
        raise exceptions.MetricsFetchException(
            f"Can not fetch exceptions, status_code={resp.status_code},"
            f" error={resp.text}"
        )

    metrics_text = resp.text

    logger.info(f"Successfully fetch the metrics, {len(metrics_text)=}, parsing...")

    metrics = text_string_to_metric_families(metrics_text)
    # merge metrics with the same name, it seems that prometheus_client didn't
    # merge them correctly

    merge_dict = {}
    for m in metrics:
        merge_dict.setdefault(m.name, []).append(m)

    unique_metrics = list()
    for values in merge_dict.values():
        samples = []
        for m in values:
            samples.extend(m.samples)

        selected_metric = _select_metric(values)
        selected_metric.samples = samples
        unique_metrics.append(selected_metric)
    return unique_metrics


def _select_metric(values):
    for v in values:
        if v.type != "unknown":
            return v
    return values[0]
