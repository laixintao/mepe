class MepeException(Exception):
    pass


class MetricsFetchException(MepeException):
    """Can't fetch metrics"""
