# MCP_SETUP.md — wiring CRUX's MCP server into IBM Bob and GitHub

> The MCP server is the keystone of the DevOps wow moment. This document covers every wire that has to land for the demo to work live: Bob registering the server, MCP Inspector for debugging, and GitHub Actions calling the gate. The whole wiring runs locally — there is no IBM Cloud or watsonx.ai dependency. If something here is unclear, fix the doc rather than working around it.

---

## 1. The big picture

```
┌─ IBM Bob IDE ──────┐                  ┌─ MCP Inspector ──┐
│ stdio transport    │                  │ streamable-http  │
└──────────┬─────────┘                  └────────┬─────────┘
           │                                     │
           │           ┌─ GitHub Actions ────────┘
           │           │ streamable-http
           ▼           ▼
   ┌───────────────────────────────────┐
   │     mcp_server/server.py          │
   │     FastMCP 3.x                   │
   │     (5 tools)                     │
   └───────────────┬───────────────────┘
                   │
                   ▼
       ┌──────────────────────┐
       │  skills/notebook-    │
       │  narrative           │
       │  skills/production-  │
       │  audit               │
       │  cached results in   │
       │  out/<stem>/         │
       └──────────────────────┘
```

Three transports, one server. That's the flexibility FastMCP gives for free.

---

## 2. Pre-flight checklist

Before you start wiring, verify these:

- [ ] Python 3.11+ is the active interpreter (`python --version`)
- [ ] `uv` is installed (`uv --version`). If not: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] `pyproject.toml` includes `fastmcp>=3.2`
- [ ] `uv sync` completes without errors
- [ ] `mcp_server/server.py` exists and runs with `uv run mcp_server/server.py --help`
- [ ] You know the **absolute path** to your repo (`pwd` on macOS/Linux, `cd` on Windows)

---

## 3. Wire 1: register the server with IBM Bob IDE

Bob discovers MCP servers through a JSON config you edit in Bob's settings, similar to `claude_desktop_config.json` for Claude Desktop. The format follows the MCP standard.

### Where Bob's MCP config lives
In Bob IDE: **Settings → MCP → Open Project MCPs** (or **Open Global MCPs** for cross-project availability).

For the hackathon, **use Project MCPs** — the config gets version-controlled with the repo and judges can verify it.

### The config snippet
Project MCP config (lives at `.bob/mcp.json` in this repo):

```json
{
  "mcpServers": {
    "crux": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/YOUR/crux",
        "run",
        "mcp_server/server.py"
      ],
      "transport": "stdio",
      "description": "CRUX: notebook intent recovery + 15-gap production audit",
      "autoApprove": []
    }
  }
}
```

**Important details (these matter; subtle bugs live here):**
- `command` should be `uv` (not `python`). FastMCP works either way, but `uv` resolves the venv automatically.
- The path under `--directory` **must be absolute**. On Windows use forward slashes or escaped backslashes (`/Users/me/crux` or `C:\\Users\\me\\crux`).
- `transport: stdio` is correct for the Bob-to-server connection. Streamable HTTP is for the Inspector and CI.
- `autoApprove: []` means every tool call requires your approval. For the demo, **leave this empty** — judges should see explicit approval prompts; that's how they know Bob is acting deliberately, not on autopilot.

### Restart Bob and verify
1. Restart Bob IDE.
2. Open Settings → MCP. The `crux` entry should appear with a green dot indicating it's reachable.
3. Open the chat. Type:
   ```
   Use the crux MCP server to audit @samples/01_clean.ipynb
   ```
4. Bob should propose calling the `audit_notebook` tool. Approve. The result should come back with a populated `AuditResult`.

### If Bob can't see the server
Common failures and fixes:

