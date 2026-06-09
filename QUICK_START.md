# ⚡ QUICK START GUIDE

## 🚀 Get Running in 3 Steps

### Step 1️⃣: Start Backend
```bash
cd backend
python main.py
```
✅ Backend running at: **http://127.0.0.1:8001**

---

### Step 2️⃣: Start Frontend
```bash
cd frontend
npm run dev
```
✅ Dashboard running at: **http://localhost:3000**

---

### Step 3️⃣: Open Dashboard
Open your browser to:
### 🌐 http://localhost:3000

---

## 🎯 What You'll See

### Dashboard Features:
- 📊 **Stats Bar**: Pending, Approved, Rejected, Total
- 📝 **Pending Tab**: Posts awaiting your review
- 📜 **History Tab**: Approved and rejected posts
- 🃏 **Post Cards**: Beautiful cards showing:
  - Raw headline
  - AI-generated viral post
  - Image thumbnail
  - Tier badge (Tier 1/2/3)
  - Source feed
  - Timestamp
- 🎬 **Action Buttons**: "Approve & Publish" or "Reject"
- 🔄 **Auto-refresh**: Updates every 30 seconds

---

## 📰 Generate New Posts

Run the pipeline to fetch and process new sports news:

```bash
python test_pipeline.py
```

This will:
1. Fetch from 4 RSS feeds
2. Filter for Indian sports
3. Generate viral posts
4. Find relevant images
5. Save to database with "pending" status

Wait 30 seconds (or refresh) and they'll appear in your dashboard!

---

## ✅ Test the Flow

1. **View Pending Posts**  
   → Open http://localhost:3000  
   → See 3 posts in the pending queue

2. **Approve a Post**  
   → Click "Approve & Publish" button  
   → Post publishes to Bluesky with image  
   → Success message appears  
   → Post moves to history

3. **Check Bluesky**  
   → Visit: https://bsky.app/profile/ustweets.bsky.social  
   → See your published post!

4. **View History**  
   → Click "History" tab  
   → See approved posts (green border)  
   → See rejected posts (red border, grayed out)

---

## 🔍 Quick Checks

### Is Backend Running?
```bash
curl http://127.0.0.1:8001/
```
Should return: `{"message": "Newsroom AI API is running",...}`

### Get Pending Posts:
```bash
curl http://127.0.0.1:8001/api/posts/pending
```
Should return: JSON array of pending posts

### Check Database:
```bash
cd database
python database_manager.py
```
Should show connection test and post count

---

## 📊 Current Status

### ✅ System Components
- Backend API: **RUNNING** on port 8001
- Frontend: **RUNNING** on port 3000
- Database: **CONNECTED** (Supabase)
- Bluesky: **AUTHENTICATED**

### 📦 Database Contents
- **3 pending posts** ready for review
- All with images, styled text, and metadata

---

## 🎮 Commands Cheat Sheet

| Action | Command |
|--------|---------|
| Start backend | `cd backend && python main.py` |
| Start frontend | `cd frontend && npm run dev` |
| Generate posts | `python test_pipeline.py` |
| View logs | `cat newsroom.log` |
| Test database | `cd database && python database_manager.py` |
| Check API | `curl http://127.0.0.1:8001/` |

---

## 🎨 Dashboard Preview

```
┌──────────────────────────────────────────────────────────┐
│  📰 Newsroom AI Dashboard                                │
│  Autonomous Sports News Pipeline                         │
├──────────────────────────────────────────────────────────┤
│  Stats Bar:                                              │
│  [Pending: 3] [Approved: 0] [Rejected: 0] [Total: 3]    │
├──────────────────────────────────────────────────────────┤
│  Tabs: [Pending] [History]                              │
├──────────────────────────────────────────────────────────┤
│  Post Cards:                                             │
│  ┌────────────────────────────────────────────┐         │
│  │ [Tier 2] Football Feed                     │         │
│  │ Raw: "England face Australia..."           │         │
│  │ Styled: "England face Australia in..."     │         │
│  │ [Image Thumbnail]                          │         │
│  │ 2026-06-08 19:18:47                        │         │
│  │ [✅ Approve & Publish] [❌ Reject]         │         │
│  └────────────────────────────────────────────┘         │
└──────────────────────────────────────────────────────────┘
```

---

## 💡 Tips

- **Auto-refresh**: Dashboard updates every 30 seconds automatically
- **Image Quality**: Photojournalist filters out low-quality images
- **Tier System**: 
  - Tier 1 = Breaking news (🚨BREAKING format)
  - Tier 2 = Standard news (clean format)
  - Tier 3 = Minor updates (minimal format)
- **Character Limit**: Posts are max 280 chars (Twitter/Bluesky standard)
- **Logs**: Check `newsroom.log` for detailed operation logs

---

## 🚨 Troubleshooting

### Backend not starting?
- Check `.env` file has all API keys
- Check port 8001 is not in use
- Check Python dependencies: `pip install -r backend/requirements.txt`

### Frontend not starting?
- Check Node.js is installed: `node --version`
- Check dependencies: `cd frontend && npm install`
- Check port 3000 is not in use

### No posts showing?
- Run `python test_pipeline.py` to generate posts
- Wait 30 seconds for auto-refresh
- Check browser console for errors
- Verify backend is running: `curl http://127.0.0.1:8001/api/posts/pending`

### Approve button not working?
- Check backend logs for errors
- Verify Bluesky credentials in `.env`
- Check network tab in browser DevTools

---

## 📚 More Info

- **Complete Architecture**: See `architect_state.md`
- **Full Documentation**: See `README.md`
- **Project Summary**: See `COMPLETION_SUMMARY.md`

---

## 🎉 Ready to Go!

Your autonomous sports newsroom is **fully operational**!

🌐 **Dashboard**: http://localhost:3000  
🔧 **API**: http://127.0.0.1:8001  
📱 **Bluesky**: https://bsky.app/profile/ustweets.bsky.social

**Enjoy your AI-powered newsroom!** 🚀
