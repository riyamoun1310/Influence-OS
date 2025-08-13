import { useState } from 'react';

export default function Analytics() {
  const [email, setEmail] = useState('riyamoun1310@gmail.com');
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAnalytics = async () => {
    setLoading(true);
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/analytics/${email}`);
    const data = await res.json();
    setAnalytics(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', padding: 24 }}>
      <h2>Content Engagement Analytics</h2>
      <div>
        <input value={email} onChange={e => setEmail(e.target.value)} style={{ width: 300 }} />
        <button onClick={fetchAnalytics} style={{ marginLeft: 8 }}>Fetch Analytics</button>
      </div>
      {loading && <p>Loading analytics...</p>}
      {analytics && (
        <div style={{ marginTop: 24, border: '1px solid #eee', borderRadius: 8, padding: 16 }}>
          <p><b>Posts:</b> {analytics.posts}</p>
          <p><b>Likes:</b> {analytics.likes}</p>
          <p><b>Comments:</b> {analytics.comments}</p>
          <p><b>Shares:</b> {analytics.shares}</p>
        </div>
      )}
    </div>
  );
}