| Symptom | Fix |
|---|---|
| Bob says "no MCP servers configured" | The `.bob/mcp.json` path is wrong; Bob looks at workspace-relative `.bob/mcp.json` and at the global config. Verify the file exists at `<repo>/.bob/mcp.json`. |
| Server shows "starting…" forever | The `--directory` path is wrong. Bob can't find the venv. `cd` into the repo, run `uv run mcp_server/server.py` manually — if that fails, fix the venv first. |
| Connects but no tools listed | The server file has an exception during startup. Check `~/.bob/logs/` (or equivalent) for stack traces. Most common cause: missing import or wrong Pydantic version. |
| Tool calls succeed but return empty results | The server is starting from the wrong working directory and can't find `out/`. Add `--cwd` to your args list or set `os.chdir()` at the top of `server.py`. |

---

## 4. Wire 2: validating with MCP Inspector

The MCP Inspector is the official debugging UI for MCP servers. It's invaluable during development and **good live demo material** — judges who've worked with MCP recognize it.

### Run the Inspector
```bash
# From the repo root
uv run mcp dev mcp_server/server.py
```

This launches the Inspector at `http://127.0.0.1:6274` and connects it to your CRUX server in dev mode. Open the URL in a browser.

### What you see in the Inspector
- **Tools tab**: lists all five CRUX tools with their JSON Schemas (auto-generated by FastMCP from your Pydantic types). Click any tool to expand its parameter form and call it manually.
- **Resources tab**: empty for CRUX (we don't expose resources, only tools).
- **Prompts tab**: empty for CRUX.
- **Notifications tab**: shows JSON-RPC traffic in real-time.

### Demo flow with the Inspector
For the wow #3 segment of the demo, you can either show Bob calling the tools (more cinematic) or show the Inspector (more concrete). The Inspector makes the MCP-ness explicit. Both work; pick one and stick with it for rehearsal.

---

## 5. Wire 3: the GitHub Actions block-on-gaps workflow

This is the DevOps closing-the-loop demo. A fake CI job calls the MCP server's `block_merge_if_critical_gaps` tool, gets back `{allow_merge: false}`, exits non-zero, and the PR shows a red ❌.

### The workflow file (`ci/block-on-gaps.yml`)

```yaml
name: CRUX block on critical gaps

on:
  pull_request:
    paths:
      - 'samples/**.ipynb'
      - 'notebooks/**.ipynb'
  workflow_dispatch:
    inputs:
      notebook:
        description: "Path to notebook (relative to repo root)"
        required: true
        default: "samples/03_chaos.ipynb"

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"

      - name: Install CRUX dependencies
        run: uv sync --frozen

      - name: Determine notebook to audit
        id: pick
        run: |
          if [ -n "${{ github.event.inputs.notebook }}" ]; then
            echo "path=${{ github.event.inputs.notebook }}" >> $GITHUB_OUTPUT
          else
            # On PR: pick the first changed notebook
            CHANGED=$(git diff --name-only origin/main...HEAD | grep '\.ipynb$' | head -n1)
            echo "path=$CHANGED" >> $GITHUB_OUTPUT
          fi

      - name: Start CRUX MCP server (background)
        run: |
          uv run mcp_server/server.py --transport streamable-http --port 8080 &
          echo $! > mcp.pid
          sleep 2  # let the server bind

      - name: Audit the notebook over MCP
        run: |
          NB="${{ steps.pick.outputs.path }}"
          curl -fsS -X POST http://127.0.0.1:8080/mcp/tools/audit_notebook \
            -H "Content-Type: application/json" \
            -d "{\"path\": \"$NB\"}" \
            -o audit_result.json
          NB_ID=$(jq -r '.notebook_id' audit_result.json)
          echo "NB_ID=$NB_ID" >> $GITHUB_ENV

      - name: Check merge eligibility
        run: |
          curl -fsS -X POST http://127.0.0.1:8080/mcp/tools/block_merge_if_critical_gaps \
            -H "Content-Type: application/json" \
            -d "{\"notebook_id\": \"$NB_ID\"}" \
            -o block_result.json
          ALLOW=$(jq -r '.allow_merge' block_result.json)
          BLOCKING=$(jq -r '.blocking_gaps | join(", ")' block_result.json)
          
          if [ "$ALLOW" = "false" ]; then
            echo "❌ CRUX blocks this merge."
            echo "Blocking gaps: $BLOCKING"
            exit 1
          else
            echo "✅ No critical gaps. Merge allowed."
          fi

      - name: Post audit dossier excerpt to PR
        if: always() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const result = JSON.parse(fs.readFileSync('block_result.json', 'utf8'));
            const body = result.allow_merge
              ? `### ✅ CRUX audit passed\nNo critical gaps detected.`
              : `### ❌ CRUX audit blocks this merge\n\nBlocking gaps: ${result.blocking_gaps.join(', ')}\n\nSee \`out/${process.env.NB_ID}/audit_dossier.md\` for the full dossier.`;
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body
            });

      - name: Cleanup
        if: always()
        run: kill $(cat mcp.pid) || true
