import { useState } from 'react';

export default function Compliance() {
  const [email, setEmail] = useState('riyamoun1310@gmail.com');
  const [content, setContent] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkCompliance = async () => {
    setLoading(true);
    setResult(null);
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/compliance-check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', padding: 24 }}>
      <h2>Compliance & Professionalism Check</h2>
      <div>
        <input value={email} onChange={e => setEmail(e.target.value)} style={{ width: 300 }} placeholder="Your email" />
      </div>
      <div style={{ marginTop: 16 }}>
        <textarea value={content} onChange={e => setContent(e.target.value)} rows={6} style={{ width: '100%' }} placeholder="Paste your LinkedIn post or content here..." />
      </div>
      <button onClick={checkCompliance} disabled={loading || !content} style={{ marginTop: 16 }}>Check Compliance</button>
      {loading && <p>Checking...</p>}
      {result && (
        <div style={{ marginTop: 24, background: '#f9f9f9', padding: 16, borderRadius: 8 }}>
          <b>Result:</b>
          <p style={{ color: result.compliant ? 'green' : 'red' }}>{result.message}</p>
        </div>
      )}
    </div>
  );
}
