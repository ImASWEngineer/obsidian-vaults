
> **Version:** 2025-05-25 | **Maintainer:** AgentBrain Core Team  
> This README consolidates the complete operating rules for *AgentBrain* and embeds the reliability safeguards derived from the *Failure‑point & Hallucination Analysis*.

---
## 📌 Protocol Mind‑map
Paste the block into any Markdown viewer that understands Mermaid to see the interactive mind‑map.

~~~mermaid
mindmap
  root((AgentBrain Command Protocol))
    Core Commands
      :UpdateGeneratedContextAndCodeInsights
        Phase 1: Doc Scan & Req Extract
        Phase 2: Source Verify
        Phase 3: breadcrumbs Docs
        Phase 4: Consolidate & Gate
      :buildProtocol
        Build Checklist
        BuildProtocolGuide.md
      :mission
        Phase Pre‑Compliance
        Phase Discovery
        Phase Planning
        Phase Implementation
        Phase Review & Delivery
    Additional Rules
      Documentation‑first
      Reference Propagation
      Context Validation (DFS)
      Think>Implement>Test Cycle
      Commit Discipline
      Reflection Embedding
      Regression Coverage
      Test‑Source Separation
      Test Data Pattern
    Memory Management
      Mission State Memories
      Protocol Context Memories
      MemoryIDs Registry
    Conversation Format
      LIFO Entry Logging
      CRUD Rules
      Audit Tags & Counters
    Foundational Principles
      Think Like Compiler
      First Principles Thinking
~~~

---
## 🔒 Reliability Safeguards & Hallucination Prevention

| ID | Failure Point (Hazard) | Embedded Mitigation | Proof‑of‑Enforcement |
| :--: | ------------------------ | --------------------- | ---------------------- |
| **A1** | Context‑window overflow | *Token‑budget guard*: `scripts/check_token_budget.sh` blocks runs above the configured limit; `conversation.md` auto‑summariser rotates old entries to an archive. | CI check `ci/token‑budget.yml` must pass |
| **A2** | Missing critical `.context/*.md` seed files | Each checklist begins with an **atomic create‑or‑fail** for required paths; the run aborts if creation fails. | Step `validate‑context‑tree` in every GitHub Action |
| **A3** | Untracked mission/protocol memory | Any `create_memory` call is followed by an enforced update to `MemoryIDs.md`; linter `lint/memory_registry.py` rejects missing entries. | `pre‑commit` hook `memory‑registry` |
| **A4** | Checklist items skipped | Parser `tools/checklist_verifier.ts` scans markdown and fails the build if an unchecked box precedes a checked one in any list. | CI job `ci/checklists.yml` |
| **A5** | Traceability Matrix missing or sparse | Gate `generate-traceability-matrix` requires at least one row per requirement; build fails otherwise. | Target in `Makefile` + CI |
| **A6** | Approval‑gate bypass | `ImplementationLock` state is validated at runtime; attempting to execute stories while locked throws an error. | Runtime assertion in `agent/locks.py` |
| **A7** | Documentation‑first rule violated | Linter `lint/docs_first.py` ensures any code diff touching `src/**` also touches related `*.md` or fails. | CI job `ci/docs_first.yml` |
| **A8** | DFS reference validation skipped | Script `scripts/dfs_linkcheck.py` walks all wiki links; any 404 aborts merge. | CI job `ci/linkcheck.yml` |
| **A9** | Test‑source mixing | ESLint / Flake8 rules forbid importing test packages from production code. | Static analysis gates |
| **A10** | Conversation log integrity loss | `conversation.md` is append‑only; git pre‑push hook blocks deletions or rewrites outside automated archival. | Hook `hooks/conv_append_only.sh` |

> **Why so many gates?**  
> Research shows that checklist and gate discipline cuts defect rates by more than 20%. Each safeguard is cheaper than an undetected hallucination.

---
## 1. Overview

*AgentBrain* is an autonomous AI engineer capable of analysing, planning and implementing complex Epics, Stories and code changes with high reliability. The protocol introduces four structured **phases**, uses **gated progression**, and follows a **documentation‑first** ethic so every change is traceable and reviewable.

---
## 2. Command Protocol

### 2.1 Core Commands

#### :UpdateGeneratedContextAndCodeInsights
Runs a documentation scan, verifies source code, links requirements to code, and writes architecture docs.

#### :buildProtocol
Executes environment‑specific build and test steps. See *BuildProtocolGuide.md*.

#### :mission
Bootstraps a new mission and drives it through discovery → planning → implementation → review.

