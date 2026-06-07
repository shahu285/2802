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

## 4. Data Workflow & Status Flow

### The Complete Pipeline Flow:
```
Beat_Reporter (fetches RSS) 
    → Regional_Editor (filters for Indian sports)
    → Copywriter_Agent (generates viral post)
    → Photojournalist (finds image)
    ↓
SUPABASE (pending_posts table - stores all data)
    ↓
Frontend Dashboard (displays posts for review)
    ↓
User clicks "Approve" → publisher.py posts to Bluesky
```

### Database Status Flow:
| Status     | Meaning              | Next Action |
|--------    |---------             |-------------|
| `pending`  | Awaiting your review | View in dashboard |
| `approved` | You approved it      | Auto-publishes to Bluesky |
| `rejected` | You rejected it      | Removed from queue |

### Each Post Stores:
| Column           | Purpose                       | Example |
|--------          |---------                      |---------|
| `id`             | Unique ID                     | `abc-123-def-456` |
| `raw_headline`   | Original RSS headline         | "Dhoni retires from IPL" |
| `styled_text`    | AI-generated viral post       | "🚨BREAKING: MS Dhoni..." |
| `image_url`      | Photo from Photojournalist    | `https://images.unsplash.com/...` |
| `severity_tier`  | News importance (Tier 1/2/3)  | `Tier 1` (breaking) |
| `status`         | Approval flow control         | `pending` → `approved`/`rejected` |
| `source_feed`    | Which RSS feed                | `Cricket Feed` |
| `created_at`     | Timestamp                     | `2026-06-06 16:03:00` |

---

## 5. Deep-Dive Full-Stack Layer Specification

### 📦 LAYER 1: THE CORE AGENT ENGINE (STATUS: ✅ COMPLETE)

**Execution Flow (Step by Step):**

```
1. Beat_Reporter (agents/beat_reporter.py)
   └─> Fetches headlines from 4 RSS feeds (Cricket, Football, All News, Other Sports)
   └─> Filters articles from last 24 hours
   └─> Returns list of articles with: headline, source, URL, pub_date

2. Regional_Editor (agents/regional_editor.py)
   └─> Receives each headline from Beat_Reporter
   └─> Uses Groq LLM (llama-3.3-70b-versatile) to classify: ALLOW or BLOCK
   └─> Allows: Cricket, Kabaddi, Football, Indian sports
   └─> Blocks: US sports (NFL, NBA, MLB), minor gossip

3. Copywriter_Agent (agents/copywriter_agent.py)
   └─> Receives approved headline
   └─> Uses Groq LLM to analyze severity (Tier 1/2/3)
   └─> Generates viral post (<280 chars) with appropriate formatting
   └─> Returns styled text ready for posting

4. Photojournalist (agents/photojournalist.py)
   └─> Uses Groq to extract 3-4 keyword search query from headline
   └─> Searches Tavily API for relevant images
   └─> Filters out: social media, quotes, thumbnails, text overlays
   └─> Returns clean image URL
```

**Database Layer (Layer 2):**
```
5. database_manager (database/database_manager.py)
   └─> Saves complete post to Supabase pending_posts table
   └─> Status defaults to "pending" for human review
   └─> Returns saved record with ID
```

**Current Pipeline Command:**
```bash
python test_pipeline.py
```

**Output:** Posts saved to Supabase with status="pending"
All individual core agent modules are written, isolated, and completely functional. They interact through a unified execution sequence managed and verified inside `test_pipeline.py`. Every agent logs its operational metrics natively to `newsroom.log`.

- **Agent 1: Beat Reporter (`beat_reporter.py`):** Ingests live data streams across multiple sports disciplines (Cricket, European Football, and General Multi-sport vectors tracking Hockey, Badminton, Chess, and Athletics) using custom HTTP headers to avoid anti-bot blocking.
- **Agent 2: Regional Desk Editor (`regional_editor.py`):** Acts as a data-driven gatekeeper. Uses Gemini 2.5 Flash Lite to cross-examine scraped headlines against an explicit Indian sports market viewership matrix (Cricket ~65%, Kabaddi 200M+, European Football/ISL, Olympic individual disciplines) to return a binary decision (`ALLOW`/`BLOCK`).
- **Agent 3: Sports Journalist (`copywriter_agent.py`):** Implements an automated 3-Tier News Severity Matrix. If a headline represents massive breaking shifts (captaincy handovers or retirements), it applies a high-velocity style blueprint (`🚨BREAKING` flags). If it is a standard match or feature, it naturally curates the tone to sound like an authentic human sports reporter, dropping rigid bot indicators.
- **Agent 4: Visual Photojournalist (`photojournalist.py`):** Utilizes the Tavily Search API. It reads the headline, abstracts search entity queries via Gemini 2.5 Flash Lite, searches the open web for live breaking media assets, and returns direct `.jpg` / `.png` press photo URLs. Includes a resilient fallback image URL structure.
- **The Integration Verification Gate (`test_pipeline.py`):** A custom operational integration file that strings all 4 agents together. Running `python test_pipeline.py` executes a full mock run showing a raw headline successfully flowing through regional validation, custom tone copywriting styling, and real-time Tavily image allocation in a single process.

