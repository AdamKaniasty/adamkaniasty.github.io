---
layout: post
title: Take a Claude Agent SDK agent from install to deploy with Agents CLI
date: 2026-11-09 12:00:00
description: Shortened guide to building, evaluating, and deploying a Claude Agent SDK agent to Google Cloud Run using Google's Agents CLI (v1.13.0), with a link to the original post.
tags: [Agents-CLI, Claude-Agent-SDK, AI-Agents, Google-Cloud]
categories: Google
about:
  - type: SoftwareApplication
    name: Agents CLI
    url: https://github.com/google/agents-cli
  - type: SoftwareApplication
    name: Claude Agent SDK
  - type: Thing
    name: Google Cloud Run
    url: https://cloud.google.com/run
  - type: Thing
    name: Agent2Agent (A2A) protocol
is_based_on:
  name: Take a Claude Agent SDK agent from install to deploy with Agents CLI
  url: https://eliasecchig.github.io/blog/2026-11-09-claude-agent-sdk/
  author_name: Elia Secchi
  author_url: https://eliasecchig.github.io/
  date_published: "2026-11-09"
---

> **Original article:** This is a shortened summary of [Take a Claude Agent SDK agent from install to deploy with Agents CLI](https://eliasecchig.github.io/blog/2026-11-09-claude-agent-sdk/) by Elia Secchi (November 9, 2026), highlighting work from Google's Agent Development Lifecycle team on [Agents CLI](https://github.com/google/agents-cli). [Read the full original walkthrough →](https://eliasecchig.github.io/blog/2026-11-09-claude-agent-sdk/)

**Summary:** Since [Agents CLI](https://github.com/google/agents-cli) v1.12.0 (walkthrough verified on [v1.13.0](https://github.com/google/agents-cli/blob/main/RELEASE_NOTES.md)), a first-party `claude` extension lets Python Claude Agent SDK developers use the same `create`, `run`, `eval`, `infra`, and `deploy` workflow as Agent Development Kit (ADK) agents. You keep defining `ClaudeAgentOptions` in `app/agent.py`, while the template wires in Cloud SQL sessions, Cloud Trace observability, CI-ready evaluations, and private Google Cloud Run deployment with Agent2Agent (A2A) support.

## Lifecycle commands at a glance

Only two commands (`run` and `eval generate`) are handled by the `claude` extension; evaluation grading, Terraform infrastructure provisioning, and Cloud Run deployment reuse the standard Agents CLI pipeline unchanged.

| Lifecycle stage       | Command                                                                                                                                | Purpose                                                                           | Handled by                        |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------- |
| Install CLI & skills  | `uvx google-agents-cli setup`                                                                                                          | Installs Agents CLI and coding-agent skills                                       | Core Agents CLI                   |
| Scaffold project      | `agents-cli create claude-agent --agent google/agents-cli/extensions/claude/template@v1.13.0 -d cloud_run --session-type cloud_sql -y` | Generates a Cloud Run + Cloud SQL Claude Agent SDK project                        | Core Agents CLI + Claude template |
| Run locally           | `agents-cli run "what's the weather in San Francisco?"`                                                                                | Runs Claude in-process via the SDK and returns a resumable session ID             | `claude` extension                |
| Generate eval traces  | `agents-cli eval generate --dataset tests/eval/datasets/basic-dataset.json -o tests/eval/output/`                                      | Runs test prompts and saves traces in the ADK-compatible format                   | `claude` extension                |
| Grade evals           | `agents-cli eval grade --traces <file>.json --config tests/eval/eval_config.yaml`                                                      | Scores outputs with a judge model and gates CI via thresholds                     | Core Agents CLI                   |
| Plan / apply infra    | `agents-cli infra single-project --project <id> [--apply]`                                                                             | Plans or provisions 42 Terraform resources (Cloud Run, Cloud SQL, IAM, telemetry) | Core Agents CLI                   |
| Validate / deploy     | `agents-cli deploy [--dry-run] --project <id>`                                                                                         | Checks APIs and IAM, then deploys privately to Cloud Run with A2A                 | Core Agents CLI                   |
| Enhance existing repo | `agents-cli scaffold enhance google/agents-cli/extensions/claude/template@v1.13.0 -d cloud_run`                                        | Adds the production template to an existing Claude Agent SDK project              | Core Agents CLI + Claude template |

## 1. How to install, scaffold, and run locally

Install Agents CLI with `uvx google-agents-cli setup`, scaffold the Claude template targeting Cloud Run with Cloud SQL sessions, install dependencies, and execute a local prompt. `agents-cli run` executes Claude in-process through the SDK and prints a session ID you can pass to `--session-id` to resume the conversation.

```bash
uvx google-agents-cli setup

agents-cli create claude-agent \
  --agent google/agents-cli/extensions/claude/template@v1.13.0 \
  -d cloud_run --session-type cloud_sql -y

cd claude-agent && agents-cli install
agents-cli run "what's the weather in San Francisco?"
```

Inside `app/agent.py`, the agent remains standard Claude Agent SDK Python code: a `@tool` exposed through an in-process Model Context Protocol (MCP) server, with built-in Claude Code tools disabled (`tools=[]`) and explicit `allowed_tools` scoping:

```python
root_agent = ClaudeAgentOptions(
    model="claude-haiku-4-5",
    system_prompt="You are Skye, a helpful assistant. Use get_weather for weather questions.",
    mcp_servers={"weather": weather_server},
    tools=[],
    allowed_tools=["mcp__weather__get_weather"],
    max_turns=10,
)
```

The selected Claude model must be enabled in Google Cloud Vertex AI Model Garden for your project. `agents-cli create` writes `GOOGLE_CLOUD_PROJECT` to `.env`, while `ANTHROPIC_VERTEX_PROJECT_ID` takes precedence if set in your shell environment.

## 2. How evaluation works across Claude Agent SDK and ADK

Agents CLI splits evaluation into two commands: `eval generate` runs the agent over a dataset and records traces, and `eval grade` scores those traces with a judge model. Because the `claude` extension writes traces in the same schema ADK agents emit, `eval grade` runs completely unchanged.

```bash
agents-cli eval generate \
  --dataset tests/eval/datasets/basic-dataset.json \
  -o tests/eval/output/

agents-cli eval grade \
  --traces tests/eval/output/<generated-eval-file>.json \
  --config tests/eval/eval_config.yaml
```

In the original walkthrough, both starter cases (`greeting` and `weather_lookup`) scored 5.0/5.0 on `custom_response_quality`. Uncommenting `thresholds:` in `tests/eval/eval_config.yaml` (or passing `--fail-under`) makes `eval grade` and `eval run` exit with code `1` on regressions (added in v1.13.0), enabling automated CI quality gates.

## 3. What production infrastructure Agents CLI provisions

Running `agents-cli infra single-project --project my-project` generates a Terraform plan with 42 Google Cloud resources without modifying anything until you pass `--apply`. Applying the plan once before the first deployment connects the agent template to managed production services:

- **Persistent sessions (Cloud SQL):** With `--session-type cloud_sql`, conversation transcripts persist in Cloud SQL so conversations survive container restarts and resume across instances.
- **Distributed traces (Cloud Trace):** Once the Terraform IAM bindings grant `roles/cloudtrace.agent`, every turn and tool call is recorded as spans under a single trace in Cloud Trace.
- **Logs, metrics, and analytics:** Trace-correlated logs export to Cloud Logging (`roles/logging.logWriter`), turn duration and token metrics export to Cloud Monitoring (`roles/monitoring.metricWriter`), and BigQuery Agent Analytics is supported via a logging sink.

## 4. How to validate and deploy securely to Cloud Run

`agents-cli deploy --dry-run --project my-project` validates enabled Google Cloud APIs (`run.googleapis.com`, `artifactregistry.googleapis.com`, `cloudbuild.googleapis.com`), checks target service status, and verifies all 4 required IAM permissions before creating any resources.

Running `agents-cli deploy` executes `gcloud beta run deploy --source .` with security defaults suited for production agents:

- `--no-allow-unauthenticated` keeps the Cloud Run service private so only authorized callers can invoke it.
- `--identity-type agent-identity` (default for new projects since v1.13.0) assigns the agent its own dedicated least-privilege Google Cloud identity instead of reusing a developer or shared service account.

After deployment, the service exposes the **Agent2Agent (A2A)** protocol and can be queried directly from the terminal:

```bash
agents-cli run --url https://<service-url> --mode a2a --app-name app "hello"
```

## Frequently asked questions

### What does the Agents CLI Claude extension replace vs. reuse from ADK?

The first-party `claude` extension only handles `agents-cli run` and `agents-cli eval generate`. Evaluation grading (`eval grade`), Terraform provisioning (`infra single-project`), and Cloud Run deployment (`deploy`) execute the exact same Agents CLI commands used for ADK agents.

### How do I migrate an existing Claude Agent SDK agent to Agents CLI?

Run `agents-cli scaffold enhance google/agents-cli/extensions/claude/template@v1.13.0 -d cloud_run` inside your repository. Agents CLI adds the production template, backs up replaced files into `.agents-cli-original/`, and lets you move your `ClaudeAgentOptions` definition into `app/agent.py`.

### Why should Terraform infra be applied before the first deploy?

Applying `agents-cli infra single-project --apply` creates the Cloud SQL session database, attaches it to the Cloud Run service configuration, and grants the agent identity the Cloud Trace, Cloud Logging, and Cloud Monitoring roles needed on first launch.

## References and related work

- **Full original article:** [Take a Claude Agent SDK agent from install to deploy with Agents CLI — Elia Secchi](https://eliasecchig.github.io/blog/2026-11-09-claude-agent-sdk/)
- **Source repository:** [google/agents-cli on GitHub](https://github.com/google/agents-cli)
- **Extensions documentation:** [Agents CLI first-party extensions guide](https://google.github.io/agents-cli/guide/extensions/first-party/)
- **Release notes:** [Agents CLI v1.13.0 release notes](https://github.com/google/agents-cli/blob/main/RELEASE_NOTES.md)

[Google Agent Development Lifecycle role (CV)]({{ '/cv/' | relative_url }}#work) · [Professional updates]({{ '/news/' | relative_url }}) · [Engineering projects]({{ '/projects/' | relative_url }})
