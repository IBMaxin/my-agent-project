# TODO - Project Roadmap

## Phase 1: Core Infrastructure ✅ COMPLETE

**Status**: Merged to main (2026-02-16)

- [x] Fix pyproject.toml dependencies
- [x] Add .env configuration support
- [x] Create interactive CLI with REPL
- [x] Add structured logging (console + file)
- [x] Create requirements.txt
- [x] Refactor code into src/ package
- [x] All testing completed and documented
- [x] README updated with troubleshooting notes

---

## Phase 2: Enhanced Tools (PLANNED)

### File Operations
- [ ] `list_files(path, pattern)` - List directory contents with glob patterns
  - Support wildcards: `*.py`, `**/*.txt`
  - Return file names, sizes, modified dates
  - Handle recursive directory traversal

- [ ] `file_info(path)` - Get detailed file metadata
  - Size in bytes and human-readable format
  - Creation and modification timestamps
  - File permissions
  - File type detection

- [ ] `append_text(path, content)` - Append to files without rewriting
  - Add content to end of file
  - Useful for logs, notes, incremental updates
  - Return confirmation with bytes appended

### Git Integration
- [ ] `git_status()` - Show current git status
  - Modified files
  - Staged changes
  - Untracked files
  - Current branch

- [ ] `git_diff(path=None)` - Show changes in files
  - Diff for specific file or all changes
  - Staged vs unstaged diffs
  - Color-coded output

- [ ] `git_commit(message)` - Commit changes with approval
  - Human approval required
  - Validate commit message format
  - Show files being committed

- [ ] `git_log(n=5)` - Show recent commit history
  - Configurable number of commits
  - Show commit hash, author, date, message
  - Optional detailed view

### Shell Improvements
- [ ] Add timeout parameter to `run_shell`
  - Default: 30 seconds
  - Configurable via .env
  - Kill processes that exceed timeout

- [ ] Return exit codes with output
  - Include return code in response
  - Distinguish success/failure
  - Better error handling

- [ ] Expand command denylist
  - Add: `mkfs`, `dd`, `fdisk`, `kill -9`
  - Make denylist configurable via .env
  - Add command whitelisting option

### Conversation Memory
- [ ] Implement conversation history
  - Track last N exchanges (configurable)
  - Maintain context across prompts
  - Prevent context window overflow

- [ ] Session persistence
  - Save conversations to disk
  - Load previous sessions
  - Session management commands

- [ ] Conversation summarization
  - Auto-summarize long conversations
  - Keep context under token limits
  - Preserve important information

---

## Phase 3: Quality & Safety (PLANNED)

### Testing
- [ ] Unit tests for each tool
  - pytest framework
  - Mock llama.cpp responses
  - Test edge cases and errors

- [ ] Integration tests
  - End-to-end agent workflows
  - Multi-step task testing
  - Tool interaction tests

- [ ] CI/CD setup
  - GitHub Actions workflow
  - Automated testing on PR
  - Mock llama.cpp server for tests

- [ ] Test coverage reporting
  - pytest-cov integration
  - Target: 80%+ coverage
  - Coverage badges

### Safety Enhancements
- [ ] Path traversal protection
  - Validate all file paths
  - Prevent `../../etc/passwd` attacks
  - Restrict to allowed directories

- [ ] Command whitelisting
  - Optional whitelist mode
  - Define allowed commands
  - More restrictive than denylist

- [ ] Audit logging
  - Log all shell commands executed
  - Track approval/rejection
  - Timestamp and user tracking

- [ ] Resource limits
  - Max file size for reads/writes
  - Max output length from shell
  - Memory and CPU limits

### Code Quality
- [ ] Add type hints throughout
  - All function signatures
  - Return types
  - mypy validation

- [ ] Setup ruff for linting
  - Auto-formatting on save
  - Import organization
  - Code style enforcement

- [ ] Pre-commit hooks
  - Run ruff before commit
  - Type checking
  - Test execution

- [ ] Improve docstrings
  - Complete all function docs
  - Add usage examples
  - Document exceptions

