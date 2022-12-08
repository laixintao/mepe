import re
import logging
from typing import List
import prometheus_client
from rich.console import Console
from rich.text import Text

console = Console()
logger = logging.getLogger(__name__)


def display(metrics: List["prometheus_client.metrics_core.Metric"]) -> None:
    for metric in metrics:
        display_metric(metric)


def display_metric(metric: "prometheus_client.metrics_core.Metric") -> None:
    name = Text(metric.name)
    # bold the common prefix which indicates the metrics group

    name.stylize("yellow")

    matcher = re.match(r"(.*?)_", metric.name)
    if matcher:
        prefix = len(matcher.group(1))
        name.stylize("bold", 0, prefix)

    _type = Text(metric.type)
    _type.stylize("magenta")

    unit = Text(metric.unit)
    unit.stylize("blue")

    total_samples = Text(f"{len(metric.samples)} total samples")
    total_samples.stylize("red")

    console.print(name, _type, unit, total_samples)

    doc = Text(metric.documentation)
    doc.stylize("green")
    console.print("  ", doc)

    labels = set()
    for sample in metric.samples:
        labels.update(sample.labels.keys())
    labels_text = Text(",".join(labels))
    if labels_text:
        labels_text.stylize("grey54")
        console.print("  ", labels_text)
