# Connector contract

Every connector exposes read-only observations as a `ConnectorResult` with:

- `value`: the returned value, or `None` on failure;
- `source`: the connector and operation name;
- `collected_at`: an ISO-8601 timestamp;
- `status`: `available`, `unavailable`, or `error`;
- `error`: a short safe explanation when the result is not available.

Connector credentials stay in the private environment file. The collector
never writes them to JSONL, activity logs, map data, or dashboard responses.
Writes and consequential actions remain behind Operator approval.
