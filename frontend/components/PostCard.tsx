'use client';

import { useState } from 'react';
import { Post, approvePost, rejectPost } from '@/lib/api';

interface PostCardProps {
  post: Post;
  onUpdate: () => void;
}

export default function PostCard({ post, onUpdate }: PostCardProps) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleApprove = async () => {
    setLoading(true);
    setMessage('');
    try {
      const result = await approvePost(post.id);
      setMessage('✅ ' + result.message);
      setTimeout(() => onUpdate(), 1500);
    } catch (error) {
      setMessage('❌ Failed to approve post');
    } finally {
      setLoading(false);
    }
  };

  const handleReject = async () => {
    setLoading(true);
    setMessage('');
    try {
      const result = await rejectPost(post.id);
      setMessage('✅ ' + result.message);
      setTimeout(() => onUpdate(), 1500);
    } catch (error) {
      setMessage('❌ Failed to reject post');
    } finally {
      setLoading(false);
    }
  };

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'Tier 1': return 'bg-red-100 text-red-800 border-red-300';
      case 'Tier 2': return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'Tier 3': return 'bg-green-100 text-green-800 border-green-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <span className={`px-3 py-1 text-xs font-semibold rounded-full border ${getTierColor(post.severity_tier)}`}>
          {post.severity_tier}
        </span>
        <span className="text-xs text-gray-500">
          {post.source_feed}
        </span>
      </div>

      {/* Raw Headline */}
      <div className="mb-3">
        <p className="text-sm text-gray-500 uppercase tracking-wide font-medium mb-1">
          Raw Headline
        </p>
        <p className="text-base font-medium text-gray-900">
          {post.raw_headline}
        </p>
      </div>

      {/* Styled Post */}
      <div className="mb-4">
        <p className="text-sm text-gray-500 uppercase tracking-wide font-medium mb-1">
          Styled Post
        </p>
        <div className="bg-gray-50 rounded-md p-3 border border-gray-200">
          <p className="text-sm whitespace-pre-wrap text-gray-800">
            {post.styled_text}
          </p>
          <p className="text-xs text-gray-400 mt-2">
            {post.styled_text.length}/280 characters
          </p>
        </div>
      </div>

      {/* Image */}
      {post.image_url && (
        <div className="mb-4">
          <p className="text-sm text-gray-500 uppercase tracking-wide font-medium mb-2">
            Image
          </p>
          <img 
            src={post.image_url} 
            alt="Post image"
            className="w-full h-48 object-cover rounded-md border border-gray-200"
          />
        </div>
      )}

      {/* Timestamp */}
      <p className="text-xs text-gray-400 mb-4">
        {new Date(post.created_at).toLocaleString()}
      </p>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          onClick={handleApprove}
          disabled={loading}
          className="flex-1 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
        >
          {loading ? 'Processing...' : '✅ Approve & Publish'}
        </button>
        <button
          onClick={handleReject}
          disabled={loading}
          className="flex-1 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
        >
          {loading ? 'Processing...' : '❌ Reject'}
        </button>
      </div>

      {/* Status Message */}
      {message && (
        <div className="mt-3 p-2 bg-blue-50 border border-blue-200 rounded text-sm text-center">
          {message}
        </div>
      )}
    </div>
  );
}
