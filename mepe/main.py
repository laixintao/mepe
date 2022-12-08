import logging, os
import click
from .scrape import fetch_metrics_url
from .display import display


def config_log(level, location):
    logging.basicConfig(
        level=level,
        filename=os.path.expanduser(location),
        filemode="a",
        format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    )


@click.command()
@click.argument("metrics-url")
@click.option(
    "--log-level", help="CRITICAL ERROR WARNING INFO DEBUG NOTSET", default="DEBUG"
)
@click.option("--log-file", help="File location to log to", default=None)
def main(metrics_url, log_level, log_file):
    if log_file:
        config_log(logging.getLevelName(log_level), log_file)
    logger = logging.getLogger(__name__)
    logger.debug(f"Logging configured with level={log_level}")
    logger.debug(f"Now fetching metrics url={metrics_url}")
    metrics = fetch_metrics_url(metrics_url)
    display(metrics)
