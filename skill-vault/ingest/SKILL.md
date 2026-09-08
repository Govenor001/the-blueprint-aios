---
name: ingest
description: Read uploaded business documents into the private vault context without overwriting approved files.

metadata:
  wing: intelligence
  department: Knowledge
  function: Document Extraction
  replaces: Manually reading every uploaded business file and copying facts into the AIOS.
  the-human: The owner approves proposed context before it becomes trusted.
  ladder:
    manual: Run ingestion and review each extracted file.
    assisted: Extract and flag proposed updates for approval.
    autonomous: Process new files on a schedule after the pattern is trusted.
  trigger: A file appears in vault/documents or the owner asks to ingest documents.
  outputs:
    - Extracted context files with source names
    - Processed-file and unreadable-file report
  kpis:
    - Files processed per run
    - Files needing owner review
  tools: [claude]
  requires-context: []
  model: fast
  autonomy: assisted
  scaffolding-phase: 2
---

## What this does
Extracts readable text from Markdown, text, CSV, PDF, and Word files into the private vault context.

## Inputs it reads
- vault/documents/ — files the owner drops for the AIOS
- vault/context/ — existing approved context

## Execution
1. Scan the incoming folder and identify each supported file.
2. Extract readable text and keep the original filename as the source.
3. Add new context or write a dated proposed file when context already exists.
4. Move completed inputs into vault/documents/processed/.
5. Report unreadable files by name; never skip them silently.

## Rules
- Never overwrite an existing context file.
- Never put vault content in the dashboard or activity log.
- If a file cannot be read, say so by name and continue.
