import { useState } from 'react';

export default function Article() {
  const [email, setEmail] = useState('riyamoun1310@gmail.com');
  const [article, setArticle] = useState('');
  const [loading, setLoading] = useState(false);

  const generateArticle = async () => {
    setLoading(true);
    setArticle('');
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/generate-article?email=${email}`);
    const data = await res.json();
    setArticle(`${data.title || ''}\n\n${data.content || ''}`);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', padding: 24 }}>
      <h2>Generate LinkedIn Article</h2>
      <div>
        <input value={email} onChange={e => setEmail(e.target.value)} style={{ width: 300 }} />
        <button onClick={generateArticle} style={{ marginLeft: 8 }}>Generate Article</button>
      </div>
      {loading && <p>Generating article...</p>}
      {article && (
        <div style={{ marginTop: 24, background: '#f9f9f9', padding: 16, borderRadius: 8 }}>
          <b>Generated Article:</b>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{article}</pre>
        </div>
      )}
    </div>
  );
}