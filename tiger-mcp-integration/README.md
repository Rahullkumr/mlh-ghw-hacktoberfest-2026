# Integrate Tiger Cloud with your AI Agent (Tiger CLI + MCP)

Connected Claude Code to Tiger Cloud through the Tiger MCP server built into the Tiger CLI,
then created and managed the database entirely through natural-language prompts.

## Setup

```powershell
# Windows (PowerShell)
irm https://cli.tigerdata.com/install.ps1 | iex

tiger auth login        # browser OAuth
tiger service list      # verify auth
tiger mcp install       # pick: claude-code, then restart Claude Code
```

## What the agent did over MCP

| MCP tool         | Action                                                                 |
|------------------|------------------------------------------------------------------------|
| `service_list`   | Confirmed the MCP connection (empty project)                           |
| `service_create` | Created service `touchgrass` (TimescaleDB, DEV, us-east-1, 0 replicas) |
| `db_query`       | Ran every schema, insert, and query in the other `tiger-*` folders     |

The service password was stored in the system keyring by the CLI and never printed.

## Built on this service

- [tiger-hypertable](../tiger-hypertable/)
- [tiger-continuous-aggregates](../tiger-continuous-aggregates/)
- [tiger-iot-sensors](../tiger-iot-sensors/)
- [tiger-crypto-ingest](../tiger-crypto-ingest/)
- [tiger-pgvector-search](../tiger-pgvector-search/)
