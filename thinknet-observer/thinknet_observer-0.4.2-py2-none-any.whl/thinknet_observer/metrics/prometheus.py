import prometheus_client


httpRequestCounter = prometheus_client.Counter(
    "http_request_total",
    "Number of HTTP requests",
    labelnames=["method", "route", "http_status"],
)

httpRequestDurationMilliSeconds = prometheus_client.Summary(
    "http_response_duration_ms",
    "Duration of HTTP requests in ms",
    labelnames=["method", "route", "http_status"],
    #   percentiles: [0.05, 0.1, 0.5, 0.9, 0.95]
)
