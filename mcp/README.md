# Codebase Memory MCP Integration

This directory contains configuration templates and schemas for integrating **Codebase Memory MCP** capabilities with your AI-assisted development workflows.

---

## 🌟 Overview & Pre-Existing Server Reuse

> [!IMPORTANT]
> **Check Before Installing**:
> * If your IDE or agentic environment ALREADY has a Codebase Memory MCP server configured (such as `codebase-memory-mcp` or native graph tools like `search_graph`, `query_graph`, `create_entities`, `read_graph`), **USE THE EXISTING SERVER DIRECTLY**.
> * **DO NOT install or configure a duplicate memory server**. The schema defined in [`memory-schema.md`](memory-schema.md) and the operational triggers in [`project-knowledge`](../.agents/skills/project-knowledge/SKILL.md) apply to your existing memory MCP server out-of-the-box.
> * The configurations below are provided purely as fallback templates for new environments that do not yet have an active memory MCP server.

---

## 🛠️ Setup Instructions (New Environments Only)

### 1. Antigravity IDE / Antigravity CLI
If not already active, add the server entry to your MCP configuration file (`~/.gemini/antigravity-ide/mcp_config.json` or `.gemini/mcp_config.json`):

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

### 2. Cursor IDE
In Cursor Settings -> Features -> MCP -> Add New MCP Server:
* **Name**: `memory`
* **Type**: `command`
* **Command**: `npx -y @modelcontextprotocol/server-memory`

### 3. Claude Desktop
Add to your `claude_desktop_config.json`:
* macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
* Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

---

## 📖 Related Documents

* [memory-schema.md](memory-schema.md) — The official entity/relation schema for durable engineering knowledge.
* [memory-config.example.json](memory-config.example.json) — Copy-pasteable fallback MCP server configuration JSON.
* [`project-knowledge/SKILL.md`](../.agents/skills/project-knowledge/SKILL.md) — Operational skill defining when agents read and write memory.
