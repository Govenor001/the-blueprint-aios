# Source contract

Scout outputs and any dashboard metric must carry:

- source: the connector, file, URL, or UNAVAILABLE;
- retrieved_at: an ISO-8601 timestamp;
- status: available, stale, or unavailable.

When a source is missing, the output says UNAVAILABLE and explains what the owner must connect. It must never fill the gap with a plausible number.

For a connection-backed panel card, `scripts/collect.py` reads only the explicit
read-only endpoint named by `endpoint_env` (or the derived
`AIOS_<CONNECTION>_<OPERATION>_URL` variable). Endpoints must use HTTPS, or local
HTTP for a bridge on the same server. Optional `token_env` values are read from
the private environment file and are never written to metric history. HTTP,
timeout, and missing-field failures are recorded as `status: error` rows so a
broken connection cannot look like a healthy zero.