```

### Test the workflow locally with `act`
[`act`](https://github.com/nektos/act) runs GitHub Actions workflows locally. For the demo, `act` is faster than waiting for real GitHub runners.

```bash
# Install act once
brew install act    # macOS
# or: curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Trigger the workflow as if a PR was opened
act pull_request -W ci/block-on-gaps.yml --container-architecture linux/amd64
```

`act` will pull the runner image, run the workflow, and exit with the same exit code GitHub would. **Use this in rehearsal**, not the real GitHub UI — it's faster and more deterministic.

### Cheaper local fallback: a plain bash script
If `act` is fussy on your demo machine, a plain shell script gives the same demo beat:

```bash
# ci/local_block_check.sh
#!/usr/bin/env bash
set -euo pipefail

NB="${1:?usage: ci/local_block_check.sh <notebook-path>}"

# Start the MCP server
uv run mcp_server/server.py --transport streamable-http --port 8080 &
SERVER_PID=$!
trap "kill $SERVER_PID 2>/dev/null || true" EXIT
sleep 2

# Audit
curl -fsS -X POST http://127.0.0.1:8080/mcp/tools/audit_notebook \
  -H "Content-Type: application/json" \
  -d "{\"path\": \"$NB\"}" -o /tmp/audit.json

NB_ID=$(jq -r '.notebook_id' /tmp/audit.json)

# Check
curl -fsS -X POST http://127.0.0.1:8080/mcp/tools/block_merge_if_critical_gaps \
  -H "Content-Type: application/json" \
  -d "{\"notebook_id\": \"$NB_ID\"}" -o /tmp/block.json

ALLOW=$(jq -r '.allow_merge' /tmp/block.json)
if [ "$ALLOW" = "false" ]; then
  echo "❌ MERGE BLOCKED"
  jq '.' /tmp/block.json
  exit 1
fi
echo "✅ Merge allowed"
```

In the demo, you `./ci/local_block_check.sh samples/03_chaos.ipynb`, the terminal prints **❌ MERGE BLOCKED**, and you say the wow #3 line.

---

## 6. Why there are no IBM Cloud or watsonx.ai wires

Earlier drafts of this document had two more sections here: a "Wire 4" for watsonx.ai (powering an LLM-generated stakeholder summary in the dossier) and a "Wire 5" for hosting the MCP server on IBM Cloud Code Engine. **Both were removed.** This is intentional, and worth understanding so you can defend the decision in Q&A.

**No watsonx.ai because the dossier is a CI artifact.** The stakeholder summary at the top of the dossier is rendered from `templates/stakeholder_summary.md.j2` over the structured `AuditResult`. Running CRUX twice on the same notebook must produce byte-identical output — that's the contract that lets CI gates make stable decisions. A deterministic Jinja2 template guarantees this. An LLM call cannot. (See `templates/stakeholder_summary.md.j2` and the rationale in `SYSTEM_DESIGN.md` invariant 1.)

**No Code Engine because local is sufficient.** The MCP server runs on `localhost:8765` for the demo. Bob talks to it over stdio. CI talks to it over HTTP, *inside* the GitHub Actions runner — the workflow starts a fresh server in the container, calls it, and tears it down. There is no scenario in the 5-minute demo where remote hosting helps; there are several scenarios where it hurts (DNS, TLS, network jitter, expired tokens). The MCP surface is identical either way, so post-hackathon deployment to any runtime — Code Engine, Cloud Run, Fly.io, your laptop — is a 10-minute follow-up task, not part of the hackathon scope.

**Net effect:** zero credentials in the repo. No `.env` for runtime. No API keys to rotate. The only secret in the entire CRUX deployment is GitHub's auto-provisioned `GITHUB_TOKEN`, which the Actions runner injects automatically. This is the correct security posture for a public-facing audit tool.

---

## 7. End-to-end smoke test (the "did everything wire?" check)

Run this from the repo root, on a clean machine state, with no Bob conversation open:

```bash
# 1. Verify deps
uv sync --frozen

