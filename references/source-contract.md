# Source contract

Scout outputs and any dashboard metric must carry:

- source: the connector, file, URL, or UNAVAILABLE;
- retrieved_at: an ISO-8601 timestamp;
- status: available, stale, or unavailable.

When a source is missing, the output says UNAVAILABLE and explains what the owner must connect. It must never fill the gap with a plausible number.
