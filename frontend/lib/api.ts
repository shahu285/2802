// API client for FastAPI backend

const API_BASE_URL = "http://127.0.0.1:8001";

export interface Post {
  id: string;
  raw_headline: string;
  styled_text: string;
  image_url: string | null;
  severity_tier: string;
  status: string;
  source_feed: string | null;
  created_at: string;
  bluesky_url: string | null;
}

export async function getPendingPosts(): Promise<Post[]> {
  const response = await fetch(`${API_BASE_URL}/api/posts/pending`, {
    cache: 'no-store'
  });
  if (!response.ok) throw new Error('Failed to fetch pending posts');
  return response.json();
}

export async function getAllPosts(): Promise<Post[]> {
  const response = await fetch(`${API_BASE_URL}/api/posts/all`, {
    cache: 'no-store'
  });
  if (!response.ok) throw new Error('Failed to fetch all posts');
  return response.json();
}

export async function approvePost(id: string): Promise<{ success: boolean; message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/posts/${id}/approve`, {
    method: 'POST',
  });
  if (!response.ok) throw new Error('Failed to approve post');
  return response.json();
}

export async function rejectPost(id: string): Promise<{ success: boolean; message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/posts/${id}/reject`, {
    method: 'POST',
  });
  if (!response.ok) throw new Error('Failed to reject post');
  return response.json();
}

export async function deletePost(id: string): Promise<{ success: boolean; message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/posts/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete post');
  return response.json();
}
