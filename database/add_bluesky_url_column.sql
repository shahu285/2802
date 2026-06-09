-- Add bluesky_url column to pending_posts table
ALTER TABLE pending_posts 
ADD COLUMN IF NOT EXISTS bluesky_url TEXT;

-- Add comment for documentation
COMMENT ON COLUMN pending_posts.bluesky_url IS 'URL of the published post on Bluesky (e.g., https://bsky.app/profile/ustweets.bsky.social/post/...)';
