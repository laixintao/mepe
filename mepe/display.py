from typing import List
import prometheus_client


def display(metrics: List["prometheus_client.metrics_core.Metric"]) -> None:
    for metric in metrics:
        display_metric(metric)


def display_metric(metric: "prometheus_client.metrics_core.Metric") -> None:
    print(metric.name)
