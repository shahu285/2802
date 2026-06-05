# 🏆 Project Architecture State Ledger: Full-Stack Sports Journalism Desk

## 1. System Overview & End Goal
The absolute end goal of this project is to build an autonomous, production-grade Multi-Agent Sports Newsroom Desk that monitors live sports feeds, performs contextual filtering for the Indian market, writes high-velocity micro-blog posts, retrieves real-time press imagery, and surfaces drafts on a modern Web Dashboard.

### The Ultimate Operational Loop:
- **Autonomous Ingestion & Curation:** Agents operate silently on a background loop fetching and filtering live breaking sports stories.
- **Human-in-the-Loop (HITL) Security Switch:** No post is ever published automatically. Drafts are sent to a web panel where a human editor reviews the compiled text and the chosen image URL.
- **One-Click Publishing Broadcast:** Upon human approval, the system triggers an outbound network adapter to publish the verified news package straight to social networks (like the decentralized Bluesky micro-blogging ecosystem).

---

## 2. Global Tech Stack (Zero-Infrastructure Cost Blueprint)
- **Layer 1 (Logic Engine):** Python Pipeline + LangChain Orchestration
- **Layer 2 (State/Memory):** Supabase (PostgreSQL Cloud Database Instance)
- **Layer 3 (Presentation):** Next.js (React/Tailwind UI Dashboard) + FastAPI (Python Gateway)
- **Model Intelligence:** Google Gemini 2.5 Flash Lite (`gemini-2.5-flash-lite`) via Free Tier Google AI Studio API for optimized speed, deterministic reasoning, and ultra-low latency.
- **Ingestion Channel:** Public XML/RSS Feeds (ESPN Cricinfo, Sky Sports, NDTV Other Sports) with browser User-Agent header spoofing proxies.
- **Real-Time Image Research Engine:** Tavily Search API (`TAVILY_API_KEY`) utilized for structured, web-grounded press image lookup.
- **Outbound Channel:** Open-source AT Protocol SDK (`atproto` Python client for Bluesky networks).

---

## 3. Production Architecture Diagram
[Ingestion Desks (RSS)] ──> [Beat Reporter (Python)]
│
▼
[Regional Desk Editor (Gemini 2.5 Flash Lite)]
│
▼
[Sports Journalist (Gemini 2.5 Flash Lite)]
│
▼
[Visual Photojournalist (Tavily API Lookup)]
│
▼
[VERIFIED INTEGRATION PIPELINE (test_pipeline.py)]
│
▼
[Supabase DB (Pending Queue Table)]
│
▼
[FastAPI Controller Gateway]
│
▼
[Next.js Frontend (HITL Approval UI)]
│
▼
[Outbound Social Media Network]


---

## 4. Deep-Dive Full-Stack Layer Specification

### 📦 LAYER 1: THE CORE AGENT ENGINE (STATUS: VERIFIED COMPLETE)
All individual core agent modules are written, isolated, and completely functional. They interact through a unified execution sequence managed and verified inside `test_pipeline.py`. Every agent logs its operational metrics natively to `newsroom.log`.

- **Agent 1: Beat Reporter (`beat_reporter.py`):** Ingests live data streams across multiple sports disciplines (Cricket, European Football, and General Multi-sport vectors tracking Hockey, Badminton, Chess, and Athletics) using custom HTTP headers to avoid anti-bot blocking.
- **Agent 2: Regional Desk Editor (`regional_editor.py`):** Acts as a data-driven gatekeeper. Uses Gemini 2.5 Flash Lite to cross-examine scraped headlines against an explicit Indian sports market viewership matrix (Cricket ~65%, Kabaddi 200M+, European Football/ISL, Olympic individual disciplines) to return a binary decision (`ALLOW`/`BLOCK`).
- **Agent 3: Sports Journalist (`copywriter_agent.py`):** Implements an automated 3-Tier News Severity Matrix. If a headline represents massive breaking shifts (captaincy handovers or retirements), it applies a high-velocity style blueprint (`🚨BREAKING` flags). If it is a standard match or feature, it naturally curates the tone to sound like an authentic human sports reporter, dropping rigid bot indicators.
- **Agent 4: Visual Photojournalist (`photojournalist.py`):** Utilizes the Tavily Search API. It reads the headline, abstracts search entity queries via Gemini 2.5 Flash Lite, searches the open web for live breaking media assets, and returns direct `.jpg` / `.png` press photo URLs. Includes a resilient fallback image URL structure.
- **The Integration Verification Gate (`test_pipeline.py`):** A custom operational integration file that strings all 4 agents together. Running `python test_pipeline.py` executes a full mock run showing a raw headline successfully flowing through regional validation, custom tone copywriting styling, and real-time Tavily image allocation in a single process.

### 🗄️ LAYER 2: THE DATABASE & MEMORY LAYER (STATUS: PENDING / NEXT UP)
This layer transitions the system from volatile local console execution to cloud-backed persistence, acting as the structural data bridge between our background AI agents and our frontend dashboard.

- **Cloud Instance:** Free-tier Supabase project running an enterprise PostgreSQL database engine.
- **Database Schema:** A main table named `pending_posts` configured with the following columns:
  - `id`: UUID (Primary Key, Auto-generated)
  - `raw_headline`: TEXT (Original source news headline)
  - `styled_text`: TEXT (The custom, style-cloned copy drafted by Agent 3)
  - `image_url`: TEXT (The live news picture URL fetched by Agent 4 via Tavily)
  - `severity_tier`: TEXT (Tier 1, Tier 2, or Tier 3 classification string)
  - `status`: TEXT (Defaults strictly to `'pending'`. Changes to `'approved'` or `'rejected'` via user dashboard)
  - `created_at`: TIMESTAMPTZ (Auto-timestamping for feed ordering)
- **Data Insertion Layer:** A python helper class (`database_manager.py`) utilizing `supabase-py` to let our agents perform async backend `INSERT` queries upon completing a successful pipeline run.

### 💻 LAYER 3: THE PRESENTATION & GATEWAY LAYER (STATUS: PENDING)
The front-facing surface layer that exposes our data storage queue to human editors and handles outbound secure network broadcasting.

- **The Backend Gateway (FastAPI):** A high-performance, lightweight Python web framework (`main.py`) that handles API requests. It provides secure endpoints for the frontend application:
  - `GET /api/posts/pending`: Fetches all items from Supabase where `status == 'pending'`.
  - `POST /api/posts/{id}/approve`: Updates status to `'approved'` in Supabase and instantly triggers the outbound network broadcast.
  - `POST /api/posts/{id}/reject`: Updates status to `'rejected'` to clean up the queue.
- **The Human-in-the-Loop Frontend (Next.js + Tailwind CSS):** A beautiful, responsive web interface built with React. It queries the FastAPI server and renders the pending posts as clean social media preview cards. Human editors can review the text layout, verify the live image, edit the text manually if desired, and click an "Approve & Publish" button.
- **The Broadcasting Adapter (`publisher.py`):** Connected directly to the FastAPI approval endpoint. It uses the official `atproto` Python SDK client to authenticate with the Bluesky network, upload the image asset binary, attach the formatted text payload, and broadcast the final sports post live to the public internet.

---

## 5. System Execution Context (Rules for Upcoming AI Agents)
Any AI model or developer continuing this repository must:
1. Strictly maintain the zero-cost architecture boundaries.
2. Use **Gemini 2.5 Flash Lite** (`gemini-2.5-flash-lite`) as the standard LLM driver for low latency and high consistency.
3. Preserve the native logging outputs routing into `newsroom.log`.
4. Ensure code structures remain highly modular, following clean functional abstraction paradigms.