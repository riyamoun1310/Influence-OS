import { useState } from 'react';

export default function News() {
  const [query, setQuery] = useState('AI');
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchNews = async () => {
    setLoading(true);
    setArticles([]);
    const res = await fetch(`http://localhost:8000/industry-news?query=${encodeURIComponent(query)}`);
    const data = await res.json();
    setArticles(data.articles || []);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', padding: 24 }}>
      <h2>Industry News & Trends</h2>
      <div>
        <input value={query} onChange={e => setQuery(e.target.value)} style={{ width: 300 }} />
        <button onClick={fetchNews} style={{ marginLeft: 8 }}>Fetch News</button>
      </div>
      {loading && <p>Loading news...</p>}
      {articles.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <ul>
            {articles.map((a, i) => (
              <li key={i} style={{ marginBottom: 16 }}>
                <a href={a.url} target="_blank" rel="noopener noreferrer"><b>{a.title}</b></a>
                <div>{a.description}</div>
                <div style={{ fontSize: 12, color: '#888' }}>{a.source?.name}</div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
