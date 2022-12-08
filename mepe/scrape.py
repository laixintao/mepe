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
    return list(metrics)
