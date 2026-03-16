# SonarQube MCP — Official Documentation

Pointers to authoritative sources.
Skills and the orchestrator agent should check these when encountering unfamiliar behavior.

## SonarQube MCP Server

| What | URL |
|------|-----|
| Setup & config | https://docs.sonarsource.com/sonarqube-mcp-server/build-and-configure/configure |
| Environment variables | https://docs.sonarsource.com/sonarqube-mcp-server/build-and-configure/environment-variables |
| All available tools | https://docs.sonarsource.com/sonarqube-mcp-server/tools |
| GitHub repo & README | https://github.com/SonarSource/sonarqube-mcp-server |
| Docker image | https://hub.docker.com/r/mcp/sonarqube |

## SonarQube Server

| What | URL |
|------|-----|
| Clean Code taxonomy | https://docs.sonarsource.com/sonarqube-server/latest/user-guide/clean-as-you-code/ |
| Web API reference | https://docs.sonarsource.com/sonarqube-server/latest/extension-guide/web-api/ |

## SonarQube for IDE (formerly SonarLint)

| What | URL |
|------|-----|
| IDE integration overview | https://docs.sonarsource.com/sonarqube-mcp-server/using/integration |
| Embedded server port control | https://community.sonarsource.com/t/how-do-i-control-the-ports-in-use-by-sonarlint/52014 |
| Port for IDE integration | https://community.sonarsource.com/t/sonarqube-mcp-server-how-to-get-the-port-for-the-ide-integration/149696 |
| SonarQube for IDE MCP config | https://community.sonarsource.com/t/sonarqube-for-ide-mcp-configuration/172698 |

Key facts:
- All IDE plugins (VS Code, IntelliJ, Eclipse) share `sonarlint-core` with hardcoded port range 64120–64130.
- Port selection is first-available — not configurable per IDE instance.
- VS Code has Quick Install for auto-configuring `SONARQUBE_IDE_PORT`; IntelliJ requires manual log inspection.
- IntelliJ: one SLOOP process per application (shared across all project windows).
- VS Code: one SLOOP process per window (each window gets its own port).
- Multiple MCP servers can safely share the same IDE port (stateless HTTP, no session tracking).
- Shared rate limit: 10 requests per `Origin` header per 10-second window (`RateLimitFilter`).


## Source Code References

Key files for understanding the embedded server and MCP bridge internals:

| File | Repo | What it reveals |
|------|------|-----------------|
| `EmbeddedServer.java` | `sonarlint-core` | Hardcoded ports 64120–64130, `DontKeepAliveReuseStrategy`, `SO_REUSEADDR` |
| `AnalyzeFileListRequestHandler.java` | `sonarlint-core` | Stateless handler, no locks, `CompletableFuture` dispatch |
| `RateLimitFilter.java` | `sonarlint-core` | 10 req/Origin/10s rate limit |
| `BackendService.kt` | `sonarlint-intellij` | `@Service(Service.Level.APP)` — application-level singleton (one SLOOP for all projects) |
| `extension.ts` | `sonarlint-vscode` | `ChildProcess.spawn()` — one SLOOP per VS Code window |
| `SonarQubeIdeBridgeClient.java` | `sonarqube-mcp-server` | HTTP POST to `localhost:{port}/sonarlint/api/analysis/files`, `Origin: http://localhost` |


## Community

| What | URL |
|------|-----|
| IDE port discovery | https://community.sonarsource.com/t/sonarqube-mcp-server-where-can-i-find-the-port/172689 |
| Configurable port request | https://community.sonarsource.com/t/allow-configurable-port-range-for-the-sonarlint-embedded-server-to-support-multi-user-remote-environ/177897 |
| IntelliJ embedded server error | https://community.sonarsource.com/t/error-in-sonarqube-for-intellij/136350 |