### Monitoring
- [ ] Token usage tracking
  - Per-session token counts
  - Cost estimation
  - Usage warnings

- [ ] Performance metrics
  - Execution time per tool
  - Agent response times
  - Bottleneck identification

- [ ] Error rate monitoring
  - Track failed operations
  - Error categorization
  - Alert on high error rates

---

## Phase 4: Advanced Features (PLANNED)

### Web & API Tools
- [ ] `web_search(query)` - Search integration
  - DuckDuckGo or other search API
  - Return top N results
  - Extract relevant snippets

- [ ] `fetch_url(url)` - Web content retrieval
  - Download web pages
  - Parse HTML content
  - Extract text and links

- [ ] `api_call(url, method, data)` - HTTP requests
  - GET, POST, PUT, DELETE support
  - JSON request/response handling
  - Authentication support

### Code Execution
- [ ] `run_python(code)` - Isolated Python execution
  - Sandboxed environment
  - Import restrictions
  - Timeout limits

- [ ] Code validation
  - Syntax checking before execution
  - Security scanning
  - Dependency analysis

### Multi-Agent Features
- [ ] Specialized agents
  - CoderAgent: Code generation and editing
  - ResearcherAgent: Information gathering
  - ReviewerAgent: Code review and QA

- [ ] Agent-to-agent communication
  - Task delegation protocol
  - Result sharing
  - Coordination mechanisms

- [ ] Task orchestration
  - Break complex tasks into subtasks
  - Assign to appropriate agents
  - Aggregate results

### Tool Creation
- [ ] `create_tool()` - Dynamic tool creation
  - Agent can define new tools
  - Validation and sandboxing
  - Store custom tools

- [ ] Tool marketplace
  - Share custom tools
  - Import community tools
  - Version management

### Workflow Automation
- [ ] Workflow templates
  - Save common task sequences
  - Parameterized workflows
  - Template library

- [ ] Workflow replay
  - Record task execution
  - Replay with modifications
  - Debugging and optimization

- [ ] Scheduled tasks
  - Cron-like scheduling
  - Periodic execution
  - Task queuing

### Deployment
- [ ] Docker support
  - Dockerfile for agent
  - Include llama.cpp in image
  - Docker Compose setup

- [ ] PyPI package
  - Publish to PyPI
  - pip installable
  - Version management

- [ ] Installation scripts
  - One-command setup
  - Dependency checking
  - Configuration wizard

---

## Documentation (ONGOING)

- [ ] Add CONTRIBUTING.md
  - Development setup
  - Code style guide
  - PR process

- [ ] Create examples/ directory
  - Common use case examples
  - Code snippets
  - Tutorial notebooks

- [ ] Add architecture diagram
  - System overview
  - Component relationships
  - Data flow

- [ ] Expand docs/tools.md
  - Detailed tool documentation
  - Parameters and return values
  - Usage examples

- [ ] Add troubleshooting guide
  - Common issues and solutions
  - FAQ section
  - Debugging tips

- [ ] Record demo videos/GIFs
  - Feature demonstrations
  - Tutorial videos
  - Animated GIFs for README

---

## Ideas / Future Considerations

### Voice Integration
- Voice input for prompts
- Text-to-speech for responses
- Hands-free operation

### Model Switching
- Hot-swap models without restart
- Multi-model support (fallback)
- Model selection per task

### Plugin System
- Third-party plugin support
- Plugin discovery and installation
- Plugin API and SDK

### Web UI
- Browser-based interface
- FastAPI backend
- React/Vue frontend

### Database Integration
- SQLite/PostgreSQL tools
- Query execution
- Schema inspection

### Cloud Integration
- AWS/GCP/Azure tools
- Cloud resource management
- Cost tracking

### Collaboration Features
- Multi-user support
- Shared sessions
- Team workspaces

---

## Notes

- Each phase builds on previous phases
- Testing happens continuously
- Documentation updates with each phase
- Backward compatibility maintained
- User feedback drives priorities

**Last Updated**: 2026-02-16