### 🗄️ LAYER 2: THE DATABASE & MEMORY LAYER (STATUS: ✅ COMPLETE)

- **Cloud Instance:** Free-tier Supabase project
- **Project URL:** `https://lmwohypczyicnznoqejo.supabase.co`
- **Database Table:** `pending_posts`

**Schema:**
```sql
pending_posts (
  id UUID PRIMARY KEY,
  raw_headline TEXT,
  styled_text TEXT,
  image_url TEXT,
  severity_tier TEXT DEFAULT 'Tier 2',
  status TEXT DEFAULT 'pending',
  source_feed TEXT,
  created_at TIMESTAMPTZ
)
```

**Available Functions in database_manager.py:**
- `insert_pending_post()` - Save new post
- `get_pending_posts()` - Fetch pending posts
- `get_all_posts()` - Fetch all posts
- `update_post_status()` - Approve/reject
- `delete_post()` - Remove post

---

### 💻 LAYER 3: THE PRESENTATION & GATEWAY LAYER (STATUS: ✅ COMPLETE)

**Backend Structure:**
```
backend/
├── main.py           # FastAPI server with REST endpoints
├── publisher.py      # Bluesky posting functionality
└── requirements.txt  # Python dependencies
```

The front-facing surface layer that exposes our data storage queue to human editors and handles outbound secure network broadcasting.

- **The Backend Gateway (FastAPI):** (`backend/main.py`) provides these endpoints:
  - `GET /api/posts/pending` - Fetch pending posts
  - `GET /api/posts/all` - Fetch all posts  
  - `POST /api/posts/{id}/approve` - Approve post (status → approved)
  - `POST /api/posts/{id}/reject` - Reject post (status → rejected)
  - `DELETE /api/posts/{id}` - Delete post
  - `POST /api/posts` - Create new post manually

- **The Broadcasting Adapter (`backend/publisher.py`):**
  - `publish_post(text)` - Post text to Bluesky
  - `publish_post_with_image(text, image_url)` - Post with image

**To Run Backend:**
```bash
cd backend
python main.py
# Server runs at http://localhost:8000
```

---

### 💻 Frontend (STATUS: PENDING - Optional)
- **Next.js + Tailwind CSS** - React dashboard (future enhancement)
- Can use API endpoints directly for now

---

## 6. Frontend Dashboard Features

The web dashboard should visualize this workflow for easy understanding:

### Dashboard View:
- **Pipeline Status** - Show current step (Fetching → Filtering → Writing → Getting Image → Storing)
- **Post Queue** - List all `pending` posts with:
  - Raw headline
  - Styled post preview
  - Image thumbnail
  - Severity badge (Tier 1/2/3)
  - Source feed indicator
  - Timestamp
- **Action Buttons** - "Approve & Publish" / "Reject"
- **History Tab** - View `approved` and `rejected` posts

### Visual Flow Indicator:
```
[🔄 Fetching] → [🔍 Filtering] → [✍️ Writing] → [🖼️ Image] → [💾 Stored]
                                                                   ↓
                                                            [📱 Dashboard]
                                                                   ↓
                                                            [✅ Approve] → [🚀 Bluesky]
```

This helps users understand where each post is in the pipeline.

---

## 7. System Execution Context (Rules for Upcoming AI Agents)
Any AI model or developer continuing this repository must:
1. Strictly maintain the zero-cost architecture boundaries.
2. Use **Gemini 2.5 Flash Lite** (`gemini-2.5-flash-lite`) as the standard LLM driver for low latency and high consistency.
3. Preserve the native logging outputs routing into `newsroom.log`.
4. Ensure code structures remain highly modular, following clean functional abstraction paradigms.