---
### 2.2 Global Checklists (All Commands)
Every protocol begins with these universal steps:

1. **Seed Context** – create/verify required `.context/*.md` files; abort if any creation fails (*A2*).
2. **Register Memory** – update `MemoryIDs.md` immediately after creating protocol/mission memories (*A3*).
3. **Token Guard** – run `check_token_budget.sh` and summarise if needed (*A1*).
4. **Execute Phase Checklists** – see per‑command sections below.
5. **Enforce Gates** – approval gates and lock checks must pass before advancing (*A6*).

---
### 2.3 :UpdateGeneratedContextAndCodeInsights Checklist

<details>
<summary>Full Checklist</summary>

- [ ] **Create protocol memory** and log to `MemoryIDs.md`
- [ ] **Seed context files** → `Breadcrumbs/.context/UpdateGeneratedContextAndCodeInsights.md`, `Breadcrumbs/.context/conversation.md`
- [ ] **Phase 1 – Documentation & Requirements**
    - [ ] Traverse project for `.md` files
    - [ ] Extract `==Requirements==` sections
    - [ ] Build initial target file list
    - [ ] Add missing `==References==` placeholders
- [ ] **Phase 2 – Source Verification**
    - [ ] Select requirement batch
    - [ ] Locate and analyse code
    - [ ] Link requirements → code entities
    - [ ] Iterate until coverage = 100%
- [ ] **Phase 3 – Hierarchical Documentation**
    - [ ] Generate `.breadcrumbs` docs, indexes, diagrams
- [ ] **Phase 4 – Consolidation**
    - [ ] Update original docs
    - [ ] **DFS link‑validate** (`dfs_linkcheck.py`) (*A8*)
    - [ ] Generate Traceability Matrix (*A5*)
    - [ ] Distribute post‑mission insights
    - [ ] Await approval gate
- [ ] **Cleanup** – delete protocol memory and context file

</details>

---
### 2.4 :buildProtocol Checklist

<details>
<summary>Full Checklist</summary>

- [ ] **Create protocol memory** and log to `MemoryIDs.md`
- [ ] **Seed context files** → `Breadcrumbs/.context/buildProtocol.md`, `Breadcrumbs/.context/conversation.md`
- [ ] **Analyse solution structure** and project dependencies
- [ ] **Select build tooling** (MSBuild, dotnet, etc.)
- [ ] **Run build**; capture artefacts
- [ ] **Run tests**; store results
- [ ] **Resolve build/test issues** using first‑principles debugging
- [ ] **Commit validation proof** (test results) to VCS
- [ ] **Approval gate** if any step fails or major decision pivot needed
- [ ] **Cleanup** – delete protocol memory and context file

</details>

---
### 2.5 :mission Checklist

<details>
<summary>Full Checklist</summary>

- [ ] **Create mission memory** and log to `MemoryIDs.md`
- [ ] **Seed context files** → `Breadcrumbs/.context/mission.md`, `Breadcrumbs/.context/conversation.md`
- [ ] **Phase: Preliminary Rule Compliance** – read additional rules, reflect in planning
- [ ] **Phase: Discovery** – clarify requirements, update `==DiscoveryInsights==`, run `:UpdateGeneratedContextAndCodeInsights`
- [ ] **Phase: Planning** – generate diagrams, risks, dependencies, `WorkBreakDownStructurePhaseI/II`; ensure `ImplementationLock` logic; seek approval gate
- [ ] **Phase: Implementation** – lock implementation, generate `StoriesQueue.json`, execute steps, seek per‑story approvals, commit work
- [ ] **Phase: Review & Delivery** – regression test, perform `==PostMissionReflection==`, ensure compliance checklists pass
- [ ] **Cleanup** – delete mission memory when complete

</details>

---
## 3. Conversation Format (LIFO Log)

All interactions are logged in `Breadcrumbs/.context/conversation.md` using the **append‑only** format below. A pre‑push git hook enforces immutability (*A10*).

> ## YYYY-MM-DD HH:MM:SS | LLM-Name | PUPC XX | PFAC XX | Δt HH:MM:SS | Action Title
> Tags: [phase:Planning] [status:pending_approval] [TechnicalCapabilities:valid_implementation] [DecisionMakingFault:false]
> Description: Planning completed. Awaiting confirmation to unlock implementation.

---
## 4. Additional Rules (Normative)

1. **Documentation‑First** – analyse docs before touching code (*A7*).
2. **Reference Propagation** – every `.

