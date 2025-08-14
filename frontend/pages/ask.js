import { useState } from 'react';

export default function AskAI() {
  const [question, setQuestion] = useState('');
  const [context, setContext] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleAsk(e) {
    e.preventDefault();
    setLoading(true);
    setError('');
    setAnswer('');
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, context })
      });
      const data = await res.json();
      if (data.answer) setAnswer(data.answer);
      else setError('No answer received.');
    } catch (err) {
      setError('Error contacting AI backend.');
    }
    setLoading(false);
  }

  return (
    <main style={{ maxWidth: 600, margin: '3rem auto', background: '#fff', borderRadius: 18, boxShadow: '0 4px 24px rgba(0,119,181,0.07)', padding: '2rem' }}>
  <h2 style={{ color: '#0077b5', marginBottom: 24 }}>Ask AI — Influence-OS1</h2>
      <form onSubmit={handleAsk} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        <label>
          <b>Question</b>
          <input
            type="text"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            required
            placeholder="Type your question..."
            style={{ width: '100%', padding: 10, borderRadius: 8, border: '1px solid #b6c6e3', marginTop: 6 }}
          />
        </label>
        <label>
          <b>Context (optional)</b>
          <textarea
            value={context}
            onChange={e => setContext(e.target.value)}
            placeholder="Add any extra context for the AI (optional)"
            style={{ width: '100%', padding: 10, borderRadius: 8, border: '1px solid #b6c6e3', minHeight: 60, marginTop: 6 }}
          />
        </label>
        <button type="submit" className="btn" disabled={loading} style={{ marginTop: 10 }}>
          {loading ? 'Thinking...' : 'Ask AI'}
        </button>
      </form>
      {answer && (
        <div style={{ marginTop: 32, background: '#e0f7fa', borderRadius: 10, padding: 18, color: '#005983' }}>
          <b>AI Answer:</b>
          <div style={{ marginTop: 8, whiteSpace: 'pre-line' }}>{answer}</div>
        </div>
      )}
      {error && (
        <div style={{ marginTop: 24, color: 'red' }}>{error}</div>
      )}
    </main>
  );
}
