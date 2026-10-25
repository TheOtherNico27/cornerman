# 1. Record architecture decisions

Date: 2026-10-23

## Status

Accepted

## Context

Cornerman makes design choices that aren't obvious from the code alone: why a FIFO queue, why the worker reads the previous batch from S3, why a native Bluetooth gateway instead of a phone. Six weeks from now, nobody (including the author) will remember the reasons unless they're written down.

## Decision

Record each significant decision as a short Architecture Decision Record in `docs/adr/`, numbered in the order the decisions are made. Each record has a title, date, status, context, decision, and consequences, following Michael Nygard's format.

A record is never rewritten once accepted. If a decision changes, a new record supersedes the old one, and the old one's status says so.

## Consequences

- Decisions can be explained, and defended in an interview, by pointing to their record.
- Writing a record takes a few minutes per decision, so only choices with real trade-offs get one.
