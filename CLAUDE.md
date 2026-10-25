# Cornerman

Punch tracking for boxing training. An M5Stack StickS3 on the back of the forearm streams motion over Bluetooth LE to a gateway on a nearby computer. The gateway posts 1-second batches to an API. A queue and a worker run the punch detector, Postgres stores the results, Redis pushes a live count to the dashboard, and everything deploys to AWS.

```
StickS3 --BLE--> gateway (PC/MacBook) --HTTPS--> FastAPI --> S3 + SQS FIFO --> worker --> Postgres
                                                                                  \--> Redis --> live dashboard
```

Until the sensor arrives, recordings from an Apple Watch (Sensor Logger) stand in for it. They're for exercising the pipeline only, never for tuning or accuracy numbers.

## Repo layout

```
src/cornerman/
  api/        HTTP API (FastAPI)
  worker/     queue consumer that runs the detector
  detector/   punch detection, a pure function
  common/     config, database, AWS clients, shared models
  gateway/    Bluetooth gateway; runs natively, never in Docker
firmware/     StickS3 firmware (PlatformIO), from Step 2b
web/          dashboard (Vite + React + TS), from Step 7
migrations/   plain SQL, applied in filename order
scripts/      one-off tools (replay a recording, convert exports)
tests/        unit/ (no services), integration/ (needs compose), fixtures/
docs/         BUILD_LOG.md, adr/, runbooks/
infra/        Terraform, from Step 9
```

`plans/` holds the local build plan and course material. It's gitignored and never pushed.

## Learning contract

The developer writes some files by hand and must be able to explain every line. For these files, write tests and stubs, teach, and review, but don't write the implementation:

| File | Step | Claude's role |
|---|---|---|
| `migrations/0001_init.sql` | 3 | Failing schema tests first, explain options, review |
| `src/cornerman/detector/core.py` (body of `detect_punches`) | 5 | Tests and stub, explain signal-processing options, review |
| `src/cornerman/gateway/decode.py` | 2b | Golden-fixture tests and stub, teach, review |
| `data/labels/*.json` and threshold tuning | 6 | Build the tools; the developer labels and tunes |
| `Dockerfile` | 8 | Explain the layers, review |
| The IAM policy statements in `infra/iam.tf` | 9 | Explain least privilege, review |
| `docs/explain.md`, `docs/postmortem-*.md`, the README pitch | 8, 12 | Templates and data; the developer writes the prose |

Rules:

1. Write tests and stubs first, then hand off with the step's lab, never a bare "make these tests pass."
2. If asked to write one of these files, remind the developer once that it's a hand-written checkpoint and ask them to confirm. If they confirm, write it and add a line to `docs/BUILD_LOG.md` saying so.
3. Each PR description lists which files the developer wrote.
4. `docs/BUILD_LOG.md` entries are written by the developer. Claude may add the heading only.

When the developer is stuck, give hints that get more specific (the concept, then where to look, then pseudocode) before any code.

## Rules for every change

- Tests never touch real AWS. They use moto, either the in-process mock or the server in compose.
- Tests never need hardware. Firmware and gateway logic are tested with golden packet fixtures in `tests/fixtures/packets/`.
- No secrets in git. Real values live in `.env` (gitignored); `.env.example` has placeholders only. CI runs gitleaks.
- Text files use LF line endings (`.gitattributes`); this repo is developed on Windows.
- One branch and one pull request per step. CI must be green before merging.

## Commands

```
uv sync                       # install everything from uv.lock (creates .venv)
uv run pytest -q              # unit tests
uv run ruff check             # lint
uv run ruff format            # format (CI runs --check)
docker compose up -d          # start Postgres and Redis
docker compose ps             # both should say (healthy)
docker compose down           # stop (add -v to also delete the database)
```

From Step 2b: `pio run -d firmware` builds the firmware, and `uv run --extra gateway python -m cornerman.gateway` runs the gateway.

The full build plan is `plans/cornerman-build.md` (local only).
