# MCP Setup Guide

This guide covers setting up MCP (Model Context Protocol) servers for Claude Code.

## Recommended: airis-mcp-gateway

The [airis-mcp-gateway](https://github.com/agiletec-inc/airis-mcp-gateway) provides a unified gateway for multiple MCP servers. This is the recommended approach for several reasons:

- **Single configuration**: One server vs configuring 8+ individual MCPs
- **Unified management**: Enable/disable servers without editing config files
- **Consistent naming**: All tools prefixed with `mcp__airis-mcp-gateway__`
- **Built-in profiles**: Save and load server combinations

## Installation

### 1. Clone the Gateway

```bash
git clone https://github.com/agiletec-inc/airis-mcp-gateway.git
cd airis-mcp-gateway
```

### 2. Install Dependencies

```bash
npm install
# or
bun install
```

### 3. Configure Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "airis-mcp-gateway": {
      "command": "node",
      "args": ["/path/to/airis-mcp-gateway/dist/index.js"],
      "env": {
        "TAVILY_API_KEY": "your-tavily-key",
        "CONTEXT7_API_KEY": "your-context7-key"
      }
    }
  }
}
```

### 4. Verify Installation

Start Claude Code and check available tools:

```
/mcp
```

You should see airis-mcp-gateway listed with its tools.

## Included MCP Servers

| Server | Tools | Purpose |
|--------|-------|---------|
| **Context7** | `resolve-library-id`, `get-library-docs` | Official library documentation lookup |
| **Tavily** | `tavily-search`, `tavily-extract`, `tavily-crawl`, `tavily-map` | Web search and content extraction |
| **Sequential Thinking** | `sequentialthinking` | Complex multi-step reasoning |
| **Magic (21st.dev)** | `21st_magic_component_builder`, `logo_search` | UI component generation |
| **BrowserMCP** | `browser_navigate`, `browser_click`, `browser_type` | Browser automation |
| **Chrome DevTools** | `navigate_page`, `take_screenshot`, `evaluate_script` | Chrome debugging |
| **Atlassian** | `getJiraIssue`, `createJiraIssue`, `getConfluencePage` | Jira/Confluence integration |
| **Gitea** | `create_issue`, `create_pull_request`, `get_file_content` | Git repository management |

## Gateway Management Commands

Once installed, you can manage servers using gateway tools:

```javascript
// List all available servers
mcp__airis-mcp-gateway__gateway_list_servers

// Enable a specific server
mcp__airis-mcp-gateway__gateway_enable_server({ server: "tavily" })

// Disable a server
mcp__airis-mcp-gateway__gateway_disable_server({ server: "atlassian" })

// Check server status
mcp__airis-mcp-gateway__gateway_get_server_status({ server: "context7" })

// Save current configuration as a profile
mcp__airis-mcp-gateway__airis_profile_save({ name: "minimal" })

// Load a saved profile
mcp__airis-mcp-gateway__airis_profile_load({ name: "minimal" })
```

## Alternative: Individual MCP Servers

If you prefer configuring servers individually, here's the manual setup:

### Context7

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"],
      "env": {}
    }
  }
}
```

### Tavily

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server"],
      "env": {
        "TAVILY_API_KEY": "your-key"
      }
    }
  }
}
```

### Sequential Thinking

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-sequential-thinking"]
    }
  }
}
```

## Gateway vs Individual: Comparison

| Aspect | Gateway | Individual |
|--------|---------|------------|
| **Config complexity** | 1 entry | 8+ entries |
| **API key management** | Centralized | Per-server |
| **Enable/disable** | Runtime commands | Edit config, restart |
| **Memory usage** | Single process | 8+ processes |
| **Tool discovery** | Unified namespace | Multiple namespaces |
| **Profiles** | Built-in | Manual |

## Troubleshooting

### Gateway not starting

1. Check the gateway is built: `npm run build`
2. Verify the path in settings.json is correct
3. Check for port conflicts (default: 3000)

### API key errors

1. Ensure environment variables are set in settings.json
2. Verify API keys are valid and have appropriate permissions

### Specific server not working

1. Use `gateway_get_server_status` to check status
2. Try `gateway_enable_server` to re-enable
3. Check server-specific requirements (e.g., Chrome for DevTools)

## Best Practices

1. **Start minimal**: Enable only servers you need
2. **Use profiles**: Save working configurations
3. **Monitor usage**: Some servers have rate limits (Tavily, Context7)
4. **Secure credentials**: Never commit API keys to version control
