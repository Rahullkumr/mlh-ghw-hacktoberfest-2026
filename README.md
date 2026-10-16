# mlh-ghw-hacktoberfest-2026

My challenge work for [MLH Global Hack Week: Hacktoberfest](https://events.mlh.io/events/14553-global-hack-week-hacktoberfest)
(Oct 9–15, 2026). One folder per challenge.

## Tiger Data

All six run on one Tiger Cloud service (`touchgrass`, TimescaleDB), set up and queried
from Claude Code through Tiger MCP.

| Challenge | Folder | Status |
|-----------|--------|--------|
| Integrate Tiger Cloud with your AI Agent with the Tiger CLI and MCP | [tiger-mcp-integration](tiger-mcp-integration/) | Submitted |
| Set up a Tiger Cloud service and create your first Hypertable | [tiger-hypertable](tiger-hypertable/) | Submitted |
| Accelerate Dashboards with Continuous Aggregates | [tiger-continuous-aggregates](tiger-continuous-aggregates/) | Submitted |
| Simulate an IoT sensor dataset for testing and development | [tiger-iot-sensors](tiger-iot-sensors/) | Submitted |
| Ingest real-time financial data into Tiger Cloud | [tiger-crypto-ingest](tiger-crypto-ingest/) | Submitted |
| Implement AI-Powered Vector Search with pgvector | [tiger-pgvector-search](tiger-pgvector-search/) | Submitted |

## Cursor / Grok Bot (SpaceX)

| Challenge | Folder | Status |
|-----------|--------|--------|
| Sign up for a Cursor Pro Account (×2) | n/a | Submitted (promo applied as $34 credit) |
| Cannot sign up for Cursor Pro Account | n/a | Submitted (Pro now part of X Subscription Premium) |
| CHALLENGE 1: Build a Mini App with Cursor | [cursor-mini-app](cursor-mini-app/) | Submitted (Rangoli Maker) |
| CHALLENGE 2: Benchmark Cursor's Models | n/a | Blocked (Cursor free weekly usage limit reached) |
| CHALLENGE 3: Create Your First Grok Bot | `grokbot-first-bot/` | To do (check Grok Bot access) |
| CHALLENGE 4: Teach Grok Bot Your First Task | `grokbot-first-task/` | To do |
| CHALLENGE 5: Build a Campus Opportunities Database | `grokbot-opportunities-db/` | To do |
| CHALLENGE 6: Teach Grok Bot a Browser Workflow | `grokbot-browser-workflow/` | To do |
| CHALLENGE 7: Run a Two-Bot Launch Relay | `grokbot-launch-relay/` | To do |

## GitHub

| Challenge | Folder | Status |
|-----------|--------|--------|
| Code with Codespaces | [github-codespaces](github-codespaces/) | Submitted |
| Getting Started with Copilot | [github-copilot-getting-started](github-copilot-getting-started/) | Completed (submission pending) |
| Intro to Repository Management | [github-repo-management](github-repo-management/) | In progress (step 1) |
| Use GitHub Copilot to Build a Simple Application | [copilot-simple-app](copilot-simple-app/) | Submitted (SIGNAL LOST) |
| Use GitHub Copilot to complete any of this week's challenges | [copilot-simple-app](copilot-simple-app/) + GitHub Discussion | Submitted |
| Signup for the GitHub Student Developer Pack | n/a | Submitted |

## Running the code

The SQL files run against any TimescaleDB service with the `timescaledb` and `vectorscale`
extensions. The crypto pipeline needs Python 3.10+; see [tiger-crypto-ingest](tiger-crypto-ingest/).
No credentials are stored in this repo.
