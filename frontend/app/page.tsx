'use client';

import { useEffect, useState } from 'react';
import { Post, getPendingPosts, getAllPosts } from '@/lib/api';
import PostCard from '@/components/PostCard';

export default function Dashboard() {
  const [pendingPosts, setPendingPosts] = useState<Post[]>([]);
  const [allPosts, setAllPosts] = useState<Post[]>([]);
  const [activeTab, setActiveTab] = useState<'pending' | 'history'>('pending');
  const [loading, setLoading] = useState(true);

  const fetchPosts = async () => {
    setLoading(true);
    try {
      const pending = await getPendingPosts();
      const all = await getAllPosts();
      setPendingPosts(pending);
      setAllPosts(all);
    } catch (error) {
      console.error('Error fetching posts:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchPosts, 30000);
    return () => clearInterval(interval);
  }, []);

  const approvedPosts = allPosts.filter(p => p.status === 'approved');
  const rejectedPosts = allPosts.filter(p => p.status === 'rejected');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-3xl font-bold text-gray-900">
            📰 Newsroom AI Dashboard
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Autonomous Sports News Pipeline
          </p>
        </div>
      </header>

      {/* Stats Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
            <p className="text-sm text-gray-500 uppercase tracking-wide">Pending</p>
            <p className="text-3xl font-bold text-blue-600">{pendingPosts.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
            <p className="text-sm text-gray-500 uppercase tracking-wide">Approved</p>
            <p className="text-3xl font-bold text-green-600">{approvedPosts.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
            <p className="text-sm text-gray-500 uppercase tracking-wide">Rejected</p>
            <p className="text-3xl font-bold text-red-600">{rejectedPosts.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
            <p className="text-sm text-gray-500 uppercase tracking-wide">Total</p>
            <p className="text-3xl font-bold text-gray-900">{allPosts.length}</p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('pending')}
              className={`${
                activeTab === 'pending'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
            >
              Pending ({pendingPosts.length})
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`${
                activeTab === 'history'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
            >
              History ({approvedPosts.length + rejectedPosts.length})
            </button>
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="text-gray-500 mt-4">Loading posts...</p>
          </div>
        ) : activeTab === 'pending' ? (
          pendingPosts.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">No pending posts</p>
              <p className="text-gray-400 text-sm mt-2">Run the pipeline to generate new posts</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {pendingPosts.map(post => (
                <PostCard key={post.id} post={post} onUpdate={fetchPosts} />
              ))}
            </div>
          )
        ) : (
          <div className="space-y-6">
            {/* Approved Posts */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">✅ Approved Posts</h2>
              {approvedPosts.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No approved posts yet</p>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {approvedPosts.map(post => (
                    <div key={post.id} className="bg-white rounded-lg shadow-md border border-green-200 p-6 opacity-75">
                      <div className="flex items-start justify-between mb-3">
                        <span className="px-3 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800 border border-green-300">
                          {post.severity_tier}
                        </span>
                        <span className="text-xs text-gray-500">{post.source_feed}</span>
                      </div>
                      <p className="text-base font-medium text-gray-900 mb-2">{post.raw_headline}</p>
                      <p className="text-sm text-gray-600 whitespace-pre-wrap mb-3">{post.styled_text}</p>
                      {post.image_url && (
                        <img src={post.image_url} alt="Post" className="w-full h-32 object-cover rounded-md mb-3" />
                      )}
                      <p className="text-xs text-gray-400 mb-2">{new Date(post.created_at).toLocaleString()}</p>
                      {post.bluesky_url && (
                        <a 
                          href={post.bluesky_url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 font-medium"
                        >
                          🔗 View on Bluesky
                          <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                          </svg>
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Rejected Posts */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">❌ Rejected Posts</h2>
              {rejectedPosts.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No rejected posts yet</p>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {rejectedPosts.map(post => (
                    <div key={post.id} className="bg-white rounded-lg shadow-md border border-red-200 p-6 opacity-50">
                      <div className="flex items-start justify-between mb-3">
                        <span className="px-3 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800 border border-red-300">
                          {post.severity_tier}
                        </span>
                        <span className="text-xs text-gray-500">{post.source_feed}</span>
                      </div>
                      <p className="text-base font-medium text-gray-900 mb-2">{post.raw_headline}</p>
                      <p className="text-sm text-gray-600 whitespace-pre-wrap">{post.styled_text}</p>
                      <p className="text-xs text-gray-400 mt-3">{new Date(post.created_at).toLocaleString()}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
