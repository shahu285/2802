# 🏆 Project Architecture State Ledger: Full-Stack Sports Journalism Desk

## 1. System Overview
An Autonomous, Data-Driven Sports Journalism Desk tailored for the Indian sports ecosystem (Cricket, European Football, Kabaddi, and Major Global/Olympic disciplines). The system operates on a zero-infrastructure cost footprint, scaling via a multi-agent workflow from ingestion to human-verified publishing.

## 2. Global Tech Stack (Zero-Cost Allocation)
- **Layer 1 (Logic Engine):** Python + LangGraph Core Orchestration
- **Layer 2 (State/Memory):** Supabase (PostgreSQL Cloud Instance)
- **Layer 3 (Presentation):** Next.js (React/Tailwind UI) + FastAPI (Python Gateway)
- **Model Intelligence:** Google Gemini 1.5 Flash (via Free Tier Google AI Studio API)
- **Ingestion Channel:** Public XML/RSS Sports Desks via Browser Headers Proxies
- **Outbound Channel:** Open-source AT Protocol SDK (`atproto` Python client for Bluesky)

## 3. Production Architecture Blueprint

[Ingestion Desks (RSS)] -> [Beat Reporter (Python)]
│
▼
[Regional Desk Editor (Gemini)]
│
▼
[Sports Journalist (Gemini)]
│
▼
[Visual Photojournalist (DDG Search)]
│
▼
[Supabase DB (Pending Queue)]
│
▼
[FastAPI Controller Gateway]
│
▼
[Next.js Frontend (HITL Approval)]
│
▼
[Bluesky Network Core]
## 4. Current Phase: Layer 1 – The Core Agent Engine
We are incrementally compiling the isolated Python agent scripts on dedicated Git branches before wrapping them into a formal state graph structure. All files implement strict, native Python `logging` to `newsroom.log`.

### Completed Checkpoints:
- [x] **Workspace Configuration:** Security guardrails active. `.env` containing tokens and `.gitignore` preventing data leaks verified.
- [x] **Agent 1: Beat Reporter (`beat_reporter.py`):** Successfully connects to ESPN Cricinfo, Sky Sports, and NDTV Other Sports RSS channels. Bypasses firewalls using User-Agent masking, fetches live headline elements, logs audit tracks, and records arrays cleanly.
- [x] **Agent 2: Regional Desk Editor (`regional_editor.py`):** Functional data-driven gatekeeper node. Uses Gemini 1.5 Flash (`temperature=0.1`) to evaluate headlines against a hardcoded Indian market viewership matrix (Cricket ~65%, Kabaddi 200M+, European Football/ISL, Olympic representation). Outputs strict binary decisions (`ALLOW`/`BLOCK`).

### Active Branch Target:
- **Current Branch:** `feature/copywriter-agent`
- **Next Task:** Build **Agent 3: The Sports Journalist (`copywriter_agent.py`)** to transform approved raw headlines into high-engagement micro-blog text posts that replicate the exact stylistic behaviors (spacing, caps emphasis, header markers) of target sports profiles like Mufaddal Vohra and Johns.

## 5. System Execution Context (How to Resume Instructions)
When this ledger is provided to a new AI session to resume work, the AI must:
1. Maintain the strict zero-cost developer constraints.
2. Ensure every written script inherits the unified native file logging configuration framework to output tracking scripts inside `newsroom.log`.
3. Provide instructions formatted as modular blueprints optimized for an internal IDE generation assistant.