import { useState } from 'react';

export default function Home() {
  const [form, setForm] = useState({
    name: 'riya',
    email: 'riyamoun1310@gmail.com',
    linkedin_url: 'https://www.linkedin.com/in/riya-moun-209449284',
    tone: 'convincing',
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/onboard`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    setMessage(data.message || 'Onboarding complete!');
  };

  return (
    <div style={{ maxWidth: 500, margin: '40px auto', padding: 24, border: '1px solid #eee', borderRadius: 8 }}>
  <h2>Influence-OS1 Onboarding</h2>
      <form onSubmit={handleSubmit}>
        <label>Name:<br />
          <input name="name" value={form.name} onChange={handleChange} required style={{ width: '100%' }} />
        </label><br /><br />
        <label>Email:<br />
          <input name="email" value={form.email} onChange={handleChange} required style={{ width: '100%' }} />
        </label><br /><br />
        <label>LinkedIn URL:<br />
          <input name="linkedin_url" value={form.linkedin_url} onChange={handleChange} required style={{ width: '100%' }} />
        </label><br /><br />
        <label>Tone:<br />
          <input name="tone" value={form.tone} onChange={handleChange} style={{ width: '100%' }} />
        </label><br /><br />
        <button type="submit">Onboard Me</button>
      </form>
      {message && <p style={{ color: 'green', marginTop: 20 }}>{message}</p>}
    </div>
  );
}
