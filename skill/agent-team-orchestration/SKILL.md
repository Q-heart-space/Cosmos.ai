---
name: agent-team-orchestration
description: "Orchestrate multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows.
  多Agent团队编排——定义角色、任务生命周期、交接协议和审查工作流。与 multi-agent-orchestrator 互补：本技能管团队结构，orchestrator 管任务并行。 触发词：建团队、多人协作、Agent协作、团队编排、Team orchestration、multi-agent."
space_scope: universal
reuse_depth: agnostic
scope_axis: governance
trust_level: notification
version: 1.0.0-ext
distribute_external: yes
depends: adversarial-audit, multi-agent-orchestrator, references/team-setup.md, references/task-lifecycle.md, references/communication.md
triggers:
  - 建团队
  - 多人协作
  - Agent协作
  - 团队编排
circuit: ⑩级联推进
deprecated: false
updated_at: 2026-08-13
---

# Agent Team Orchestration

Production playbook for running multi-agent teams with clear roles, structured task flow, and quality gates.

## Quick Start: Minimal 2-Agent Team

A builder and a reviewer. The simplest useful team.

### 1. Define Roles

```
Orchestrator (you) — Route tasks, track state, report results
Builder agent     — Execute work, produce artifacts
```

### 2. Spawn a Task

```
1. Create task record (file, DB, or task board)
2. Spawn builder with:
   - Task ID and description
   - Output path for artifacts
   - Handoff instructions (what to produce, where to put it)
3. On completion: review artifacts, mark done, report
4. **对抗式审查（adversarial-audit）**：≥3 Agent时强制执行——独立Agent审计·递归闭环修复·零P0
```

### 3. Add a Reviewer

```
Builder produces artifact → Reviewer checks it → Orchestrator ships or returns
```

That's the core loop. Everything below scales this pattern.

## Core Concepts

### Roles

Every agent has one primary role. Overlap causes confusion.

| Role | Purpose | Model guidance |
|------|---------|---------------|
| **Orchestrator** | Route work, track state, make priority calls | High-reasoning model (handles judgment) |
| **Builder** | Produce artifacts — code, docs, configs | Can use cost-effective models for mechanical work |
| **Reviewer** | Verify quality, push back on gaps | High-reasoning model (catches what builders miss) |
| **Ops** | Cron jobs, standups, health checks, dispatching | Cheapest model that's reliable |

→ *Read [references/team-setup.md](references/team-setup.md) when defining a new team or adding agents.*

### Task States

Every task moves through a defined lifecycle:

```
Inbox → Assigned → In Progress → Review → Done | Failed
```

**Rules:**
- Orchestrator owns state transitions — don't rely on agents to update their own status
- Every transition gets a comment (who, what, why)
- Failed is a valid end state — capture why and move on

→ *Read [references/task-lifecycle.md](references/task-lifecycle.md) when designing task flows or debugging stuck tasks.*

### Handoffs

When work passes between agents, the handoff message includes:

1. **What was done** — summary of changes/output
2. **Where artifacts are** — exact file paths
3. **How to verify** — test commands or acceptance criteria
4. **Known issues** — anything incomplete or risky
5. **What's next** — clear next action for the receiving agent

Bad handoff: *"Done, check the files."*
Good handoff: *"Built auth module at `/shared/artifacts/auth/`. Run `npm test auth` to verify. Known issue: rate limiting not implemented yet. Next: reviewer checks error handling edge cases."*

### Reviews

Cross-role reviews prevent quality drift:

- **Builders review specs** — "Is this feasible? What's missing?"
- **Reviewers check builds** — "Does this match the spec? Edge cases?"
- **Orchestrator reviews priorities** — "Is this the right work right now?"

Skip the review step and quality degrades within 3-5 tasks. Every time.

→ *Read [references/communication.md](references/communication.md) when setting up agent communication channels.*
→ *Read [references/patterns.md](references/patterns.md) for proven multi-step workflows.*

## Reference Files

| File | Read when... |
|------|-------------|
| [team-setup.md](references/team-setup.md) | Defining agents, roles, models, workspaces |
| [task-lifecycle.md](references/task-lifecycle.md) | Designing task states, transitions, comments |
| [communication.md](references/communication.md) | Setting up async/sync communication, artifact paths |
| [patterns.md](references/patterns.md) | Implementing specific workflows (spec→build→test, parallel research, escalation) |

## Common Pitfalls

### Spawning without clear artifact output paths
Agent produces great work, but you can't find it. Always specify the exact output path in the spawn prompt. Use a shared artifacts directory with predictable structure.

### No review step = quality drift
"It's a small change, skip review." Do this three times and you have compounding errors. Every artifact gets at least one set of eyes that didn't produce it.

### Agents not commenting on task progress
Silent agents create coordination blind spots. Require comments at: start, blocker, handoff, completion. If an agent goes silent, assume it's stuck.

### Not verifying agent capabilities before assigning
Assigning browser-based testing to an agent without browser access. Assigning image work to a text-only model. Check capabilities before routing.

### Orchestrator doing execution work
The orchestrator routes and tracks — it doesn't build. The moment you start "just quickly doing this one thing," you've lost oversight of the rest of the team.

### 🆕 Spawning agents without concurrency governance (铁律BS·META-117·2026-07-24)
Multiple agents spawned in parallel compete for disk I/O → resource exhaustion → all agents fail. Always route agent spawns through `python scripts/concurrency_governor.py --submit "agent_task" --priority P1 --source "multi-agent"` to enforce resource pool limits (max_workers=4). Without this, a team of 5 agents doing heavy file operations will self-destruct.

## When NOT to Use This Skill

- **Single-agent setups** — Just follow standard AGENTS.md conventions. Team orchestration adds overhead that solo agents don't need.
- **One-off task delegation** — Use `sessions_spawn` directly. This skill is for sustained workflows with multiple handoffs.
- **Simple question routing** — If you're just forwarding a question to a specialist, that's a message, not a workflow.

This skill is for **sustained team workflows** — recurring collaboration patterns where agents depend on each other's output over multiple tasks.

## 盲区与自审
- 本技能的已知盲区：本技能只提供团队结构编排方法论（角色/任务生命周期/交接/审查），不执行实际的任务分发与调度（那是 multi-agent-orchestrator 的职责）；单Agent、一次性委托、简单问答路由等场景不适用。其有效性依赖底层 Agent 平台真实支持 `sessions_spawn`/`run_in_background`/`bypassPermissions`，若平台无此能力，编排脚本无法落地。
- 自审方式：当"建团队"请求出现但迟迟没有 Agent 真正被 spawn 时，检查是否误把结构设计当成了执行调度；当任务卡在 Inbox 无流转时，检查是否缺少 Reviewer 角色或交接信息不完整。
