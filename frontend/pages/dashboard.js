import { useState } from 'react';

export default function Dashboard() {
  const [email, setEmail] = useState('riyamoun1310@gmail.com');
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [content, setContent] = useState('');
  const [contentLoading, setContentLoading] = useState(false);

  const fetchProfile = async () => {
    setLoading(true);
    const res = await fetch(`http://localhost:8000/profile/${email}`);
    const data = await res.json();
    setProfile(data.profile);
    setLoading(false);
  };

  const generateContent = async () => {
    setContentLoading(true);
    const res = await fetch(`http://localhost:8000/generate-content?email=${email}`);
    const data = await res.json();
    setContent(data.content);
    setContentLoading(false);
  };

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', padding: 24 }}>
      <h2>Influence OS Dashboard</h2>
      <div>
        <input value={email} onChange={e => setEmail(e.target.value)} style={{ width: 300 }} />
        <button onClick={fetchProfile} style={{ marginLeft: 8 }}>Fetch Profile</button>
      </div>
      {loading && <p>Loading profile...</p>}
      {profile && (
        <div style={{ marginTop: 24, border: '1px solid #eee', borderRadius: 8, padding: 16 }}>
          <h3>{profile.name}</h3>
          <p><b>Email:</b> {profile.email}</p>
          <p><b>LinkedIn:</b> <a href={profile.linkedin_url} target="_blank" rel="noopener noreferrer">{profile.linkedin_url}</a></p>
          <p><b>Tone:</b> {profile.tone}</p>
        </div>
      )}
      <div style={{ marginTop: 32 }}>
        <button onClick={generateContent} disabled={contentLoading}>Generate Convincing LinkedIn Post</button>
        {contentLoading && <p>Generating content...</p>}
        {content && (
          <div style={{ marginTop: 16, background: '#f9f9f9', padding: 16, borderRadius: 8 }}>
            <b>Generated Content:</b>
            <p>{content}</p>
          </div>
        )}
      </div>
    </div>
  );
}
