import os


_DEFAULT_BUCKETS = [0.05, 0.1, 0.5, 0.9, 0.95]
_DEFAULT_LABELS = ["method", "route", "http_status", "serviceName", "namespace"]

NAMESPACE = os.getenv("SERVICE_NAME_PREFIX", default="UNDEFINED")
SERVICENAME = os.getenv("SERVICE_NAME", default="UNDEFINED")
DICT_REQURIED_LABELS = {"namespace": NAMESPACE, "serviceName": SERVICENAME}
