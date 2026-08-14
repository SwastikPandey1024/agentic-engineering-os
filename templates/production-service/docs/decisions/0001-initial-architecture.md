# ADR-0001: Structured JSON Logging & Request ID Propagation

## Status
Accepted

## Context
Production services require distributed traceability across microservices and centralized log forwarders (Datadog, Grafana Loki, CloudWatch).

## Decision
We implement a custom `RequestIDMiddleware` that injects `X-Request-ID` headers into context variables and outputs structured JSON logs to `stdout`.

## Consequences
* **Positive**: 100% correlation across all API access logs and error traces; zero external logging agent coupling.
* **Negative**: Minor CPU formatting overhead per log record (< 0.1ms).

## Verification
* Test in `tests/test_logging.py` asserts `X-Request-ID` is returned in response headers.
