# 📰 Multi-Agent Sports Newsroom AI

An autonomous, full-stack sports journalism pipeline that fetches, filters, writes, and publishes sports news to social media with human-in-the-loop approval.

## 🎯 What It Does

1. **Fetches** sports news from 4 RSS feeds (Cricket, Football, All News, Other Sports)
2. **Filters** headlines using AI (focuses on Indian sports market)
3. **Writes** viral social media posts (<280 chars) with smart tier-based formatting
4. **Finds** relevant images using AI-powered search
5. **Saves** everything to a database with "pending" status
6. **Shows** posts in a modern web dashboard for review
7. **Publishes** approved posts to Bluesky with images

## 🏗️ Architecture

```
RSS Feeds → Beat Reporter → Regional Editor → Copywriter → Photojournalist
                                ↓
                         Supabase Database
                                ↓
                    FastAPI Backend (Port 8001)
                                ↓
                    Next.js Dashboard (Port 3000)
                                ↓
                           Bluesky API
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- API Keys in `.env` file:
  - `GROQ_API_KEY`
  - `TAVILY_API_KEY`
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY`
  - `BLUESKY_HANDLE`
  - `BLUESKY_PASSWORD`

### Installation

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Running the System

**1. Start Backend API:**
```bash
cd backend
python main.py
# Runs at http://127.0.0.1:8001
```

**2. Start Frontend Dashboard:**
```bash
cd frontend
npm run dev
# Runs at http://localhost:3000
```

**3. Generate Posts:**
```bash
python test_pipeline.py
```

**4. Open Dashboard:**
Open your browser to `http://localhost:3000`

## 📁 Project Structure

```
2802/
├── agents/                    # Layer 1: AI Agents
│   ├── beat_reporter.py      # Fetches RSS feeds
│   ├── regional_editor.py    # AI filtering
│   ├── copywriter_agent.py   # AI post writing
│   └── photojournalist.py    # AI image search
│
├── database/                  # Layer 2: Database
│   └── database_manager.py   # Supabase CRUD operations
│
├── backend/                   # Layer 3: API
│   ├── main.py               # FastAPI server
│   ├── publisher.py          # Bluesky posting
│   └── requirements.txt
│
├── frontend/                  # Layer 4: Dashboard
│   ├── app/
│   │   └── page.tsx          # Main dashboard
│   ├── components/
│   │   └── PostCard.tsx      # Post card component
│   ├── lib/
│   │   └── api.ts            # API client
│   └── package.json
│
├── test_pipeline.py          # Full pipeline test
├── architect_state.md        # Complete documentation
└── .env                      # API keys (not in git)
```

## 🎨 Dashboard Features

- **Stats Bar**: Shows pending, approved, rejected, and total posts
- **Pending Tab**: Review posts awaiting approval
- **History Tab**: View approved and rejected posts
- **Post Cards**: Display headline, styled text, image, tier, source
- **Actions**: "Approve & Publish" or "Reject" buttons
- **Auto-Refresh**: Updates every 30 seconds

## 🔧 Tech Stack

### Backend
- **Python 3.10+** with FastAPI
- **LangChain** for agent orchestration
- **Groq** (llama-3.3-70b-versatile) for AI
- **Tavily API** for image search
- **Supabase** (PostgreSQL) for database
- **Bluesky AT Protocol** for publishing

### Frontend
- **Next.js 16** with TypeScript
- **Tailwind CSS** for styling
- **React Hooks** for state management

## 📊 Database Schema

**Table: `pending_posts`**
```sql
id              UUID PRIMARY KEY
raw_headline    TEXT
styled_text     TEXT
image_url       TEXT
severity_tier   TEXT (Tier 1/2/3)
status          TEXT (pending/approved/rejected)
source_feed     TEXT
created_at      TIMESTAMPTZ
```

## 🌐 API Endpoints

- `GET /api/posts/pending` - Fetch pending posts
- `GET /api/posts/all` - Fetch all posts
- `POST /api/posts/{id}/approve` - Approve & publish
- `POST /api/posts/{id}/reject` - Reject post
- `DELETE /api/posts/{id}` - Delete post

## 🎯 Workflow Example

1. **Pipeline runs** → Fetches "Kohli scores century in IPL final"
2. **Regional Editor** → ✅ ALLOW (Indian cricket)
3. **Copywriter** → Generates: "🚨BREAKING: Virat Kohli scores century..."
4. **Photojournalist** → Finds image from Tavily
5. **Database** → Saves with status="pending"
6. **Dashboard** → Shows in pending queue
7. **Editor** → Clicks "Approve & Publish"
8. **Backend** → Posts to Bluesky with image
9. **Result** → Live on https://bsky.app/profile/ustweets.bsky.social

## 🧪 Testing

**View Pending Posts:**
```bash
curl http://127.0.0.1:8001/api/posts/pending
```

**Approve a Post:**
```bash
curl -X POST http://127.0.0.1:8001/api/posts/{post_id}/approve
```

**Run Full Pipeline:**
```bash
python test_pipeline.py
```

## 📝 Logs

All operations are logged to `newsroom.log` with detailed timestamps and agent names.

## 🔐 Security

- API keys stored in `.env` (gitignored)
- No automatic publishing (human approval required)
- CORS enabled for frontend-backend communication
- Supabase Row Level Security (RLS) can be configured

## 🚧 Future Enhancements

- [ ] Automated scheduling (cron job)
- [ ] Multi-platform publishing (X, Threads, Instagram)
- [ ] Advanced analytics and metrics
- [ ] Duplicate detection
- [ ] Post editing before approval
- [ ] Bulk actions
- [ ] Email/Slack notifications

## 📖 Documentation

See `architect_state.md` for complete system architecture and implementation details.

## 👤 Author

Shahu Ugale

## 📄 License

This project is for educational and portfolio purposes.