# 2. Run an audit without Bob
uv run crux audit samples/02_messy.ipynb
# Expect: out/02_messy/ populated with all artifacts. Parity test passes.

# 3. Start the MCP server
uv run mcp_server/server.py &
SERVER_PID=$!
sleep 2

# 4. Inspect the server
uv run mcp dev mcp_server/server.py
# Open http://127.0.0.1:6274 in browser, click 'Connect', see five tools.

# 5. Verify Bob can reach it
# Open Bob IDE. New chat. Type: "use crux to audit @samples/01_clean.ipynb"
# Bob should propose audit_notebook. Approve. Result returns.

# 6. Trigger the CI gate
./ci/local_block_check.sh samples/03_chaos.ipynb
# Expect: terminal prints ❌ MERGE BLOCKED, exits 1.

# 7. Cleanup
kill $SERVER_PID
```

If all six steps pass, every wire is hot. You can demo.

---

## 8. Troubleshooting reference

| Error | Likely cause | Fix |
|---|---|---|
| `RuntimeError: Event loop already running` in stdio mode | Two MCP servers competing on stdin | Make sure only one Bob conversation is started |
| FastMCP imports fail | Wrong package: `pip install fastmcp` (jlowin/fastmcp) — not the older `mcp.server.fastmcp` shipped inside the official SDK. They're different now. | `uv add fastmcp` (Apache 2.0, version >= 3.2) |
| MCP Inspector shows "Connection refused" | Server bound to wrong port or interface | Run with `--port 8080 --host 127.0.0.1` explicitly |
| GitHub Actions runner can't find `uv` | astral-sh/setup-uv@v3 step failed | Pin a specific version: `with: version: "0.5.x"` |
| Bob calls a tool but result is empty | Server's working directory differs from Bob's | Add `--cwd <abs path>` to args, or call `os.chdir()` in `server.py` |
| `block_merge_if_critical_gaps` always returns `allow_merge: true` even on chaos sample | The cached AuditResult in `out/03_chaos/` is stale or never produced | Run `crux audit samples/03_chaos.ipynb` first, then re-call the gate |

---

## 9. Security notes (for a public repo submission)

- The `.bobignore` excludes `.env`, `secrets/`, `*.key`, and `config/credentials.json` from Bob's reach. These patterns are defensive — CRUX itself uses no credentials at runtime, but the patterns guard against accidental key paste during development.
- The `.gitignore` excludes the same patterns plus `out/` and `internal-monologue/` (keep `bob_sessions/` committed for judging).
- The MCP server, in stdio mode, has no auth — that's fine for local. In HTTP mode it should add an API key middleware for production. There's a comment in `server.py` saying so.
- **No IBM Cloud, watsonx.ai, or third-party API keys are needed at any point in the CRUX pipeline.** The audit, the dossier rendering, and the MCP server all run with zero external credentials. This is a deliberate design choice — see `SYSTEM_DESIGN.md` invariant 1.

---

*If a wire isn't behaving, run §7 end to end before debugging individual components. Most "is the integration broken?" questions resolve at one of those steps.*
