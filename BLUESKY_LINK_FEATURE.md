# 🔗 Bluesky Link Feature - Implementation Guide

## ✨ What's New

When you approve a post for publication, the system now:
1. Publishes the post to Bluesky
2. Captures the Bluesky post URL
3. Saves it to the database
4. Displays a clickable "View on Bluesky" link in the History section

---

## 🔧 Setup Required

### Step 1: Add Database Column

You need to add a new column to your Supabase database table.

**Go to Supabase SQL Editor:**
1. Visit: https://supabase.com/dashboard/project/lmwohypczyicnznoqejo
2. Click **"SQL Editor"** in the left sidebar
3. Click **"New Query"**
4. Paste this SQL:

```sql
ALTER TABLE pending_posts 
ADD COLUMN IF NOT EXISTS bluesky_url TEXT;

COMMENT ON COLUMN pending_posts.bluesky_url 
IS 'URL of the published post on Bluesky';
```

5. Click **"Run"** (or press Ctrl+Enter)
6. You should see: "Success. No rows returned"

---

## 🎯 How It Works

### Backend Flow:
```
1. User clicks "Approve & Publish" in dashboard
   ↓
2. Backend publishes post to Bluesky
   ↓
3. Bluesky returns AT URI: "at://did:plc:xxx/app.bsky.feed.post/abc123"
   ↓
4. Backend converts to web URL: 
   "https://bsky.app/profile/ustweets.bsky.social/post/abc123"
   ↓
5. Backend saves URL to database (bluesky_url column)
   ↓
6. Backend updates status to "approved"
   ↓
7. Frontend receives response and refreshes
```

### Frontend Display:
```
In the History tab → Approved Posts section:
Each approved post now shows:
- 🔗 View on Bluesky (clickable link)
- Opens in new tab
- External link icon
```

---

## 📝 Code Changes Made

### 1. Database Manager (`database/database_manager.py`)
Added `bluesky_url` parameter to `update_post_status()`:

```python
def update_post_status(post_id: str, new_status: str, bluesky_url: str = None) -> bool:
    update_data = {"status": new_status}
    if bluesky_url:
        update_data["bluesky_url"] = bluesky_url
    # ... rest of the code
```

### 2. Backend API (`backend/main.py`)
Updated `/api/posts/{id}/approve` endpoint to:
- Extract post ID from Bluesky AT URI
- Convert to web URL format
- Save URL when updating post status

```python
# Convert AT URI to web URL
post_rkey = uri.split("/")[-1]
bluesky_url = f"https://bsky.app/profile/{BLUESKY_HANDLE}/post/{post_rkey}"

# Save to database
update_post_status(post_id, "approved", bluesky_url)
```

### 3. Frontend Types (`frontend/lib/api.ts`)
Added `bluesky_url` field to Post interface:

```typescript
export interface Post {
  // ... other fields
  bluesky_url: string | null;
}
```

### 4. Frontend UI (`frontend/app/page.tsx`)
Added link display in approved posts:

```tsx
{post.bluesky_url && (
  <a 
    href={post.bluesky_url} 
    target="_blank" 
    rel="noopener noreferrer"
    className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 font-medium"
  >
    🔗 View on Bluesky
    <svg>...</svg> {/* External link icon */}
  </a>
)}
```

---

## 🧪 Testing the Feature

### Test 1: Approve a Post
1. Open dashboard: http://localhost:3000
2. Go to "Pending" tab
3. Click "Approve & Publish" on any post
4. Wait for success message

### Test 2: View in History
1. Click "History" tab
2. Find the approved post (green border)
3. Look for the "🔗 View on Bluesky" link at the bottom
4. Click the link

### Test 3: Verify Link
1. Link should open Bluesky in new tab
2. You should see your published post
3. URL format: `https://bsky.app/profile/ustweets.bsky.social/post/xxxxx`

---

## 📊 Database Schema (Updated)

**Table: `pending_posts`**
```sql
id              UUID PRIMARY KEY
raw_headline    TEXT
styled_text     TEXT
image_url       TEXT
severity_tier   TEXT
status          TEXT
source_feed     TEXT
created_at      TIMESTAMPTZ
bluesky_url     TEXT              ← NEW COLUMN
```

---

## 🎨 UI Preview

### Before (old):
```
┌─────────────────────────────────┐
│ [Tier 2] Football Feed          │
│ Headline: "England vs..."       │
│ Post: "England face..."         │
│ [Image]                         │
│ 2026-06-08 19:18:47             │
└─────────────────────────────────┘
```

### After (new):
```
┌─────────────────────────────────┐
│ [Tier 2] Football Feed          │
│ Headline: "England vs..."       │
│ Post: "England face..."         │
│ [Image]                         │
│ 2026-06-08 19:18:47             │
│ 🔗 View on Bluesky ↗            │  ← NEW LINK
└─────────────────────────────────┘
```

---

## 🔍 Troubleshooting

### Link not showing?
- ✅ Check that you ran the SQL to add the column
- ✅ Restart the backend server
- ✅ Approve a NEW post (old posts won't have the URL)
- ✅ Refresh the dashboard

### Link format incorrect?
- Check `BLUESKY_HANDLE` in `.env` file
- Should be: `ustweets.bsky.social` (no @ symbol)

### Link goes to 404?
- The post might not have published successfully
- Check `newsroom.log` for errors
- Verify Bluesky credentials

---

## 💡 Future Enhancements

Possible improvements:
- [ ] Add link preview/thumbnail
- [ ] Show engagement stats (likes, reposts)
- [ ] Add "Open in Bluesky App" button for mobile
- [ ] Track click analytics
- [ ] Add "Copy Link" button

---

## ✅ Checklist

To complete the setup:

- [ ] Run SQL in Supabase to add `bluesky_url` column
- [ ] Backend server restarted (already done ✅)
- [ ] Frontend running (should auto-update)
- [ ] Test by approving a new post
- [ ] Verify link appears in History tab
- [ ] Click link and confirm it opens correct Bluesky post

---

## 📸 Expected Result

When you approve a post:
1. Success message: "✅ Post approved and published to Bluesky!"
2. Post moves to History → Approved Posts
3. Post card shows blue "🔗 View on Bluesky" link
4. Clicking link opens: `https://bsky.app/profile/ustweets.bsky.social/post/[post-id]`
5. You see your published post on Bluesky

---

## 🎉 Benefits

✨ **Easy verification** - Quickly check if post was published  
✨ **Direct access** - One click to view live post  
✨ **Better tracking** - Keep record of all published URLs  
✨ **Professional** - Shows complete publication workflow  

---

## 📞 Support

If you have issues:
1. Check `newsroom.log` for error messages
2. Verify SQL was executed successfully in Supabase
3. Ensure backend and frontend are both running
4. Try approving a fresh post (not an old one)

---

**Status:** Implementation complete! Just run the SQL and test! 🚀
